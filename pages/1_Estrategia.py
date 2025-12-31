import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

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
    
    /* CAJAS DE ACCIÓN */
    .action-box-red {
        background: #FEF2F2; 
        padding: 20px; 
        border-radius: 10px; 
        border: 1px solid #FECACA;
        border-left: 5px solid #EF4444;
        height: 100%;
    }
    .action-box-blue {
        background: #EFF6FF; 
        padding: 20px; 
        border-radius: 10px; 
        border: 1px solid #BFDBFE;
        border-left: 5px solid #3B82F6;
        height: 100%;
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
            
            # Datos Proveedor Base
            prov = np.random.choice(proveedores_list)
            
            # Simulación de métricas proveedor para evaluación
            if prov == 'DistriGlobal':
                lead_time = np.random.randint(2, 5)
                fill_rate = np.random.uniform(0.95, 1.0)
                post_venta = np.random.uniform(8, 10)
            elif prov == 'MegaTools':
                lead_time = np.random.randint(10, 25)
                fill_rate = np.random.uniform(0.70, 0.90)
                post_venta = np.random.uniform(4, 7)
            else:
                lead_time = np.random.randint(5, 15)
                fill_rate = np.random.uniform(0.85, 0.98)
                post_venta = np.random.uniform(6, 9)

            # Cálculo de meses de cobertura y días de inventario
            # Días de cobertura = (Stock / Demanda Mensual) * 30 días
            dias_cobertura = (stock / demanda) * 30 if demanda > 0 else 999 
            
            if stock == 0: estado = "🔴 Quiebre"
            elif dias_cobertura < 25: estado = "🟠 Riesgo" # Menos de un mes de stock
            elif dias_cobertura > 120: estado = "🔵 Excedente" # Más de 4 meses de stock
            else: estado = "🟢 Óptimo"
            
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
                'Dias_Inventario': dias_cobertura, # Nuevo KPI
                'Lead_Time_Real': lead_time,
                'Fill_Rate': fill_rate, 
                'Post_Venta': post_venta,
                'Estado': estado
            })
            
    return pd.DataFrame(data)

df_base = generar_data_avanzada()
df = df_base.copy() # Usamos una copia para los filtros


# --- FUNCIÓN LÓGICA DE RECOMENDACIÓN DE PROVEEDOR ---
def recomendar_mejor_proveedor(row):
    """
    Simula una licitación rápida entre los 4 proveedores para este producto.
    Criterios de Ponderación: 80% Precio, 10% Tiempo, 5% Fill Rate, 5% Postventa.
    Devuelve el nombre del proveedor ganador.
    """
    proveedores_sim = ['DistriGlobal', 'FerreAbastos', 'MegaTools', 'Importados SA']
    scores = {}
    
    # Costo base del producto (para simular ofertas)
    costo_base = row['Costo']
    
    for p in proveedores_sim:
        # Simulamos variaciones de oferta por proveedor (Fijos para simplificar la consistencia)
        if p == 'DistriGlobal':
            factor_precio = 1.05 # Más caro (mejor calidad/servicio)
            tiempo = 3
            fill = 0.98
            post = 9.0
        elif p == 'MegaTools':
            factor_precio = 0.90 # Muy barato (peor calidad/servicio)
            tiempo = 20
            fill = 0.80
            post = 5.0
        elif p == 'Importados SA':
            factor_precio = 0.95 
            tiempo = 10 
            fill = 0.90
            post = 7.0
        else: # FerreAbastos (Promedio)
            factor_precio = 1.00
            tiempo = 7
            fill = 0.92
            post = 8.0
            
        precio_oferta = costo_base * factor_precio
        
        # Normalización (Simplificada para score 0-100)
        # Precio: Menor es mejor. Usamos inverso (un precio más bajo da un score más alto)
        score_precio = (costo_base / precio_oferta) * 100 
        
        # Tiempo: Menor es mejor. (Tiempo alto penaliza)
        score_tiempo = max(0, 100 - (tiempo * 3)) # Pasa de 0 a 100, 3 días = 91, 20 días = 40
        
        # Fill Rate: Directo
        score_fill = fill * 100
        
        # Post Venta: Directo (es sobre 10, escalamos a 100)
        score_post = post * 10
        
        # PONDERACIÓN DEL CLIENTE
        # 80% Precio, 10% Tiempo, 5% Fill Rate, 5% Postventa
        final_score = (score_precio * 0.80) + (score_tiempo * 0.10) + (score_fill * 0.05) + (score_post * 0.05)
        scores[p] = final_score

    # Retorna el proveedor con max score
    mejor_proveedor = max(scores, key=scores.get)
    return mejor_proveedor

# ==============================================================================
# --- 4. SIDEBAR Y FILTROS ---
# ==============================================================================
with st.sidebar:
    st.markdown("### 🧭 Navegación")
    st.page_link("Home.py", label="Volver al Inicio", icon="🏠")
    st.divider()
    
    st.header("🎛️ Filtros Globales")
    filtro_cat = st.multiselect("Categoría", df_base['Categoria'].unique(), default=df_base['Categoria'].unique())
    filtro_prov = st.multiselect("Proveedor", df_base['Proveedor'].unique())
    
    # Aplicar filtros
    df = df_base.copy()
    if filtro_cat:
        df = df[df['Categoria'].isin(filtro_cat)]
    if filtro_prov:
        df = df[df['Proveedor'].isin(filtro_prov)]
        
    st.caption("Los filtros afectan todas las pestañas y KPIs.")
    if df.empty:
        st.error("⚠️ La combinación de filtros no arrojó resultados.")
        st.stop() # Detiene la ejecución si no hay datos

# ==============================================================================
# --- 5. CABECERA ---
# ==============================================================================
c_head1, c_head2 = st.columns([0.8, 8])
with c_head1:
    st.markdown("<div style='font-size: 45px; text-align: center;'>⚡</div>", unsafe_allow_html=True)
with c_head2:
    st.title("NEXUS PRO | Control & Estrategia")
    st.markdown("<span style='color: #64748B;'>Tablero de control ejecutivo para la toma de decisiones estratégicas.</span>", unsafe_allow_html=True)

st.write("")

# ==============================================================================
# --- 6. INSIGHTS & KPIs ---
# ==============================================================================
total_inv = df['Valor_Inventario'].sum()
total_utilidad = df['Utilidad_Mensual'].sum()
dias_inv_avg = df[df['Demanda_Mes'] > 0]['Dias_Inventario'].mean() # Solo para productos con demanda
quiebres_df = df[df['Estado'] == "🔴 Quiebre"].copy()
excedentes_df = df[df['Estado'] == "🔵 Excedente"].copy()
# KPI de Rotación de Inventario (Días)
if dias_inv_avg < 30: # Rotación alta / stock bajo
    rotacion_text = "Rápida"
    rotacion_type = "d-pos"
elif dias_inv_avg > 90: # Rotación lenta / stock alto
    rotacion_text = "Lenta"
    rotacion_type = "d-neg"
else:
    rotacion_text = "Óptima"
    rotacion_type = "d-neu"

# KPI de Quiebres (para el insight)
quiebres_utilidad_perdida = quiebres_df['Utilidad_Mensual'].sum() # Utilidad que se deja de ganar al estar en quiebre

st.markdown(f"""
<div class="ai-box">
    <div class="ai-title">🤖 Diagnóstico Nexus AI</div>
    <p style="margin: 0; color: #334155; line-height: 1.6;">
        El análisis de <strong>{len(df):,} referencias</strong> indica una rotación promedio de <strong>{dias_inv_avg:.0f} días</strong>.
        <br>• <strong>Foco Prioritario (Quiebres):</strong> Urge reabastecer los <strong>{len(quiebres_df)} productos agotados</strong>, que representan una potencial pérdida de <strong>${quiebres_utilidad_perdida/1e6:,.1f}M</strong> en utilidad mensual.
        <br>• <strong>Eficiencia de Capital (Excedentes):</strong> Hay <strong>${excedentes_df['Valor_Inventario'].sum()/1e6:,.1f}M</strong> en inventario lento.
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

kpi(k1, "Valor Inventario Total", f"${total_inv/1e6:,.1f} M", "+3.2% vs Obj", "d-neu")
kpi(k2, "Días Inventario en Existencia", f"{dias_inv_avg:.0f} Días", rotacion_text, rotacion_type)
kpi(k3, "Capital Inmovilizado (Excedentes)", f"${excedentes_df['Valor_Inventario'].sum()/1e6:,.1f} M", "Optimizable", "d-neu")
kpi(k4, "Utilidad Mensual Proyectada", f"${total_utilidad/1e6:,.1f} M", "Mensual", "d-pos")

# ==============================================================================
# --- 7. ANÁLISIS DETALLADO (TABS) ---
# ==============================================================================
st.markdown("---")
st.markdown("### 📊 Tablero de Decisiones")

tab1, tab2, tab3 = st.tabs(["💰 Rentabilidad & Esfuerzo", "🚛 Diagnóstico Proveedor", "🎯 Rotación de Inventario"])

with tab1:
    st.markdown("""<p class="section-desc"><b>¿Dónde enfocamos esfuerzos?</b> Identifica qué categorías impulsan tu ganancia ("Motores") y cuáles consumen capital sin rotar ("Frenos").</p>""", unsafe_allow_html=True)
    col_rent1, col_rent2 = st.columns(2)
    df_cat = df.groupby('Categoria').agg({'Utilidad_Mensual': 'sum', 'Valor_Inventario': 'sum', 'Margen_Pct': 'mean'}).reset_index()
    
    with col_rent1:
        st.markdown("##### 🚀 Motores de Rentabilidad (Utilidad Total)")
        fig_bar = px.bar(df_cat.sort_values('Utilidad_Mensual', ascending=True), x='Utilidad_Mensual', y='Categoria', orientation='h', text_auto='.2s', color='Utilidad_Mensual', color_continuous_scale=['#CCFBF1', '#2DD4BF', '#0F766E'])
        fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Utilidad Mensual ($)", yaxis_title=None, coloraxis_showscale=False, height=350)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_rent2:
        st.markdown("##### ⚓ Frenos de Capital (Inventario vs Margen)")
        fig_scat = px.scatter(df_cat, x='Valor_Inventario', y='Margen_Pct', size='Valor_Inventario', color='Categoria', text='Categoria', color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_scat.update_layout(plot_bgcolor='rgba(0,0,0,0)', xaxis_title="Dinero Atrapado ($)", yaxis_title="Margen (%)", height=350, showlegend=False)
        fig_scat.update_traces(textposition='top center')
        st.plotly_chart(fig_scat, use_container_width=True)

with tab2:
    st.markdown("""<p class="section-desc"><b>Auditoría de Cumplimiento.</b> Evaluamos a los socios logísticos por confiabilidad (tiempos) y completitud (Fill Rate).</p>""", unsafe_allow_html=True)
    prov_score = df.groupby('Proveedor').agg({'Lead_Time_Real': 'mean', 'Fill_Rate': 'mean', 'Valor_Inventario': 'sum'}).reset_index()
    prov_score['Check_Tiempo'] = prov_score['Lead_Time_Real'].apply(lambda x: "✅ Rápido" if x < 8 else ("⚠️ Lento" if x < 15 else "❌ Crítico"))
    prov_score['Check_Entregas'] = prov_score['Fill_Rate'].apply(lambda x: "✅ Completo" if x > 0.95 else ("⚠️ Parcial" if x > 0.85 else "❌ Incompleto"))
    
    col_audit1, col_audit2 = st.columns([2, 1])
    with col_audit1:
        st.markdown("##### 📋 Scorecard de Cumplimiento")
        st.dataframe(prov_score, column_config={"Proveedor": "Socio Logístico", "Lead_Time_Real": st.column_config.NumberColumn("Días Promedio", format="%.1f d"), "Fill_Rate": st.column_config.ProgressColumn("Tasa Entrega (%)", min_value=0, max_value=1, format="%.0f%%"), "Check_Tiempo": "Auditoría Tiempo", "Check_Entregas": "Auditoría Calidad", "Valor_Inventario": st.column_config.NumberColumn("Volumen Compra", format="$%d")}, hide_index=True, use_container_width=True)
    with col_audit2:
        st.info("💡 **Criterios de Evaluación:**")
        st.markdown("- **✅ Rápido:** < 8 días\n- **❌ Crítico:** > 15 días\n- **✅ Completo:** > 95%\n- **❌ Incompleto:** < 85%")
        df_stack = df.groupby(['Proveedor', 'Estado']).size().reset_index(name='Conteo')
        fig_stack = px.bar(df_stack, x='Proveedor', y='Conteo', color='Estado', color_discrete_map={'🟢 Óptimo': '#34D399', '🔴 Quiebre': '#F87171', '🔵 Excedente': '#60A5FA', '🟠 Riesgo': '#FBBF24'})
        fig_stack.update_layout(height=200, margin=dict(t=10, l=0, r=0, b=0), showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_stack, use_container_width=True)

with tab3:
    st.markdown("""<p class="section-desc"><b>Eficiencia de Capital.</b> Días promedio que el inventario permanece antes de venderse (meta: 30-90 días).</p>""", unsafe_allow_html=True)
    c_gauge, c_details = st.columns([1, 1])
    
    # Calcular Rotación por Categoría
    rotacion_cat = df.groupby('Categoria').agg(
        Total_Stock=('Stock', 'sum'), 
        Total_Demanda=('Demanda_Mes', 'sum')
    ).reset_index()
    # Calcular Días de Inventario de Cobertura
    rotacion_cat['Dias_Inventario'] = rotacion_cat.apply(
        lambda row: (row['Total_Stock'] / row['Total_Demanda']) * 30 if row['Total_Demanda'] > 0 else 999, axis=1
    )
    
    with c_gauge:
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number", 
            value = dias_inv_avg, 
            number = {'suffix': " Días", 'font': {'size': 50, 'color': '#0F172A'}}, 
            domain = {'x': [0, 1], 'y': [0, 1]}, 
            title = {'text': "Rotación Promedio (Días)", 'font': {'size': 18, 'color': '#64748B'}}, 
            gauge = {
                'axis': {'range': [0, 180], 'tickwidth': 0, 'tickcolor': "white"}, 
                'bar': {'color': "#10B981"}, 
                'bgcolor': "white", 
                'borderwidth': 0, 
                'bordercolor': "gray", 
                'steps': [
                    {'range': [0, 25], 'color': "#FEF2F2"}, # Rotación muy rápida/stock bajo
                    {'range': [25, 90], 'color': "#DCFCE7"}, # Óptimo
                    {'range': [90, 180], 'color': "#F0F9FF"} # Lento/Excedente
                ], 
                'threshold': {'line': {'color': "#FBBF24", 'width': 4}, 'thickness': 0.75, 'value': 90}}
        ))
        fig_gauge.update_layout(height=300, margin=dict(t=50, b=10, l=30, r=30), paper_bgcolor='rgba(0,0,0,0)', font={'family': "Inter, sans-serif"})
        st.plotly_chart(fig_gauge, use_container_width=True)
    with c_details:
        st.success(f"La rotación promedio es de **{dias_inv_avg:.0f} días**.")
        st.markdown(f"Esto se traduce en que el capital está atado por **{dias_inv_avg:.0f} días** antes de generar flujo.\n\n**Acciones Clave de Rotación:**\n1.  Priorizar la venta de **Excedentes** (> 120 días).\n2.  Revisar **categorías lentas** en la gráfica inferior.\n3.  Ajustar frecuencia de pedidos a **30-60 días**.")
        
        st.markdown("##### 🔄 Rotación por Categoría")
        fig_pie = px.pie(rotacion_cat, values='Dias_Inventario', names='Categoria', color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_traces(textinfo='label+percent', hole=.3)
        fig_pie.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0), showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)


# ==============================================================================
# --- 8. CENTRO DE ACCIÓN (LÓGICA ACTUALIZADA) ---
# ==============================================================================
st.markdown("---")
st.markdown("### ⚡ Centro de Acción: Nexus Pro")

col_quiebres, col_excedentes = st.columns(2)

# --- COLUMNA 1: GESTIÓN DE QUIEBRES (Con Recomendador IA) ---
with col_quiebres:
    st.markdown("""<div class="action-box-red"><h4 style="color: #991B1B; margin:0;">🚨 Prioridad URGENTE: Quiebres de Stock</h4><p style="color: #7F1D1D;">Selección de los 6 productos con mayor utilidad potencial perdida.</p></div>""", unsafe_allow_html=True)
    st.write("")
    
    if not quiebres_df.empty:
        # Seleccionar top 6 quiebres por POTENCIAL DE UTILIDAD PERDIDA (Utilidad_Mensual)
        quiebres_top = quiebres_df.sort_values('Utilidad_Mensual', ascending=False).head(6).copy()
        
        # Aplicar el motor de recomendación fila por fila
        quiebres_top['Mejor_Opcion_IA'] = quiebres_top.apply(recomendar_mejor_proveedor, axis=1)
        
        st.dataframe(
            quiebres_top[['SKU', 'Producto', 'Proveedor', 'Mejor_Opcion_IA', 'Utilidad_Mensual']],
            column_config={
                "Proveedor": "Prov. Actual",
                "Mejor_Opcion_IA": st.column_config.TextColumn("⭐ Sugerencia IA", help="Proveedor mejor evaluado: 80% Precio, 10% Tiempo, 5% Fill Rate, 5% Postventa"),
                "Utilidad_Mensual": st.column_config.NumberColumn("Ganancia Perdida/Mes", format="$%d")
            },
            hide_index=True,
            use_container_width=True
        )
        
        if st.button("🛒 Ejecutar Pedido Inteligente (6 Productos)", type="primary"):
            st.toast("Analizando la mejor oferta...", icon="🤖")
            time.sleep(1.5)
            st.success(f"¡Órdenes de compra generadas! Se han seleccionado los **proveedores sugeridos por Nexus AI** para reponer los 6 productos más críticos. Pedido #ORD-{np.random.randint(10000,99999)} enviado al ERP.")
            st.balloons()
    else:
        st.success("✅ No hay quiebres de stock críticos con potencial de pérdida en este momento.")

# --- COLUMNA 2: LIBERACIÓN DE EFECTIVO (Con Campañas Dinámicas) ---
with col_excedentes:
    st.markdown("""<div class="action-box-blue"><h4 style="color: #1E40AF; margin:0;">💎 Estrategia: Liberación de Efectivo</h4><p style="color: #1E3A8A;">Convierte el inventario quieto (más de 4 meses) en flujo de caja inmediato.</p></div>""", unsafe_allow_html=True)
    st.write("")
    
    if not excedentes_df.empty:
        # Seleccionar top 6 excedentes por valor de inventario
        excedentes_top = excedentes_df.sort_values('Valor_Inventario', ascending=False).head(6).copy()
        
        # Selector de Estrategia
        estrategia = st.radio(
            "Seleccione Tipo de Campaña:",
            ["Opción 1: Liquidación (Costo + 5%)", "Opción 2: Gran Remate (PVP - 50%)"],
            horizontal=True,
            key='campana_radio' # Añadido key para evitar errores de duplicidad
        )
        
        # Calcular nuevo precio según estrategia
        if "Opción 1" in estrategia:
            excedentes_top['Precio_Promo'] = excedentes_top['Costo'] * 1.05
            tag_promo = "LIQUIDACIÓN"
        else:
            excedentes_top['Precio_Promo'] = excedentes_top['Precio'] * 0.50
            tag_promo = "REMATE -50%"
            
        st.dataframe(
            excedentes_top[['SKU', 'Producto', 'Stock', 'Precio', 'Precio_Promo']],
            column_config={
                "Precio": st.column_config.NumberColumn("Precio Actual", format="$%d"),
                "Precio_Promo": st.column_config.NumberColumn(f"⚡ Precio {tag_promo}", format="$%d")
            },
            hide_index=True,
            use_container_width=True
        )
        
        if st.button("📢 Lanzar Campaña & Notificar", type="secondary"):
            st.toast("Generando listados...", icon="📄")
            time.sleep(1)
            st.toast("Enviando alerta a Gerencia Comercial...", icon="💬")
            time.sleep(1)
            st.success(f"¡Campaña **{tag_promo}** Activada! Listado de productos excedentes enviado por correo y alerta de WhatsApp disparada.")
    else:
        st.success("✅ Tu inventario está saludable. No hay excedentes críticos que requieran campaña.")
