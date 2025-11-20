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
    page_title="NEXUS | Recepción XML Inteligente",
    page_icon="📥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ESTILOS CSS (FUSIÓN DE AMBOS ESTILOS) ---
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
    
    /* Cajas de Métricas */
    .metric-box {
        background-color: #F8F9FA;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        border-top: 4px solid #2E86C1;
    }
    .metric-val { font-size: 24px; font-weight: bold; color: #2E86C1; }
    .metric-lbl { font-size: 12px; color: #666; text-transform: uppercase; }
    
    /* Tablas y Alertas */
    .stDataFrame { border: 1px solid #eee; border-radius: 5px; }
    
    /* Botones */
    div.stButton > button:first-child { border-radius: 6px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# --- 3. GESTIÓN DE ESTADO (SESSION STATE) ---
if 'reception_step' not in st.session_state:
    st.session_state.reception_step = 1 # 1: Carga, 2: Conteo, 3: Cierre

if 'current_invoice_data' not in st.session_state:
    st.session_state.current_invoice_data = None

# Base de datos maestra simulada (Persistente)
if 'master_db' not in st.session_state:
    st.session_state.master_db = pd.DataFrame({
        'SKU_Interno': ['FER-DIS-001', 'FER-TOR-002', 'PIN-VIN-003', 'REF-1001'],
        'SKU_Proveedor': ['RTRXA0080106', 'REF-TEST-001', 'REF-TEST-002', '7704488003302'], 
        'Descripcion_Interna': ['Disco Corte Metal 4.5"', 'Tornillo Drywall', 'Vinilo Blanco', 'Producto Existente Ejemplo'],
        'Stock_Actual': [100, 500, 40, 15],
        'Costo_Ultima_Compra': [9200, 50, 120000, 130000]
    })

# --- 4. MOTOR DE PARSING (Lógica del PRIMER CÓDIGO - La que funciona bien) ---
def clean_tag(tag):
    """Elimina los namespaces {urn...} de los tags XML."""
    return tag.split('}', 1)[1] if '}' in tag else tag

def parse_dian_xml_engine(uploaded_file):
    """
    Lee el XML (AttachedDocument), extrae la factura interna (CDATA) y parsea los ítems.
    Basado en la lógica robusta que lee Abrasivos, Pintuco, etc.
    """
    try:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        
        # 1. Datos del Encabezado (AttachedDocument)
        namespaces = {'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
                      'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}
        
        # Intentar obtener proveedor del contenedor externo
        proveedor_tag = root.find('.//cac:SenderParty/cac:PartyTaxScheme/cbc:RegistrationName', namespaces)
        proveedor = proveedor_tag.text if proveedor_tag is not None else "Proveedor Desconocido"
        
        # 2. Extraer el XML interno (CDATA dentro de Description)
        desc_tag = root.find('.//cac:Attachment/cac:ExternalReference/cbc:Description', namespaces)
        
        if desc_tag is None or not desc_tag.text:
            return None, "No se encontró el contenido de la factura (Invoice) dentro del XML."
            
        xml_content = desc_tag.text.strip()
        
        # Parsear el XML interno
        invoice_root = ET.fromstring(xml_content)
        
        # Namespace map para el Invoice interno
        ns_inv = {'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
                  'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}
        
        # Datos Generales Factura
        folio = invoice_root.find('.//cbc:ID', ns_inv).text
        fecha = invoice_root.find('.//cbc:IssueDate', ns_inv).text
        
        # Totales
        # total_sin_imp = float(invoice_root.find('.//cac:LegalMonetaryTotal/cbc:LineExtensionAmount', ns_inv).text)
        # total_con_imp = float(invoice_root.find('.//cac:LegalMonetaryTotal/cbc:PayableAmount', ns_inv).text)
        
        # 3. Extraer Líneas (Ítems)
        items = []
        for line in invoice_root.findall('.//cac:InvoiceLine', ns_inv):
            # Cantidad
            qty_tag = line.find('.//cbc:InvoicedQuantity', ns_inv)
            qty = float(qty_tag.text) if qty_tag is not None else 0.0
            
            # Descripción
            desc_tag = line.find('.//cac:Item/cbc:Description', ns_inv)
            desc = desc_tag.text if desc_tag is not None else "Sin Descripción"
            
            # Referencia / SKU (Buscar en varios lugares posibles)
            sku = "GENERICO"
            std_id = line.find('.//cac:Item/cac:StandardItemIdentification/cbc:ID', ns_inv)
            seller_id = line.find('.//cac:Item/cac:SellersItemIdentification/cbc:ID', ns_inv)
            
            if std_id is not None and std_id.text: sku = std_id.text
            elif seller_id is not None and seller_id.text: sku = seller_id.text
            
            # Precios
            price_tag = line.find('.//cac:Price/cbc:PriceAmount', ns_inv)
            price_unit = float(price_tag.text) if price_tag is not None else 0.0
            
            total_tag = line.find('.//cbc:LineExtensionAmount', ns_inv)
            line_total = float(total_tag.text) if total_tag is not None else 0.0
            
            # Impuestos
            tax_amount = 0.0
            tax_tag = line.find('.//cac:TaxTotal/cbc:TaxAmount', ns_inv)
            if tax_tag is not None:
                tax_amount = float(tax_tag.text)
            
            items.append({
                'SKU_Proveedor': sku,
                'Descripcion_Factura': desc,
                'Cantidad_Facturada': qty,
                'Precio_Unitario': price_unit,
                'Subtotal': line_total,
                'Impuesto': tax_amount,
                'Total_Linea': line_total + tax_amount
            })
            
        header_data = {
            'Proveedor': proveedor,
            'Folio': folio,
            'Fecha': fecha
        }
        
        return header_data, pd.DataFrame(items)
        
    except Exception as e:
        return None, f"Error procesando XML: {str(e)}"

# --- 5. FUNCIONES DE NEGOCIO Y UTILIDADES ---

def homologar_inventario(df_factura):
    """Cruza los ítems de la factura con la BD Maestra."""
    maestro = st.session_state.master_db
    
    # Cruzar por SKU exacto
    df_merged = pd.merge(df_factura, maestro, on='SKU_Proveedor', how='left')
    
    # Identificar si es nuevo
    df_merged['Estado_Producto'] = np.where(df_merged['SKU_Interno'].isna(), '🆕 NUEVO', '✅ EXISTENTE')
    
    # Generar SKU Temporal para los nuevos
    def generar_sku(row):
        if pd.notna(row['SKU_Interno']): return row['SKU_Interno']
        # Lógica simple para SKU temporal
        clean_sku = ''.join(e for e in str(row['SKU_Proveedor']) if e.isalnum())[-4:]
        return f"NUEVO-{clean_sku}"

    df_merged['SKU_Interno_Final'] = df_merged.apply(generar_sku, axis=1)
    df_merged['Descripcion_Final'] = df_merged['Descripcion_Interna'].fillna(df_merged['Descripcion_Factura'])
    
    # Calculo de variación de precio
    df_merged['Diferencia_Precio_Pct'] = np.where(
        df_merged['Costo_Ultima_Compra'].notna() & (df_merged['Costo_Ultima_Compra'] > 0),
        ((df_merged['Precio_Unitario'] - df_merged['Costo_Ultima_Compra']) / df_merged['Costo_Ultima_Compra']) * 100,
        0
    )
    
    return df_merged

def generar_excel_conciliacion(df, folio, proveedor):
    """Genera un Excel con formato bonito para descargar."""
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    # Columnas a exportar
    cols_export = ['SKU_Interno_Final', 'Descripcion_Final', 'Cantidad_Facturada', 
                   'Cant_Recibida', 'Diferencia', 'Estado_Conciliacion', 'Precio_Unitario', 'Total_Linea']
    
    df[cols_export].to_excel(writer, index=False, sheet_name='Conciliacion')
    
    workbook = writer.book
    worksheet = writer.sheets['Conciliacion']
    
    # Formatos
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#2E86C1', 'font_color': 'white', 'border': 1})
    red_fmt = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'}) 
    
    for col_num, value in enumerate(cols_export):
        worksheet.write(0, col_num, value, header_fmt)
        worksheet.set_column(col_num, col_num, 20)
        
    writer.close()
    return output.getvalue()

# --- 6. INTERFAZ DE USUARIO (SIDEBAR) ---
with st.sidebar:
    st.title("NEXUS XML")
    st.progress(st.session_state.reception_step / 3)
    
    if st.session_state.current_invoice_data:
        h = st.session_state.current_invoice_data['header']
        st.info(f"📄 **{h['Folio']}**\n\nProveedor: {h['Proveedor']}")
    
    st.divider()
    if st.button("🔄 Reiniciar Proceso"):
        st.session_state.reception_step = 1
        st.session_state.current_invoice_data = None
        st.rerun()

st.title("📥 Recepción Inteligente XML")

# ==============================================================================
# PASO 1: CARGA Y ANÁLISIS (Motor Parsing + Homologación)
# ==============================================================================
if st.session_state.reception_step == 1:
    st.markdown("""
    <div class="step-container">
        <div class="step-title">1️⃣ Carga de Factura Electrónica</div>
        Sube el XML. El sistema extraerá los ítems y verificará precios y existencias.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader("Arrastra el XML (AttachedDocument) aquí:", type=['xml'])
    with col2:
        st.write("") # Espacio
        st.write("")
        if st.button("🪄 Cargar Demo"):
            st.session_state['demo_mode'] = True
            st.toast("Modo Demo Activado", icon="🧪")

    # Lógica de Procesamiento
    header = None
    df_items = None
    error_msg = None

    if uploaded_file is not None:
        header, df_items = parse_dian_xml_engine(uploaded_file) # Usamos el motor bueno
        if df_items is None:
            error_msg = header # El mensaje de error viene en la primera variable

    elif st.session_state.get('demo_mode'):
        # Simulamos resultado del motor para DEMO
        header = {'Proveedor': 'ABRASIVOS DEMO S.A', 'Folio': 'PG639060', 'Fecha': '2025-11-20'}
        df_items = pd.DataFrame([
            {'SKU_Proveedor': 'RTRXA0080106', 'Descripcion_Factura': 'MULTI-FLEX #80', 'Cantidad_Facturada': 25.0, 'Precio_Unitario': 9403.0, 'Total_Linea': 235075.0},
            {'SKU_Proveedor': 'NUEVO-999', 'Descripcion_Factura': 'ITEM NUEVO XML', 'Cantidad_Facturada': 10.0, 'Precio_Unitario': 5000.0, 'Total_Linea': 50000.0}
        ])

    # Mostrar Resultados Preliminares
    if header and df_items is not None:
        # Ejecutar homologación
        df_homologado = homologar_inventario(df_items)
        
        # Guardar en sesión temporalmente
        temp_data = {'header': header, 'items': df_homologado}
        
        # KPIs Header
        st.divider()
        k1, k2, k3 = st.columns(3)
        k1.markdown(f"<div class='metric-box'><div class='metric-val'>{header['Folio']}</div><div class='metric-lbl'>Factura</div></div>", unsafe_allow_html=True)
        k2.markdown(f"<div class='metric-box'><div class='metric-val'>{header['Proveedor']}</div><div class='metric-lbl'>Proveedor</div></div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='metric-box'><div class='metric-val'>${df_items['Total_Linea'].sum():,.0f}</div><div class='metric-lbl'>Total Neto</div></div>", unsafe_allow_html=True)

        st.markdown("### 🔍 Análisis de Precios y Homologación")
        
        # Colorear diferencias de precio
        def color_precio(val):
            if val > 5: return "color: red; font-weight: bold"
            if val < 0: return "color: green"
            return ""

        st.dataframe(
            df_homologado[[
                'SKU_Proveedor', 'Descripcion_Factura', 'Estado_Producto', 
                'Cantidad_Facturada', 'Precio_Unitario', 'Costo_Ultima_Compra', 'Diferencia_Precio_Pct'
            ]].style.map(color_precio, subset=['Diferencia_Precio_Pct']).format({
                'Precio_Unitario': '${:,.2f}',
                'Costo_Ultima_Compra': '${:,.2f}',
                'Diferencia_Precio_Pct': '{:+.1f}%'
            }),
            use_container_width=True
        )

        nuevos = df_homologado[df_homologado['Estado_Producto'] == '🆕 NUEVO']
        if not nuevos.empty:
            st.warning(f"⚠️ Se crearán {len(nuevos)} productos nuevos en el maestro.")
        
        st.markdown("---")
        if st.button("➡️ Confirmar Datos e Iniciar Conteo Físico", type="primary", use_container_width=True):
            st.session_state.current_invoice_data = temp_data
            st.session_state.reception_step = 2
            st.rerun()
            
    elif error_msg:
        st.error(error_msg)

# ==============================================================================
# PASO 2: CONTEO FÍSICO (Data Editor)
# ==============================================================================
elif st.session_state.reception_step == 2:
    st.markdown("""
    <div class="step-container">
        <div class="step-title">2️⃣ Verificación Física (Bodega)</div>
        Confirma las cantidades recibidas. Usa el botón de "Auto-rellenar" si confías en la factura.
    </div>
    """, unsafe_allow_html=True)
    
    data = st.session_state.current_invoice_data['items']
    
    # Preparar DF para edición
    df_conteo = data[['SKU_Interno_Final', 'Descripcion_Final', 'Cantidad_Facturada']].copy()
    # Si ya existía un conteo previo (al volver atrás), recuperarlo, sino ceros
    if 'conteo_real' in st.session_state.current_invoice_data:
        pass # Ya está cargado
    else:
        df_conteo['Cant_Recibida'] = 0.0
        df_conteo['Novedad'] = ""

    c_tools, c_grid = st.columns([1, 4])
    
    with c_tools:
        st.markdown("#### Acciones")
        if st.button("⚡ Todo OK", help="Copia la cantidad facturada a recibida"):
            df_conteo['Cant_Recibida'] = df_conteo['Cantidad_Facturada']
            st.toast("Cantidades copiadas", icon="✅")
    
    with c_grid:
        edited_conteo = st.data_editor(
            df_conteo,
            column_config={
                "SKU_Interno_Final": st.column_config.TextColumn("Ref. Interna", disabled=True),
                "Descripcion_Final": st.column_config.TextColumn("Producto", disabled=True),
                "Cantidad_Facturada": st.column_config.NumberColumn("Facturado", disabled=True),
                "Cant_Recibida": st.column_config.NumberColumn("Conteo Físico", required=True),
                "Novedad": st.column_config.TextColumn("Observación")
            },
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            key="editor_conteo"
        )

    st.markdown("---")
    col_prev, col_next = st.columns([1, 5])
    
    if col_prev.button("⬅️ Atrás"):
        st.session_state.reception_step = 1
        st.rerun()
        
    if col_next.button("➡️ Finalizar y Conciliar", type="primary"):
        st.session_state.current_invoice_data['conteo_real'] = edited_conteo
        st.session_state.reception_step = 3
        st.rerun()

# ==============================================================================
# PASO 3: CONCILIACIÓN Y CIERRE
# ==============================================================================
elif st.session_state.reception_step == 3:
    st.markdown("""
    <div class="step-container">
        <div class="step-title">3️⃣ Cierre de Recepción</div>
        Revisión final de discrepancias y actualización de inventario.
    </div>
    """, unsafe_allow_html=True)
    
    # Preparar datos finales
    df_base = st.session_state.current_invoice_data['items']
    df_conteo = st.session_state.current_invoice_data['conteo_real']
    header = st.session_state.current_invoice_data['header']
    
    # Merge final
    # Usamos indices o merge por SKU. Como el orden se mantiene en el editor, podemos usar asignación directa o merge seguro.
    # Haremos merge por SKU para seguridad.
    df_final = pd.merge(
        df_conteo,
        df_base[['SKU_Interno_Final', 'Precio_Unitario', 'Total_Linea', 'Estado_Producto']],
        on='SKU_Interno_Final',
        how='left'
    )
    
    # Calcular discrepancias
    df_final['Diferencia'] = df_final['Cant_Recibida'] - df_final['Cantidad_Facturada']
    df_final['Estado_Conciliacion'] = np.where(df_final['Diferencia'] == 0, '✅ OK', 
                                      np.where(df_final['Diferencia'] < 0, '🔴 FALTANTE', '🟡 SOBRANTE'))
    
    # KPIs
    faltantes = df_final[df_final['Diferencia'] < 0]
    valor_entrada = (df_final['Cant_Recibida'] * df_final['Precio_Unitario']).sum()
    
    k1, k2, k3 = st.columns(3)
    k1.metric("Unidades Recibidas", int(df_final['Cant_Recibida'].sum()))
    k2.metric("Valor Entrada (Costo)", f"${valor_entrada:,.0f}")
    k3.metric("Referencias con Faltantes", len(faltantes), delta_color="inverse")
    
    # Tabla Final
    def highlight_diff(row):
        if row['Diferencia'] < 0: return ['background-color: #ffebee'] * len(row)
        if row['Diferencia'] > 0: return ['background-color: #e8f5e9'] * len(row)
        return [''] * len(row)

    st.dataframe(
        df_final[[
            'SKU_Interno_Final', 'Descripcion_Final', 'Cantidad_Facturada', 
            'Cant_Recibida', 'Diferencia', 'Estado_Conciliacion', 'Precio_Unitario'
        ]].style.apply(highlight_diff, axis=1).format({'Precio_Unitario': '${:,.0f}'}),
        use_container_width=True
    )
    
    if not faltantes.empty:
        st.error("Hay diferencias en el conteo. Descargue el reporte para reclamar.")
    
    st.markdown("---")
    
    c_excel, c_save = st.columns(2)
    
    with c_excel:
        excel_data = generar_excel_conciliacion(df_final, header['Folio'], header['Proveedor'])
        st.download_button(
            label="📥 Descargar Reporte (Excel)",
            data=excel_data,
            file_name=f"Recepcion_{header['Folio']}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
    with c_save:
        btn_txt = "💾 Guardar y Actualizar Inventario"
        if st.button(btn_txt, type="primary", use_container_width=True):
            with st.spinner("Actualizando Kardex..."):
                time.sleep(2)
                
                # Actualizar Mock DB (Lógica de actualización)
                nuevos = df_final[df_final['Estado_Producto'] == '🆕 NUEVO']
                if not nuevos.empty:
                    nuevos_bd = pd.DataFrame({
                        'SKU_Interno': nuevos['SKU_Interno_Final'],
                        'SKU_Proveedor': ['XML-REF'] * len(nuevos),
                        'Descripcion_Interna': nuevos['Descripcion_Final'],
                        'Stock_Actual': nuevos['Cant_Recibida'],
                        'Costo_Ultima_Compra': nuevos['Precio_Unitario']
                    })
                    st.session_state.master_db = pd.concat([st.session_state.master_db, nuevos_bd], ignore_index=True)
                
                # Actualizar existentes (Simplificado: sumamos stock al Mock DB)
                for idx, row in df_final.iterrows():
                    sku = row['SKU_Interno_Final']
                    cant = row['Cant_Recibida']
                    st.session_state.master_db.loc[st.session_state.master_db['SKU_Interno'] == sku, 'Stock_Actual'] += cant

                st.balloons()
                st.success("¡Recepción #REC-2024-001 Creada con Éxito!")
                
                time.sleep(3)
                st.session_state.reception_step = 1
                st.session_state.current_invoice_data = None
                st.rerun()
