import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE PÁGINA (Debe ser lo primero) ---
st.set_page_config(
    page_title="Nexus AI | Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS PREMIUM (MODO DARK/NEON) ---
st.markdown("""
<style>
    /* Fondo y tipografía base */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Tarjetas KPI */
    .metric-card {
        background: linear-gradient(145deg, #1e232a, #161b22);
        border-radius: 15px;
        padding: 20px;
        border-left: 5px solid #2E86C1;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 15px;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.5);
    }
    .metric-value { font-size: 28px; font-weight: bold; color: white; }
    .metric-label { font-size: 14px; color: #a0a0a0; text-transform: uppercase; letter-spacing: 1px; }
    .metric-delta { font-size: 12px; font-weight: bold; }
    .delta-pos { color: #00CC96; }
    .delta-neg { color: #EF553B; }
    
    /* Caja de Insights IA */
    .ai-box {
        background: rgba(46, 134, 193, 0.1);
        border: 1px solid #2E86C1;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 25px;
    }
    .ai-title { color: #2E86C1; font-weight: bold; font-size: 1.1rem; display: flex; align-items: center; gap: 10px; }
    
    /* Tablas personalizadas */
    div[data-testid="stDataFrame"] {
        background-color: #161b22;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- GENERADOR DE DATOS AVANZADO (SIMULACIÓN) ---
@st.cache_data
def generar_data_avanzada():
    np.random.seed(42) # Para consistencia
    categorias = {
        'Herramientas': ['Taladros', 'Pulidoras', 'Sierras', 'Kits Manuales'],
        'Construcción': ['Cementos', 'Aditivos', 'Impermeabilizantes', 'Estucos'],
        'Acabados': ['Pintura Tipo 1', 'Esmaltes', 'Brochas', 'Rodillos'],
        'Eléctricos': ['Cableado', 'Tomas', 'Iluminación LED', 'Tableros'],
        'Plomería': ['Tubos PVC', 'Grifería', 'Accesorios', 'Pegamentos']
    }
    
    data = []
    for cat, subcats in categorias.items():
        for _ in range(25): # 25 productos por categoría
            subcat = np.random.choice(subcats)
            sku = f"{cat[:3].upper()}-{np.random.randint(1000,9999)}"
            costo = np.random.uniform(5000, 250000)
            margen = np.random.uniform(0.25, 0.60)
            precio = costo * (1 + margen)
            
            demanda_mensual = np.random.poisson(20)
            stock = int(demanda_mensual * np.random.uniform(0, 4)) # Entre 0 y 4 meses de stock
            lead_time = np.random.choice([2, 5, 15, 45, 60]) # Días proveedor
            
            # Lógica de Estado
            meses_cobertura = stock / demanda_mensual if demanda_mensual > 0 else 99
            if stock == 0: estado = "🔴 Quiebre (Crítico)"
            elif meses_cobertura < 0.5: estado = "🟠 Riesgo Quiebre"
            elif meses_cobertura > 4: estado = "🔵 Excedente (Inmovilizado)"
            else: estado = "🟢 Saludable"
            
            data.append({
                'SKU': sku,
                'Producto': f"{subcat} Premium {np.random.randint(1,100)}",
                'Categoria': cat,
                'Subcategoria': subcat,
                'Costo': costo,
                'Precio': precio,
                'Stock': stock,
                'Demanda_Mes': demanda_mensual,
                'Lead_Time': lead_time,
                'Proveedor': np.random.choice(['DistriGlobal', 'FerreAbastos', 'MegaTools', 'Importados SA']),
                'Estado': estado,
                'Valor_Inventario': stock * costo,
                'Rotacion_Dias': lead_time + np.random.randint(-5, 10)
            })
            
    return pd.DataFrame(data)

df = generar_data_avanzada()

# --- SIDEBAR DE NAVEGACIÓN Y FILTROS ---
with st.sidebar:
    # --- CORRECCIÓN CRÍTICA DE NAVEGACIÓN ---
    # Asegúrate de que "Portafolio_Servicios.py" es el nombre REAL de tu archivo principal
    st.page_link("Portafolio_Servicios.py", label="Volver al Inicio", icon="🏠")
    
    st.divider()
    st.header("🎛️ Panel de Control")
    filtro_cat = st.multiselect("Filtrar Categoría", df['Categoria'].unique(), default=df['Categoria'].unique())
    filtro_prov = st.multiselect("Filtrar Proveedor", df['Proveedor'].unique())
    
    if filtro_cat:
        df = df[df['Categoria'].isin(filtro_cat)]
    if filtro_prov:
        df = df[df['Proveedor'].isin(filtro_prov)]
        
    st.info("📅 Datos actualizados: Tiempo Real")

# --- CABECERA ESTRATÉGICA ---
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.markdown("# ⚡") # Aquí iría tu logo
with col_title:
    st.title("NEXUS PRO | Inteligencia de Inventarios")
    st.markdown("**Vista Ejecutiva:** Análisis de capital, rotación y predicción de demanda.")

# --- 1. DIAGNÓSTICO IA (El Gancho de Venta) ---
total_inv = df['Valor_Inventario'].sum()
quiebres = df[df['Estado'].str.contains("Quiebre")]
excedentes = df[df['Estado'].str.contains("Excedente")]
costo_oportunidad = quiebres['Demanda_Mes'].sum() * quiebres['Precio'].mean() # Venta perdida estimada
capital_congelado = excedentes['Valor_Inventario'].sum()

st.markdown(f"""
<div class="ai-box">
    <div class="ai-title">🤖 Nexus AI Insights</div>
    <p style="margin-top: 10px; margin-bottom: 0;">
        He analizado <strong>{len(df)} referencias</strong>. Tu salud de inventario es del <strong>78%</strong>.
        <br>⚠️ <strong>Alerta Crítica:</strong> Detecté <strong>{len(quiebres)} productos en quiebre</strong> que están generando una pérdida de oportunidad de <strong>${costo_oportunidad/1e6:,.1f}M</strong> mensuales.
        <br>💰 <strong>Oportunidad de Flujo de Caja:</strong> Tienes <strong>${capital_congelado/1e6:,.1f}M</strong> en stock inmovilizado (Excedentes) que podrías liquidar para liberar capital.
    </p>
</div>
""", unsafe_allow_html=True)

# --- 2. KPIs DE ALTO IMPACTO (Formato Tarjeta) ---
c1, c2, c3, c4 = st.columns(4)

def card(col, title, value, delta, is_good=True):
    color = "delta-pos" if is_good else "delta-neg"
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-delta {color}">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

card(c1, "Valor Total Inventario", f"${total_inv/1e6:,.1f} M", "▲ 2.4% vs Mes Anterior", True)
card(c2, "Capital Congelado", f"${capital_congelado/1e6:,.1f} M", "▼ Se requiere acción", False)
card(c3, "Ventas Perdidas (Est)", f"${costo_oportunidad/1e6:,.1f} M", "▼ Por Quiebres de Stock", False)
card(c4, "Días de Inventario (DSI)", f"{df['Stock'].mean()/df['Demanda_Mes'].mean()*30:.0f} Días", "▲ Dentro del objetivo", True)

# --- 3. VISUALIZACIÓN AVANZADA (Layout Asimétrico) ---
st.markdown("### 📊 Análisis Visual Profundo")

tab_vis1, tab_vis2, tab_vis3 = st.tabs(["Mapa de Calor Financiero", "Rendimiento de Proveedores", "Distribución de Salud"])

with tab_vis1:
    # TREEMAP: El mejor gráfico para ver dónde está el dinero
    st.markdown("##### ¿Dónde está invertido mi dinero? (Tamaño = Valor Inventario, Color = Estado)")
    fig_tree = px.treemap(
        df, 
        path=[px.Constant("Inventario Total"), 'Categoria', 'Subcategoria', 'Producto'], 
        values='Valor_Inventario',
        color='Estado',
        color_discrete_map={
            '🟢 Saludable': '#00CC96', 
            '🔴 Quiebre (Crítico)': '#EF553B', 
            '🟠 Riesgo Quiebre': '#FFA15A', 
            '🔵 Excedente (Inmovilizado)': '#636EFA'
        },
        hover_data=['Stock', 'Costo']
    )
    fig_tree.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=450)
    st.plotly_chart(fig_tree, use_container_width=True)

with tab_vis2:
    # SCATTER: Lead Time vs Valor (Riesgo Proveedor)
    col_prov1, col_prov2 = st.columns([3, 1])
    with col_prov1:
        fig_scatter = px.scatter(
            df, 
            x="Lead_Time", 
            y="Valor_Inventario", 
            size="Demanda_Mes", 
            color="Proveedor",
            hover_name="Producto",
            title="Análisis de Riesgo: Tiempos de Entrega vs. Capital Expuesto",
            labels={"Lead_Time": "Tiempo de Entrega (Días)", "Valor_Inventario": "Dinero Invertido ($)"}
        )
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)
    with col_prov2:
        st.info("""
        **Interpretación:**
        Los puntos más a la derecha son proveedores lentos.
        Si las burbujas son grandes y altas, tienes **mucho dinero atrapado con proveedores lentos**.
        ¡Negocia mejores tiempos o cambia de proveedor!
        """)

with tab_vis3:
    # SUNBURST: Distribución
    c_pie1, c_pie2 = st.columns(2)
    with c_pie1:
        fig_sun = px.sunburst(df, path=['Categoria', 'Estado'], values='Valor_Inventario')
        st.plotly_chart(fig_sun, use_container_width=True)
    with c_pie2:
        # Gauge Chart para nivel de servicio
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = (1 - (len(quiebres)/len(df))) * 100,
            title = {'text': "Nivel de Servicio Actual"},
            gauge = {'axis': {'range': [None, 100]},
                     'bar': {'color': "#00CC96"},
                     'steps': [
                         {'range': [0, 80], 'color': "#EF553B"},
                         {'range': [80, 95], 'color': "#FFA15A"}],
                     'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 95}}))
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)

# --- 4. CENTRO DE COMANDOS (Tablas Accionables) ---
st.markdown("---")
st.markdown("### 🚀 Centro de Comandos: Acciones Recomendadas")

col_action_left, col_action_right = st.columns(2)

with col_action_left:
    st.error(f"🚨 URGENTE: Reabastecer ({len(quiebres)} SKUs)")
    st.markdown("Estos productos tienen venta activa pero Stock 0. **Estás perdiendo dinero cada hora.**")
    
    df_buy = quiebres[['SKU', 'Producto', 'Proveedor', 'Demanda_Mes', 'Costo']].copy()
    df_buy['Sugerencia_Compra'] = df_buy['Demanda_Mes'] * 1.5 # Sugerir comprar para mes y medio
    df_buy['Inversion_Req'] = df_buy['Sugerencia_Compra'] * df_buy['Costo']
    
    st.dataframe(
        df_buy.sort_values('Demanda_Mes', ascending=False).head(10),
        column_config={
            "Inversion_Req": st.column_config.NumberColumn("Inversión ($)", format="$%d"),
            "Demanda_Mes": st.column_config.ProgressColumn("Demanda", format="%d", min_value=0, max_value=df_buy['Demanda_Mes'].max()),
        },
        hide_index=True,
        use_container_width=True
    )
    st.button("Generar Órdenes de Compra Automáticas", type="primary", key="btn_buy_auto")

with col_action_right:
    st.warning(f"💰 OPORTUNIDAD: Liquidar ({len(excedentes)} SKUs)")
    st.markdown("Estos productos tienen **más de 4 meses de stock**. Lanza promociones para recuperar liquidez.")
    
    df_sell = excedentes[['SKU', 'Producto', 'Stock', 'Demanda_Mes', 'Valor_Inventario']].copy()
    df_sell['Meses_Cobertura'] = df_sell['Stock'] / df_sell['Demanda_Mes']
    
    st.dataframe(
        df_sell.sort_values('Valor_Inventario', ascending=False).head(10),
        column_config={
            "Valor_Inventario": st.column_config.NumberColumn("Capital Atrapado", format="$%d"),
            "Meses_Cobertura": st.column_config.NumberColumn("Meses Stock", format="%.1f m"),
        },
        hide_index=True,
        use_container_width=True
    )
    st.button("Crear Campaña de Liquidación (Promo)", key="btn_sell_auto")
