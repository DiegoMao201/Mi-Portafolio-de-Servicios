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
# --- 2. CSS PREMIUM (ESTILO CLARO / FRESCO) ---
# ==============================================================================
st.markdown("""
<style>
    /* IMPORTAR FUENTE */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&display=swap');

    /* --- FONDO GENERAL --- */
    .stApp {
        background-color: #F8FAFC; /* Slate 50 */
        color: #334155; /* Slate 700 */
        font-family: 'Inter', sans-serif;
    }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    /* TARJETAS KPI */
    .metric-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        transition: transform 0.2s ease;
        border-left: 5px solid #0EA5E9; /* Sky Blue */
    }
    .metric-card:hover { transform: translateY(-4px); }
    .metric-label { font-size: 0.8rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 1.6rem; font-weight: 800; color: #0F172A; margin: 5px 0; }
    
    /* DELTAS (Indicadores de cambio) */
    .delta-badge {
        font-size: 0.75rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 6px;
        display: inline-block;
    }
    .d-pos { background-color: #DCFCE7; color: #166534; } /* Verde suave */
    .d-neg { background-color: #FEE2E2; color: #991B1B; } /* Rojo suave */
    .d-neu { background-color: #F1F5F9; color: #475569; }

    /* CAJA DE INSIGHTS IA */
    .ai-box {
        background: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 30px;
    }
    .ai-title { color: #0369A1; font-weight: 700; font-size: 1.1rem; display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }

    /* ESTILOS DE TEXTO EXPLICATIVO */
    .section-desc { font-size: 0.95rem; color: #64748B; line-height: 1.5; margin-bottom: 15px; }

    /* BOTONES */
    div.stButton > button {
        background: linear-gradient(135deg, #0EA5E9 0%, #2563EB 100%);
        color: white;
        border: none;
        font-weight: 600;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(14, 165, 233, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- 3. GENERADOR DE DATOS AVANZADO ---
# ==============================================================================
@st.cache_data
def generar_data_avanzada():
    np.random.seed(42)
    categorias = {
        'Herramientas': ['Taladros', 'Pulidoras', 'Sierras', 'Kits Manuales'],
        'Construcción': ['Cementos', 'Aditivos', 'Impermeabilizantes', 'Estucos'],
        'Acabados': ['Pintura Tipo 1', 'Esmaltes', 'Brochas', 'Rodillos'],
        'Eléctricos': ['Cableado', 'Tomas', 'Iluminación LED', 'Tableros'],
        'Plomería': ['Tubos PVC', 'Grifería', 'Accesorios', 'Pegamentos']
    }
    
    proveedores_list = ['DistriGlobal', 'FerreAbastos', 'MegaTools', 'Importados SA']
    
    data = []
    for cat, subcats in categorias.items():
        for _ in range(30): 
            subcat = np.random.choice(subcats)
            sku = f"{cat[:3].upper()}-{np.random.randint(1000,9999)}"
            costo = np.random.uniform(5000, 250000)
            margen = np.random.uniform(0.15, 0.55) # Margen bruto
            precio = costo * (1 + margen)
            
            demanda = np.random.poisson(25)
            stock = int(demanda * np.random.uniform(0, 5))
            
            # Datos Proveedor
            prov = np.random.choice(proveedores_list)
            # Simulamos cumplimiento: DistriGlobal es bueno, MegaTools es malo
            if prov == 'DistriGlobal':
                lead_time = np.random.randint(2, 5)
                fill_rate = np.random.uniform(0.95, 1.0)
            elif prov == 'MegaTools':
                lead_time = np.random.randint(10, 25)
                fill_rate = np.random.uniform(0.70, 0.90)
            else:
                lead_time = np.random.randint(5, 15)
                fill_rate = np.random.uniform(0.85, 0.98)

            meses_cob = stock / demanda if demanda > 0 else 99
            
            if stock == 0: estado = "🔴 Quiebre"
            elif meses_cob < 0.8: estado = "🟠 Riesgo"
            elif meses_cob > 4: estado = "🔵 Excedente"
            else: estado = "🟢 Óptimo"
            
            # Rentabilidad bruta mensual estimada
            utilidad_mensual = (precio - costo) * demanda

            data.append({
                'SKU': sku,
                'Producto': f"{subcat} Pro {np.random.randint(100,999)}",
                'Categoria': cat,
                'Subcategoria': subcat,
                'Proveedor': prov,
                'Costo': costo,
                'Precio': precio,
                'Margen_Pct': margen,
                'Utilidad_Mensual': utilidad_mensual,
                'Stock': stock,
                'Demanda_Mes': demanda,
                'Valor_Inventario': stock * costo,
                'Lead_Time_Real': lead_time,
                'Fill_Rate': fill_rate, # Porcentaje de entrega completa
                'Estado': estado
            })
            
    return pd.DataFrame(data)

df = generar_data_avanzada()

# ==============================================================================
# --- 4. SIDEBAR Y FILTROS ---
# ==============================================================================
with st.sidebar:
    st.markdown("### 🧭 Navegación")
    st.page_link("Portafolio_Servicios.py", label="Volver al Inicio", icon="🏠")
    st.divider()
    
    st.header("🎛️ Filtros Globales")
    filtro_cat = st.multiselect("Categoría", df['Categoria'].unique(), default=df['Categoria'].unique())
    filtro_prov = st.multiselect("Proveedor", df['Proveedor'].unique())
    
    if filtro_cat:
        df = df[df['Categoria'].isin(filtro_cat)]
    if filtro_prov:
        df = df[df['Proveedor'].isin(filtro_prov)]
        
    st.caption("Los filtros afectan todas las pestañas y KPIs.")

# ==============================================================================
# --- 5. CABECERA ---
# ==============================================================================
c_head1, c_head2 = st.columns([0.8, 8])
with c_head1:
    st.markdown("<div style='font-size: 45px; text-align: center;'>⚡</div>", unsafe_allow_html=True)
with c_head2:
    st.title("NEXUS PRO | Inteligencia de Inventarios")
    st.markdown("<span style='color: #64748B;'>Tablero de control ejecutivo para la toma de decisiones estratégicas.</span>", unsafe_allow_html=True)

st.write("")

# ==============================================================================
# --- 6. INSIGHTS & KPIs ---
# ==============================================================================
total_inv = df['Valor_Inventario'].sum()
quiebres_df = df[df['Estado'] == "🔴 Quiebre"]
excedentes_df = df[df['Estado'] == "🔵 Excedente"]
fill_rate_avg = df['Fill_Rate'].mean() * 100

st.markdown(f"""
<div class="ai-box">
    <div class="ai-title">🤖 Diagnóstico Nexus AI</div>
    <p style="margin: 0; color: #334155; line-height: 1.6;">
        El análisis de <strong>{len(df)} referencias</strong> muestra una salud operativa del <strong>{fill_rate_avg:.1f}%</strong> en abastecimiento.
        <br>• <strong>Foco Prioritario:</strong> Resolver los <strong>{len(quiebres_df)} productos agotados</strong> para recuperar ventas.
        <br>• <strong>Eficiencia de Capital:</strong> Hay <strong>${excedentes_df['Valor_Inventario'].sum()/1e6:,.1f}M</strong> en inventario lento que frena la rentabilidad.
    </p>
</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
def kpi(col, label, value, badge_text, badge_type):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="delta-badge {badge_type}">{badge_text}</div>
        </div>
        """, unsafe_allow_html=True)

kpi(k1, "Valor Inventario", f"${total_inv/1e6:,.1f} M", "+3.2% vs Obj", "d-neu")
kpi(k2, "Nivel de Servicio (Fill Rate)", f"{fill_rate_avg:.1f}%", "-2% vs Meta", "d-neg")
kpi(k3, "Capital Inmovilizado", f"${excedentes_df['Valor_Inventario'].sum()/1e6:,.1f} M", "Optimizable", "d-neu")
kpi(k4, "Rentabilidad Proyectada", f"${df['Utilidad_Mensual'].sum()/1e6:,.1f} M", "Mensual", "d-pos")

# ==============================================================================
# --- 7. ANÁLISIS DETALLADO (TABS) ---
# ==============================================================================
st.markdown("### 📊 Tablero de Decisiones")

tab1, tab2, tab3 = st.tabs(["💰 Rentabilidad & Esfuerzo", "🚛 Diagnóstico Proveedor", "🎯 Nivel de Servicio"])

# --- TAB 1: RENTABILIDAD (NUEVO ENFOQUE) ---
with tab1:
    st.markdown("""
    <p class="section-desc">
    <b>¿Dónde enfocamos esfuerzos?</b> Identifica qué categorías impulsan tu ganancia ("Motores") 
    y cuáles consumen capital sin rotar ("Frenos"). Usa colores frescos para facilitar la lectura.
    </p>
    """, unsafe_allow_html=True)
    
    col_rent1, col_rent2 = st.columns(2)
    
    # Agrupación por categoría
    df_cat = df.groupby('Categoria').agg({
        'Utilidad_Mensual': 'sum',
        'Valor_Inventario': 'sum',
        'Margen_Pct': 'mean'
    }).reset_index()
    
    with col_rent1:
        st.markdown("##### 🚀 Motores de Rentabilidad (Utilidad Total)")
        fig_bar = px.bar(
            df_cat.sort_values('Utilidad_Mensual', ascending=True),
            x='Utilidad_Mensual',
            y='Categoria',
            orientation='h',
            text_auto='.2s',
            color='Utilidad_Mensual',
            color_continuous_scale=['#CCFBF1', '#2DD4BF', '#0F766E'] # Teal fresco
        )
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Utilidad Mensual ($)",
            yaxis_title=None,
            coloraxis_showscale=False,
            height=350
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.caption("Estas categorías pagan las cuentas. Prioridad: **Mantener Stock**.")

    with col_rent2:
        st.markdown("##### ⚓ Frenos de Capital (Inventario vs Margen)")
        # Scatter Plot: Eje X = Valor Inventario, Eje Y = Margen Promedio
        fig_scat = px.scatter(
            df_cat,
            x='Valor_Inventario',
            y='Margen_Pct',
            size='Valor_Inventario',
            color='Categoria',
            text='Categoria',
            color_discrete_sequence=px.colors.qualitative.Pastel # Colores suaves
        )
        fig_scat.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Dinero Atrapado en Inventario ($)",
            yaxis_title="Margen Promedio (%)",
            height=350,
            showlegend=False
        )
        fig_scat.update_traces(textposition='top center')
        st.plotly_chart(fig_scat, use_container_width=True)
        st.caption("Cuadrante inferior derecho (Mucho dinero, poco margen) requiere **Liquidación**.")

# --- TAB 2: DIAGNÓSTICO PROVEEDOR (CHECKLIST) ---
with tab2:
    st.markdown("""
    <p class="section-desc">
    <b>Auditoría de Cumplimiento.</b> Evaluamos a los socios logísticos no solo por precio, sino por 
    confiabilidad (tiempos) y completitud (Fill Rate).
    </p>
    """, unsafe_allow_html=True)
    
    # Crear Scorecard
    prov_score = df.groupby('Proveedor').agg({
        'Lead_Time_Real': 'mean',
        'Fill_Rate': 'mean',
        'Valor_Inventario': 'sum'
    }).reset_index()
    
    # Lógica de Check
    prov_score['Check_Tiempo'] = prov_score['Lead_Time_Real'].apply(lambda x: "✅ Rápido" if x < 8 else ("⚠️ Lento" if x < 15 else "❌ Crítico"))
    prov_score['Check_Entregas'] = prov_score['Fill_Rate'].apply(lambda x: "✅ Completo" if x > 0.95 else ("⚠️ Parcial" if x > 0.85 else "❌ Incompleto"))
    
    col_audit1, col_audit2 = st.columns([2, 1])
    
    with col_audit1:
        st.markdown("##### 📋 Scorecard de Cumplimiento")
        st.dataframe(
            prov_score,
            column_config={
                "Proveedor": "Socio Logístico",
                "Lead_Time_Real": st.column_config.NumberColumn("Días Promedio", format="%.1f d"),
                "Fill_Rate": st.column_config.ProgressColumn("Tasa Entrega (%)", min_value=0, max_value=1, format="%.0f%%"),
                "Check_Tiempo": "Auditoría Tiempo",
                "Check_Entregas": "Auditoría Calidad",
                "Valor_Inventario": st.column_config.NumberColumn("Volumen Compra", format="$%d")
            },
            hide_index=True,
            use_container_width=True
        )
    
    with col_audit2:
        st.info("💡 **Criterios de Evaluación:**")
        st.markdown("""
        - **✅ Rápido:** < 8 días
        - **❌ Crítico:** > 15 días
        - **✅ Completo:** > 95% de la orden
        - **❌ Incompleto:** < 85% de la orden
        """)
        
        # Gráfica simple de barras apiladas de estado por proveedor
        df_stack = df.groupby(['Proveedor', 'Estado']).size().reset_index(name='Conteo')
        fig_stack = px.bar(df_stack, x='Proveedor', y='Conteo', color='Estado', 
                           color_discrete_map={
                               '🟢 Óptimo': '#34D399', 
                               '🔴 Quiebre': '#F87171', 
                               '🔵 Excedente': '#60A5FA', 
                               '🟠 Riesgo': '#FBBF24'
                           })
        fig_stack.update_layout(height=200, margin=dict(t=10, l=0, r=0, b=0), showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_stack, use_container_width=True)
        st.caption("Distribución de salud de stock por proveedor.")

# --- TAB 3: NIVEL DE SERVICIO (GAUGE CENTRADO) ---
with tab3:
    st.markdown("""
    <p class="section-desc">
    <b>Termómetro de Satisfacción.</b> ¿Estamos listos para vender? Este indicador resume la probabilidad 
    de tener el producto cuando el cliente lo pide.
    </p>
    """, unsafe_allow_html=True)
    
    c_gauge, c_details = st.columns([1, 1])
    
    servicio_actual = (1 - (len(quiebres_df) / len(df))) * 100
    
    with c_gauge:
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = servicio_actual,
            number = {'suffix': "%", 'font': {'size': 50, 'color': '#0F172A'}}, # Número grande y centrado
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Disponibilidad Total", 'font': {'size': 18, 'color': '#64748B'}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 0, 'tickcolor': "white"},
                'bar': {'color': "#10B981"}, # Emerald Green
                'bgcolor': "white",
                'borderwidth': 0,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 85], 'color': "#F1F5F9"}, # Gris fondo
                    {'range': [0, servicio_actual], 'color': "#34D399"} # Color progreso dinámico si se quisiera complejo, aquí simple
                ],
                'threshold': {
                    'line': {'color': "#F87171", 'width': 4},
                    'thickness': 0.75,
                    'value': 95
                }
            }
        ))
        # Ajustes para que el chart se vea limpio y centrado
        fig_gauge.update_layout(
            height=300, 
            margin=dict(t=50, b=10, l=30, r=30),
            paper_bgcolor='rgba(0,0,0,0)',
            font={'family': "Inter, sans-serif"}
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with c_details:
        st.success(f"Actualmente tienes un **{servicio_actual:.1f}% de disponibilidad**.")
        st.markdown(f"""
        Esto significa que de cada 100 clientes que entran hoy, **{int(servicio_actual)}** encuentran lo que buscan inmediatamente.
        
        **Acciones para llegar al 95% (Meta):**
        1.  Cubrir los **{len(quiebres_df)} productos en quiebre** urgente.
        2.  Revisar a **MegaTools** (Proveedor con menor Fill Rate).
        3.  Redistribuir los excedentes de la categoría **{excedentes_df['Categoria'].mode()[0]}**.
        """)

# ==============================================================================
# --- 8. CENTRO DE ACCIÓN ---
# ==============================================================================
st.markdown("---")
st.markdown("### ⚡ Acciones Recomendadas")

ca1, ca2 = st.columns(2)

with ca1:
    st.markdown(f"""
    <div style="background: #FEF2F2; padding: 15px; border-radius: 8px; border-left: 4px solid #F87171;">
        <h5 style="margin:0; color: #991B1B;">⚠️ Reabastecimiento Crítico</h5>
        <p style="font-size: 0.9rem; color: #7F1D1D;">{len(quiebres_df)} productos clave agotados. Impacto directo en ventas.</p>
    </div>
    """, unsafe_allow_html=True)
    st.button("Generar Pedidos Automáticos", use_container_width=True)

with ca2:
    st.markdown(f"""
    <div style="background: #ECFEFF; padding: 15px; border-radius: 8px; border-left: 4px solid #0EA5E9;">
        <h5 style="margin:0; color: #0C4A6E;">💎 Liberación de Efectivo</h5>
        <p style="font-size: 0.9rem; color: #0e7490;">${excedentes_df['Valor_Inventario'].sum()/1e6:,.1f}M atrapados en stock lento. Sugerimos promo flash.</p>
    </div>
    """, unsafe_allow_html=True)
    st.button("Crear Campaña de Liquidación", use_container_width=True)
