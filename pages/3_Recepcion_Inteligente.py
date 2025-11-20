import streamlit as st
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import io
import time
import random

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="NEXUS | Recepción XML Inteligente",
    page_icon="📥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ESTILOS CSS (CONSISTENCIA CON PÁGINA 2) ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #333333; font-family: 'Segoe UI', sans-serif; }
    
    /* Cajas de Métricas */
    .metric-container {
        background-color: #F8F9FA;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        border-top: 4px solid #2E86C1;
    }
    .metric-val { font-size: 24px; font-weight: bold; color: #2E86C1; }
    .metric-lbl { font-size: 12px; color: #666; text-transform: uppercase; }
    
    /* Alertas de precios */
    .price-up { color: #E74C3C; font-weight: bold; }
    .price-ok { color: #27AE60; font-weight: bold; }
    
    /* Botones */
    div.stButton > button:first-child { border-radius: 6px; font-weight: 600; }
    
    /* XML Viewer styling */
    .xml-box {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px;
        font-family: monospace;
        font-size: 12px;
        height: 150px;
        overflow-y: scroll;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE PARSING XML (INGENIERÍA UBL 2.1 COLOMBIA) ---
# Esta función es el corazón del módulo. Lee la estructura compleja de la DIAN.

def clean_tag(tag):
    """Elimina los namespaces molestos {urn...} de los tags XML para facilitar la lectura."""
    return tag.split('}', 1)[1] if '}' in tag else tag

def parse_dian_xml(uploaded_file):
    """
    Lee el XML (AttachedDocument), extrae la factura interna (CDATA) y parsea los ítems.
    Funciona para Abrasivos, Pintuco y cualquier facturador electrónico estándar.
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
        
        # 2. Extraer el XML interno (La factura real está dentro de Description)
        # Buscamos el bloque CDATA que contiene la <Invoice>
        desc_tag = root.find('.//cac:Attachment/cac:ExternalReference/cbc:Description', namespaces)
        
        if desc_tag is None or not desc_tag.text:
            return None, "No se encontró el contenido de la factura (Invoice) dentro del XML."
            
        xml_content = desc_tag.text.strip()
        
        # Parsear el XML interno
        invoice_root = ET.fromstring(xml_content)
        
        # Namespace map para el Invoice interno (puede variar ligeramente)
        ns_inv = {'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
                  'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}
        
        # Datos Generales Factura
        folio = invoice_root.find('.//cbc:ID', ns_inv).text
        fecha = invoice_root.find('.//cbc:IssueDate', ns_inv).text
        
        # Totales
        total_sin_imp = float(invoice_root.find('.//cac:LegalMonetaryTotal/cbc:LineExtensionAmount', ns_inv).text)
        total_con_imp = float(invoice_root.find('.//cac:LegalMonetaryTotal/cbc:PayableAmount', ns_inv).text)
        
        # 3. Extraer Líneas (Ítems)
        items = []
        for line in invoice_root.findall('.//cac:InvoiceLine', ns_inv):
            # Cantidad
            qty = float(line.find('.//cbc:InvoicedQuantity', ns_inv).text)
            
            # Descripción
            desc = line.find('.//cac:Item/cbc:Description', ns_inv).text
            
            # Referencia / SKU (Buscar en varios lugares posibles)
            sku = "N/A"
            std_id = line.find('.//cac:Item/cac:StandardItemIdentification/cbc:ID', ns_inv)
            seller_id = line.find('.//cac:Item/cac:SellersItemIdentification/cbc:ID', ns_inv)
            
            if std_id is not None: sku = std_id.text
            elif seller_id is not None: sku = seller_id.text
            
            # Precios
            price_unit = float(line.find('.//cac:Price/cbc:PriceAmount', ns_inv).text)
            line_total = float(line.find('.//cbc:LineExtensionAmount', ns_inv).text)
            
            # Impuestos (Puede haber varios, tomamos el total de la línea)
            tax_amount = 0.0
            tax_tag = line.find('.//cac:TaxTotal/cbc:TaxAmount', ns_inv)
            if tax_tag is not None:
                tax_amount = float(tax_tag.text)
            
            items.append({
                'SKU_Proveedor': sku,
                'Descripcion': desc,
                'Cantidad_Facturada': qty,
                'Precio_Unitario': price_unit,
                'Subtotal': line_total,
                'Impuesto': tax_amount,
                'Total_Linea': line_total + tax_amount
            })
            
        header_data = {
            'Proveedor': proveedor,
            'Folio': folio,
            'Fecha': fecha,
            'Subtotal': total_sin_imp,
            'Total_Pagar': total_con_imp
        }
        
        return header_data, pd.DataFrame(items)
        
    except Exception as e:
        return None, f"Error procesando XML: {str(e)}"

# --- 4. DATOS MOCK (SIMULACIÓN BASE DE DATOS) ---
@st.cache_data
def get_mock_db():
    # Simulamos que tenemos estos productos en nuestro sistema para comparar precios
    return pd.DataFrame({
        'SKU_Interno': ['REF-1001', 'REF-1002', 'REF-1003', 'REF-1004'],
        'SKU_Proveedor': ['RTRXA0080106', '7704488003302', '7704488003319', '5890592'], # SKUs de tus XMLs ejemplo
        'Costo_Ultima_Compra': [9200, 130000, 130000, 250000],
        'Stock_Actual': [15, 4, 2, 10],
        'Orden_Compra_Pendiente': [25, 8, 2, 0] # Coincide con tus ejemplos
    })

# --- 5. UI: BARRA LATERAL ---
with st.sidebar:
    st.page_link("Portafolio_Servicios.py", label="🏠 Volver al Inicio", icon="🔙")
    st.divider()
    st.title("Configuración")
    almacen = st.selectbox("Almacén de Recepción:", ["Sede Principal", "Bodega Norte", "Tienda Centro"])
    st.info("Este módulo procesa archivos XML estándar UBL 2.1 (Facturación Electrónica DIAN).")
    
    # Botón para cargar XML de prueba (Demo Magic)
    if st.button("🪄 Cargar XML Demo (Abrasivos)", type="secondary"):
        st.session_state['demo_mode'] = 'abrasivos'
        st.toast("XML de prueba cargado en memoria", icon="💾")

# --- 6. UI: ENCABEZADO ---
st.title("📥 Recepción Inteligente XML")
st.markdown(f"Importación automática de inventario y cruce de cuentas para **{almacen}**.")

# --- 7. ZONA DE CARGA ---
col_upload, col_status = st.columns([2, 1])

with col_upload:
    uploaded_file = st.file_uploader("Arrastra el archivo XML de la factura aquí:", type=['xml'])

# --- LÓGICA DE PROCESAMIENTO ---
header = None
df_items = None
error_msg = None

# Si el usuario sube un archivo
if uploaded_file is not None:
    header, df_items = parse_dian_xml(uploaded_file)
    if df_items is None:
        st.error(error_msg)

# Si el usuario usa el botón DEMO (Simulación con tus datos reales copiados)
elif st.session_state.get('demo_mode') == 'abrasivos':
    # Simulamos el resultado del parsing de tu primer XML (Abrasivos)
    header = {
        'Proveedor': 'Abrasivos de Colombia S.A',
        'Folio': 'PG639060',
        'Fecha': '2025-11-19',
        'Subtotal': 235075.00,
        'Total_Pagar': 270806.40
    }
    df_items = pd.DataFrame([{
        'SKU_Proveedor': 'RTRXA0080106',
        'Descripcion': 'MULTI-FLEX #80 rollo de 6" x25mts',
        'Cantidad_Facturada': 25.0,
        'Precio_Unitario': 9403.00,
        'Subtotal': 235075.00,
        'Impuesto': 35731.40,
        'Total_Linea': 270806.40
    }])

# --- 8. VISTA DE RESULTADOS ---
if header and df_items is not None:
    
    # 8.1 Encabezado de Factura (KPIs)
    st.divider()
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.markdown(f"""<div class="metric-container"><div class="metric-val">{header['Proveedor']}</div><div class="metric-lbl">Proveedor Detectado</div></div>""", unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"""<div class="metric-container"><div class="metric-val">{header['Folio']}</div><div class="metric-lbl">N° Factura</div></div>""", unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"""<div class="metric-container"><div class="metric-val">${header['Total_Pagar']:,.0f}</div><div class="metric-lbl">Total a Pagar (Inc. IVA)</div></div>""", unsafe_allow_html=True)
    with kpi4:
        st.markdown(f"""<div class="metric-container"><div class="metric-val">{len(df_items)}</div><div class="metric-lbl">Líneas / Referencias</div></div>""", unsafe_allow_html=True)

    # 8.2 CRUCE INTELIGENTE (MATCHING)
    st.markdown("### 🔍 Análisis de Discrepancias (Cruce Automático)")
    
    # Cargar base de datos mock
    df_db = get_mock_db()
    
    # Cruzar Factura vs Sistema (Join por SKU proveedor)
    df_analisis = pd.merge(df_items, df_db, on='SKU_Proveedor', how='left')
    
    # Lógica de Semáforo y Validación
    df_analisis['SKU_Interno'] = df_analisis['SKU_Interno'].fillna("⚠️ NUEVO")
    df_analisis['Diferencia_Costo'] = df_analisis['Precio_Unitario'] - df_analisis['Costo_Ultima_Compra']
    df_analisis['Diferencia_Costo_Pct'] = (df_analisis['Diferencia_Costo'] / df_analisis['Costo_Ultima_Compra']) * 100
    
    # Calcular cantidades pendientes vs recibidas
    df_analisis['Estado_Recepcion'] = np.where(
        df_analisis['Cantidad_Facturada'] == df_analisis['Orden_Compra_Pendiente'],
        "✅ OK",
        np.where(
            df_analisis['Cantidad_Facturada'] > df_analisis['Orden_Compra_Pendiente'],
            "🔴 Exceso", "🟡 Parcial"
        )
    )
    
    # Preparar DF para visualización
    df_view = df_analisis[[
        'SKU_Proveedor', 'Descripcion', 'SKU_Interno', 
        'Cantidad_Facturada', 'Orden_Compra_Pendiente', 'Estado_Recepcion',
        'Precio_Unitario', 'Costo_Ultima_Compra', 'Diferencia_Costo_Pct'
    ]].copy()

    # Formatear para mostrar
    def color_diff(val):
        if pd.isna(val): return "color: black"
        if val > 5: return "color: red; font-weight: bold" # Alerta si subió > 5%
        if val < 0: return "color: green" # Bajó precio
        return "color: gray"

    st.dataframe(
        df_view.style.map(color_diff, subset=['Diferencia_Costo_Pct'])
                     .format({
                         'Precio_Unitario': '${:,.2f}', 
                         'Costo_Ultima_Compra': '${:,.2f}',
                         'Diferencia_Costo_Pct': '{:+.1f}%',
                         'Cantidad_Facturada': '{:,.0f}',
                         'Orden_Compra_Pendiente': '{:,.0f}'
                     }),
        use_container_width=True,
        column_config={
            "SKU_Interno": st.column_config.TextColumn("Homologación", help="Código interno del sistema"),
            "Diferencia_Costo_Pct": st.column_config.TextColumn("Var. Precio", help="Variación vs última compra"),
            "Estado_Recepcion": st.column_config.Column("Match OC")
        }
    )

    # Alertas Inteligentes
    items_nuevos = df_analisis[df_analisis['SKU_Interno'] == "⚠️ NUEVO"]
    items_caros = df_analisis[df_analisis['Diferencia_Costo_Pct'] > 5]
    
    c_alert1, c_alert2 = st.columns(2)
    with c_alert1:
        if not items_nuevos.empty:
            st.warning(f"⚠️ **Atención:** Se detectaron {len(items_nuevos)} productos nuevos no registrados en el maestro. Se crearán automáticamente.")
            with st.expander("Ver productos nuevos"):
                st.dataframe(items_nuevos[['SKU_Proveedor', 'Descripcion']])
        else:
            st.success("✅ Todos los productos están homologados en el maestro.")
            
    with c_alert2:
        if not items_caros.empty:
            st.error(f"💸 **Alerta de Precios:** {len(items_caros)} productos subieron más del 5% de costo.")
            with st.expander("Ver variaciones de precio"):
                 st.dataframe(items_caros[['Descripcion', 'Precio_Unitario', 'Costo_Ultima_Compra', 'Diferencia_Costo_Pct']])
        else:
            st.success("✅ Precios estables respecto a la última compra.")

    # --- 9. ACCIONES DE CIERRE ---
    st.markdown("### 🚀 Acciones de Recepción")
    
    c_act1, c_act2, c_act3 = st.columns([1, 1, 2])
    
    with c_act1:
        if st.button("💾 Guardar Recepción", type="primary", use_container_width=True):
            with st.spinner("Actualizando inventario y costos promedios..."):
                time.sleep(2)
                st.success(f"Inventario actualizado en {almacen}.")
                st.toast("Entrada de mercancía #REC-2024-999 creada", icon="✅")
                
    with c_act2:
        if st.button("🖨️ Imprimir Etiquetas", use_container_width=True):
            st.toast(f"Generando {int(df_items['Cantidad_Facturada'].sum())} etiquetas de código de barras...", icon="🏷️")
            time.sleep(1)
            st.info("PDF de etiquetas enviado a la impresora de bodega.")

else:
    # Estado inicial (Placeholder visual)
    st.info("👈 Sube un XML o usa el botón de 'Cargar XML Demo' en la barra lateral para ver la magia.")
    
    # Mostrar estructura esperada para educar al usuario
    with st.expander("¿Qué tipo de XML procesamos?"):
        st.markdown("""
        Este sistema está diseñado para la **Facturación Electrónica de Colombia (DIAN - UBL 2.1)**.
        Procesamos automáticamente:
        * `AttachedDocument` (Contenedor principal)
        * `Invoice` (Datos financieros incrustados en CDATA)
        * Validación automática de `cbc:InvoicedQuantity` y `cac:StandardItemIdentification`.
        """)
