import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
import io

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
    /* Importar fuente (opcional si ya está cargada en main) */
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
        border-left: 5px solid #00CC96; /* Verde Éxito por defecto */
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
        background: rgba(99, 110, 250, 0.1); /* Azul Plotly */
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
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- 3. MOTOR DE DATOS (SIMULACIÓN BASADA EN TU ESTRUCTURA REAL) ---
# ==============================================================================
@st.cache_data
def generar_datos_comerciales():
    """
    Genera un DataFrame que imita la estructura de tu archivo real 'ventas_detalle.csv'.
    Incluye lógica de Marcas, Vendedores (Mostradores) y Documentos (Facturas/Albaranes).
    """
    np.random.seed(42)
    
    # Configuración basada en tu código
    vendedores_mostrador = ["MOSTRADOR PEREIRA", "MOSTRADOR ARMENIA", "MOSTRADOR MANIZALES", "MOSTRADOR LAURELES"]
    vendedores_calle = ["JUAN PEREZ", "MARIA RODRIGUEZ", "CARLOS GOMEZ", "ANALISTA COMERCIAL"]
    todos_vendedores = vendedores_mostrador + vendedores_calle
    
    productos_cl4 = ['ESTUCOMAS', 'PINTULUX', 'KORAZA', 'VINILTEX', 'VINILICO']
    otras_marcas = ['ABRACOL', 'YALE', 'SAINT GOBAIN', 'GOYA', 'ALLEGION']
    
    data = []
    fecha_inicio = datetime(2024, 1, 1)
    
    # Generar 2000 transacciones simuladas
    for i in range(2000):
        fecha = fecha_inicio + timedelta(days=np.random.randint(0, 365))
        vendedor = np.random.choice(todos_vendedores)
        
        # Lógica de Documento: 85% Facturas, 10% Albaranes (Pendientes), 5% Notas Crédito
        tipo_rand = np.random.random()
        if tipo_rand < 0.85:
            tipo_doc = "FACTURA ELECTRONICA"
            factor = 1
        elif tipo_rand < 0.95:
            tipo_doc = "ALBARAN DE VENTA" # Dinero pendiente
            factor = 1
        else:
            tipo_doc = "NOTA CREDITO"
            factor = -1
            
        # Producto
        es_cl4 = np.random.random() < 0.4 # 40% son productos clave CL4
        if es_cl4:
            prod_nombre = np.random.choice(productos_cl4)
            categoria = "PINTURAS"
            marca = "PINTUCO"
        else:
            prod_nombre = f"ARTICULO {np.random.choice(otras_marcas)} {np.random.randint(100,999)}"
            categoria = "FERRETERIA"
            marca = np.random.choice(otras_marcas)
            
        cliente_id = f"C-{np.random.randint(1000, 1200)}" # 200 clientes únicos
        cliente_nombre = f"FERRETERIA {cliente_id} SAS"
        
        valor_base = np.random.exponential(500000) # Ventas variadas
        
        data.append({
            'fecha_venta': fecha,
            'anio': fecha.year,
            'mes': fecha.month,
            'Serie': f"F{fecha.strftime('%m%d')}-{i}",
            'TipoDocumento': tipo_doc,
            'nomvendedor': vendedor,
            'cliente_id': cliente_id,
            'nombre_cliente': cliente_nombre,
            'nombre_articulo': prod_nombre,
            'categoria_producto': categoria,
            'nombre_marca': marca,
            'valor_venta': valor_base * factor,
            'unidades': np.random.randint(1, 50)
        })
        
    df = pd.DataFrame(data)
    
    # Generar Presupuestos (Metas)
    df_presupuesto = pd.DataFrame({
        'nomvendedor': todos_vendedores,
        'presupuesto_mensual': [np.random.randint(80, 150)*1000000 for _ in todos_vendedores]
    })
    
    return df, df_presupuesto

# Cargar datos en sesión
if 'df_ventas' not in st.session_state:
    st.session_state.df_ventas, st.session_state.df_metas = generar_datos_comerciales()

df = st.session_state.df_ventas
df_metas = st.session_state.df_metas

# --- BARRA LATERAL DE FILTROS (Estilo Gerencial) ---
with st.sidebar:
    st.page_link("Portafolio_Servicios.py", label="Volver al Inicio", icon="🏠")
    st.divider()
    
    st.header("🎛️ Filtros de Análisis")
    
    # Filtro Mes (Asumimos año actual simulado)
    meses_disponibles = sorted(df['mes'].unique())
    mes_sel = st.selectbox("Seleccionar Mes", meses_disponibles, index=len(meses_disponibles)-1, format_func=lambda x: datetime(2024, x, 1).strftime('%B'))
    
    # Filtro Vendedor
    lista_vendedores = ["TODOS"] + sorted(df['nomvendedor'].unique().tolist())
    vendedor_sel = st.selectbox("Fuerza de Ventas", lista_vendedores)
    
    st.divider()
    st.info("🧠 **Neural Sync:**\nLas ventas registradas aquí actualizan automáticamente los puntos de reorden en el Módulo de Inventarios.")

# --- FILTRADO DE DATOS ---
df_periodo = df[df['mes'] == mes_sel].copy()

if vendedor_sel != "TODOS":
    df_periodo = df_periodo[df_periodo['nomvendedor'] == vendedor_sel]
    # Ajustar meta para mostrar solo la del vendedor
    meta_actual = df_metas[df_metas['nomvendedor'] == vendedor_sel]['presupuesto_mensual'].sum()
else:
    meta_actual = df_metas['presupuesto_mensual'].sum()

# ==============================================================================
# --- 4. CÁLCULOS DE NEGOCIO (LÓGICA DE TU CÓDIGO ORIGINAL ADAPTADA) ---
# ==============================================================================

# 1. Venta Neta (Facturas - Notas Crédito) vs Albaranes (Pendiente)
venta_neta = df_periodo[df_periodo['TipoDocumento'].isin(['FACTURA ELECTRONICA', 'NOTA CREDITO'])]['valor_venta'].sum()
albaranes_pendientes = df_periodo[df_periodo['TipoDocumento'] == 'ALBARAN DE VENTA']['valor_venta'].sum()

# 2. Lógica CL4 (Oportunidades de Venta Cruzada)
# Identificar clientes que compraron ALGO en el mes, pero NO compraron productos clave
productos_clave = ['ESTUCOMAS', 'PINTULUX', 'KORAZA', 'VINILTEX', 'VINILICO']
clientes_activos = df_periodo['cliente_id'].unique()

oportunidades = []
for cliente in clientes_activos:
    compras_cliente = df_periodo[df_periodo['cliente_id'] == cliente]
    productos_comprados = compras_cliente['nombre_articulo'].unique()
    
    # Lógica simple de tu script: verificar qué falta del mix ideal
    faltantes = [p for p in productos_clave if not any(p in prod for prod in productos_comprados)]
    
    if len(faltantes) > 0 and len(faltantes) < len(productos_clave): # Si compró al menos uno, pero faltan otros
        nombre_cliente = compras_cliente['nombre_cliente'].iloc[0]
        vendedor_asig = compras_cliente['nomvendedor'].iloc[0]
        total_compra = compras_cliente['valor_venta'].sum()
        oportunidades.append({
            'Cliente': nombre_cliente,
            'Vendedor': vendedor_asig,
            'Potencial': len(faltantes),
            'Faltantes': ", ".join(faltantes[:3]), # Mostrar primeros 3
            'Valor Compra Actual': total_compra
        })

df_oportunidades = pd.DataFrame(oportunidades)

# ==============================================================================
# --- 5. INTERFAZ DE USUARIO (DASHBOARD) ---
# ==============================================================================

# Encabezado
st.title("NEXUS COMMERCIAL | Neural Sales Engine")
st.markdown(f"**Periodo Analizado:** {datetime(2024, mes_sel, 1).strftime('%B %Y')} | **Estado:** 🟢 Sincronizado con ERP")

# --- SECCIÓN 1: KPIS GERENCIALES ---
col1, col2, col3, col4 = st.columns(4)

cumplimiento = (venta_neta / meta_actual * 100) if meta_actual > 0 else 0
delta_color = "kpi-alert" if cumplimiento < 80 else ""

with col1:
    st.markdown(f"""
    <div class="kpi-card {delta_color}">
        <div class="kpi-title">Venta Neta Facturada</div>
        <div class="kpi-value">${venta_neta/1e6:,.1f} M</div>
        <div class="kpi-sub">Meta: ${meta_actual/1e6:,.1f} M ({cumplimiento:.1f}%)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #636EFA;">
        <div class="kpi-title">Dinero Pendiente (Albaranes)</div>
        <div class="kpi-value">${albaranes_pendientes/1e6:,.1f} M</div>
        <div class="kpi-sub">⚠️ Mercancía entregada sin facturar</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    tickets = df_periodo['Serie'].nunique()
    ticket_promedio = venta_neta / tickets if tickets > 0 else 0
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #FFA15A;">
        <div class="kpi-title">Ticket Promedio</div>
        <div class="kpi-value">${ticket_promedio/1e3:,.0f} K</div>
        <div class="kpi-sub">📊 {tickets} Transacciones</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    n_oportunidades = len(df_oportunidades)
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #AB63FA;">
        <div class="kpi-title">Oportunidades (Algoritmo CL4)</div>
        <div class="kpi-value">{n_oportunidades}</div>
        <div class="kpi-sub">🚀 Clientes con potencial de Cross-Selling</div>
    </div>
    """, unsafe_allow_html=True)

# --- SECCIÓN 2: PESTAÑAS DE ANÁLISIS PROFUNDO ---
st.markdown("### 📡 Centro de Análisis Estratégico")
tab_dash, tab_opps, tab_team, tab_docs = st.tabs([
    "📊 Radar Comercial", 
    "🧬 Matriz de Oportunidades (CL4)", 
    "👥 Fuerza de Ventas",
    "📄 Auditoría de Documentos"
])

# === TAB 1: RADAR COMERCIAL (VISUALIZACIONES) ===
with tab_dash:
    c_chart1, c_chart2 = st.columns([2, 1])
    
    with c_chart1:
        st.subheader("Tendencia de Ventas vs Presupuesto")
        # Crear datos simulados diarios para el gráfico
        dias_mes = df_periodo.groupby('fecha_venta')['valor_venta'].sum().reset_index()
        dias_mes['Acumulado'] = dias_mes['valor_venta'].cumsum()
        meta_lineal = [meta_actual * (i/len(dias_mes)) for i in range(1, len(dias_mes)+1)]
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=dias_mes['fecha_venta'], y=dias_mes['Acumulado'], fill='tozeroy', name='Venta Real', line=dict(color='#00CC96')))
        fig_trend.add_trace(go.Scatter(x=dias_mes['fecha_venta'], y=meta_lineal, name='Proyección Meta', line=dict(color='#EF553B', dash='dot')))
        
        fig_trend.update_layout(
            height=350, 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=0, r=0, t=20, b=20)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with c_chart2:
        st.subheader("Mix de Categorías")
        fig_pie = px.sunburst(
            df_periodo[df_periodo['valor_venta']>0], 
            path=['categoria_producto', 'nombre_marca'], 
            values='valor_venta',
            color='valor_venta',
            color_continuous_scale='Tealgrn'
        )
        fig_pie.update_layout(height=350, margin=dict(l=0, r=0, t=20, b=20))
        st.plotly_chart(fig_pie, use_container_width=True)

# === TAB 2: OPORTUNIDADES (La lógica CL4 de tu script) ===
with tab_opps:
    st.markdown("""
    <div class="ai-insight-box">
        <div class="ai-icon">🧠</div>
        <div>
            <h4 style="margin:0; color:#636EFA">Algoritmo de Detección de Patrones (CL4)</h4>
            <p style="margin:5px 0 0 0; font-size:0.9rem;">
                El sistema ha analizado el comportamiento de compra de <b>{len(clientes_activos)} clientes</b>.
                Se han detectado <b>{n_oportunidades} clientes</b> que compraron productos base (ej. Koraza) pero olvidaron complementarios (ej. Estucomas/Viniltex).
                <br>👉 <i>Acción sugerida: Exportar lista y enviar a fuerza de ventas para gestión telefónica inmediata.</i>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not df_oportunidades.empty:
        # Ordenar por potencial de venta (Valor de compra actual indica tamaño de cliente)
        df_show_opps = df_oportunidades.sort_values('Valor Compra Actual', ascending=False).head(15)
        
        st.dataframe(
            df_show_opps,
            column_config={
                "Valor Compra Actual": st.column_config.ProgressColumn("Tamaño Cliente", format="$%d", min_value=0, max_value=int(df_show_opps['Valor Compra Actual'].max())),
                "Faltantes": st.column_config.TextColumn("Productos a Ofrecer (Cross-Sell)"),
                "Potencial": st.column_config.NumberColumn("Gap Score")
            },
            use_container_width=True,
            hide_index=True
        )
        
        col_dl_1, col_dl_2 = st.columns([1, 4])
        with col_dl_1:
            # Simulación de exportación
            st.download_button(
                label="📥 Descargar Reporte CL4 (Excel)",
                data="Simulacion Excel",
                file_name="Oportunidades_CL4.xlsx",
                mime="text/csv"
            )
    else:
        st.success("¡Increíble! Todos los clientes activos tienen el mix de productos completo.")

# === TAB 3: RANKING VENDEDORES ===
with tab_team:
    st.subheader("🏆 Rendimiento Fuerza de Ventas")
    
    # Agrupar por vendedor
    ranking = df_periodo.groupby('nomvendedor').agg(
        Venta=('valor_venta', 'sum'),
        Transacciones=('Serie', 'nunique')
    ).reset_index()
    
    # Unir con metas
    ranking = ranking.merge(df_metas, on='nomvendedor', how='left')
    ranking['Cumplimiento'] = (ranking['Venta'] / ranking['presupuesto_mensual']) * 100
    ranking = ranking.sort_values('Cumplimiento', ascending=False)
    
    # Gráfico de Barras
    fig_bar = px.bar(
        ranking, 
        x='Cumplimiento', 
        y='nomvendedor', 
        orientation='h',
        text_auto='.1f',
        color='Cumplimiento',
        color_continuous_scale=['#EF553B', '#FFA15A', '#00CC96'],
        title="Ranking de Cumplimiento (%)"
    )
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, font=dict(color='white'), plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True)

# === TAB 4: AUDITORÍA ALBARANES (Tu código de control) ===
with tab_docs:
    st.subheader("📄 Auditoría de Ingresos Pendientes (Albaranes)")
    st.warning("Estas transacciones han movido inventario pero NO han generado factura electrónica (Cartera). Requieren atención inmediata.")
    
    df_albaranes = df_periodo[df_periodo['TipoDocumento'] == 'ALBARAN DE VENTA'][['fecha_venta', 'Serie', 'nombre_cliente', 'nomvendedor', 'valor_venta']].copy()
    
    if not df_albaranes.empty:
        st.dataframe(
            df_albaranes,
            column_config={
                "fecha_venta": st.column_config.DateColumn("Fecha"),
                "valor_venta": st.column_config.NumberColumn("Valor Pendiente", format="$%d")
            },
            use_container_width=True
        )
        
        if st.button("⚡ Convertir Albaranes a Facturas (Simulación ERP)"):
            with st.spinner("Conectando con DIAN y ERP... Generando Facturas Electrónicas..."):
                time.sleep(2)
            st.balloons()
            st.success(f"Se han procesado {len(df_albaranes)} documentos correctamente. El inventario y cartera están sincronizados.")
    else:
        st.success("✅ No hay albaranes pendientes. Todo está facturado.")

# ==============================================================================
# --- 6. CIERRE Y CONEXIÓN CON EL ECOSISTEMA ---
# ==============================================================================
st.divider()
col_footer_l, col_footer_r = st.columns([3, 1])

with col_footer_l:
    st.markdown("""
    #### 🔗 Integración de Ecosistema
    Este módulo comercial no trabaja aislado. 
    * Las ventas aquí registradas se descuentan en tiempo real del **Módulo de Inventarios**.
    * El algoritmo CL4 alimenta las sugerencias de compra en el **Módulo Logístico**.
    """)

with col_footer_r:
    if st.button("📡 Sincronizar Todo"):
        st.toast("Sincronizando Ventas...", icon="💰")
        time.sleep(1)
        st.toast("Actualizando Stocks...", icon="📦")
        time.sleep(1)
        st.toast("Recalculando KPIs...", icon="📊")
        st.success("Ecosistema NEXUS actualizado.")
