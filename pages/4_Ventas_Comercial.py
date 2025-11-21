import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import io # Necesario para generar el Excel en memoria

# ==============================================================================
# --- 1. CONFIGURACIÓN DE PÁGINA ---
# ==============================================================================
st.set_page_config(
    page_title="NEXUS SALES | Inteligencia Comercial",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# --- 2. ESTILOS CSS PREMIUM (IDENTIDAD VISUAL GM-DATOVATE) ---
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }

    /* KPI CARDS */
    .kpi-card {
        background: linear-gradient(145deg, #1e232a, #161b22);
        border-radius: 15px;
        padding: 20px;
        border-left: 5px solid #00CC96;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    .kpi-card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,204,150,0.2); }
    
    .kpi-title { font-size: 14px; color: #a0a0a0; text-transform: uppercase; letter-spacing: 1.2px; font-weight: 600; }
    .kpi-value { font-size: 32px; font-weight: 800; color: #ffffff; margin: 10px 0; }
    .kpi-sub { font-size: 12px; color: #00CC96; font-weight: bold; display: flex; align-items: center; gap: 5px; }
    .kpi-alert { border-left-color: #EF553B !important; }
    .kpi-alert .kpi-sub { color: #EF553B !important; }

    /* AI INSIGHT BOX */
    .ai-insight-box {
        background: rgba(99, 110, 250, 0.1);
        border: 1px solid #636EFA;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 30px;
        display: flex;
        align-items: flex-start;
        gap: 15px;
    }
    .ai-icon { font-size: 2rem; animation: pulse 2s infinite; }
    
    @keyframes pulse {
        0% { text-shadow: 0 0 0 rgba(99, 110, 250, 0.4); }
        70% { text-shadow: 0 0 20px rgba(99, 110, 250, 0); }
        100% { text-shadow: 0 0 0 rgba(99, 110, 250, 0); }
    }

    /* TABLAS */
    div[data-testid="stDataFrame"] {
        background-color: #161b22;
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #30363d;
    }

    /* BOTONES */
    div.stButton > button {
        background: linear-gradient(90deg, #00CC96 0%, #00A878 100%);
        color: white;
        border: none;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- 3. MOTOR DE DATOS (SIMULACIÓN MEJORADA CON RENTABILIDAD) ---
# ==============================================================================
@st.cache_data
def generar_datos_comerciales():
    """
    Genera datos simulados incluyendo Costos para análisis de Margen.
    """
    np.random.seed(42)
    
    vendedores_mostrador = ["MOSTRADOR PEREIRA", "MOSTRADOR ARMENIA", "MOSTRADOR MANIZALES", "MOSTRADOR LAURELES"]
    vendedores_calle = ["JUAN PEREZ", "MARIA RODRIGUEZ", "CARLOS GOMEZ", "ANALISTA COMERCIAL"]
    todos_vendedores = vendedores_mostrador + vendedores_calle
    
    productos_cl4 = ['ESTUCOMAS', 'PINTULUX', 'KORAZA', 'VINILTEX', 'VINILICO']
    otras_marcas = ['ABRACOL', 'YALE', 'SAINT GOBAIN', 'GOYA', 'ALLEGION', 'SEGUREX', '3M']
    categorias_base = ["PINTURAS", "CERRAJERIA", "HERRAMIENTAS", "ABRASIVOS", "SEGURIDAD"]

    data = []
    fecha_inicio = datetime(2024, 1, 1)
    
    # Simulamos "Personalidad" de vendedores (Algunos venden más volumen, otros más margen)
    perfiles_vendedores = {}
    for v in todos_vendedores:
        perfiles_vendedores[v] = {
            'factor_desc': np.random.uniform(0.05, 0.25), # Descuento promedio que dan
            'cat_fuerte': np.random.choice(categorias_base) # Categoría donde son fuertes
        }

    for i in range(2500):
        fecha = fecha_inicio + timedelta(days=np.random.randint(0, 365))
        vendedor = np.random.choice(todos_vendedores)
        perfil = perfiles_vendedores[vendedor]
        
        # Tipo Documento
        tipo_rand = np.random.random()
        if tipo_rand < 0.88: tipo_doc, factor = "FACTURA ELECTRONICA", 1
        elif tipo_rand < 0.96: tipo_doc, factor = "ALBARAN DE VENTA", 1
        else: tipo_doc, factor = "NOTA CREDITO", -1
            
        # Producto y Categoría
        if np.random.random() < 0.6: # 60% probabilidad de vender su categoría fuerte
            categoria = perfil['cat_fuerte']
            prod_nombre = f"{categoria} PREMIUM {np.random.randint(100,999)}"
        else:
            categoria = np.random.choice([c for c in categorias_base if c != perfil['cat_fuerte']])
            prod_nombre = f"ARTICULO {categoria} {np.random.randint(100,999)}"

        # CL4 Logica
        if categoria == "PINTURAS":
            marca = "PINTUCO"
            if np.random.random() < 0.5: prod_nombre = np.random.choice(productos_cl4)
        else:
            marca = np.random.choice(otras_marcas)

        # Valores Financieros
        costo_base = np.random.randint(10000, 500000)
        margen_teorico = 0.35 # 35% margen base
        precio_lista = costo_base / (1 - margen_teorico)
        
        # Aplicar descuento según vendedor
        descuento_real = np.random.normal(perfil['factor_desc'], 0.02)
        precio_venta = precio_lista * (1 - descuento_real)
        
        valor_venta_total = precio_venta * factor
        costo_total = costo_base * factor
        utilidad = valor_venta_total - costo_total
        
        cliente_id = f"C-{np.random.randint(1000, 1150)}"
        
        data.append({
            'fecha_venta': fecha,
            'mes': fecha.month,
            'Serie': f"F{fecha.strftime('%m%d')}-{i}",
            'TipoDocumento': tipo_doc,
            'nomvendedor': vendedor,
            'cliente_id': cliente_id,
            'nombre_cliente': f"CLIENTE {cliente_id}",
            'nombre_articulo': prod_nombre,
            'categoria_producto': categoria,
            'nombre_marca': marca,
            'valor_venta': valor_venta_total,
            'costo_venta': costo_total,
            'utilidad': utilidad,
            'unidades': np.random.randint(1, 20)
        })
        
    df = pd.DataFrame(data)
    # Calcular margen %
    df['margen_pct'] = (df['utilidad'] / df['valor_venta']).fillna(0) * 100
    
    # Generar Metas
    df_metas = pd.DataFrame({
        'nomvendedor': todos_vendedores,
        'presupuesto_mensual': [np.random.randint(90, 180)*1000000 for _ in todos_vendedores]
    })
    
    return df, df_metas

# --- CARGA DE DATOS ---
if 'df_ventas' not in st.session_state:
    st.session_state.df_ventas, st.session_state.df_metas = generar_datos_comerciales()

df = st.session_state.df_ventas
df_metas = st.session_state.df_metas

# ==============================================================================
# --- 4. FUNCIÓN GENERADORA DE EXCEL PROFESIONAL (CORRECCIÓN DEL ERROR) ---
# ==============================================================================
def generar_excel_gerencial(df_periodo, df_kpi_vendedores, df_oportunidades, mes_nombre):
    """
    Crea un archivo Excel Binario real (bytes) con múltiples hojas y formato.
    """
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    
    # Estilos
    fmt_header = workbook.add_format({'bold': True, 'bg_color': '#1F4E78', 'font_color': 'white', 'border': 1, 'align': 'center'})
    fmt_currency = workbook.add_format({'num_format': '$ #,##0', 'border': 1})
    fmt_pct = workbook.add_format({'num_format': '0.0%', 'border': 1})
    fmt_text = workbook.add_format({'border': 1})
    
    # --- HOJA 1: RESUMEN EJECUTIVO ---
    df_kpi_vendedores.to_excel(writer, sheet_name='Desempeño Vendedores', startrow=1, index=False)
    ws1 = writer.sheets['Desempeño Vendedores']
    
    # Encabezados Hoja 1
    for col_num, value in enumerate(df_kpi_vendedores.columns.values):
        ws1.write(0, col_num, value, fmt_header)
    ws1.set_column('A:A', 25) # Vendedor
    ws1.set_column('B:C', 18, fmt_currency) # Ventas
    ws1.set_column('D:E', 12, fmt_pct) # Cumplimiento/Margen
    ws1.set_column('F:F', 15, fmt_currency) # Ticket
    ws1.set_column('G:G', 40) # Recomendación
    
    # --- HOJA 2: OPORTUNIDADES CL4 ---
    if not df_oportunidades.empty:
        df_oportunidades.to_excel(writer, sheet_name='Oportunidades Cross-Sell', startrow=1, index=False)
        ws2 = writer.sheets['Oportunidades Cross-Sell']
        for col_num, value in enumerate(df_oportunidades.columns.values):
            ws2.write(0, col_num, value, fmt_header)
        ws2.set_column('A:B', 20)
        ws2.set_column('C:C', 12) # Potencial
        ws2.set_column('D:D', 35) # Faltantes
        ws2.set_column('E:E', 18, fmt_currency)

    # --- HOJA 3: DATA CRUDA (VENTAS) ---
    # Exportamos una muestra o todo el mes
    df_export = df_periodo[['fecha_venta', 'Serie', 'nombre_cliente', 'nomvendedor', 'nombre_articulo', 'categoria_producto', 'valor_venta', 'utilidad']].copy()
    df_export.to_excel(writer, sheet_name='Detalle Transacciones', startrow=1, index=False)
    ws3 = writer.sheets['Detalle Transacciones']
    for col_num, value in enumerate(df_export.columns.values):
        ws3.write(0, col_num, value, fmt_header)
    ws3.set_column('A:A', 15)
    ws3.set_column('B:F', 20)
    ws3.set_column('G:H', 15, fmt_currency)

    writer.close()
    return output.getvalue()

# ==============================================================================
# --- 5. LÓGICA DEL DASHBOARD ---
# ==============================================================================

# Sidebar
with st.sidebar:
    st.page_link("Portafolio_Servicios.py", label="Volver al Inicio", icon="🏠")
    st.divider()
    st.header("🎛️ Filtros de Mando")
    meses_disponibles = sorted(df['mes'].unique())
    mes_sel = st.selectbox("Periodo Contable", meses_disponibles, index=len(meses_disponibles)-1, format_func=lambda x: datetime(2024, x, 1).strftime('%B %Y').upper())
    
    st.info("💡 **Tip Gerencial:**\nUtiliza la pestaña 'Análisis de Equipo' para ver la matriz de rentabilidad vs volumen.")

# Filtrar Data Global
df_periodo = df[df['mes'] == mes_sel].copy()
df_periodo_facturado = df_periodo[df_periodo['TipoDocumento'].isin(['FACTURA ELECTRONICA', 'NOTA CREDITO'])]

# Cálculos Globales
venta_total = df_periodo_facturado['valor_venta'].sum()
utilidad_total = df_periodo_facturado['utilidad'].sum()
margen_global_pct = (utilidad_total / venta_total * 100) if venta_total > 0 else 0
meta_mes = df_metas['presupuesto_mensual'].sum()
cumplimiento_global = (venta_total / meta_mes * 100) if meta_mes > 0 else 0

# --- HEADER ---
st.title("NEXUS COMMERCIAL | Centro de Comando")
st.markdown(f"**Periodo:** {datetime(2024, mes_sel, 1).strftime('%B %Y')} | **Estado:** 🟢 Datos Auditados")

# --- KPIS SUPERIORES ---
k1, k2, k3, k4 = st.columns(4)
k1.markdown(f"""<div class="kpi-card"><div class="kpi-title">Venta Neta</div><div class="kpi-value">${venta_total/1e6:,.1f} M</div><div class="kpi-sub">Meta: ${meta_mes/1e6:,.1f} M ({cumplimiento_global:.1f}%)</div></div>""", unsafe_allow_html=True)
k2.markdown(f"""<div class="kpi-card"><div class="kpi-title">Utilidad Bruta</div><div class="kpi-value">${utilidad_total/1e6:,.1f} M</div><div class="kpi-sub">Margen Global: {margen_global_pct:.1f}%</div></div>""", unsafe_allow_html=True)
k3.markdown(f"""<div class="kpi-card" style="border-left-color:#636EFA"><div class="kpi-title">Transacciones</div><div class="kpi-value">{df_periodo_facturado['Serie'].nunique()}</div><div class="kpi-sub">Ticket Promedio: ${venta_total/df_periodo_facturado['Serie'].nunique():,.0f}</div></div>""", unsafe_allow_html=True)
k4.markdown(f"""<div class="kpi-card" style="border-left-color:#AB63FA"><div class="kpi-title">Cartera Vencida (Sim)</div><div class="kpi-value">4.2%</div><div class="kpi-sub">Sana (< 5%)</div></div>""", unsafe_allow_html=True)

# --- PESTAÑAS PRINCIPALES ---
tab_analisis, tab_equipo, tab_cl4, tab_export = st.tabs([
    "📊 Análisis 360°", 
    "🧠 Inteligencia de Equipo", 
    "🧬 Oportunidades (CL4)",
    "📥 Exportación Gerencial"
])

# === TAB 1: ANÁLISIS 360 ===
with tab_analisis:
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Tendencia Diaria vs Meta")
        diario = df_periodo_facturado.groupby('fecha_venta')['valor_venta'].sum().reset_index()
        diario['acum'] = diario['valor_venta'].cumsum()
        # Linea de meta lineal
        meta_lineal = [meta_mes * (i/30) for i in range(1, len(diario)+1)] # Aprox
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=diario['fecha_venta'], y=diario['acum'], fill='tozeroy', name='Real', line=dict(color='#00CC96')))
        fig.add_trace(go.Scatter(x=diario['fecha_venta'], y=meta_lineal, name='Proyección Ideal', line=dict(color='white', dash='dot')))
        fig.update_layout(height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.subheader("Rentabilidad por Categoría")
        cat_rent = df_periodo_facturado.groupby('categoria_producto')[['valor_venta', 'utilidad']].sum().reset_index()
        cat_rent['margen'] = (cat_rent['utilidad'] / cat_rent['valor_venta'] * 100)
        
        fig_bar = px.bar(cat_rent, x='margen', y='categoria_producto', orientation='h', color='margen', title="Margen %", color_continuous_scale='RdYlGn')
        fig_bar.update_layout(height=350, font=dict(color='white'))
        st.plotly_chart(fig_bar, use_container_width=True)

# === TAB 2: INTELIGENCIA DE EQUIPO (SUPER ANÁLISIS) ===
with tab_equipo:
    st.markdown("### 🕵️ Evaluación de Desempeño de Vendedores")
    
    # Preparar Datos Agrupados
    df_vendedores = df_periodo_facturado.groupby('nomvendedor').agg(
        Ventas_Totales=('valor_venta', 'sum'),
        Utilidad_Total=('utilidad', 'sum'),
        Transacciones=('Serie', 'nunique'),
        Ticket_Prom=('valor_venta', 'mean')
    ).reset_index()
    
    df_vendedores['Margen_Pct'] = (df_vendedores['Utilidad_Total'] / df_vendedores['Ventas_Totales'] * 100)
    df_vendedores = df_vendedores.merge(df_metas, on='nomvendedor', how='left')
    df_vendedores['Cumplimiento'] = (df_vendedores['Ventas_Totales'] / df_vendedores['presupuesto_mensual'] * 100)
    
    # GENERADOR DE RECOMENDACIONES IA
    def generar_insight(row):
        if row['Cumplimiento'] > 100 and row['Margen_Pct'] > 30:
            return "🌟 ESTRELLA: Mantener incentivos. Potenciar como mentor."
        elif row['Cumplimiento'] > 100 and row['Margen_Pct'] < 25:
            return "⚠️ VOLUMEN RIESGOSO: Vende mucho pero con mucho descuento. Revisar política de precios."
        elif row['Cumplimiento'] < 80 and row['Margen_Pct'] > 35:
            return "💎 NICHO: Excelente margen, pero bajo volumen. Asignar clientes más grandes."
        else:
            return "🚨 ALERTA: Bajo rendimiento integral. Requiere plan de choque o capacitación."

    df_vendedores['Recomendacion_IA'] = df_vendedores.apply(generar_insight, axis=1)

    # 1. MATRIZ DE RENDIMIENTO (SCATTER PLOT)
    col_matrix, col_heatmap = st.columns([3, 2])
    
    with col_matrix:
        st.subheader("Matriz de Posicionamiento: Volumen vs Rentabilidad")
        fig_matrix = px.scatter(
            df_vendedores, 
            x='Cumplimiento', 
            y='Margen_Pct', 
            size='Ventas_Totales', 
            color='Recomendacion_IA',
            hover_name='nomvendedor',
            text='nomvendedor',
            color_discrete_map={
                "🌟 ESTRELLA: Mantener incentivos. Potenciar como mentor.": "#00CC96",
                "⚠️ VOLUMEN RIESGOSO: Vende mucho pero con mucho descuento. Revisar política de precios.": "#FFA15A",
                "💎 NICHO: Excelente margen, pero bajo volumen. Asignar clientes más grandes.": "#636EFA",
                "🚨 ALERTA: Bajo rendimiento integral. Requiere plan de choque o capacitación.": "#EF553B"
            }
        )
        # Líneas promedio
        avg_cump = df_vendedores['Cumplimiento'].mean()
        avg_marg = df_vendedores['Margen_Pct'].mean()
        
        fig_matrix.add_hline(y=avg_marg, line_dash="dot", annotation_text="Margen Promedio", annotation_position="bottom right")
        fig_matrix.add_vline(x=avg_cump, line_dash="dot", annotation_text="Cumplimiento Promedio", annotation_position="top right")
        
        fig_matrix.update_traces(textposition='top center')
        fig_matrix.update_layout(height=500, plot_bgcolor='rgba(255,255,255,0.05)', xaxis_title="Cumplimiento de Meta (%)", yaxis_title="Margen de Rentabilidad (%)")
        st.plotly_chart(fig_matrix, use_container_width=True)
        
    with col_heatmap:
        st.subheader("ADN del Vendedor (Heatmap)")
        st.info("Intensidad de ventas por Categoría")
        
        # Pivot para Heatmap
        heatmap_data = df_periodo_facturado.groupby(['nomvendedor', 'categoria_producto'])['valor_venta'].sum().reset_index()
        fig_heat = px.density_heatmap(
            heatmap_data, 
            x='categoria_producto', 
            y='nomvendedor', 
            z='valor_venta', 
            color_continuous_scale='Viridis'
        )
        fig_heat.update_layout(height=500)
        st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Detalle Táctico de Vendedores")
    # Tabla Estilizada
    st.dataframe(
        df_vendedores[['nomvendedor', 'Ventas_Totales', 'Cumplimiento', 'Margen_Pct', 'Ticket_Prom', 'Recomendacion_IA']],
        column_config={
            "nomvendedor": "Vendedor",
            "Ventas_Totales": st.column_config.NumberColumn("Venta Total", format="$%d"),
            "Cumplimiento": st.column_config.ProgressColumn("Meta %", format="%.1f%%", min_value=0, max_value=120),
            "Margen_Pct": st.column_config.NumberColumn("Margen %", format="%.1f%%"),
            "Ticket_Prom": st.column_config.NumberColumn("Ticket Promedio", format="$%d"),
            "Recomendacion_IA": "Diagnóstico Algorítmico"
        },
        use_container_width=True,
        hide_index=True
    )

# === TAB 3: OPORTUNIDADES CL4 ===
with tab_cl4:
    st.markdown("""
    <div class="ai-insight-box">
        <div class="ai-icon">🧬</div>
        <div>
            <h4>Algoritmo CL4: Detección de Venta Cruzada</h4>
            <p>Analiza patrones de compra incompletos. Ejemplo: Cliente compra Pintura pero no compra Estuco ni Brochas.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Logica CL4 (Recalculada para asegurar datos)
    productos_clave = ['ESTUCOMAS', 'PINTULUX', 'KORAZA', 'VINILTEX', 'VINILICO']
    clientes_activos = df_periodo['cliente_id'].unique()
    oportunidades = []
    
    for cliente in clientes_activos:
        compras = df_periodo[df_periodo['cliente_id'] == cliente]
        prods = compras['nombre_articulo'].unique()
        faltantes = [p for p in productos_clave if not any(p in x for x in prods)]
        
        # Si compró productos de pintura (PINTUCO) pero le faltan claves
        if any("PINTUCO" in x for x in compras['nombre_marca'].unique()) and len(faltantes) > 0:
            oportunidades.append({
                'Cliente': compras['nombre_cliente'].iloc[0],
                'Vendedor': compras['nomvendedor'].iloc[0],
                'Potencial': len(faltantes),
                'Faltantes': ", ".join(faltantes[:3]),
                'Valor Compra Actual': compras['valor_venta'].sum()
            })
            
    df_opps = pd.DataFrame(oportunidades)
    
    if not df_opps.empty:
        df_opps = df_opps.sort_values('Valor Compra Actual', ascending=False)
        st.dataframe(
            df_opps.head(20),
            column_config={
                "Valor Compra Actual": st.column_config.NumberColumn("Valor Cliente", format="$%d"),
                "Potencial": st.column_config.NumberColumn("Score Oportunidad", help="Más alto = Más productos faltan")
            },
            use_container_width=True, hide_index=True
        )
    else:
        st.success("No se detectaron brechas de portafolio críticas en este periodo.")

# === TAB 4: EXPORTACIÓN (LA SOLUCIÓN AL PROBLEMA) ===
with tab_export:
    st.markdown("### 📥 Centro de Descargas Gerenciales")
    st.info("Genera un archivo Excel consolidado con todas las métricas, análisis de IA y detalles operativos para la junta directiva.")
    
    c_down1, c_down2 = st.columns([2, 1])
    
    with c_down1:
        # PREPARACIÓN DEL ARCHIVO
        fecha_reporte = datetime(2024, mes_sel, 1).strftime('%Y_%m')
        nombre_archivo = f"Reporte_Gerencial_NEXUS_{fecha_reporte}.xlsx"
        
        # Usamos la función corregida
        excel_data = generar_excel_gerencial(df_periodo, df_vendedores, df_opps, datetime(2024, mes_sel, 1).strftime('%B'))
        
        st.download_button(
            label=f"📊 DESCARGAR REPORTE EJECUTIVO ({datetime(2024, mes_sel, 1).strftime('%B')})",
            data=excel_data,
            file_name=nombre_archivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Click para descargar el análisis completo en formato .xlsx compatible con Excel 2013+"
        )
        
    with c_down2:
        st.markdown("**Contenido del Reporte:**")
        st.markdown("""
        * ✅ **Sheet 1:** KPIs y Matriz de Vendedores
        * ✅ **Sheet 2:** Oportunidades CL4 (Leads)
        * ✅ **Sheet 3:** Data Transaccional (Auditoría)
        """)

# ==============================================================================
# --- 6. FOOTER ---
# ==============================================================================
st.divider()
st.markdown(f"<div style='text-align:center; color:#666;'>NEXUS OS v2.5 | Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>", unsafe_allow_html=True)
