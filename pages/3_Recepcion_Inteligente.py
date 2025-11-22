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
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ESTILOS CSS (FUSIÓN Y MEJORAS) ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #333333; font-family: 'Segoe UI', sans-serif; }
    
    /* Contenedor Principal de Pasos (Step Container) */
    .step-container {
        background-color: #F0F8FF;
        padding: 25px;
        border-radius: 12px;
        border-left: 8px solid #2E86C1;
        margin-bottom: 30px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .step-title { 
        font-size: 24px; 
        font-weight: bold; 
        color: #2E86C1; 
        margin-bottom: 10px; 
        display: flex; 
        align-items: center;
    }
    .step-icon { margin-right: 10px; font-size: 28px; }

    /* Cajas de Métricas */
    .metric-box {
        background-color: #F8F9FA;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        border-top: 4px solid #1ABC9C; /* Nuevo color para KPIs principales */
        transition: transform 0.2s;
    }
    .metric-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
    }
    .metric-val { font-size: 28px; font-weight: 800; color: #1ABC9C; }
    .metric-lbl { font-size: 13px; color: #666; text-transform: uppercase; margin-top: 5px; }
    
    /* Alertas de Beneficios */
    .benefit-alert {
        padding: 15px;
        border-radius: 8px;
        background-color: #eafaea; /* Fondo verde claro */
        border-left: 5px solid #1ABC9C; /* Borde verde fuerte */
        margin-top: 15px;
        margin-bottom: 20px;
        font-size: 15px;
        line-height: 1.6;
    }
    .benefit-alert strong { color: #1ABC9C; }

    /* Botones */
    div.stButton > button:first-child { 
        border-radius: 6px; 
        font-weight: 700; 
        transition: background-color 0.3s;
    }
    .st-emotion-cache-1cpx97z.e1f1d6z51 { /* Target Streamlit primary button */
        background-color: #2E86C1 !important;
        border-color: #2E86C1 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. GESTIÓN DE ESTADO (SESSION STATE) ---
if 'reception_step' not in st.session_state:
    st.session_state.reception_step = 0 # 0: Inicio/Dashboard, 1: Carga, 2: Conteo, 3: Cierre

if 'current_invoice_data' not in st.session_state:
    st.session_state.current_invoice_data = None

# Base de datos maestra simulada (Persistente)
if 'master_db' not in st.session_state:
    st.session_state.master_db = pd.DataFrame({
        'SKU_Interno': ['FER-DIS-001', 'FER-TOR-002', 'PIN-VIN-003', 'REF-1001'],
        'SKU_Proveedor': ['RTRXA0080106', 'REF-TEST-001', 'REF-TEST-002', '7704488003302'], 
        'Descripcion_Interna': ['Disco Corte Metal 4.5"', 'Tornillo Drywall 1/2"', 'Vinilo Blanco Galón', 'Producto Existente Ejemplo'],
        'Stock_Actual': [100.0, 500.0, 40.0, 15.0],
        'Costo_Ultima_Compra': [9200.0, 50.0, 120000.0, 130000.0]
    })

# --- 4. MOTOR DE PARSING (Mantiene el parseo robusto) ---
def clean_tag(tag):
    """Elimina los namespaces {urn...} de los tags XML."""
    return tag.split('}', 1)[1] if '}' in tag else tag

def parse_dian_xml_engine(uploaded_file):
    """
    Lee el XML (AttachedDocument), extrae la factura interna (CDATA) y parsea los ítems,
    incluyendo la extracción de Totales de Impuestos.
    """
    try:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()
        
        # 1. Extracción de Metadatos (Proveedor)
        namespaces = {'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
                      'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
                      'ad': 'urn:dian:gov:co:facturaelectronica:AttachedDocument'}
        
        proveedor_tag = root.find('.//cac:SenderParty/cac:PartyTaxScheme/cbc:RegistrationName', namespaces)
        proveedor = proveedor_tag.text if proveedor_tag is not None else "Proveedor Desconocido"
        
        # 2. Extraer el XML interno (CDATA dentro de Description)
        desc_tag = root.find('.//cac:Attachment/cac:ExternalReference/cbc:Description', namespaces)
        
        if desc_tag is None or not desc_tag.text:
            return None, "No se encontró el contenido de la factura (Invoice) dentro del XML. Archivo Inválido."
            
        xml_content = desc_tag.text.strip()
        
        # Parsear el XML interno
        invoice_root = ET.fromstring(xml_content)
        
        # Namespace map para el Invoice interno
        ns_inv = {'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
                  'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}
        
        # Datos Generales Factura
        folio = invoice_root.find('.//cbc:ID', ns_inv).text
        fecha = invoice_root.find('.//cbc:IssueDate', ns_inv).text
        
        # Totales Generales
        total_sin_imp_tag = invoice_root.find('.//cac:LegalMonetaryTotal/cbc:LineExtensionAmount', ns_inv)
        total_sin_imp = float(total_sin_imp_tag.text) if total_sin_imp_tag is not None else 0.0

        total_con_imp_tag = invoice_root.find('.//cac:LegalMonetaryTotal/cbc:PayableAmount', ns_inv)
        total_con_imp = float(total_con_imp_tag.text) if total_con_imp_tag is not None else 0.0
        
        iva_total = 0.0
        tax_total_element = invoice_root.find('.//cac:TaxTotal/cbc:TaxAmount', ns_inv)
        if tax_total_element is not None:
             iva_total = float(tax_total_element.text)
        else:
             iva_total = total_con_imp - total_sin_imp

        # 3. Extraer Líneas (Ítems)
        items = []
        for i, line in enumerate(invoice_root.findall('.//cac:InvoiceLine', ns_inv)):
            # USAMOS UN ÍNDICE ÚNICO PARA CADA LÍNEA DE FACTURA
            line_id = i + 1 
            
            qty_tag = line.find('.//cbc:InvoicedQuantity', ns_inv)
            qty = float(qty_tag.text) if qty_tag is not None else 0.0
            
            desc_tag = line.find('.//cac:Item/cbc:Description', ns_inv)
            desc = desc_tag.text if desc_tag is not None else "Sin Descripción"
            
            # Referencia / SKU
            sku = "GENERICO"
            std_id = line.find('.//cac:Item/cac:StandardItemIdentification/cbc:ID', ns_inv)
            seller_id = line.find('.//cac:Item/cac:SellersItemIdentification/cbc:ID', ns_inv)
            
            if std_id is not None and std_id.text: sku = std_id.text
            elif seller_id is not None and seller_id.text: sku = seller_id.text
            
            # Precios
            price_tag = line.find('.//cac:Price/cbc:PriceAmount', ns_inv)
            price_unit = float(price_tag.text) if price_tag is not None else 0.0
            
            total_tag = line.find('.//cbc:LineExtensionAmount', ns_inv)
            line_subtotal = float(total_tag.text) if total_tag is not None else 0.0
            
            # Impuestos de Línea
            line_tax_amount = 0.0
            tax_tag = line.find('.//cac:TaxTotal/cbc:TaxAmount', ns_inv)
            if tax_tag is not None:
                line_tax_amount = float(tax_tag.text)
            
            items.append({
                'Line_ID': line_id, # Clave de unicidad
                'SKU_Proveedor': sku,
                'Descripcion_Factura': desc,
                'Cantidad_Facturada': qty,
                'Precio_Unitario': price_unit,
                'Subtotal_Linea': line_subtotal,
                'Impuesto_Linea': line_tax_amount,
                'Total_Linea': line_subtotal + line_tax_amount
            })
            
        header_data = {
            'Proveedor': proveedor,
            'Folio': folio,
            'Fecha': fecha,
            'Subtotal_Factura': total_sin_imp,
            'IVA_Factura': iva_total,
            'Total_Factura': total_con_imp
        }
        
        return header_data, pd.DataFrame(items)
        
    except Exception as e:
        return None, f"Error procesando XML. Asegúrese de que es un AttachedDocument (DIAN): {str(e)}"

# --- 5. FUNCIONES DE NEGOCIO Y UTILIDADES ---

def homologar_inventario(df_factura):
    """Cruza los ítems de la factura con la BD Maestra."""
    maestro = st.session_state.master_db
    
    # Cruzar por SKU_Proveedor
    df_merged = pd.merge(df_factura, maestro, on='SKU_Proveedor', how='left', suffixes=('_Factura', '_Maestro'))
    
    # Identificar si es nuevo
    df_merged['Estado_Producto'] = np.where(df_merged['SKU_Interno'].isna(), '🆕 NUEVO', '✅ EXISTENTE')
    
    # Generar SKU Temporal para los nuevos y usar el interno para existentes
    def generar_sku_final(row):
        if pd.notna(row['SKU_Interno']): 
            return row['SKU_Interno'] # Ya existe en el maestro
        # Lógica simple para SKU temporal (NUEVO-AAAA)
        # Usamos el Line_ID para garantizar que cada línea tenga un SKU_Interno_Final único, 
        # aunque el SKU_Proveedor se repita, evitando el merge duplicado en la conciliación.
        clean_sku = ''.join(e for e in str(row['SKU_Proveedor']) if e.isalnum())[:8]
        return f"NUEVO-{clean_sku}-{row['Line_ID']}"

    df_merged['SKU_Interno_Final'] = df_merged.apply(generar_sku_final, axis=1)
    df_merged['Descripcion_Final'] = df_merged['Descripcion_Interna'].fillna(df_merged['Descripcion_Factura'])
    
    # Calculo de variación de precio
    df_merged['Diferencia_Precio_Pct'] = np.where(
        df_merged['Costo_Ultima_Compra'].notna() & (df_merged['Costo_Ultima_Compra'] > 0),
        ((df_merged['Precio_Unitario'] - df_merged['Costo_Ultima_Compra']) / df_merged['Costo_Ultima_Compra']) * 100,
        np.nan 
    )
    
    return df_merged

def generar_excel_conciliacion(df, folio, proveedor):
    """Genera un Excel con formato bonito para descargar (USO INTERNO - Conciliación)."""
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    # Columnas a exportar
    cols_export = [
        'SKU_Interno_Final', 'Descripcion_Final', 'Cantidad_Facturada', 'Cant_Recibida', 
        'Diferencia', 'Estado_Conciliacion', 'Precio_Unitario', 'Total_Linea'
    ]
    
    df[cols_export].to_excel(writer, index=False, sheet_name='Conciliacion')
    
    workbook = writer.book
    worksheet = writer.sheets['Conciliacion']
    
    # Formatos
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#2E86C1', 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
    
    for col_num, value in enumerate(cols_export):
        worksheet.write(0, col_num, value, header_fmt)
        worksheet.set_column(col_num, col_num, 20)
        
    writer.close()
    return output.getvalue()

def generar_datos_erp(df, header):
    """Genera el Excel y el TXT con la información de la recepción final para el ERP."""
    
    # 1. Preparar DF para ERP
    df_erp = df[[
        'SKU_Interno_Final', 
        'Descripcion_Final', 
        'Cant_Recibida', 
        'Precio_Unitario'
    ]].copy()
    
    df_erp = df_erp.rename(columns={
        'SKU_Interno_Final': 'REFERENCIA_INTERNA',
        'Descripcion_Final': 'NOMBRE_PRODUCTO',
        'Cant_Recibida': 'UNIDADES_RECIBIDAS',
        'Precio_Unitario': 'COSTO_UNITARIO'
    })
    
    # Asegurar que solo se incluyan ítems recibidos (Cant_Recibida > 0)
    df_erp = df_erp[df_erp['UNIDADES_RECIBIDAS'] > 0]

    # --- Generación de Excel ---
    output_excel = io.BytesIO()
    writer_excel = pd.ExcelWriter(output_excel, engine='xlsxwriter')
    
    # Hoja de Encabezado (para referencia)
    df_header_info = pd.DataFrame([header]).T.reset_index()
    df_header_info.columns = ['Campo', 'Valor']
    df_header_info.to_excel(writer_excel, sheet_name='Encabezado', index=False)
    
    # Hoja de Detalle (el que sube al ERP)
    df_erp.to_excel(writer_excel, sheet_name='Detalle_Compra', index=False)

    writer_excel.close()
    excel_data = output_excel.getvalue()

    # --- Generación de TXT (Formato Plano Delimitado por Comas) ---
    output_txt = io.StringIO()
    # Escribir encabezado de la compra (simulación)
    output_txt.write(f"TIPO_COMPRA,PROVEEDOR_ID,NUMERO_FACTURA,FECHA_FACTURA\n")
    output_txt.write(f"FACTURA_VENTA,{header['Proveedor']},{header['Folio']},{header['Fecha']}\n")
    output_txt.write("REFERENCIA_INTERNA,UNIDADES_RECIBIDAS,COSTO_UNITARIO,COSTO_TOTAL\n")

    # Escribir líneas de detalle
    for index, row in df_erp.iterrows():
        total = row['UNIDADES_RECIBIDAS'] * row['COSTO_UNITARIO']
        output_txt.write(
            f"{row['REFERENCIA_INTERNA']},"
            f"{row['UNIDADES_RECIBIDAS']},"
            f"{row['COSTO_UNITARIO']:.2f},"
            f"{total:.2f}\n"
        )
    
    txt_data = output_txt.getvalue().encode('utf-8')
    
    return excel_data, txt_data

# --- 6. INTERFAZ DE USUARIO (SIDEBAR Y MAIN DASHBOARD) ---

with st.sidebar:
    st.title("NEXUS XML")
    
    # Definir pasos para el progreso visual
    step_map = {0: "Inicio", 1: "Carga XML", 2: "Conteo Físico", 3: "Cierre ERP"}
    current_step_name = step_map.get(st.session_state.reception_step, "Inicio")
    st.markdown(f"**Progreso:** {st.session_state.reception_step}/3 - {current_step_name}")
    st.progress(st.session_state.reception_step / 3)
    
    if st.session_state.current_invoice_data:
        h = st.session_state.current_invoice_data['header']
        st.info(f"📄 **Factura: {h['Folio']}**\n\n**Proveedor:** {h['Proveedor']}\n**Total:** ${h['Total_Factura']:,.0f}")
    
    st.divider()
    if st.button("🔄 Reiniciar Proceso y Volver al Inicio"):
        st.session_state.reception_step = 0
        st.session_state.current_invoice_data = None
        if 'demo_mode' in st.session_state: del st.session_state.demo_mode
        st.rerun()

st.title("🚀 Recepción Inteligente de Mercancía Vía XML")

# ==============================================================================
# PASO 0: DASHBOARD DE INICIO (El Brutal)
# ==============================================================================
if st.session_state.reception_step == 0:
    st.markdown("""
    <div class="step-container">
        <div class="step-title"><span class="step-icon">💡</span>Inicio Rápido: El Poder de la Automatización</div>
        Cero errores, cero digitación manual, cero pérdidas de tiempo. **NEXUS** transforma su recepción en un proceso ágil y totalmente controlado.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ¿Por qué automatizar la Recepción con NEXUS?")
    
    c_speed, c_accuracy, c_erp = st.columns(3)
    
    with c_speed:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-val'>95%</div>
            <div class='metric-lbl'>Reducción de Tiempo</div>
            <p style='font-size: 14px; margin-top: 10px; color: #555;'>No más teclear cada ítem. El sistema lee el XML y lo compara en segundos.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with c_accuracy:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-val'>0%</div>
            <div class='metric-lbl'>Errores de Digitación</div>
            <p style='font-size: 14px; margin-top: 10px; color: #555;'>La lectura directa del XML elimina por completo el riesgo de errores humanos en cantidades y precios.</p>
        </div>
        """, unsafe_allow_html=True)

    with c_erp:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-val'>1 CLIC</div>
            <div class='metric-lbl'>Integración con ERP</div>
            <p style='font-size: 14px; margin-top: 10px; color: #555;'>Generamos un archivo listo (TXT/Excel) para subir la compra a su sistema contable (SAP, SIIGO, etc.).</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("▶️ Iniciar Recepción (Paso 1)", type="primary", use_container_width=True):
        st.session_state.reception_step = 1
        st.rerun()

# ==============================================================================
# PASO 1: CARGA Y ANÁLISIS (Motor Parsing + Homologación)
# ==============================================================================
elif st.session_state.reception_step == 1:
    st.markdown("""
    <div class="step-container">
        <div class="step-title"><span class="step-icon">1️⃣</span> Carga de Factura Electrónica y Validación</div>
        El sistema extrae, valida e identifica automáticamente cualquier anomalía en precios o inventario.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="benefit-alert">
    ✅ **Beneficio Clave (Paso 1):** Detección de Fugas. Aquí sabrá si su proveedor le subió el precio (variación mayor al 5%) o le envió un producto nuevo. ¡Tome decisiones antes de recibir la mercancía!
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    uploaded_file = None

    with col1:
        uploaded_file = st.file_uploader("Arrastra el XML (AttachedDocument de la DIAN) aquí:", type=['xml'])
    with col2:
        st.write("") 
        st.write("")
        if st.button("🪄 Cargar Demo (Simulación)"):
            st.session_state['demo_mode'] = True
            st.toast("Modo Demo Activado", icon="🧪")

    # Lógica de Procesamiento
    header = None
    df_items = None
    error_msg = None

    if uploaded_file is not None:
        header, df_items = parse_dian_xml_engine(uploaded_file) 
        if df_items is None:
            error_msg = header 

    elif st.session_state.get('demo_mode'):
        # Simulamos resultado del motor para DEMO (Asegurando Line_ID para la unicidad)
        header = {
            'Proveedor': 'FERRETERIA EJEMPLO S.A', 
            'Folio': 'PG639060', 
            'Fecha': '2025-11-20',
            'Subtotal_Factura': 285075.0,
            'IVA_Factura': 54164.25,
            'Total_Factura': 339239.25
        }
        df_items = pd.DataFrame([
            {'Line_ID': 1, 'SKU_Proveedor': 'RTRXA0080106', 'Descripcion_Factura': 'MULTI-FLEX #80', 'Cantidad_Facturada': 25.0, 'Precio_Unitario': 9403.0, 'Subtotal_Linea': 235075.0, 'Impuesto_Linea': 44664.25, 'Total_Linea': 279739.25},
            {'Line_ID': 2, 'SKU_Proveedor': 'NUEVO-999', 'Descripcion_Factura': 'GRANALLA ACERO TEMPLADO', 'Cantidad_Facturada': 10.0, 'Precio_Unitario': 5000.0, 'Subtotal_Linea': 50000.0, 'Impuesto_Linea': 9500.0, 'Total_Linea': 59500.0},
            # Ítem duplicado en SKU_Proveedor pero distinto Line_ID para probar homologación (genera SKU_Interno_Final diferente)
            {'Line_ID': 3, 'SKU_Proveedor': 'NUEVO-999', 'Descripcion_Factura': 'GRANALLA ACERO TEMPLADO C/IVA', 'Cantidad_Facturada': 5.0, 'Precio_Unitario': 6000.0, 'Subtotal_Linea': 30000.0, 'Impuesto_Linea': 5700.0, 'Total_Linea': 35700.0}
        ])

    # Mostrar Resultados Preliminares
    if header and df_items is not None:
        # Ejecutar homologación
        df_homologado = homologar_inventario(df_items)
        
        # Guardar en sesión temporalmente
        temp_data = {'header': header, 'items': df_homologado}
        
        # KPIs Header (Totales)
        st.divider()
        k1, k2, k3, k4 = st.columns(4)
        k1.markdown(f"<div class='metric-box'><div class='metric-val'>{header['Folio']}</div><div class='metric-lbl'>Factura</div></div>", unsafe_allow_html=True)
        k2.markdown(f"<div class='metric-box'><div class='metric-val'>${header['Subtotal_Factura']:,.0f}</div><div class='metric-lbl'>Subtotal</div></div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='metric-box'><div class='metric-val'>${header['IVA_Factura']:,.0f}</div><div class='metric-lbl'>IVA (Impuesto)</div></div>", unsafe_allow_html=True)
        k4.markdown(f"<div class='metric-box'><div class='metric-val'>${header['Total_Factura']:,.0f}</div><div class='metric-lbl'>Total C/IVA</div></div>", unsafe_allow_html=True)


        st.markdown("### 🔍 Análisis de Precios y Homologación")
        
        # Colorear diferencias de precio
        def color_precio(val):
            if pd.isna(val): return "" # No aplica para nuevos
            if val > 5: return "color: red; font-weight: bold; background-color: #ffcccc"
            if val < -5: return "color: green; font-weight: bold; background-color: #ccffcc"
            return ""

        st.dataframe(
            df_homologado[[
                'SKU_Proveedor', 'Descripcion_Factura', 'Estado_Producto', 'SKU_Interno_Final',
                'Cantidad_Facturada', 'Precio_Unitario', 'Costo_Ultima_Compra', 'Diferencia_Precio_Pct'
            ]].style.map(color_precio, subset=['Diferencia_Precio_Pct']).format({
                'Precio_Unitario': 'COP {:,.0f}',
                'Costo_Ultima_Compra': 'COP {:,.0f}',
                'Diferencia_Precio_Pct': '{:+.1f}%',
                'Cantidad_Facturada': '{:,.0f}'
            }),
            use_container_width=True,
            column_order=('SKU_Proveedor', 'Descripcion_Factura', 'Estado_Producto', 'SKU_Interno_Final', 'Cantidad_Facturada', 'Precio_Unitario', 'Costo_Ultima_Compra', 'Diferencia_Precio_Pct')
        )

        nuevos = df_homologado[df_homologado['Estado_Producto'] == '🆕 NUEVO']
        if not nuevos.empty:
            st.warning(f"⚠️ **Atención:** Se identificaron **{len(nuevos)}** productos sin referencia interna. Serán creados temporalmente con un ID único por línea para la conciliación.")
        
        st.markdown("---")
        if st.button("➡️ Confirmar Datos e Iniciar Conteo Físico", type="primary", use_container_width=True):
            st.session_state.current_invoice_data = temp_data
            st.session_state.reception_step = 2
            st.rerun()
            
    elif error_msg:
        st.error(error_msg)

# ==============================================================================
# PASO 2: CONTEO FÍSICO (Simulación Lector de Barras)
# ==============================================================================
elif st.session_state.reception_step == 2:
    st.markdown("""
    <div class="step-container">
        <div class="step-title"><span class="step-icon">2️⃣</span> Verificación Física (El Cuadre de Bodega)</div>
        ¡Simule un proceso de bodega eficiente! Use el lector de códigos de barras (o ingrese el SKU/Cantidad) y capture la recepción en tiempo real.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="benefit-alert">
    **Beneficio Clave (Paso 2):** Agilidad en Bodega. Con la ayuda de un escáner de barras, el operario solo valida las unidades, minimizando el tiempo de descarga y la posibilidad de enviar mercancía sin registrar. ¡El inventario se actualiza con la realidad del conteo físico!
    </div>
    """, unsafe_allow_html=True)
    
    data = st.session_state.current_invoice_data['items']
    
    # Preparar DF de conteo si no existe (inicializar Cant_Recibida y Novedad)
    if 'conteo_real' not in st.session_state.current_invoice_data:
        # Usamos Line_ID como clave de unicidad invisible
        df_conteo_init = data[['Line_ID', 'SKU_Interno_Final', 'Descripcion_Final', 'Cantidad_Facturada']].copy()
        df_conteo_init['Cant_Recibida'] = 0.0
        df_conteo_init['Novedad'] = ""
        st.session_state.current_invoice_data['conteo_real'] = df_conteo_init
    
    df_conteo = st.session_state.current_invoice_data['conteo_real'].copy()

    
    # --- Formulario de Simulación (Lector de Barras) ---
    with st.form("form_barcode_scan"):
        st.markdown("#### Simulación de Escaneo / Ingreso Rápido")
        col_scan_sku, col_scan_qty = st.columns([2, 1])
        
        scanned_sku = col_scan_sku.text_input("SKU / Código de Barras (Presione Enter)", key="scanned_sku").strip()
        scanned_qty = col_scan_qty.number_input("Unidades Recibidas", min_value=0.0, value=1.0, step=1.0, key="scanned_qty")
        
        submit_scan = st.form_submit_button("✅ Registrar Entrada")
        
        if submit_scan and scanned_sku:
            # Buscar el SKU en las referencias finales (interna o temporal)
            match_index = df_conteo[df_conteo['SKU_Interno_Final'] == scanned_sku].index
            
            if match_index.empty:
                 # Intentar buscar por SKU_Proveedor en el DF base
                match_base = data[data['SKU_Proveedor'] == scanned_sku]
                if not match_base.empty:
                    # Si hay un match, tomamos el primer SKU_Interno_Final asociado
                    final_sku = match_base.iloc[0]['SKU_Interno_Final']
                    match_index = df_conteo[df_conteo['SKU_Interno_Final'] == final_sku].index
                    if len(match_index) > 1:
                        st.warning(f"SKU {scanned_sku} está repetido en la factura. Asigne manualmente la cantidad en la tabla de conteo.")
                        # Si está repetido, no podemos asignarlo automáticamente con el lector.
                        match_index = pd.Index([])

            
            if not match_index.empty:
                idx = match_index[0]
                # Sumar las unidades al conteo actual
                df_conteo.loc[idx, 'Cant_Recibida'] = df_conteo.loc[idx, 'Cant_Recibida'] + scanned_qty
                st.session_state.current_invoice_data['conteo_real'] = df_conteo
                st.toast(f"Registrado {scanned_qty} unid. de {df_conteo.loc[idx, 'Descripcion_Final']}", icon="📦")
                time.sleep(0.1)
                st.rerun() 
            else:
                st.error(f"SKU '{scanned_sku}' no encontrado en la factura. Verifique o ingrese manualmente la cantidad.")
                
    # --- Herramientas y Grid del Conteo ---
    c_tools, c_grid = st.columns([1, 4])
    
    with c_tools:
        st.markdown("#### Acciones")
        if st.button("⚡ TODO OK (Auto-Recibir)", help="Copia la cantidad facturada a recibida para todas las líneas"):
            df_conteo['Cant_Recibida'] = df_conteo['Cantidad_Facturada']
            st.session_state.current_invoice_data['conteo_real'] = df_conteo
            st.toast("Cantidades copiadas (Todo OK)", icon="✅")
            st.rerun() 
            
    with c_grid:
        # Aquí es donde se usa Line_ID como clave oculta para garantizar que los datos vuelvan correctamente
        edited_conteo = st.data_editor(
            df_conteo,
            column_config={
                "Line_ID": st.column_config.NumberColumn(disabled=True, width="hidden"), # Ocultar la clave
                "SKU_Interno_Final": st.column_config.TextColumn("Ref. Interna (Conteo)", disabled=True),
                "Descripcion_Final": st.column_config.TextColumn("Producto", disabled=True),
                "Cantidad_Facturada": st.column_config.NumberColumn("Facturado", disabled=True, format="%.0f"),
                "Cant_Recibida": st.column_config.NumberColumn("Conteo Físico", required=True, min_value=0.0, step=1.0, format="%.0f"),
                "Novedad": st.column_config.TextColumn("Observación")
            },
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            key="editor_conteo"
        )

    st.markdown("---")
    col_prev, col_next = st.columns([1, 5])
    
    if col_prev.button("⬅️ Atrás (Análisis)", help="Volver al paso de validación del XML"):
        st.session_state.reception_step = 1
        st.rerun()
        
    if col_next.button("➡️ Finalizar y Conciliar", type="primary"):
        # Guardar la edición final de la grilla
        st.session_state.current_invoice_data['conteo_real'] = edited_conteo
        st.session_state.reception_step = 3
        st.rerun()

# ==============================================================================
# PASO 3: CONCILIACIÓN Y CIERRE (Conexión ERP)
# ==============================================================================
elif st.session_state.reception_step == 3:
    st.markdown("""
    <div class="step-container">
        <div class="step-title"><span class="step-icon">3️⃣</span> Cierre, Conciliación Final y Conexión ERP</div>
        Revisión de la diferencia entre lo facturado y lo contado. Generación de archivos listos para su sistema.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="benefit-alert">
    **Beneficio Clave (Paso 3):** Archivos Listos para Subir. El proceso termina con un archivo (Excel/TXT) que cumple con el formato de su ERP para subir la compra. ¡El inventario se actualiza en segundos sin que nadie digite el detalle de la factura!
    </div>
    """, unsafe_allow_html=True)
    
    # Preparar datos finales
    df_base = st.session_state.current_invoice_data['items']
    df_conteo = st.session_state.current_invoice_data['conteo_real']
    header = st.session_state.current_invoice_data['header']
    
    # Merge final USANDO 'Line_ID' como clave para EVITAR DUPLICADOS
    df_final = pd.merge(
        df_conteo,
        # Seleccionamos las columnas relevantes del DF base
        df_base[['Line_ID', 'Precio_Unitario', 'Total_Linea', 'Estado_Producto', 'SKU_Proveedor', 'Costo_Ultima_Compra', 'Descripcion_Interna']],
        on='Line_ID', # Clave UNICA de la línea de factura
        how='left'
    )
    
    # Eliminar la clave temporal de Line_ID si se usó para el merge
    if 'SKU_Interno_Final' in df_final.columns and 'Line_ID' in df_final.columns:
        # Se mantienen 'SKU_Interno_Final', 'Descripcion_Final' del df_conteo (ya que contiene los datos del editor)
        pass

    # Calcular discrepancias
    df_final['Diferencia'] = df_final['Cant_Recibida'] - df_final['Cantidad_Facturada']
    df_final['Estado_Conciliacion'] = np.where(df_final['Diferencia'] == 0, '✅ OK', 
                                     np.where(df_final['Diferencia'] < 0, '🔴 FALTANTE', '🟡 SOBRANTE'))
    
    # Calcular valores
    valor_entrada = (df_final['Cant_Recibida'] * df_final['Precio_Unitario']).sum()
    
    # KPIs
    faltantes = df_final[df_final['Diferencia'] < 0]
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Unidades Recibidas", int(df_final['Cant_Recibida'].sum()))
    k2.metric("Valor Entrada (Costo)", f"${valor_entrada:,.0f}")
    k3.metric("Referencias con Diferencia", len(df_final[df_final['Diferencia'] != 0]), delta_color="off")
    k4.metric("Referencias con Faltantes", len(faltantes), delta_color="inverse")
    
    st.markdown("### 📋 Resumen de la Conciliación (Factura vs. Conteo)")
        
    # Tabla Final
    def highlight_diff(row):
        # Color rojo para faltantes, verde para sobrantes
        if row['Diferencia'] < 0: return ['background-color: #ffebee'] * len(row)
        if row['Diferencia'] > 0: return ['background-color: #e8f5e9'] * len(row)
        return [''] * len(row)

    st.dataframe(
        df_final[[
            'SKU_Interno_Final', 'Descripcion_Final', 'Cantidad_Facturada', 
            'Cant_Recibida', 'Diferencia', 'Estado_Conciliacion', 'Precio_Unitario', 'Total_Linea'
        ]].style.apply(highlight_diff, axis=1).format({
            'Precio_Unitario': '${:,.0f}',
            'Total_Linea': '${:,.0f}',
            'Cantidad_Facturada': '{:,.0f}',
            'Cant_Recibida': '{:,.0f}',
            'Diferencia': '{:,.0f}'
        }),
        use_container_width=True
    )
    
    if not faltantes.empty:
        st.error("🚨 ¡Atención! Hay discrepancias en el conteo. Revise el reporte de conciliación antes de subir al ERP.")
    
    st.markdown("---")
    st.markdown("### 💾 Generación de Archivos para ERP y Actualización")
    
    c_excel_rep, c_excel_erp, c_txt_erp, c_save = st.columns(4)
    
    # 1. Reporte de Conciliación (Para uso interno/Reclamos)
    with c_excel_rep:
        excel_data_conc = generar_excel_conciliacion(df_final, header['Folio'], header['Proveedor'])
        st.download_button(
            label="📥 Reporte Interno (Excel)",
            data=excel_data_conc,
            file_name=f"CONCILIACION_{header['Folio']}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Reporte detallado de la diferencia entre Facturado vs. Contado.",
            use_container_width=True
        )

    # 2. Archivos para Subir al ERP
    excel_erp_data, txt_erp_data = generar_datos_erp(df_final, header)
    
    with c_excel_erp:
        st.download_button(
            label="📄 Archivo Compra ERP (Excel)",
            data=excel_erp_data,
            file_name=f"ERP_COMPRA_EXCEL_{header['Folio']}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Formato listo para subir la compra a su sistema contable/ERP.",
            use_container_width=True
        )
        
    with c_txt_erp:
        st.download_button(
            label="📝 Archivo Compra ERP (TXT)",
            data=txt_erp_data,
            file_name=f"ERP_COMPRA_TXT_{header['Folio']}.txt",
            mime="text/plain",
            help="Formato plano (CSV/TXT) delimitado, ideal para ERPs antiguos.",
            use_container_width=True
        )
        
    # 3. Botón de Actualización de Inventario (Acción Final)
    with c_save:
        btn_txt = "🚀 Finalizar y Actualizar Inventario"
        if st.button(btn_txt, type="primary", use_container_width=True):
            with st.spinner("Actualizando Maestro y Kardex..."):
                time.sleep(2)
                
                # 1. Identificar y añadir nuevos productos (usando el SKU_Interno_Final único)
                nuevos_recibidos = df_final[(df_final['Estado_Producto'] == '🆕 NUEVO') & (df_final['Cant_Recibida'] > 0)]
                if not nuevos_recibidos.empty:
                    # Crear el DataFrame de nuevos SIN DUPLICAR (gracias al Line_ID en el SKU_Interno_Final)
                    nuevos_a_db = pd.DataFrame({
                        'SKU_Interno': nuevos_recibidos['SKU_Interno_Final'],
                        'SKU_Proveedor': nuevos_recibidos['SKU_Proveedor'], 
                        'Descripcion_Interna': nuevos_recibidos['Descripcion_Final'],
                        'Stock_Actual': nuevos_recibidos['Cant_Recibida'],
                        'Costo_Ultima_Compra': nuevos_recibidos['Precio_Unitario']
                    })
                    st.session_state.master_db = pd.concat([st.session_state.master_db, nuevos_a_db], ignore_index=True)
                
                # 2. Actualizar stock y costo de existentes (usando el SKU_Interno único)
                existentes_actualizar = df_final[df_final['Estado_Producto'] == '✅ EXISTENTE']
                for idx, row in existentes_actualizar.iterrows():
                    sku = row['SKU_Interno_Final'] # Es el SKU_Interno real de la BD
                    cant = row['Cant_Recibida']
                    costo_nuevo = row['Precio_Unitario']
                    
                    # 1. Sumar Stock (solo si la cantidad recibida es positiva)
                    # USAMOS .loc con el SKU_Interno de la BD Maestra para asegurarnos de que solo actualizamos una fila
                    if cant > 0:
                         st.session_state.master_db.loc[st.session_state.master_db['SKU_Interno'] == sku, 'Stock_Actual'] += cant
                    
                    # 2. Actualizar Costo de Última Compra
                    st.session_state.master_db.loc[st.session_state.master_db['SKU_Interno'] == sku, 'Costo_Ultima_Compra'] = costo_nuevo


                st.balloons()
                st.success(f"¡Recepción {header['Folio']} Finalizada! Inventario actualizado con éxito. Regresando al inicio...")
                
                time.sleep(3)
                st.session_state.reception_step = 0
                st.session_state.current_invoice_data = None
                if 'demo_mode' in st.session_state: del st.session_state.demo_mode
                st.rerun()

# Fin del script
