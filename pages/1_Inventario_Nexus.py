import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# --- 1. CONFIGURACIÓN DE PÁGINA ---
# ==============================================================================
st.set_page_config(
    page_title="Nexus AI | Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# --- 2. CSS PREMIUM (ESTILO CLARO / UNIFICADO) ---
# ==============================================================================
st.markdown("""
<style>
    /* IMPORTAR FUENTE */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&display=swap');

    /* --- FONDO GENERAL (LIGHT THEME) --- */
    .stApp {
        background-color: #F8FAFC; /* Gris muy suave (Slate 50) */
        color: #1E293B; /* Slate 800 */
        font-family: 'Inter', sans-serif;
    }
    
    /* MODIFICAR SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    /* TARJETAS KPI (Dashboard Widgets) */
    .metric-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border-left: 5px solid #2563EB; /* Acento Azul */
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    .metric-label {
        font-size: 0.85rem;
        color: #64748B; /* Slate 500 */
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0F172A; /* Slate 900 */
    }

    .metric-delta {
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 8px;
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
    }

    .delta-pos { 
        background-color: #DCFCE7; /* Verde claro */
        color: #166534; /* Verde oscuro */
    }
    
    .delta-neg { 
        background-color: #FEE2E2; /* Rojo claro */
        color: #991B1B; /* Rojo oscuro */
    }
    
    .delta-neu {
        background-color: #F1F5F9;
        color: #475569;
    }

    /* CAJA DE INSIGHTS IA */
    .ai-box {
        background: #F0F9FF; /* Azul cielo muy claro */
        border: 1px solid #BAE6FD;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 30px;
        position: relative;
    }
    
    .ai-title { 
        color: #0284C7; /* Azul fuerte */
        font-weight: 800; 
        font-size: 1.1rem; 
        display: flex; 
        align-items: center; 
        gap: 10px;
        margin-bottom: 10px;
    }

    /* ESTILIZAR TABLAS DATAFRAME */
    div[data-testid="stDataFrame"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    /* BOTONES PRIMARIOS */
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #0284C7 100%);
        color: white;
        border: none;
        font-weight: 600;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }
    
    h1, h2, h3, h4 {
        color: #0F172A;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- 3. GENERADOR DE DATOS AVANZADO (LÓGICA) ---
# ==============================================================================
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

# ==============================================================================
# --- 4. SIDEBAR DE NAVEGACIÓN Y FILTROS ---
# ==============================================================================
with st.sidebar:
    # --- ENLACE DE RETORNO ---
    st.markdown("### 🧭 Navegación")
    st.page_link("Portafolio_Servicios.py", label="Volver al Inicio", icon="🏠")
    
    st.divider()
    st.header("🎛️ Filtros de Control")
    filtro_cat = st.multiselect("Categoría", df['Categoria'].unique(), default=df['Categoria'].unique())
    filtro_prov = st.multiselect("Proveedor", df['Proveedor'].unique())
    
    if filtro_cat:
        df = df[df['Categoria'].isin(filtro_cat)]
    if filtro_prov:
        df = df[df['Proveedor'].isin(filtro_prov)]
        
    st.markdown("---")
    st.caption("📅 Datos actualizados: Tiempo Real")

# ==============================================================================
# --- 5. CABECERA ESTRATÉGICA ---
# ==============================================================================
col_logo, col_title = st.columns([0.8, 8])
with col_logo:
    st.markdown("<div style='font-size: 50px; text-align: center;'>⚡</div>", unsafe_allow_html=True)
with col_title:
    st.title("NEXUS PRO | Inteligencia de Inventarios")
    st.markdown("<span style='color: #64748B; font-size: 1.1rem;'>Vista Ejecutiva: Análisis de capital, rotación y predicción de demanda en tiempo real.</span>", unsafe_allow_html=True)

st.write("") # Espaciador

# ==============================================================================
# --- 6. DIAGNÓSTICO IA ---
# ==============================================================================
total_inv = df['Valor_Inventario'].sum()
quiebres = df[df['Estado'].str.contains("Quiebre")]
excedentes = df[df['Estado'].str.contains("Excedente")]
costo_oportunidad = quiebres['Demanda_Mes'].sum() * quiebres['Precio'].mean() # Venta perdida estimada
capital_congelado = excedentes['Valor_Inventario'].sum()

st.markdown(f"""
<div class="ai-box">
    <div class="ai-title">🤖 Nexus AI Insights</div>
    <p style="margin-top: 5px; margin-bottom: 0; color: #334155; line-height: 1.6;">
        He analizado <strong>{len(df)} referencias</strong>. Tu salud de inventario es del <strong>78%</strong>.
        <br>⚠️ <strong style="color: #EF4444;">Alerta Crítica:</strong> Detecté <strong>{len(quiebres)} productos en quiebre</strong> que están generando una pérdida de oportunidad de <strong>${costo_oportunidad/1e6:,.1f}M</strong> mensuales.
        <br>💰 <strong style="color: #2563EB;">Oportunidad de Flujo de Caja:</strong> Tienes <strong>${capital_congelado/1e6:,.1f}M</strong> en stock inmovilizado (Excedentes) que podrías liquidar para liberar capital.
    </p>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# --- 7. KPIs DE ALTO IMPACTO ---
# ==============================================================================
c1, c2, c3, c4 = st.columns(4)

def card(col, title, value, delta, status="neu"):
    # status: pos (verde), neg (rojo), neu (gris)
    color_class = f"delta-{status}"
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-delta {color_class}">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

card(c1, "Valor Total Inventario", f"${total_inv/1e6:,.1f} M", "▲ 2.4% vs Mes Ant.", "pos")
card(c2, "Capital Congelado", f"${capital_congelado/1e6:,.1f} M", "▼ Acción Requerida", "neg")
card(c3, "Ventas Perdidas (Est)", f"${costo_oportunidad/1e6:,.1f} M", "▼ Por Quiebres", "neg")
card(c4, "Días de Inventario (DSI)", f"{df['Stock'].mean()/df['Demanda_Mes'].mean()*30:.0f} Días", "▲ En Objetivo", "pos")

# ==============================================================================
# --- 8. VISUALIZACIÓN AVANZADA ---
# ==============================================================================
st.markdown("### 📊 Análisis Visual Profundo")

tab_vis1, tab_vis2, tab_vis3 = st.tabs(["Mapa de Calor Financiero", "Rendimiento de Proveedores", "Distribución de Salud"])

# Configuración de colores para Plotly Light Theme
colors_map = {
    '🟢 Saludable': '#10B981',      # Emerald 500
    '🔴 Quiebre (Crítico)': '#EF4444', # Red 500
    '🟠 Riesgo Quiebre': '#F59E0B',    # Amber 500
    '🔵 Excedente (Inmovilizado)': '#3B82F6' # Blue 500
}

with tab_vis1:
    # TREEMAP
    st.markdown("<h5 style='color: #475569;'>¿Dónde está invertido mi dinero? (Tamaño = Valor Inventario)</h5>", unsafe_allow_html=True)
    fig_tree = px.treemap(
        df, 
        path=[px.Constant("Inventario Total"), 'Categoria', 'Subcategoria', 'Producto'], 
        values='Valor_Inventario',
        color='Estado',
        color_discrete_map=colors_map,
        hover_data=['Stock', 'Costo']
    )
    # Ajustes visuales para tema claro
    fig_tree.update_layout(
        margin=dict(t=0, l=0, r=0, b=0), 
        height=450,
        font=dict(family="Inter, sans-serif"),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_tree, use_container_width=True)

with tab_vis2:
    # SCATTER
    col_prov1, col_prov2 = st.columns([3, 1])
    with col_prov1:
        fig_scatter = px.scatter(
            df, 
            x="Lead_Time", 
            y="Valor_Inventario", 
            size="Demanda_Mes", 
            color="Proveedor",
            hover_name="Producto",
            title="Matriz de Riesgo: Tiempo vs Capital",
            labels={"Lead_Time": "Tiempo de Entrega (Días)", "Valor_Inventario": "Capital Invertido ($)"}
        )
        fig_scatter.update_layout(
            height=400,
            template="plotly_white", # Tema claro por defecto
            font=dict(family="Inter, sans-serif", color="#334155"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0'),
            yaxis=dict(showgrid=True, gridcolor='#E2E8F0')
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    with col_prov2:
        st.info("""
        **Interpretación:**
        Los puntos a la derecha son proveedores lentos.
        Burbujas grandes y altas indican **mucho dinero atrapado** con baja eficiencia.
        ¡Negocia mejores tiempos!
        """)

with tab_vis3:
    # SUNBURST & GAUGE
    c_pie1, c_pie2 = st.columns(2)
    with c_pie1:
        fig_sun = px.sunburst(
            df, 
            path=['Categoria', 'Estado'], 
            values='Valor_Inventario',
            color='Estado',
            color_discrete_map=colors_map
        )
        fig_sun.update_layout(font=dict(family="Inter, sans-serif"), margin=dict(t=0, l=0, r=0, b=0))
        st.plotly_chart(fig_sun, use_container_width=True)
    with c_pie2:
        # Gauge Chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = (1 - (len(quiebres)/len(df))) * 100,
            title = {'text': "Nivel de Servicio Actual", 'font': {'size': 20, 'color': '#334155'}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#334155"},
                'bar': {'color': "#10B981"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#E2E8F0",
                'steps': [
                    {'range': [0, 80], 'color': "#FEE2E2"},
                    {'range': [80, 95], 'color': "#FEF3C7"}],
                'threshold': {'line': {'color': "#EF4444", 'width': 4}, 'thickness': 0.75, 'value': 95}
            }
        ))
        fig_gauge.update_layout(height=300, font=dict(family="Inter, sans-serif"), paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_gauge, use_container_width=True)

# ==============================================================================
# --- 9. CENTRO DE COMANDOS (TABLAS ACCIONABLES) ---
# ==============================================================================
st.markdown("---")
st.markdown("### 🚀 Centro de Comandos: Acciones Recomendadas")

col_action_left, col_action_right = st.columns(2)

# --- PANEL DE COMPRAS ---
with col_action_left:
    st.markdown("""
    <div style="background-color: #FEF2F2; padding: 15px; border-radius: 8px; border-left: 5px solid #EF4444; margin-bottom: 15px;">
        <h4 style="margin:0; color: #991B1B;">🚨 URGENTE: Reabastecer ({skus} SKUs)</h4>
        <p style="margin:0; color: #7F1D1D; font-size: 0.9rem;">Productos con venta activa pero Stock 0. <b>Estás perdiendo ventas.</b></p>
    </div>
    """.format(skus=len(quiebres)), unsafe_allow_html=True)
    
    df_buy = quiebres[['SKU', 'Producto', 'Proveedor', 'Demanda_Mes', 'Costo']].copy()
    df_buy['Sugerencia_Compra'] = df_buy['Demanda_Mes'] * 1.5 
    df_buy['Inversion_Req'] = df_buy['Sugerencia_Compra'] * df_buy['Costo']
    
    max_val_demanda = int(df_buy['Demanda_Mes'].max()) if not df_buy.empty else 100

    st.dataframe(
        df_buy.sort_values('Demanda_Mes', ascending=False).head(10),
        column_config={
            "Inversion_Req": st.column_config.NumberColumn("Inversión ($)", format="$%d"),
            "Demanda_Mes": st.column_config.ProgressColumn(
                "Demanda", 
                format="%d", 
                min_value=0, 
                max_value=max_val_demanda
            ),
        },
        hide_index=True,
        use_container_width=True
    )
    st.button("Generar Órdenes de Compra Automáticas", type="primary", key="btn_buy_auto")

# --- PANEL DE LIQUIDACIÓN ---
with col_action_right:
    st.markdown("""
    <div style="background-color: #EFF6FF; padding: 15px; border-radius: 8px; border-left: 5px solid #3B82F6; margin-bottom: 15px;">
        <h4 style="margin:0; color: #1E40AF;">💰 OPORTUNIDAD: Liquidar ({skus} SKUs)</h4>
        <p style="margin:0; color: #1E3A8A; font-size: 0.9rem;">Productos con >4 meses de stock. <b>Lanza promociones para recuperar caja.</b></p>
    </div>
    """.format(skus=len(excedentes)), unsafe_allow_html=True)
    
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
