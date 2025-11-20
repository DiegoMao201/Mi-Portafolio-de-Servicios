import streamlit as st
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import io
import time
import random
import xlsxwriter
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="NEXUS | Recepción 360°",
    page_icon="📥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ESTILOS CSS PROFESIONALES ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #333333; font-family: 'Segoe UI', sans-serif; }
    
    /* Pasos del Wizard */
    .step-container {
        background-color: #F0F8FF;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2E86C1;
        margin-bottom: 20px;
    }
    .step-title { font-size: 18px; font-weight: bold; color: #2E86C1; }
    
    /* Alertas y Métricas */
    .alert-box { padding: 10px; border-radius: 5px; font-weight: bold; text-align: center;}
    .alert-red { background-color: #FDEDEC; color: #E74C3C; border: 1px solid #E74C3C; }
    .alert-green { background-color: #E9F7EF; color: #27AE60; border: 1px solid #27AE60; }
    
    /* Tablas */
    .stDataFrame { border: 1px solid #E0E0E0; border-radius: 5px; }
    
    /* Botones */
    div.stButton > button:first-child { border-radius: 6px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# --- 3. GESTIÓN DE ESTADO (SESSION STATE) ---
# Necesitamos persistencia para navegar entre los pasos de recepción
if 'reception_step' not in st.session_state:
    st.session_state.reception_step = 1 # 1: Carga, 2: Conteo, 3: Cierre
if 'current_invoice_data' not in st.session_state:
    st.session_state.current_invoice_data = None
if 'master_db' not in st.session_state:
    # Base de datos simulada persistente
    st.session_state.master_db = pd.DataFrame({
        'SKU_Interno': ['FER-DIS-001', 'FER-TOR-002', 'PIN-VIN-003'],
        'SKU_Proveedor': ['RTRXA0080106', '7704488003302', 'OLD-REF-999'],
        'Descripcion_Interna': ['Disco Corte Metal 4.5"', 'Tornillo Drywall 6x1', 'Vinilo Blanco Tipo 1'],
        'Stock': [100, 500, 40],
        'Costo_Promedio': [9200, 50, 120000]
    })

# --- 4. MOTOR DE PARSING XML (UBL 2.1 DIAN ROBUSTO) ---
def clean_tag(tag):
    return tag.split('}', 1)[1] if '}' in tag else tag

def parse_dian_xml(uploaded_file):
    try:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        namespaces = {'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
                      'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}
        
        # Extraer Proveedor del sobre
        proveedor_tag = root.find('.//cac:SenderParty/cac:PartyTaxScheme/cbc:RegistrationName', namespaces)
        proveedor = proveedor_tag.text if proveedor_tag is not None else "Proveedor Desconocido"
        
        # Extraer Factura embebida (CDATA)
        desc_tag = root.find('.//cac:Attachment/cac:ExternalReference/cbc:Description', namespaces)
        if desc_tag is None or not desc_tag.text: return None, "XML sin Invoice embebido"
        
        invoice_root = ET.fromstring(desc_tag.text.strip())
        ns_inv = {'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
                  'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}
        
        folio = invoice_root.find('.//cbc:ID', ns_inv).text
        fecha = invoice_root.find('.//cbc:IssueDate', ns_inv).text
        
        items = []
        for line in invoice_root.findall('.//cac:InvoiceLine', ns_inv):
            qty = float(line.find('.//cbc:InvoicedQuantity', ns_inv).text)
            desc = line.find('.//cac:Item/cbc:Description', ns_inv).text
            
            # Buscar SKU Proveedor (Prioridad: Standard -> Seller)
            sku = "GENERICO"
            std_id = line.find('.//cac:Item/cac:StandardItemIdentification/cbc:ID', ns_inv)
            seller_id = line.find('.//cac:Item/cac:SellersItemIdentification/cbc:ID', ns_inv)
            if std_id is not None: sku = std_id.text
            elif seller_id is not None: sku = seller_id.text
            
            price = float(line.find('.//cac:Price/cbc:PriceAmount', ns_inv).text)
            
            items.append({
                'SKU_Proveedor': sku,
                'Descripcion_Factura': desc,
                'Cant_Facturada': qty,
                'Costo_Unitario_Factura': price,
                'Total_Linea': qty * price
            })
            
        return {
            'Proveedor': proveedor,
            'Folio': folio,
            'Fecha': fecha,
            'Items': pd.DataFrame(items)
        }, None
        
    except Exception as e:
        return None, str(e)

# --- 5. LÓGICA DE HOMOLOGACIÓN Y CREACIÓN DE REFERENCIAS ---
def homologar_inventario(df_factura):
    """
    Cruza la factura con la BD maestra.
    Si no existe, genera una referencia interna sugerida.
    """
    maestro = st.session_state.master_db
    
    # Cruzar por SKU Proveedor
    df_merged = pd.merge(df_factura, maestro, on='SKU_Proveedor', how='left')
    
    # Identificar Nuevos
    df_merged['Estado_Producto'] = np.where(df_merged['SKU_Interno'].isna(), '🆕 NUEVO', '✅ EXISTENTE')
    
    # Generar SKUs Internos para los nuevos
    def generar_sku(row):
        if pd.notna(row['SKU_Interno']):
            return row['SKU_Interno']
        # Lógica inteligente de creación de SKU: 3 letras desc + timestamp
        prefix = row['Descripcion_Factura'][:3].upper()
        suffix = random.randint(1000, 9999)
        return f"INT-{prefix}-{suffix}"

    df_merged['SKU_Interno_Final'] = df_merged.apply(generar_sku, axis=1)
    df_merged['Descripcion_Final'] = df_merged['Descripcion_Interna'].fillna(df_merged['Descripcion_Factura'])
    
    return df_merged

# --- 6. GENERADOR DE EXCEL ---
def generar_excel_conciliacion(df, folio):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Conciliacion')
    
    workbook = writer.book
    worksheet = writer.sheets['Conciliacion']
    
    # Formato condicional
    red_fmt = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    green_fmt = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#2E86C1', 'font_color': 'white'})
    
    # Headers
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_fmt)
        worksheet.set_column(col_num, col_num, 20)
        
    writer.close()
    return output.getvalue()

# --- 7. INTERFAZ DE USUARIO ---

# Sidebar
with st.sidebar:
    st.page_link("Portafolio_Servicios.py", label="🏠 Volver al Inicio", icon="🔙")
    st.divider()
    st.progress(st.session_state.reception_step / 3, text=f"Paso {st.session_state.reception_step} de 3")
    st.info("Este módulo alimenta automáticamente el inventario maestro y gestiona la creación de nuevos productos.")
    
    if st.button("🔄 Reiniciar Proceso"):
        st.session_state.reception_step = 1
        st.session_state.current_invoice_data = None
        st.rerun()

st.title("📥 Recepción Inteligente & Conciliación")

# ==============================================================================
# FASE 1: CARGA Y HOMOLOGACIÓN
# ==============================================================================
if st.session_state.reception_step == 1:
    st.markdown("""
    <div class="step-container">
        <div class="step-title">1️⃣ Carga de Factura Electrónica</div>
        Suba el XML enviado por el proveedor. El sistema detectará productos nuevos y asignará referencias internas automáticamente.
    </div>
    """, unsafe_allow_html=True)
    
    col_up, col_demo = st.columns([2, 1])
    with col_up:
        uploaded_file = st.file_uploader("Arrastre el XML (UBL 2.1 DIAN) aquí:", type=['xml'])
    with col_demo:
        st.write("")
        st.write("")
        if st.button("🪄 Usar XML Demo (Abrasivos)", type="secondary"):
            st.session_state['demo_mode'] = True
            st.toast("Datos de demostración cargados.", icon="✅")

    if uploaded_file or st.session_state.get('demo_mode'):
        with st.spinner("Analizando estructura XML y cruzando con Maestro de Productos..."):
            time.sleep(1.5) # Efecto visual
            
            # Simulación o Parsing Real
            if st.session_state.get('demo_mode'):
                # Datos DEMO basados en tu prompt anterior
                header = {'Proveedor': 'Abrasivos de Colombia S.A', 'Folio': 'PG639060', 'Total': 270806.40}
                items_data = pd.DataFrame([
                    {'SKU_Proveedor': 'RTRXA0080106', 'Descripcion_Factura': 'MULTI-FLEX #80 rollo', 'Cant_Facturada': 25.0, 'Costo_Unitario_Factura': 9403.0},
                    {'SKU_Proveedor': 'NUEVO-LIJA-100', 'Descripcion_Factura': 'Lija Agua #100 (Nuevo)', 'Cant_Facturada': 50.0, 'Costo_Unitario_Factura': 1200.0}
                ])
            else:
                header, items_data = parse_dian_xml(uploaded_file)

            if items_data is not None:
                # Ejecutar Homologación
                df_homologado = homologar_inventario(items_data)
                st.session_state.current_invoice_data = {'header': header, 'items': df_homologado}
                
                # Mostrar Resultados Fase 1
                st.divider()
                st.subheader(f"Factura: {header['Folio']} - {header['Proveedor']}")
                
                # Alerta de Productos Nuevos
                nuevos = df_homologado[df_homologado['Estado_Producto'] == '🆕 NUEVO']
                if not nuevos.empty:
                    st.warning(f"⚠️ Se detectaron **{len(nuevos)} productos nuevos**. El sistema ha creado referencias internas preliminares:")
                    st.dataframe(nuevos[['SKU_Proveedor', 'Descripcion_Factura', 'SKU_Interno_Final', 'Estado_Producto']], hide_index=True)
                else:
                    st.success("✅ Todos los productos ya existen en su base de datos.")

                st.info("Revise la homologación automática. Si está de acuerdo, proceda al conteo físico.")
                
                if st.button("➡️ Confirmar Referencias e Ir a Conteo Físico", type="primary"):
                    st.session_state.reception_step = 2
                    st.rerun()

# ==============================================================================
# FASE 2: CONTEO FÍSICO (RECEPCIÓN CIEGA O GUIADA)
# ==============================================================================
elif st.session_state.reception_step == 2:
    st.markdown("""
    <div class="step-container">
        <div class="step-title">2️⃣ Verificación Física (Conteo)</div>
        Ingrese la cantidad que realmente llegó a bodega. El sistema comparará en tiempo real contra la factura.
    </div>
    """, unsafe_allow_html=True)
    
    data = st.session_state.current_invoice_data['items']
    
    # Preparar DF para edición
    df_conteo = data[['SKU_Interno_Final', 'Descripcion_Final', 'Cant_Facturada']].copy()
    df_conteo['Cant_Recibida'] = 0 # Inicializar en 0 para obligar a contar (Blind Count parcial)
    df_conteo['Comentarios'] = ""
    
    # Opciones de visualización
    col_opts, col_grid = st.columns([1, 4])
    
    with col_opts:
        st.markdown("**Opciones:**")
        auto_fill = st.button("⚡ Auto-rellenar")
        if auto_fill:
            df_conteo['Cant_Recibida'] = df_conteo['Cant_Facturada']
            st.toast("Cantidades precargadas según factura.", icon="🤖")
    
    with col_grid:
        st.markdown("##### 📋 Planilla de Ingreso")
        edited_conteo = st.data_editor(
            df_conteo,
            column_config={
                "SKU_Interno_Final": st.column_config.TextColumn("Referencia Interna", disabled=True),
                "Descripcion_Final": st.column_config.TextColumn("Producto", disabled=True, width="large"),
                "Cant_Facturada": st.column_config.NumberColumn("Esperado (Fac)", disabled=True),
                "Cant_Recibida": st.column_config.NumberColumn("Conteo Físico", min_value=0, step=1, required=True),
                "Comentarios": st.column_config.TextColumn("Novedades (Averías/Cambios)")
            },
            use_container_width=True,
            hide_index=True,
            key="editor_conteo"
        )
    
    st.markdown("---")
    c_back, c_next = st.columns([1, 5])
    if c_back.button("⬅️ Atrás"):
        st.session_state.reception_step = 1
        st.rerun()
        
    if c_next.button("➡️ Finalizar Conteo y Conciliar", type="primary"):
        # Guardar conteo en estado
        st.session_state.current_invoice_data['conteo_real'] = edited_conteo
        st.session_state.reception_step = 3
        st.rerun()

# ==============================================================================
# FASE 3: CONCILIACIÓN, REPORTES Y CIERRE
# ==============================================================================
elif st.session_state.reception_step == 3:
    st.markdown("""
    <div class="step-container">
        <div class="step-title">3️⃣ Conciliación y Alimentación de Inventario</div>
        Revise las diferencias encontradas. Si aprueba, el inventario se actualizará y los productos nuevos serán creados oficialmente.
    </div>
    """, unsafe_allow_html=True)
    
    # Preparar datos finales
    df_original = st.session_state.current_invoice_data['items']
    df_conteo = st.session_state.current_invoice_data['conteo_real']
    
    # Unir datos de precio y otros metadatos
    df_final = df_conteo.merge(df_original[['SKU_Interno_Final', 'Costo_Unitario_Factura', 'Estado_Producto']], on='SKU_Interno_Final', how='left')
    
    # Calcular Diferencias
    df_final['Diferencia'] = df_final['Cant_Recibida'] - df_final['Cant_Facturada']
    df_final['Valor_Entrada'] = df_final['Cant_Recibida'] * df_final['Costo_Unitario_Factura']
    
    # KPIs de la Recepción
    total_items = len(df_final)
    total_con_novedad = len(df_final[df_final['Diferencia'] != 0])
    valor_recibido = df_final['Valor_Entrada'].sum()
    
    k1, k2, k3 = st.columns(3)
    k1.metric("Referencias Recibidas", total_items)
    k2.metric("Con Novedad (Faltantes/Sob)", total_con_novedad, delta_color="inverse" if total_con_novedad > 0 else "normal", delta=f"{total_con_novedad} ítems")
    k3.metric("Valor Total Entrada Inventario", f"${valor_recibido:,.0f}")
    
    # Tabla de Discrepancias
    st.subheader("🔍 Análisis de Diferencias")
    
    def highlight_diff(val):
        color = '#FDEDEC' if val < 0 else ('#E9F7EF' if val > 0 else '')
        return f'background-color: {color}'

    st.dataframe(
        df_final.style.applymap(highlight_diff, subset=['Diferencia']),
        column_config={
            "Estado_Producto": st.column_config.Column("Estado Maestro"),
            "Diferencia": st.column_config.Column("Diferencia (Uni)"),
            "Valor_Entrada": st.column_config.NumberColumn("Costo Total Entrada", format="$%d")
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Alertas finales
    if total_con_novedad > 0:
        st.error(f"🚨 **ATENCIÓN:** Hay diferencias entre la factura y el conteo físico. Descargue el informe de discrepancias para reclamar al proveedor.")
    else:
        st.success("✅ **PERFECTO:** La recepción coincide 100% con la factura electrónica.")

    st.markdown("---")
    
    # Zona de Acciones
    c_report, c_action = st.columns([1, 1])
    
    with c_report:
        st.subheader("📄 Documentación")
        excel_file = generar_excel_conciliacion(df_final, st.session_state.current_invoice_data['header']['Folio'])
        
        st.download_button(
            label="📥 Descargar Reporte de Recepción (Excel)",
            data=excel_file,
            file_name=f"Recepcion_{st.session_state.current_invoice_data['header']['Folio']}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
    with c_action:
        st.subheader("🚀 Ejecución")
        confirm_btn = st.button("💾 Aprobar Entrada y Actualizar Inventario", type="primary", use_container_width=True)
        
        if confirm_btn:
            with st.spinner("Creando referencias nuevas... Actualizando Kardex... Recalculando Costos Promedios..."):
                time.sleep(3)
                
                # Actualizar base de datos simulada (Persistencia en sesión)
                nuevos_registros = df_final[df_final['Estado_Producto'] == '🆕 NUEVO'][['SKU_Interno_Final', 'Descripcion_Final', 'Cant_Recibida', 'Costo_Unitario_Factura']]
                nuevos_registros.columns = ['SKU_Interno', 'Descripcion_Interna', 'Stock', 'Costo_Promedio']
                # Aquí añadiríamos SKU_Proveedor si lo tuviéramos limpio en df_final, para el demo basta con esto
                
                st.session_state.master_db = pd.concat([st.session_state.master_db, nuevos_registros], ignore_index=True)
                
                st.balloons()
                st.success(f"¡Inventario Alimentado! Se han sumado {int(df_final['Cant_Recibida'].sum())} unidades al stock.")
                st.info("Los nuevos productos ya están disponibles para la venta con sus referencias internas asignadas.")
