import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import random
import io
from fpdf import FPDF # Asegúrate de que fpdf esté en requirements.txt
import xlsxwriter # Asegúrate de que xlsxwriter esté en requirements.txt

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="NEXUS OPS | Abastecimiento Estratégico",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS (TEMA CLARO Y LEGIBLE) ---
st.markdown("""
<style>
    /* Fondo General y Tipografía */
    .stApp {
        background-color: #FFFFFF;
        color: #333333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Tarjetas de Métricas (KPIs) */
    .metric-card {
        background-color: #F8F9FA;
        border: 1px solid #E9ECEF;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #2E86C1;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #2E86C1;
    }
    .metric-label {
        font-size: 14px;
        color: #666666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Bloques de Guía Estratégica (Narrativa de Venta) */
    .guide-box {
        background-color: #E8F4FD;
        border-left: 4px solid #2E86C1;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
        color: #0C3658;
    }
    .guide-title {
        font-weight: bold;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 5px;
    }
    
    /* Personalización de Tabs */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    /* Botones primarios más fuertes */
    div.stButton > button:first-child {
        font-weight: bold;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. MOTOR DE SIMULACIÓN DE DATOS ---
@st.cache_data
def init_mock_data():
    """Genera datos base para la demostración."""
    tiendas = ['Sede Principal', 'Norte', 'Sur', 'Occidente', 'Outlet']
    proveedores = ['DISTRIBUIDORA GLOBAL', 'IMPORTADOS S.A.', 'ACEROS DEL CARIBE', 'HERRAMIENTAS PRO', 'ELECTRO-MUNDO']
    categorias = ['Herramientas', 'Construcción', 'Eléctricos', 'Pinturas', 'Seguridad Ind.']
    
    data = []
    for i in range(1001, 1081): # 80 productos
        cat = random.choice(categorias)
        sku = f"{cat[:3].upper()}-{i}"
        costo = np.random.randint(5000, 250000)
        
        for tienda in tiendas:
            demanda = np.random.randint(0, 60)
            stock = np.random.randint(0, 120)
            
            # Lógica para forzar escenarios interesantes
            if random.random() < 0.15: stock = 0 # Quiebre
            if random.random() < 0.10: stock = 300 # Excedente masivo
            
            # Cálculo de necesidades
            necesidad = max(0, (demanda * 1.5) - stock) # Cobertura 1.5 meses
            excedente = max(0, stock - (demanda * 3)) # Excedente si > 3 meses
            
            # Clasificación ABC
            valor_movimiento = demanda * costo
            abc = 'A' if valor_movimiento > 5000000 else ('B' if valor_movimiento > 1000000 else 'C')

            data.append({
                'SKU': sku,
                'Descripcion': f"Item {cat} Profesional {i}",
                'Categoria': cat,
                'Marca_Nombre': random.choice(['Makita', 'Bosch', '3M', 'Pintuco', 'Schneider']),
                'Proveedor': random.choice(proveedores),
                'Almacen_Nombre': tienda,
                'Stock': stock,
                'Costo_Promedio_UND': costo,
                'Precio_Venta': costo * 1.4,
                'Peso_Articulo': round(random.uniform(0.5, 10.0), 2),
                'Demanda_Mes': demanda,
                'Necesidad_Total': int(necesidad),
                'Excedente_Trasladable': int(excedente),
                'Stock_En_Transito': 0,
                'Segmento_ABC': abc
            })
    return pd.DataFrame(data)

if 'df_maestro' not in st.session_state:
    st.session_state.df_maestro = init_mock_data()

# Lógica de abastecimiento
def calcular_abastecimiento(df):
    df['Sugerencia_Traslado'] = df.apply(lambda x: min(x['Necesidad_Total'], 12) if x['Necesidad_Total'] > 0 else 0, axis=1)
    df['Sugerencia_Compra'] = (df['Necesidad_Total'] - df['Sugerencia_Traslado']).clip(lower=0)
    return df

df_work = calcular_abastecimiento(st.session_state.df_maestro.copy())

# --- 2. GENERADORES DE DOCUMENTOS (PDF Y EXCEL) ---

def generar_excel(df, hoja="Reporte"):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name=hoja)
    
    workbook = writer.book
    worksheet = writer.sheets[hoja]
    header_fmt = workbook.add_format({'bold': True, 'fg_color': '#2E86C1', 'font_color': 'white', 'border': 1})
    
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_fmt)
        worksheet.set_column(col_num, col_num, 20)
        
    writer.close()
    return output.getvalue()

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'NEXUS OPS - Reporte Operativo', 0, 1, 'C')
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

def generar_pdf(df, titulo):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    
    pdf.cell(0, 10, f"{titulo} - Generado: {datetime.now().strftime('%Y-%m-%d')}", 0, 1)
    pdf.ln(5)
    
    # Tabla simple
    col_width = pdf.w / (len(df.columns) + 1)
    row_height = 6
    
    # Header
    pdf.set_font("Arial", 'B', 8)
    for col in df.columns:
        pdf.cell(col_width, row_height, str(col)[:12], 1) # Truncar nombres largos
    pdf.ln()
    
    # Rows
    pdf.set_font("Arial", '', 8)
    for i, row in df.iterrows():
        for col in df.columns:
            txt = str(row[col])
            pdf.cell(col_width, row_height, txt[:15], 1) # Truncar datos largos
        pdf.ln()
        
    return pdf.output(dest='S').encode('latin-1')

# --- UI: BARRA LATERAL ---
with st.sidebar:
    st.page_link("Portafolio_Servicios.py", label="🏠 Volver al Inicio", icon="🔙")
    st.divider()
    st.image("https://cdn-icons-png.flaticon.com/512/1541/1541476.png", width=60)
    st.title("Filtros Globales")
    
    lista_tiendas = ["Todas"] + sorted(df_work['Almacen_Nombre'].unique())
    filtro_tienda = st.selectbox("Sede / Almacén:", lista_tiendas)
    
    lista_marcas = sorted(df_work['Marca_Nombre'].unique())
    filtro_marca = st.multiselect("Filtrar Marcas:", lista_marcas, default=lista_marcas[:3])
    
    st.info("📅 Datos en Tiempo Real\nConexión ERP: Activa")

# Filtrado Global
if filtro_tienda != "Todas":
    df_vista = df_work[df_work['Almacen_Nombre'] == filtro_tienda]
else:
    df_vista = df_work

if filtro_marca:
    df_vista = df_vista[df_vista['Marca_Nombre'].isin(filtro_marca)]

# --- UI: ENCABEZADO ---
st.title("🏭 NEXUS OPS | Centro de Control Logístico")
st.markdown("Plataforma unificada para la automatización de compras, traslados y optimización de inventario.")

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Diagnóstico Estratégico", 
    "🚚 Gestión de Traslados", 
    "🛒 Gestión de Compras", 
    "📡 Torre de Control"
])

# === TAB 1: DIAGNÓSTICO ===
with tab1:
    st.markdown("""
    <div class="guide-box">
        <div class="guide-title">💡 Guía Estratégica: Diagnóstico</div>
        Esta vista le permite identificar en segundos dónde está atrapado su capital y dónde está perdiendo ventas. 
        Los gráficos interactivos le permiten profundizar desde la Categoría hasta el SKU.
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    
    total_inv = df_vista['Stock'] * df_vista['Costo_Promedio_UND']
    total_compra = df_vista['Sugerencia_Compra'] * df_vista['Costo_Promedio_UND']
    total_ahorro = df_vista['Sugerencia_Traslado'] * df_vista['Costo_Promedio_UND']
    skus_quiebre = len(df_vista[df_vista['Stock'] == 0])

    with c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Valor Inventario</div><div class="metric-value">${total_inv.sum()/1e6:,.1f} M</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card" style="border-color:#EF553B;"><div class="metric-label">Necesidad de Compra</div><div class="metric-value" style="color:#EF553B">${total_compra.sum()/1e6:,.1f} M</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card" style="border-color:#00CC96;"><div class="metric-label">Ahorro x Traslados</div><div class="metric-value" style="color:#00CC96">${total_ahorro.sum()/1e6:,.1f} M</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-card"><div class="metric-label">SKUs en Quiebre</div><div class="metric-value">{skus_quiebre}</div></div>', unsafe_allow_html=True)

    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.subheader("Distribución de Inversión (Drill-down)")
        # Sunburst Chart (Mucho mejor que barras simples)
        fig_sun = px.sunburst(
            df_vista, 
            path=['Categoria', 'Marca_Nombre'], 
            values='Costo_Promedio_UND',
            color='Segmento_ABC',
            color_discrete_map={'A':'#EF553B', 'B':'#FFA15A', 'C':'#00CC96'},
            title="Jerarquía de Valor: Categoría > Marca"
        )
        fig_sun.update_layout(height=450)
        st.plotly_chart(fig_sun, use_container_width=True)
        
    with col_chart2:
        st.subheader("Salud del Inventario")
        # Gauge Chart
        eficiencia = 100 - (skus_quiebre / len(df_vista) * 100)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = eficiencia,
            title = {'text': "Nivel de Servicio (%)"},
            gauge = {'axis': {'range': [None, 100]},
                     'bar': {'color': "#2E86C1"},
                     'steps': [
                         {'range': [0, 80], 'color': "#F9EBEA"},
                         {'range': [80, 100], 'color': "#E8F8F5"}],
                     'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}}))
        fig_gauge.update_layout(height=350)
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.info("**Análisis:** Un nivel de servicio del 90%+ es ideal. Si está por debajo, priorice las compras de productos 'A'.")

# === TAB 2: TRASLADOS ===
with tab2:
    st.markdown("""
    <div class="guide-box">
        <div class="guide-title">🚚 Guía Estratégica: Centro de Traslados</div>
        El algoritmo cruza tiendas con **Excedentes** vs tiendas con **Necesidades**.
        <br>1. Seleccione los ítems que desea aprobar.
        <br>2. Descargue el PDF/Excel para bodega o envíe la orden directamente.
    </div>
    """, unsafe_allow_html=True)
    
    df_traslados = df_vista[df_vista['Sugerencia_Traslado'] > 0].copy()
    
    if df_traslados.empty:
        st.success("✅ Inventario balanceado. No se requieren traslados en este momento.")
    else:
        # Preparar datos para edición
        df_traslados['Origen_Sugerido'] = df_traslados['Almacen_Nombre'].apply(lambda x: "Sede Principal" if x != "Sede Principal" else "Norte")
        df_display_tras = df_traslados[['SKU', 'Descripcion', 'Origen_Sugerido', 'Almacen_Nombre', 'Sugerencia_Traslado', 'Costo_Promedio_UND']].head(15)
        df_display_tras.columns = ['SKU', 'Producto', 'Origen', 'Destino', 'Cantidad', 'Costo Unit.']
        df_display_tras['Seleccionar'] = False
        
        # Editor interactivo
        edited_traslados = st.data_editor(
            df_display_tras,
            column_config={
                "Seleccionar": st.column_config.CheckboxColumn(required=True),
                "Cantidad": st.column_config.NumberColumn(min_value=1, step=1),
                "Costo Unit.": st.column_config.NumberColumn(format="$%d")
            },
            use_container_width=True,
            hide_index=True,
            key="editor_tras"
        )
        
        # Lógica de Selección
        seleccionados_tras = edited_traslados[edited_traslados['Seleccionar']]
        
        st.markdown("---")
        col_actions1, col_actions2, col_actions3 = st.columns(3)
        
        if not seleccionados_tras.empty:
            cant_total = seleccionados_tras['Cantidad'].sum()
            valor_total = (seleccionados_tras['Cantidad'] * seleccionados_tras['Costo Unit.']).sum()
            
            with col_actions1:
                st.caption("Resumen Selección")
                st.markdown(f"**{len(seleccionados_tras)} Ítems** | **{cant_total} Unidades**")
                st.markdown(f"Valor Mercancía: **${valor_total:,.0f}**")
            
            with col_actions2:
                st.caption("Exportar Documentos")
                
                # Generar Excel
                excel_data = generar_excel(seleccionados_tras, "Traslados")
                st.download_button(
                    label="📥 Descargar Excel (Bodega)",
                    data=excel_data,
                    file_name="Orden_Traslado.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                
                # Generar PDF
                pdf_data = generar_pdf(seleccionados_tras, "ORDEN DE TRASLADO INTERNO")
                st.download_button(
                    label="📄 Descargar PDF (Legal)",
                    data=pdf_data,
                    file_name="Orden_Traslado.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
            with col_actions3:
                st.caption("Acción Inmediata")
                if st.button("🚀 Procesar y Notificar", type="primary", use_container_width=True):
                    with st.spinner("Conectando con API de Logística..."):
                        time.sleep(2)
                        st.success(f"¡Orden procesada! Se envió notificación a {seleccionados_tras['Origen'].unique()[0]}.")
                        st.toast("Correo enviado a logistica@empresa.com", icon="📧")
        else:
            st.info("👆 Seleccione ítems en la tabla para ver las opciones de exportación.")

# === TAB 3: COMPRAS ===
with tab3:
    st.markdown("""
    <div class="guide-box">
        <div class="guide-title">🛒 Guía Estratégica: Generador de Compras</div>
        El sistema sugiere compras basadas en el <b>Punto de Reorden</b> y el <b>Lead Time</b> del proveedor.
        Agrupe sus compras por proveedor para optimizar costos de envío.
    </div>
    """, unsafe_allow_html=True)
    
    df_compras = df_vista[df_vista['Sugerencia_Compra'] > 0].copy()
    
    # Filtro Proveedor
    list_prov = sorted(df_compras['Proveedor'].unique())
    sel_prov = st.selectbox("Seleccionar Proveedor para Generar Orden:", list_prov)
    
    df_prov = df_compras[df_compras['Proveedor'] == sel_prov].head(20)
    df_prov['Total_Linea'] = df_prov['Sugerencia_Compra'] * df_prov['Costo_Promedio_UND']
    
    # Preparar tabla
    df_display_compra = df_prov[['SKU', 'Descripcion', 'Stock', 'Sugerencia_Compra', 'Costo_Promedio_UND', 'Total_Linea']]
    df_display_compra.columns = ['SKU', 'Producto', 'Stock Actual', 'Cant. Sugerida', 'Costo Unit.', 'Total Estimado']
    df_display_compra['Incluir'] = True
    
    edited_compras = st.data_editor(
        df_display_compra,
        column_config={
            "Incluir": st.column_config.CheckboxColumn(required=True),
            "Cant. Sugerida": st.column_config.NumberColumn(min_value=1, step=1),
            "Costo Unit.": st.column_config.NumberColumn(format="$%d"),
            "Total Estimado": st.column_config.ProgressColumn(format="$%d", min_value=0, max_value=int(df_display_compra['Total Estimado'].max()))
        },
        use_container_width=True,
        hide_index=True,
        key="editor_compra"
    )
    
    seleccionados_compra = edited_compras[edited_compras['Incluir']]
    
    st.markdown("---")
    c_buy1, c_buy2 = st.columns([2, 1])
    
    with c_buy1:
        total_oc = (seleccionados_compra['Cant. Sugerida'] * seleccionados_compra['Costo Unit.']).sum()
        st.subheader(f"Total Orden de Compra: ${total_oc:,.0f}")
        st.markdown(f"Proveedor: **{sel_prov}** | Ítems: **{len(seleccionados_compra)}**")
        
    with c_buy2:
        st.markdown("#### Exportar Orden")
        # Excel
        excel_oc = generar_excel(seleccionados_compra, "Orden_Compra")
        st.download_button("📥 Excel (Formato Proveedor)", data=excel_oc, file_name=f"OC_{sel_prov}.xlsx", use_container_width=True)
        
        # PDF
        pdf_oc = generar_pdf(seleccionados_compra, f"ORDEN DE COMPRA - {sel_prov}")
        st.download_button("📄 PDF (Formato Firma)", data=pdf_oc, file_name=f"OC_{sel_prov}.pdf", use_container_width=True)
        
        if st.button("📧 Enviar por Email al Proveedor", type="primary", use_container_width=True):
            time.sleep(1)
            st.toast(f"Orden enviada a pedidos@{sel_prov.lower().replace(' ', '')}.com", icon="✅")

# === TAB 4: TRACKING ===
with tab4:
    st.subheader("📡 Torre de Control: Seguimiento en Vivo")
    
    # Datos Mock de Tracking
    tracking_data = [
        {"ID": "OC-2024-001", "Fecha": "2024-02-20", "Tipo": "Compra", "Proveedor/Destino": "DISTRIBUIDORA GLOBAL", "Estado": "🟢 Recibido", "Total": "$15,400,000"},
        {"ID": "OC-2024-002", "Fecha": "2024-02-21", "Tipo": "Compra", "Proveedor/Destino": "IMPORTADOS S.A.", "Estado": "🟡 En Tránsito", "Total": "$8,200,000"},
        {"ID": "TR-2024-88", "Fecha": "2024-02-22", "Tipo": "Traslado", "Proveedor/Destino": "Tienda Norte -> Sur", "Estado": "🔵 Despachado", "Total": "$0"},
        {"ID": "OC-2024-003", "Fecha": "2024-02-22", "Tipo": "Compra", "Proveedor/Destino": "HERRAMIENTAS PRO", "Estado": "⚪ Pendiente Aprobación", "Total": "$4,500,000"},
    ]
    df_track = pd.DataFrame(tracking_data)
    
    st.dataframe(
        df_track,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Estado": st.column_config.Column(width="medium"),
            "Total": st.column_config.TextColumn(width="small")
        }
    )
    
    st.button("🔄 Actualizar Estados (API Transportadora)")
