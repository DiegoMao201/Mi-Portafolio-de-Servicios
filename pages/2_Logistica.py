import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
import io
from fpdf import FPDF
import xlsxwriter

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="NEXUS PRO | Abastecimiento Estratégico",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ESTILOS CSS (TEMA CLARO Y CORPORATIVO) ---
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
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #2E86C1;
    }
    .metric-label {
        font-size: 13px;
        color: #666666;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Bloques de Guía Estratégica (Narrativa de Venta) */
    .guide-box {
        background-color: #E8F4FD;
        border-left: 4px solid #2E86C1;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 25px;
        color: #0C3658;
        font-size: 15px;
    }
    .guide-title {
        font-weight: 700;
        font-size: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }
    
    /* Personalización de Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.0rem;
        font-weight: 600;
    }
    
    /* Botones */
    div.stButton > button:first-child {
        border-radius: 6px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE SIMULACIÓN DE DATOS (BACKEND SIMULADO) ---
@st.cache_data
def init_mock_data():
    """Genera datos base realistas para la demostración."""
    tiendas = ['Sede Principal', 'Norte', 'Sur', 'Occidente', 'Outlet']
    proveedores = ['DISTRIBUIDORA GLOBAL', 'IMPORTADOS S.A.', 'ACEROS DEL CARIBE', 'HERRAMIENTAS PRO', 'ELECTRO-MUNDO']
    categorias = ['Herramientas', 'Construcción', 'Eléctricos', 'Pinturas', 'Seguridad Ind.']
    
    data = []
    for i in range(1001, 1081): # 80 productos simulados
        cat = random.choice(categorias)
        sku = f"{cat[:3].upper()}-{i}"
        costo = np.random.randint(5000, 250000)
        
        for tienda in tiendas:
            demanda = np.random.randint(0, 60)
            stock = np.random.randint(0, 120)
            
            # Lógica para forzar escenarios interesantes para el demo
            if random.random() < 0.15: stock = 0 # Quiebre forzado
            if random.random() < 0.10: stock = 300 # Excedente forzado
            
            # Cálculo de necesidades (Lógica de negocio)
            necesidad = max(0, (demanda * 1.5) - stock) # Cobertura ideal 1.5 meses
            excedente = max(0, stock - (demanda * 3)) # Excedente si supera 3 meses
            
            # Clasificación ABC basada en valor
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

# Inicializar estado
if 'df_maestro' not in st.session_state:
    st.session_state.df_maestro = init_mock_data()

# Lógica de abastecimiento (Separa qué se puede trasladar vs comprar)
def calcular_abastecimiento(df):
    # Si hay necesidad, intentamos cubrir hasta 12 unidades con traslados (simulación)
    df['Sugerencia_Traslado'] = df.apply(lambda x: min(x['Necesidad_Total'], 12) if x['Necesidad_Total'] > 0 else 0, axis=1)
    # Lo que falte, se compra
    df['Sugerencia_Compra'] = (df['Necesidad_Total'] - df['Sugerencia_Traslado']).clip(lower=0)
    return df

df_work = calcular_abastecimiento(st.session_state.df_maestro.copy())

# --- MOCK DE DATOS PARA LA TORRE DE CONTROL (ACTUALIZADO) ---
@st.cache_data
def get_tracking_data(df_maestro):
    """Genera datos simulados y persistentes de órdenes de compra y traslado."""
    
    proveedores = df_maestro['Proveedor'].unique()
    almacenes = df_maestro['Almacen_Nombre'].unique()
    
    data_list = []
    
    # Simulación de Órdenes de Compra (OC)
    for i in range(101, 111):
        date_created = datetime.now() - timedelta(days=random.randint(1, 45))
        supplier = random.choice(proveedores)
        
        # Simulación de estados con probabilidad
        rand_val = random.random()
        if rand_val < 0.2:
            status = "🟢 Recibido (100%)"
            date_status = date_created + timedelta(days=random.randint(20, 30))
        elif rand_val < 0.4:
            status = "🟡 En Tránsito (Llega Hoy)"
            date_status = date_created + timedelta(days=random.randint(15, 19))
        elif rand_val < 0.6:
            status = "🔵 Despachado (En Ruta)"
            date_status = date_created + timedelta(days=random.randint(5, 14))
        elif rand_val < 0.8:
            status = "⚪ Pendiente Aprobación"
            date_status = date_created
        else:
            status = "🔴 Cancelada/Rechazada"
            date_status = date_created + timedelta(days=random.randint(1, 5))
            
        data_list.append({
            "ID_Orden": f"OC-{date_created.year}-1{i}",
            "Fecha_Creacion": date_created.strftime('%Y-%m-%d'),
            "Tipo": "Compra",
            "Portafolio": random.choice(df_maestro['Categoria'].unique()),
            "Tercero": supplier,
            "Almacen_Destino": random.choice(almacenes),
            "Estado": status,
            "Fecha_Estimada_Llegada": (date_status + timedelta(days=random.randint(1, 5))).strftime('%Y-%m-%d') if 'En Tránsito' in status else '',
            "Valor_Total": random.randint(3000000, 25000000),
            "Comentario": f"OC para {supplier}. Gestión de stock bajo."
        })

    # Simulación de Órdenes de Traslado (TR)
    for i in range(80, 85):
        date_created = datetime.now() - timedelta(days=random.randint(1, 15))
        store_origin = random.choice(almacenes)
        store_dest = random.choice([a for a in almacenes if a != store_origin])
        
        rand_val = random.random()
        if rand_val < 0.3:
            status = "🟢 Recibido (100%)"
            date_status = date_created + timedelta(days=random.randint(3, 7))
        elif rand_val < 0.7:
            status = "🔵 Despachado (En Ruta)"
            date_status = date_created + timedelta(days=random.randint(1, 3))
        else:
            status = "⚪ Pendiente Picking"
            date_status = date_created
            
        data_list.append({
            "ID_Orden": f"TR-{date_created.year}-0{i}",
            "Fecha_Creacion": date_created.strftime('%Y-%m-%d'),
            "Tipo": "Traslado",
            "Portafolio": random.choice(df_maestro['Categoria'].unique()),
            "Tercero": f"{store_origin} -> {store_dest}",
            "Almacen_Destino": store_dest,
            "Estado": status,
            "Fecha_Estimada_Llegada": (date_status + timedelta(days=random.randint(1, 2))).strftime('%Y-%m-%d') if 'Despachado' in status else '',
            "Valor_Total": 0,
            "Comentario": f"Traslado de excedente de {store_origin}."
        })
        
    df = pd.DataFrame(data_list)
    df['Fecha_Creacion'] = pd.to_datetime(df['Fecha_Creacion'])
    return df

# Inicializar datos de tracking
if 'df_tracking' not in st.session_state:
    st.session_state.df_tracking = get_tracking_data(st.session_state.df_maestro)


# --- 4. FUNCIONES GENERADORAS DE ARCHIVOS (EXCEL Y PDF) ---

def generar_excel(df, hoja="Reporte"):
    """Genera un archivo Excel en memoria bytes."""
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    # Pre-procesamiento: Quitar 'Seleccionar' y formatear
    df_temp = df.drop(columns=['Seleccionar'], errors='ignore')
    if 'Costo Unit.' in df_temp.columns:
        df_temp['Costo Unit.'] = df_temp['Costo Unit.'].apply(lambda x: f"${x:,.0f}")
    if 'Total Estimado' in df_temp.columns:
        df_temp['Total Estimado'] = df_temp['Total Estimado'].apply(lambda x: f"${x:,.0f}")
        
    df_temp.to_excel(writer, index=False, sheet_name=hoja)
    
    workbook = writer.book
    worksheet = writer.sheets[hoja]
    
    # Formatos profesionales
    header_fmt = workbook.add_format({'bold': True, 'fg_color': '#2E86C1', 'font_color': 'white', 'border': 1})
    
    for col_num, value in enumerate(df_temp.columns.values):
        worksheet.write(0, col_num, value, header_fmt)
        # Ajustar ancho
        worksheet.set_column(col_num, col_num, 20)
    
    writer.close()
    return output.getvalue()

class PDFReport(FPDF):
    """Clase personalizada para el PDF."""
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(46, 134, 193) # Azul corporativo
        self.cell(0, 10, 'NEXUS PRO - Reporte Operativo', 0, 1, 'C')
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

def generar_pdf(df, titulo):
    """Genera un PDF simple con tabla en memoria bytes."""
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"{titulo}", 0, 1, 'L')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 10, f"Fecha Generación: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'L')
    pdf.ln(5)
    
    # Pre-procesamiento: Quitar 'Seleccionar' y formatear para PDF
    df_temp = df.drop(columns=['Seleccionar'], errors='ignore').copy()
    if 'Costo Unit.' in df_temp.columns:
        df_temp['Costo Unit.'] = df_temp['Costo Unit.'].apply(lambda x: f"${x:,.0f}")
    if 'Total Estimado' in df_temp.columns:
        df_temp['Total Estimado'] = df_temp['Total Estimado'].apply(lambda x: f"${x:,.0f}")

    # Tabla simple
    num_cols = len(df_temp.columns)
    col_width = 190 / num_cols if num_cols > 0 else 10
    row_height = 7
    
    # Encabezados
    pdf.set_font("Arial", 'B', 8)
    pdf.set_fill_color(232, 244, 253) # Azul muy claro
    for col in df_temp.columns:
        clean_col = str(col)[:15]
        pdf.cell(col_width, row_height, clean_col, 1, 0, 'C', True)
    pdf.ln()
    
    # Filas
    pdf.set_font("Arial", '', 8)
    for i, row in df_temp.iterrows():
        for col in df_temp.columns:
            txt = str(row[col])
            # Truncar texto de celda si es muy largo
            pdf.cell(col_width, row_height, txt[:18], 1, 0, 'C')
        pdf.ln()
    
    return bytes(pdf.output())

# --- 5. UI: BARRA LATERAL DE NAVEGACIÓN ---
with st.sidebar:
    st.page_link("Home.py", label="🏠 Volver al Inicio", icon="🔙")
    st.divider()
    
    # Simulación de logo
    st.markdown("<h2 style='text-align: center; color: #2E86C1;'>NEXUS PRO</h2>", unsafe_allow_html=True)
    
    st.subheader("Filtros Globales")
    
    lista_tiendas = ["Todas"] + sorted(df_work['Almacen_Nombre'].unique())
    filtro_tienda = st.selectbox("Sede / Almacén:", lista_tiendas)
    
    lista_marcas = sorted(df_work['Marca_Nombre'].unique())
    filtro_marca = st.multiselect("Filtrar Marcas:", lista_marcas, default=lista_marcas[:3])
    
    st.divider()
    st.info("🟢 **Conexión ERP:** Establecida\n📅 **Datos:** Tiempo Real")

# Aplicar Filtros Globales
if filtro_tienda != "Todas":
    df_vista = df_work[df_work['Almacen_Nombre'] == filtro_tienda]
else:
    df_vista = df_work

if filtro_marca:
    df_vista = df_vista[df_vista['Marca_Nombre'].isin(filtro_marca)]

# --- 6. UI: ENCABEZADO PRINCIPAL ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🏭 Abastecimiento Inteligente")
    st.markdown("Gestión unificada de abastecimiento, inventarios y distribución.")
with col_h2:
    if st.button("🔄 Actualizar Análisis"):
        st.toast("Recalculando algoritmos de abastecimiento...", icon="🤖")
        time.sleep(1)
        # Forzamos un recálculo simple para simular frescura de datos
        st.session_state.df_maestro = init_mock_data()
        st.session_state.df_tracking = get_tracking_data(st.session_state.df_maestro)
        st.rerun()

# --- 7. PESTAÑAS DE CONTENIDO ---
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
        Esta vista le permite identificar en segundos dónde está atrapado su capital y dónde está perdiendo ventas por quiebres.
        <br>Utilice el gráfico de <b>Nivel de Servicio</b> para medir la calidad de su inventario actual.
    </div>
    """, unsafe_allow_html=True)

    # KPIs Principales
    c1, c2, c3, c4 = st.columns(4)
    
    total_inv = (df_vista['Stock'] * df_vista['Costo_Promedio_UND']).sum()
    total_compra = (df_vista['Sugerencia_Compra'] * df_vista['Costo_Promedio_UND']).sum()
    total_ahorro = (df_vista['Sugerencia_Traslado'] * df_vista['Costo_Promedio_UND']).sum()
    skus_quiebre = len(df_vista[df_vista['Stock'] == 0])

    with c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Valor Inventario Actual</div><div class="metric-value">${total_inv/1e6:,.1f} M</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card" style="border-color:#EF553B;"><div class="metric-label">Inversión Requerida</div><div class="metric-value" style="color:#EF553B">${total_compra/1e6:,.1f} M</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card" style="border-color:#00CC96;"><div class="metric-label">Ahorro x Traslados</div><div class="metric-value" style="color:#00CC96">${total_ahorro/1e6:,.1f} M</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-card"><div class="metric-label">SKUs en Quiebre</div><div class="metric-value">{skus_quiebre}</div></div>', unsafe_allow_html=True)

    # Gráficos Avanzados
    st.markdown("---")
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.subheader("Distribución de Inversión (Interactivo)")
        # Sunburst Chart: Categoría -> Marca
        fig_sun = px.sunburst(
            df_vista, 
            path=['Categoria', 'Marca_Nombre'], 
            values='Costo_Promedio_UND',
            color='Segmento_ABC',
            color_discrete_map={'A':'#EF553B', 'B':'#FFA15A', 'C':'#00CC96'},
            title="Haga clic en los sectores para profundizar (Drill-down)"
        )
        fig_sun.update_layout(height=450, margin=dict(t=30, l=0, r=0, b=0))
        st.plotly_chart(fig_sun, use_container_width=True)
        
    with col_chart2:
        st.subheader("Salud del Inventario")
        # Gauge Chart (Velocímetro)
        eficiencia = 100 - (skus_quiebre / len(df_vista) * 100) if len(df_vista) > 0 else 100
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = eficiencia,
            title = {'text': "Nivel de Servicio (%)"},
            gauge = {'axis': {'range': [None, 100]},
                     'bar': {'color': "#2E86C1"},
                     'steps': [
                         {'range': [0, 85], 'color': "#F9EBEA"},
                         {'range': [85, 100], 'color': "#E8F8F5"}],
                     'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}}))
        fig_gauge.update_layout(height=350, margin=dict(t=50, l=20, r=20, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.info("✅ **Meta:** Mantener el nivel de servicio por encima del 90% para asegurar la satisfacción del cliente.")

# === TAB 2: TRASLADOS ===
with tab2:
    st.markdown("""
    <div class="guide-box">
        <div class="guide-title">🚚 Guía Estratégica: Centro de Traslados</div>
        El sistema detecta automáticamente dónde sobra mercancía y dónde falta.
        <br><b>Acción:</b> Seleccione los productos en la tabla, descargue la orden y envíela a bodega para ahorrar capital de compra.
    </div>
    """, unsafe_allow_html=True)
    
    df_traslados = df_vista[df_vista['Sugerencia_Traslado'] > 0].copy()
    
    if df_traslados.empty:
        st.success("✅ Excelente. El inventario está balanceado. No se requieren traslados.")
    else:
        # Preparar datos para edición
        # Simulamos un origen lógico
        df_traslados['Origen_Sugerido'] = df_traslados['Almacen_Nombre'].apply(lambda x: "Sede Principal" if x != "Sede Principal" else "Norte")
        
        df_display_tras = df_traslados[['SKU', 'Descripcion', 'Origen_Sugerido', 'Almacen_Nombre', 'Sugerencia_Traslado', 'Costo_Promedio_UND']].head(20)
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
            key="editor_traslados_principal"
        )
        
        seleccionados_tras = edited_traslados[edited_traslados['Seleccionar']]
        
        st.markdown("---")
        
        # Panel de Acciones
        if not seleccionados_tras.empty:
            cant_total = seleccionados_tras['Cantidad'].sum()
            valor_total = (seleccionados_tras['Cantidad'] * seleccionados_tras['Costo Unit.']).sum()
            
            col_res, col_exp, col_act = st.columns([1, 1, 1])
            
            with col_res:
                st.markdown("#### Resumen")
                st.info(f"📦 **{len(seleccionados_tras)} Referencias**\n\n📊 **{cant_total} Unidades**\n\n💰 Valor: **${valor_total:,.0f}**")
            
            with col_exp:
                st.markdown("#### Exportar Documentos")
                
                # Generar Excel
                excel_data = generar_excel(seleccionados_tras, "Orden_Traslado")
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
                
            with col_act:
                st.markdown("#### Ejecución")
                if st.button("🚀 Procesar Traslado y Notificar", type="primary", use_container_width=True):
                    with st.spinner("Enviando notificaciones a Jefes de Bodega..."):
                        time.sleep(2)
                        st.success(f"¡Orden procesada! Se notificó a {seleccionados_tras['Origen'].iloc[0]} y {seleccionados_tras['Destino'].iloc[0]}.")
                        st.balloons()
        else:
            st.warning("👆 Por favor, seleccione al menos un ítem en la tabla para activar las opciones de exportación y envío.")

# === TAB 3: COMPRAS ===
with tab3:
    st.markdown("""
    <div class="guide-box">
        <div class="guide-title">🛒 Guía Estratégica: Generador de Compras</div>
        Aquí convertimos las "Sugerencias del Algoritmo" en "Órdenes de Compra" reales.
        <br>1. Seleccione un proveedor.
        <br>2. Ajuste las cantidades sugeridas si es necesario.
        <br>3. Genere el PDF para firma o envíe el email directamente.
    </div>
    """, unsafe_allow_html=True)
    
    df_compras = df_vista[df_vista['Sugerencia_Compra'] > 0].copy()
    
    # Filtro de Proveedor
    col_filtro_prov, col_info_prov = st.columns([1, 2])
    
    with col_filtro_prov:
        list_prov = sorted(df_compras['Proveedor'].unique())
        if not list_prov:
            st.success("No hay necesidades de compra pendientes.")
            st.stop()
            
        sel_prov = st.selectbox("Seleccionar Proveedor para Orden:", list_prov)
    
    # Filtrar datos
    df_prov = df_compras[df_compras['Proveedor'] == sel_prov].head(20)
    df_prov['Total_Linea'] = df_prov['Sugerencia_Compra'] * df_prov['Costo_Promedio_UND']
    
    with col_info_prov:
        total_sug = df_prov['Total_Linea'].sum()
        st.info(f"El sistema sugiere **{len(df_prov)} referencias** para **{sel_prov}** por un valor total de **${total_sug:,.0f}**")
    
    # Preparar tabla
    df_display_compra = df_prov[['SKU', 'Descripcion', 'Stock', 'Sugerencia_Compra', 'Costo_Promedio_UND', 'Total_Linea']]
    df_display_compra.columns = ['SKU', 'Producto', 'Stock Actual', 'Cant. Sugerida', 'Costo Unit.', 'Total Estimado']
    df_display_compra['Incluir'] = True # Checkbox por defecto activado
    
    st.markdown("##### Detalle de la Orden")
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
        key="editor_compra_principal"
    )
    
    seleccionados_compra = edited_compras[edited_compras['Incluir']]
    
    st.markdown("---")
    
    if not seleccionados_compra.empty:
        c_buy1, c_buy2 = st.columns([1, 1])
        
        with c_buy1:
            total_oc = (seleccionados_compra['Cant. Sugerida'] * seleccionados_compra['Costo Unit.']).sum()
            st.subheader(f"Total Orden: **${total_oc:,.0f}**")
            st.markdown(f"Items Seleccionados: **{len(seleccionados_compra)}**")
            
            if st.button("📧 Enviar Orden al Proveedor", type="primary", use_container_width=True):
                with st.spinner(f"Enviando correo a pedidos@{sel_prov.lower().replace(' ', '')}.com..."):
                    time.sleep(1.5)
                    st.success("✅ Orden enviada exitosamente.")
                    st.toast("Copia enviada a compras@tuempresa.com", icon="📨")
            
        with c_buy2:
            st.markdown("#### Descargar Archivos")
            # Excel
            excel_oc = generar_excel(seleccionados_compra, "Orden_Compra")
            st.download_button("📥 Descargar Excel (Formato Proveedor)", data=excel_oc, file_name=f"OC_{sel_prov}.xlsx", use_container_width=True)
            
            # PDF
            pdf_oc = generar_pdf(seleccionados_compra, f"ORDEN DE COMPRA - {sel_prov}")
            st.download_button("📄 Descargar PDF (Formato Firma)", data=pdf_oc, file_name=f"OC_{sel_prov}.pdf", use_container_width=True)
    else:
        st.warning("Seleccione al menos un producto para generar la orden.")

# === TAB 4: TRACKING (TORRE DE CONTROL ACTUALIZADA) ===
with tab4:
    st.header("📡 Torre de Control: Orquestación Total de la Cadena")
    
    st.markdown("""
    <div class="guide-box">
        <div class="guide-title">🚀 Valor Estratégico: Control y Aprendizaje</div>
        Esta Torre de Control le ofrece visibilidad total sobre **cada movimiento** (compra y traslado). 
        <br>Al centralizar esta información, la aplicación futura podrá:
        <ul>
            <li>**Evaluar Proveedores** en tiempo de entrega y faltantes.</li>
            <li>**Optimizar Rutas** de traslado.</li>
            <li>**Recomendar mejores proveedores** basándose en el historial de eficiencia.</li>
        </ul>
        **Todo el flujo operativo está bajo control.**
    </div>
    """, unsafe_allow_html=True)
    
    # 1. FILTROS DE LA TORRE DE CONTROL
    st.subheader("Filtros de Órdenes")
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    
    df_track_work = st.session_state.df_tracking.copy()

    with col_f1:
        tipo_orden = st.multiselect("Tipo de Orden:", ["Compra", "Traslado"], default=["Compra", "Traslado"])
        df_track_work = df_track_work[df_track_work['Tipo'].isin(tipo_orden)]

    with col_f2:
        estados = sorted(df_track_work['Estado'].unique())
        estado_sel = st.multiselect("Filtrar por Estado:", estados, default=[e for e in estados if 'Pendiente' in e or 'Tránsito' in e or 'Despachado' in e])
        df_track_work = df_track_work[df_track_work['Estado'].isin(estado_sel)]
        
    with col_f3:
        proveedores_list = sorted(df_track_work[df_track_work['Tipo'] == 'Compra']['Tercero'].unique())
        tercero_sel = st.multiselect("Proveedor / Ruta:", proveedores_list, default=proveedores_list)
        # Aseguramos incluir las rutas de traslado si se seleccionó ese tipo
        tercero_sel.extend(df_track_work[df_track_work['Tipo'] == 'Traslado']['Tercero'].unique())
        df_track_work = df_track_work[df_track_work['Tercero'].isin(tercero_sel)]

    with col_f4:
        # Filtro de fecha de creación (rango)
        min_date = df_track_work['Fecha_Creacion'].min().date() if not df_track_work.empty else datetime.now().date() - timedelta(days=30)
        max_date = df_track_work['Fecha_Creacion'].max().date() if not df_track_work.empty else datetime.now().date()
        date_range = st.date_input("Rango de Creación:", [min_date, max_date], max_value=datetime.now().date())
        
        if len(date_range) == 2:
            start_date = pd.to_datetime(date_range[0])
            end_date = pd.to_datetime(date_range[1]) + timedelta(days=1) # Incluir el final del día
            df_track_work = df_track_work[
                (df_track_work['Fecha_Creacion'] >= start_date) & 
                (df_track_work['Fecha_Creacion'] < end_date)
            ]

    st.markdown("---")
    
    # 2. TABLA DE GESTIÓN INTERACTIVA
    st.subheader("Gestión de Órdenes Pendientes y en Curso")
    
    # Preparamos la tabla para el Data Editor
    df_display_track = df_track_work.copy()
    
    # Formateo de columnas
    df_display_track['Valor_Total_Fmt'] = df_display_track.apply(lambda x: f"${x['Valor_Total']:,.0f}" if x['Tipo'] == 'Compra' else 'N/A', axis=1)
    df_display_track = df_display_track.sort_values(by='Fecha_Creacion', ascending=False)
    
    # Seleccionamos y renombramos columnas para la vista
    df_display_track = df_display_track[[
        'ID_Orden', 'Tipo', 'Fecha_Creacion', 'Tercero', 'Portafolio', 
        'Estado', 'Fecha_Estimada_Llegada', 'Valor_Total_Fmt', 'Comentario'
    ]]
    df_display_track.columns = [
        'ID', 'Tipo', 'Creada', 'Tercero/Ruta', 'Portafolio', 
        'Estado Actual', 'Llegada Est.', 'Valor (Compra)', 'Notas'
    ]

    
    if df_display_track.empty:
        st.warning("No hay órdenes que coincidan con los filtros seleccionados.")
    else:
        # Lógica de colores para los estados
        def get_color_style(estado):
            if 'Recibido' in estado: return 'background-color: #E8F8F5; color: #008000; font-weight: bold;' # Verde claro
            if 'Tránsito' in estado: return 'background-color: #FFF9E8; color: #FFA500; font-weight: bold;' # Amarillo claro
            if 'Despachado' in estado: return 'background-color: #E8F4FD; color: #2E86C1; font-weight: bold;' # Azul claro
            if 'Pendiente' in estado: return 'background-color: #F8F8F8; color: #555555;' # Gris claro
            if 'Cancelada' in estado or 'Rechazada' in estado: return 'background-color: #F9EBEA; color: #FF0000; font-weight: bold;' # Rojo claro
            return ''

        # Aplicamos el estilo de color (requiere una función de formato CSS en el dataframe)
        st.dataframe(
            df_display_track.style.applymap(get_color_style, subset=['Estado Actual']),
            use_container_width=True,
            hide_index=True,
            column_config={
                'ID': st.column_config.TextColumn("ID", width="small"),
                'Tipo': st.column_config.TextColumn("Tipo", width="small"),
                'Estado Actual': st.column_config.TextColumn("Estado Actual", width="medium"),
                'Llegada Est.': st.column_config.DateColumn("Llegada Est.", format="YYYY-MM-DD", width="small"),
                'Valor (Compra)': st.column_config.TextColumn("Valor (Compra)", width="small"),
                'Notas': st.column_config.TextColumn("Notas", width="medium")
            }
        )

    st.markdown("---")
    
    # 3. ACCIONES Y MÉTRICAS DE APRENDIZAJE
    st.subheader("Métricas Operativas Clave")
    
    # Simulación de KPIs de la Torre de Control
    df_compra = st.session_state.df_tracking[st.session_state.df_tracking['Tipo'] == 'Compra']
    oc_recibidas = len(df_compra[df_compra['Estado'].str.contains('Recibido')])
    oc_totales = len(df_compra)
    ot_recibidas = len(st.session_state.df_tracking[st.session_state.df_tracking['Tipo'] == 'Traslado']['Estado'].str.contains('Recibido'))
    ot_totales = len(st.session_state.df_tracking[st.session_state.df_tracking['Tipo'] == 'Traslado'])
    
    col_kpi_t1, col_kpi_t2, col_kpi_t3 = st.columns(3)
    
    with col_kpi_t1:
        tasa_cumplimiento = (oc_recibidas / oc_totales) * 100 if oc_totales > 0 else 0
        st.metric(label="Cumplimiento OC (Recibidas/Total)", value=f"{tasa_cumplimiento:,.1f}%", delta_color="normal", delta=f"{oc_recibidas}/{oc_totales}")
        st.caption("Mide la efectividad del proceso de compra.")

    with col_kpi_t2:
        # Tiempo promedio de entrega (Simulación)
        tiempo_promedio = random.randint(18, 25) # Días
        st.metric(label="Lead Time Prom. Proveedores", value=f"{tiempo_promedio} días", delta_color="inverse", delta=f"-2 días (vs mes ant.)")
        st.caption("Métrica crítica para el reabastecimiento.")

    with col_kpi_t3:
        # Traslados completados
        tasa_traslado = (ot_recibidas / ot_totales) * 100 if ot_totales > 0 else 0
        st.metric(label="Efectividad de Traslados", value=f"{tasa_traslado:,.1f}%", delta_color="normal", delta=f"{ot_recibidas}/{ot_totales}")
        st.caption("Indica la eficiencia en la redistribución interna.")

    st.markdown("#### Tablero de Aprendizaje")
    st.warning("🤖 En una implementación completa, esta sección mostraría un ranking de proveedores basado en **Lead Time**, **Faltantes** (inventario) y **Costo** (OC), permitiendo a NEXUS PRO optimizar continuamente las decisiones de compra.")
    
    if st.button("Simular Actualización de Estados de Órdenes", use_container_width=True):
        st.toast("Simulando una actualización de estado en las órdenes...", icon="📡")
        
        # Lógica de gestión simulada: mover 1 orden pendiente a 'Despachado'
        df_pending = st.session_state.df_tracking[st.session_state.df_tracking['Estado'].str.contains('Pendiente Aprobación')]
        if not df_pending.empty:
            idx = df_pending.index[0]
            st.session_state.df_tracking.loc[idx, 'Estado'] = "🔵 Despachado (En Ruta)"
            st.session_state.df_tracking.loc[idx, 'Fecha_Estimada_Llegada'] = (datetime.now() + timedelta(days=random.randint(5, 15))).strftime('%Y-%m-%d')
            st.success(f"La orden **{st.session_state.df_tracking.loc[idx, 'ID_Orden']}** ha pasado a **Despachado**.")
            st.rerun()
        else:
            st.info("No hay órdenes pendientes para simular el avance de estado.")
