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
    page_title="NEXUS | Recepción Inteligente XML",
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
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #2E86C1;
        margin-bottom: 25px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .step-title { font-size: 20px; font-weight: bold; color: #2E86C1; margin-bottom: 10px; }
    
    /* Alertas y Métricas */
    .metric-box {
        background-color: #F8F9FA; border: 1px solid #E0E0E0; border-radius: 8px;
        padding: 15px; text-align: center;
    }
    .metric-val { font-size: 24px; font-weight: bold; color: #2E86C1; }
    .metric-lbl { font-size: 12px; color: #666; text-transform: uppercase; }
    
    /* Botones */
    div.stButton > button:first-child { border-radius: 6px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# --- 3. GESTIÓN DE ESTADO (SESSION STATE) ---
if 'reception_step' not in st.session_state:
    st.session_state.reception_step = 1 # 1: Carga, 2: Conteo, 3: Cierre
if 'current_invoice_data' not in st.session_state:
    st.session_state.current_invoice_data = None

# Base de datos maestra simulada (Persistencia durante la sesión)
if 'master_db' not in st.session_state:
    st.session_state.master_db = pd.DataFrame({
        'SKU_Interno': ['FER-DIS-001', 'FER-TOR-002', 'PIN-VIN-003'],
        'SKU_Proveedor': ['OLD-REF-999', 'REF-TEST-001', 'REF-TEST-002'], # Referencias ejemplo
        'Descripcion_Interna': ['Disco Corte Metal 4.5"', 'Tornillo Drywall 6x1', 'Vinilo Blanco Tipo 1'],
        'Stock': [100, 500, 40],
        'Costo_Promedio': [9200, 50, 120000]
    })

# --- 4. MOTOR DE PARSING XML ROBUSTO (UBL 2.1 DIAN) ---
# Esta función es capaz de leer la estructura compleja AttachedDocument -> Description -> Invoice
def parse_dian_xml_robust(uploaded_file):
    try:
        # Leer el archivo
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        
        # Namespaces comunes en DIAN UBL 2.1
        namespaces = {
            'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
            'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
            'sts': 'dian:gov:co:facturaelectronica:Structures-2-1'
        }
        
        # 1. Intentar obtener el Proveedor del XML externo (AttachedDocument)
        proveedor_tag = root.find('.//cac:SenderParty/cac:PartyTaxScheme/cbc:RegistrationName', namespaces)
        proveedor_nit_tag = root.find('.//cac:SenderParty/cac:PartyTaxScheme/cbc:CompanyID', namespaces)
        
        proveedor = proveedor_tag.text if proveedor_tag is not None else "Proveedor Desconocido"
        nit = proveedor_nit_tag.text if proveedor_nit_tag is not None else "N/A"
        
        # 2. Buscar la Factura Embebida (CDATA dentro de Description)
        # Esta es la clave para leer facturas colombianas
        desc_tag = root.find('.//cac:Attachment/cac:ExternalReference/cbc:Description', namespaces)
        
        if desc_tag is None or not desc_tag.text:
            return None, "No se encontró el contenedor de factura (Invoice) dentro del XML."
            
        # Parsear el XML interno (La factura real)
        xml_content = desc_tag.text.strip()
        invoice_root = ET.fromstring(xml_content)
        
        # Redefinir namespaces para el documento interno (a veces cambian ligeramente)
        ns_inv = {
            'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
            'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
        }
        
        # Extraer Datos Generales
        folio = invoice_root.find('.//cbc:ID', ns_inv).text
        fecha = invoice_root.find('.//cbc:IssueDate', ns_inv).text
        
        # Extraer Ítems (Línea a Línea)
        items = []
        for line in invoice_root.findall('.//cac:InvoiceLine', ns_inv):
            # Cantidad
            qty_tag = line.find('.//cbc:InvoicedQuantity', ns_inv)
            qty = float(qty_tag.text) if qty_tag is not None else 0.0
            
            # Descripción
            desc_tag = line.find('.//cac:Item/cbc:Description', ns_inv)
            desc = desc_tag.text if desc_tag is not None else "Sin Descripción"
            
            # Referencia / SKU del Proveedor
            sku = "GENERICO"
            # Buscar en ID Estándar
            std_id = line.find('.//cac:Item/cac:StandardItemIdentification/cbc:ID', ns_inv)
            # Buscar en ID Vendedor (Más común)
            seller_id = line.find('.//cac:Item/cac:SellersItemIdentification/cbc:ID', ns_inv)
            
            if std_id is not None and std_id.text: sku = std_id.text
            elif seller_id is not None and seller_id.text: sku = seller_id.text
            
            # Precio Unitario
            price_tag = line.find('.//cac:Price/cbc:PriceAmount', ns_inv)
            price = float(price_tag.text) if price_tag is not None else 0.0
            
            # Total Línea (Antes de impuestos)
            total_tag = line.find('.//cbc:LineExtensionAmount', ns_inv)
            total_linea = float(total_tag.text) if total_tag is not None else (qty * price)
            
            items.append({
                'SKU_Proveedor': sku,
                'Descripcion_Factura': desc,
                'Cant_Facturada': qty,
                'Costo_Unitario_Factura': price,
                'Total_Linea': total_linea
            })
            
        return {
            'Proveedor': proveedor,
            'NIT': nit,
            'Folio': folio,
            'Fecha': fecha,
            'Items': pd.DataFrame(items)
        }, None
        
    except Exception as e:
        return None, f"Error crítico procesando XML: {str(e)}"

# --- 5. LÓGICA DE HOMOLOGACIÓN ---
def homologar_inventario(df_factura):
    """
    Cruza los ítems de la factura con la base de datos maestra.
    Si el producto no existe, crea una referencia interna sugerida.
    """
    maestro = st.session_state.master_db
    
    # 1. Cruzar por SKU exacto
    df_merged = pd.merge(df_factura, maestro, on='SKU_Proveedor', how='left')
    
    # 2. Identificar estado
    df_merged['Estado_Producto'] = np.where(df_merged['SKU_Interno'].isna(), '🆕 NUEVO', '✅ EXISTENTE')
    
    # 3. Generar SKU Interno para los nuevos
    def generar_sku_inteligente(row):
        if pd.notna(row['SKU_Interno']):
            return row['SKU_Interno']
        
        # Crear código inteligente: 3 letras iniciales + código proveedor o random
        palabras = row['Descripcion_Factura'].split()
        prefix = palabras[0][:3].upper() if len(palabras) > 0 else "GEN"
        # Usar parte del SKU proveedor si es limpio, o un random seguro
        clean_sku_prov = ''.join(e for e in str(row['SKU_Proveedor']) if e.isalnum())[-4:]
        if not clean_sku_prov: clean_sku_prov = str(random.randint(1000,9999))
        
        return f"INT-{prefix}-{clean_sku_prov}"

    df_merged['SKU_Interno_Final'] = df_merged.apply(generar_sku_inteligente, axis=1)
    df_merged['Descripcion_Final'] = df_merged['Descripcion_Interna'].fillna(df_merged['Descripcion_Factura'])
    
    return df_merged

# --- 6. GENERADOR DE EXCEL DE CONCILIACIÓN ---
def generar_excel_conciliacion(df, folio, proveedor):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Conciliacion')
    
    workbook = writer.book
    worksheet = writer.sheets['Conciliacion']
    
    # Formatos
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#2E86C1', 'font_color': 'white', 'border': 1})
    red_fmt = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'}) # Para faltantes
    green_fmt = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'}) # Para OK
    money_fmt = workbook.add_format({'num_format': '$#,##0'})
    
    # Escribir encabezados
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_fmt)
        worksheet.set_column(col_num, col_num, 20)
        
    # Formato condicional para columna 'Diferencia'
    col_idx_diff = df.columns.get_loc('Diferencia')
    worksheet.conditional_format(1, col_idx_diff, len(df), col_idx_diff,
                                 {'type': 'cell', 'criteria': '<', 'value': 0, 'format': red_fmt})
    
    writer.close()
    return output.getvalue()

# --- 7. INTERFAZ DE USUARIO ---

# Sidebar
with st.sidebar:
    st.page_link("Portafolio_Servicios.py", label="🏠 Volver al Inicio", icon="🔙")
    st.divider()
    st.title("Progreso")
    st.progress(st.session_state.reception_step / 3)
    
    if st.session_state.current_invoice_data:
        st.info(f"📄 Procesando: **{st.session_state.current_invoice_data['header']['Folio']}**")
        st.caption(f"Proveedor: {st.session_state.current_invoice_data['header']['Proveedor']}")
    
    st.divider()
    if st.button("🔄 Reiniciar Proceso"):
        st.session_state.reception_step = 1
        st.session_state.current_invoice_data = None
        st.rerun()

st.title("📥 Recepción Inteligente & Conciliación")

# ==============================================================================
# FASE 1: CARGA DE XML Y HOMOLOGACIÓN
# ==============================================================================
if st.session_state.reception_step == 1:
    st.markdown("""
    <div class="step-container">
        <div class="step-title">1️⃣ Carga de Factura Electrónica (XML)</div>
        Arrastre el archivo XML recibido del proveedor. El sistema leerá el código UBL 2.1, extraerá los ítems y verificará si existen en su inventario.
    </div>
    """, unsafe_allow_html=True)
    
    col_up, col_demo = st.columns([3, 1])
    
    with col_up:
        uploaded_file = st.file_uploader("Subir archivo XML (AttachedDocument):", type=['xml'])
        
    with col_demo:
        st.write("")
        st.write("")
        if st.button("🪄 Cargar XML Demo (Abrasivos)", type="secondary"):
            st.session_state['demo_mode'] = True
            st.toast("Datos de prueba cargados.", icon="✅")

    # Procesamiento
    if uploaded_file or st.session_state.get('demo_mode'):
        with st.spinner("Desencriptando AttachedDocument y leyendo Invoice..."):
            time.sleep(1.5) # Simulación de proceso
            
            header = None
            items_data = None
            error = None
            
            if st.session_state.get('demo_mode'):
                # Datos Mock exactos de tu ejemplo Abrasivos
                header = {
                    'Proveedor': 'ABRASIVOS DE COLOMBIA S.A', 
                    'NIT': '890911327',
                    'Folio': 'PG639060', 
                    'Fecha': '2025-11-19'
                }
                items_data = pd.DataFrame([
                    {'SKU_Proveedor': 'RTRXA0080106', 'Descripcion_Factura': 'MULTI-FLEX #80 rollo de 6" x25mts', 'Cant_Facturada': 25.0, 'Costo_Unitario_Factura': 9403.0, 'Total_Linea': 235075.0},
                    {'SKU_Proveedor': 'NUEVO-LIJA-100', 'Descripcion_Factura': 'Lija Agua #100 Grano Fino', 'Cant_Facturada': 50.0, 'Costo_Unitario_Factura': 1200.0, 'Total_Linea': 60000.0}
                ])
            elif uploaded_file:
                header, items_data = parse_dian_xml_robust(uploaded_file)
                error = items_data # Si retorna error
            
            if header and items_data is not None and not isinstance(items_data, str):
                # Ejecutar lógica de homologación
                df_homologado = homologar_inventario(items_data)
                st.session_state.current_invoice_data = {'header': header, 'items': df_homologado}
                
                # Mostrar Resultados
                st.divider()
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"<div class='metric-box'><div class='metric-val'>{header['Folio']}</div><div class='metric-lbl'>Factura N°</div></div>", unsafe_allow_html=True)
                c2.markdown(f"<div class='metric-box'><div class='metric-val'>{header['Proveedor']}</div><div class='metric-lbl'>Proveedor</div></div>", unsafe_allow_html=True)
                c3.markdown(f"<div class='metric-box'><div class='metric-val'>{len(df_homologado)}</div><div class='metric-lbl'>Referencias</div></div>", unsafe_allow_html=True)
                
                st.markdown("### 🕵️‍♂️ Resultado de Homologación Automática")
                
                # Separar nuevos de existentes
                nuevos = df_homologado[df_homologado['Estado_Producto'] == '🆕 NUEVO']
                
                if not nuevos.empty:
                    st.warning(f"⚠️ **Atención:** Se encontraron {len(nuevos)} productos nuevos. El sistema ha creado las siguientes referencias internas automáticamente:")
                    st.dataframe(
                        nuevos[['SKU_Proveedor', 'Descripcion_Factura', 'SKU_Interno_Final', 'Estado_Producto']],
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.success("✅ Todos los productos ya existen en el maestro. Referencias cruzadas correctamente.")
                
                st.markdown("---")
                if st.button("➡️ Confirmar Datos e Iniciar Recepción Física", type="primary", use_container_width=True):
                    st.session_state.reception_step = 2
                    st.rerun()
                    
            elif error:
                st.error(f"Error: {error}")

# ==============================================================================
# FASE 2: CONTEO FÍSICO (AUTOMATIZADO)
# ==============================================================================
elif st.session_state.reception_step == 2:
    st.markdown("""
    <div class="step-container">
        <div class="step-title">2️⃣ Verificación Física (Conteo en Bodega)</div>
        Ingrese la cantidad recibida. Puede usar un lector de código de barras o ingresar manualmente.
        El sistema comparará en tiempo real lo contado vs. la factura.
    </div>
    """, unsafe_allow_html=True)
    
    data = st.session_state.current_invoice_data['items']
    
    # Preparar dataframe para edición
    df_conteo = data[['SKU_Interno_Final', 'Descripcion_Final', 'Cant_Facturada']].copy()
    df_conteo['Cant_Recibida'] = 0 # Inicializar en 0 para obligar conteo
    df_conteo['Comentario_Recibo'] = ""
    
    # Herramientas de Conteo
    col_tools, col_table = st.columns([1, 3])
    
    with col_tools:
        st.markdown("#### 🛠️ Herramientas")
        if st.button("⚡ Auto-rellenar (Todo llegó OK)", help="Úselo solo si confía plenamente en el proveedor"):
            df_conteo['Cant_Recibida'] = df_conteo['Cant_Facturada']
            st.toast("Cantidades copiadas de la factura.", icon="✅")
        
        st.info("💡 **Tip:** Si usa lector de barras, asegúrese de que el cursor esté en la celda de cantidad.")

    with col_table:
        st.markdown("#### 📋 Planilla de Ingreso")
        edited_conteo = st.data_editor(
            df_conteo,
            column_config={
                "SKU_Interno_Final": st.column_config.TextColumn("Ref. Interna", disabled=True, help="Código interno asignado"),
                "Descripcion_Final": st.column_config.TextColumn("Producto", disabled=True, width="large"),
                "Cant_Facturada": st.column_config.NumberColumn("Facturado", disabled=True, format="%.0f"),
                "Cant_Recibida": st.column_config.NumberColumn("Conteo Físico", min_value=0, step=1, required=True, format="%.0f"),
                "Comentario_Recibo": st.column_config.TextColumn("Novedad", placeholder="Avería, caja abierta...")
            },
            use_container_width=True,
            hide_index=True,
            key="editor_conteo_fisico"
        )
    
    st.markdown("---")
    c_prev, c_next = st.columns([1, 5])
    
    if c_prev.button("⬅️ Atrás"):
        st.session_state.reception_step = 1
        st.rerun()
        
    if c_next.button("➡️ Finalizar Conteo y Conciliar", type="primary"):
        # Guardar el conteo
        st.session_state.current_invoice_data['conteo_real'] = edited_conteo
        st.session_state.reception_step = 3
        st.rerun()

# ==============================================================================
# FASE 3: CONCILIACIÓN Y CIERRE
# ==============================================================================
elif st.session_state.reception_step == 3:
    st.markdown("""
    <div class="step-container">
        <div class="step-title">3️⃣ Conciliación Final y Alimentación de Inventario</div>
        Revise las diferencias. Si hay faltantes, descargue el reporte para reclamo. 
        Al aprobar, los productos nuevos se crearán y el stock se sumará al sistema.
    </div>
    """, unsafe_allow_html=True)
    
    # Procesar Datos Finales
    df_base = st.session_state.current_invoice_data['items']
    df_conteo = st.session_state.current_invoice_data['conteo_real']
    
    # Unir
    df_final = df_conteo.merge(
        df_base[['SKU_Interno_Final', 'Costo_Unitario_Factura', 'Total_Linea', 'Estado_Producto']], 
        on='SKU_Interno_Final', 
        how='left'
    )
    
    # Cálculos
    df_final['Diferencia'] = df_final['Cant_Recibida'] - df_final['Cant_Facturada']
    df_final['Valor_Entrada'] = df_final['Cant_Recibida'] * df_final['Costo_Unitario_Factura']
    df_final['Estado_Conciliacion'] = np.where(df_final['Diferencia'] == 0, '✅ OK', 
                                      np.where(df_final['Diferencia'] < 0, '🔴 FALTANTE', '🟡 SOBRANTE'))

    # KPIs de Cierre
    faltantes = df_final[df_final['Diferencia'] < 0]
    sobrantes = df_final[df_final['Diferencia'] > 0]
    valor_total_entrada = df_final['Valor_Entrada'].sum()
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Referencias Procesadas", len(df_final))
    k2.metric("Valor Entrada Inventario", f"${valor_total_entrada:,.0f}")
    k3.metric("Faltantes (Unidades)", int(abs(faltantes['Diferencia'].sum())), delta_color="inverse")
    k4.metric("Productos Nuevos a Crear", len(df_final[df_final['Estado_Producto'] == '🆕 NUEVO']))
    
    # Tabla de Resultados con Colores
    st.subheader("🔍 Detalle de Conciliación")
    
    def highlight_rows(row):
        if row['Diferencia'] < 0: return ['background-color: #FDEDEC'] * len(row)
        if row['Diferencia'] > 0: return ['background-color: #FEF9E7'] * len(row)
        return [''] * len(row)

    st.dataframe(
        df_final[[
            'SKU_Interno_Final', 'Descripcion_Final', 'Estado_Producto', 
            'Cant_Facturada', 'Cant_Recibida', 'Diferencia', 'Estado_Conciliacion', 
            'Costo_Unitario_Factura', 'Comentario_Recibo'
        ]].style.apply(highlight_rows, axis=1).format({
            'Costo_Unitario_Factura': '${:,.2f}',
            'Cant_Facturada': '{:.0f}',
            'Cant_Recibida': '{:.0f}',
            'Diferencia': '{:.0f}'
        }),
        use_container_width=True
    )
    
    # Alertas
    if not faltantes.empty:
        st.error(f"🚨 **BLOQUEO DE CALIDAD:** Hay {len(faltantes)} referencias con faltantes. Descargue el reporte para reclamar nota crédito.")
    
    st.markdown("---")
    
    # Acciones Finales
    col_excel, col_save = st.columns(2)
    
    with col_excel:
        st.markdown("#### 📄 Documentación")
        excel_data = generar_excel_conciliacion(
            df_final, 
            st.session_state.current_invoice_data['header']['Folio'],
            st.session_state.current_invoice_data['header']['Proveedor']
        )
        st.download_button(
            label="📥 Descargar Reporte de Discrepancias (Excel)",
            data=excel_data,
            file_name=f"Recepcion_{st.session_state.current_invoice_data['header']['Folio']}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
    with col_save:
        st.markdown("#### 🚀 Ejecución")
        btn_label = "💾 Aprobar con Novedades" if not faltantes.empty else "💾 Aprobar Entrada Perfecta"
        if st.button(btn_label, type="primary", use_container_width=True):
            with st.spinner("Registrando entrada en Kardex... Creando productos nuevos..."):
                time.sleep(3)
                
                # Actualizar BD Maestra (Simulación)
                nuevos = df_final[df_final['Estado_Producto'] == '🆕 NUEVO']
                if not nuevos.empty:
                    nuevos_bd = pd.DataFrame({
                        'SKU_Interno': nuevos['SKU_Interno_Final'],
                        'SKU_Proveedor': ['N/A'] * len(nuevos), # Simplificado
                        'Descripcion_Interna': nuevos['Descripcion_Final'],
                        'Stock': nuevos['Cant_Recibida'],
                        'Costo_Promedio': nuevos['Costo_Unitario_Factura']
                    })
                    st.session_state.master_db = pd.concat([st.session_state.master_db, nuevos_bd], ignore_index=True)
                
                st.balloons()
                st.success(f"¡Inventario Actualizado! Se han sumado {int(df_final['Cant_Recibida'].sum())} unidades.")
                st.info(f"Las referencias nuevas ({len(nuevos)}) han sido creadas y ya están disponibles para la venta.")
                
                # Resetear
                time.sleep(4)
                st.session_state.reception_step = 1
                st.session_state.current_invoice_data = None
                st.rerun()
