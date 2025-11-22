import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

# ==============================================================================
# --- 1. CONFIGURACIÓN DE PÁGINA & IDENTIDAD ---
# ==============================================================================
st.set_page_config(
    page_title="NEXUS | Commercial Board",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# --- 2. ESTILOS CSS PREMIUM (LIGHT THEME / CORPORATIVO) ---
# ==============================================================================
st.markdown("""
<style>
    /* IMPORTAR FUENTE */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    /* FONDO Y TIPOGRAFÍA */
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

    /* HEADER HERO */
    .nexus-hero {
        background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%);
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .nexus-badge {
        background-color: #E0F2FE;
        color: #0369A1;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 1px solid #BAE6FD;
    }

    /* KPI CARDS REFINADAS */
    .metric-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        transition: all 0.2s ease;
        border-left: 5px solid #3B82F6; /* Azul Corporativo */
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .metric-container:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }
    .metric-label { color: #64748B; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; }
    .metric-value { font-size: 2rem; font-weight: 800; color: #0F172A; margin: 8px 0; }
    .metric-delta { font-size: 0.85rem; font-weight: 600; display: flex; align-items: center; gap: 5px; }
    
    .delta-pos { color: #166534; background-color: #DCFCE7; padding: 2px 8px; border-radius: 6px; }
    .delta-neg { color: #991B1B; background-color: #FEE2E2; padding: 2px 8px; border-radius: 6px; }

    /* AI INSIGHT CARD */
    .ai-card {
        background: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-left: 5px solid #0EA5E9;
        border-radius: 10px;
        padding: 20px;
        margin-top: 15px;
    }
    .ai-title { color: #0369A1; font-weight: 800; display: flex; align-items: center; gap: 10px; font-size: 1rem; margin-bottom: 8px; }
    
    /* BOTONES */
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #0284C7 100%);
        color: white;
        border: none;
        font-weight: 600;
        padding: 0.6rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(37, 99, 235, 0.3);
    }
    
    h1, h2, h3 { color: #0F172A; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- 3. MOTOR DE DATOS (SIMULACIÓN DE VENTAS) ---
# ==============================================================================
@st.cache_data
def generar_datos_nexus():
    np.random.seed(123)
    
    # 4 ACTORES CLAVE
    vendedores = ["CARLOS (Senior)", "ANA (Junior)", "POS CENTRAL", "POS NORTE"]
    
    data = []
    fecha_inicio = datetime(2024, 1, 1)
    # Categorías ampliadas para el análisis adicional
    categorias = ["PINTURAS", "HERRAMIENTAS", "SOLVENTES", "IMPERMEABILIZANTES", "ELECTRICOS", "GRIFERIA"]
    
    perfiles = {
        "CARLOS (Senior)": {"ticket_mu": 1500000, "margen_base": 0.40, "frecuencia": 0.6},
        "ANA (Junior)":    {"ticket_mu": 800000,  "margen_base": 0.18, "frecuencia": 1.5},
        "POS CENTRAL":     {"ticket_mu": 250000,  "margen_base": 0.30, "frecuencia": 2.0},
        "POS NORTE":       {"ticket_mu": 450000,  "margen_base": 0.35, "frecuencia": 0.8},
    }

    for i in range(1500): 
        fecha = fecha_inicio + timedelta(days=np.random.randint(0, 365))
        vendedor = np.random.choice(vendedores)
        perfil = perfiles[vendedor]
        
        # Probabilidad de venta
        if np.random.random() > 0.4: 
            
            # Generar Venta
            base_venta = np.random.lognormal(np.log(perfil['ticket_mu']), 0.6)
            margen_real = np.random.normal(perfil['margen_base'], 0.05)
            if margen_real < 0.05: margen_real = 0.05 
            
            costo = base_venta * (1 - margen_real)
            utilidad = base_venta - costo
            
            cat = np.random.choice(categorias)
            
            data.append({
                'fecha': fecha,
                'mes': fecha.month,
                'mes_nombre': fecha.strftime('%B'),
                'vendedor': vendedor,
                'categoria': cat,
                'cliente': f"C-{np.random.randint(1000,5000)}",
                'venta': base_venta,
                'costo': costo,
                'utilidad': utilidad,
                'margen_pct': margen_real * 100
            })
            
    df = pd.DataFrame(data)
    
    # Metas Mensuales
    metas = {
        "CARLOS (Senior)": 80000000,
        "ANA (Junior)": 120000000, 
        "POS CENTRAL": 50000000,
        "POS NORTE": 30000000
    }
    
    df_metas = pd.DataFrame(list(metas.items()), columns=['vendedor', 'meta'])
    
    return df, df_metas

df, df_metas = generar_datos_nexus()

# ==============================================================================
# --- 4. GENERADOR DE EXCEL "CONSULTORÍA" ---
# ==============================================================================
def generar_excel_premium(df_filtrado, df_resumen):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    
    # --- FORMATOS ---
    f_header = workbook.add_format({'bold': True, 'bg_color': '#0F172A', 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
    f_currency = workbook.add_format({'num_format': '$ #,##0', 'border': 1})
    f_pct = workbook.add_format({'num_format': '0.0%', 'border': 1, 'align': 'center'})
    f_alert_bad = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    f_alert_good = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
    f_title = workbook.add_format({'bold': True, 'font_size': 14, 'font_color': '#1E293B'})

    # --- HOJA 1: TABLERO DE MANDO ---
    sheet_name = 'Tablero Estratégico'
    df_resumen.to_excel(writer, sheet_name=sheet_name, startrow=3, index=False)
    ws = writer.sheets[sheet_name]
    
    ws.merge_range('A1:F1', 'REPORTE DE RENDIMIENTO COMERCIAL - NEXUS SYSTEM', f_title)
    ws.write('A2', f"Generado: {datetime.now().strftime('%Y-%m-%d')}")
    
    ws.set_column('A:A', 25)
    ws.set_column('B:C', 18, f_currency)
    ws.set_column('D:E', 12, f_pct)
    
    ws.conditional_format('B4:B10', {'type': 'data_bar', 'bar_color': '#63C384'})
    ws.conditional_format('E4:E10', {'type': 'cell', 'criteria': '<', 'value': 0.20, 'format': f_alert_bad})
    ws.conditional_format('E4:E10', {'type': 'cell', 'criteria': '>', 'value': 0.30, 'format': f_alert_good})

    # --- HOJA 2: DATA ---
    df_filtrado.to_excel(writer, sheet_name='Data Auditada', index=False)
    writer.close()
    return output.getvalue()

# ==============================================================================
# --- 5. INTERFAZ DE USUARIO ---
# ==============================================================================

# Sidebar
with st.sidebar:
    st.markdown("### 🧭 Panel de Control")
    mes_sel = st.selectbox("Periodo de Análisis", df['mes_nombre'].unique(), index=len(df['mes_nombre'].unique())-1)
    
    st.divider()
    st.markdown("#### ⚙️ Configuración de Vista")
    st.checkbox("Mostrar Proyecciones", value=True)
    st.checkbox("Incluir Notas de Crédito", value=False)
    
    st.markdown("---")
    st.caption("🟢 Conexión ERP: Estable")
    st.page_link("Portafolio_Servicios.py", label="Volver al Inicio", icon="🏠")

# Filtrado
df_mes = df[df['mes_nombre'] == mes_sel].copy()

# --- HERO SECTION ---
st.markdown("""
<div class="nexus-hero">
    <div>
        <span class="nexus-badge">NEXUS COMMERCIAL v3.0</span>
        <h1 style="margin: 10px 0 5px 0; font-size: 2rem; font-weight: 900; color: #0F172A;">Centro de Inteligencia Comercial</h1>
        <p style="color: #64748B; margin: 0; max-width: 700px; font-size: 1rem;">
            Tablero unificado que cruza <strong>transacciones en tiempo real</strong> con rentabilidad real.
            Detecta patrones de venta, eficiencia de vendedores y oportunidades de margen ocultas.
        </p>
    </div>
    <div style="font-size: 3.5rem; opacity: 0.8;">📊</div>
</div>
""", unsafe_allow_html=True)

# --- KPIS MACRO ---
venta_total = df_mes['venta'].sum()
margen_global = (df_mes['utilidad'].sum() / venta_total * 100)
ticket_promedio = df_mes['venta'].mean()
trx_total = df_mes.shape[0]

c1, c2, c3, c4 = st.columns(4)

def kpi_card(col, label, value, sub_val, is_pos=True):
    style_class = "delta-pos" if is_pos else "delta-neg"
    icon = "▲" if is_pos else "▼"
    with col:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-delta">
                <span class="{style_class}">{icon} {sub_val}</span>
                <span style="color: #94A3B8; margin-left: 5px;">vs mes anterior</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

kpi_card(c1, "Venta Neta Cerrada", f"${venta_total/1e6:,.1f} M", "4.5%")
kpi_card(c2, "Margen Utilidad Real", f"{margen_global:.1f}%", "1.2%")
kpi_card(c3, "Ticket Promedio", f"${ticket_promedio/1e3:,.0f} K", "0.8%", False)
kpi_card(c4, "Transacciones", f"{trx_total}", "12%")

# --- CUERPO PRINCIPAL (TABS) ---
st.write("")
tab_performance, tab_trends, tab_dna, tab_export = st.tabs(["📊 Rendimiento & Matriz", "📈 Tendencias & Categorías", "🧬 ADN Comparativo", "📥 Reportes"])

# === TAB 1: MATRIZ DE EFICIENCIA ===
with tab_performance:
    col_main_chart, col_insight = st.columns([2, 1])
    
    # Data Agrupada
    df_group = df_mes.groupby('vendedor').agg(
        Venta=('venta', 'sum'),
        Margen_Pct=('margen_pct', 'mean'),
        Trx=('cliente', 'count')
    ).reset_index()
    
    df_group = df_group.merge(df_metas, on='vendedor')
    df_group['Cumplimiento'] = (df_group['Venta'] / df_group['meta']) * 100
    
    with col_main_chart:
        st.markdown("##### 🎯 Matriz de Eficiencia: Volumen vs. Rentabilidad")
        
        fig = px.scatter(df_group, x="Cumplimiento", y="Margen_Pct", 
                         size="Venta", color="vendedor",
                         hover_name="vendedor", text="vendedor",
                         size_max=50,
                         color_discrete_sequence=px.colors.qualitative.Prism) # Colores Profesionales
        
        # Líneas de referencia
        fig.add_hline(y=25, line_width=1, line_dash="dash", line_color="#94A3B8", annotation_text="Margen Mín (25%)")
        fig.add_vline(x=100, line_width=1, line_dash="dash", line_color="#94A3B8", annotation_text="Meta (100%)")
        
        fig.update_traces(textposition='top center', marker=dict(line=dict(width=1, color='White')))
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Cumplimiento de Presupuesto (%)", showgrid=True, gridcolor='#E2E8F0'),
            yaxis=dict(title="Margen de Rentabilidad Promedio (%)", showgrid=True, gridcolor='#E2E8F0'),
            showlegend=False,
            height=400,
            font=dict(family="Inter, sans-serif", color="#334155")
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_insight:
        st.markdown("##### 🧠 Diagnóstico IA")
        
        top_vendedor = df_group.sort_values('Venta', ascending=False).iloc[0]
        low_margin = df_group.sort_values('Margen_Pct').iloc[0]
        
        st.markdown(f"""
        <div class="ai-card">
            <div class="ai-title">🌟 LIDERAZGO DE MERCADO</div>
            <p style="font-size: 0.95rem; color: #475569; margin-top: 5px;">
                <strong>{top_vendedor['vendedor']}</strong> lidera con un cumplimiento del <strong>{top_vendedor['Cumplimiento']:.1f}%</strong>. 
                Su ticket promedio y frecuencia son el modelo a replicar este mes.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="ai-card" style="border-left-color: #EF4444; background-color: #FEF2F2; border-color: #FECACA;">
            <div class="ai-title" style="color: #991B1B;">⚠️ FUGA DE MARGEN</div>
            <p style="font-size: 0.95rem; color: #7F1D1D; margin-top: 5px;">
                <strong>{low_margin['vendedor']}</strong> tiene una rentabilidad del <strong>{low_margin['Margen_Pct']:.1f}%</strong> (Bajo promedio).
                <br><em>Acción:</em> Revisar política de descuentos manuales en POS.
            </p>
        </div>
        """, unsafe_allow_html=True)

# === TAB 2: TENDENCIAS & CATEGORÍAS (NUEVO RESUMEN IMPRESIONANTE) ===
with tab_trends:
    st.markdown("#### 📈 Análisis Temporal y de Producto")
    
    c_trend1, c_trend2 = st.columns([2, 1])
    
    with c_trend1:
        # GRÁFICO DE LINEAS (VENTAS DIARIAS)
        df_daily = df_mes.groupby('fecha').agg({'venta': 'sum'}).reset_index()
        fig_line = px.line(df_daily, x='fecha', y='venta', title="Evolución Diaria de Ventas", markers=True)
        fig_line.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title=None,
            yaxis_title="Venta ($)",
            height=350,
            line_dict=dict(color='#3B82F6'),
            font=dict(family="Inter, sans-serif", color="#334155")
        )
        fig_line.update_traces(line_color='#2563EB', line_width=3)
        st.plotly_chart(fig_line, use_container_width=True)
        
    with c_trend2:
        # GRÁFICO DE DONA (CATEGORÍAS)
        df_cat = df_mes.groupby('categoria').agg({'utilidad': 'sum'}).reset_index()
        fig_pie = px.donut(df_cat, values='utilidad', names='categoria', title="Rentabilidad por Categoría", hole=0.6)
        fig_pie.update_layout(
            height=350, 
            showlegend=False,
            font=dict(family="Inter, sans-serif", color="#334155")
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

# === TAB 3: ADN COMPARATIVO ===
with tab_dna:
    st.markdown("#### 🧬 Comparativa 1 a 1: Fortalezas y Debilidades")
    
    c_sel1, c_sel2 = st.columns(2)
    v1 = c_sel1.selectbox("Agente A", df_group['vendedor'].unique(), index=0)
    v2 = c_sel2.selectbox("Agente B", df_group['vendedor'].unique(), index=1)
    
    # Radar Chart Logic
    def get_radar_data(v_name):
        row = df_group[df_group['vendedor'] == v_name].iloc[0]
        max_vals = df_group[['Venta', 'Margen_Pct', 'Trx']].max()
        return [
            row['Venta'] / max_vals['Venta'],
            row['Margen_Pct'] / max_vals['Margen_Pct'],
            row['Trx'] / max_vals['Trx'],
            row['Venta'] / max_vals['Venta'] 
        ]

    categories = ['Volumen', 'Rentabilidad', 'Velocidad (Trx)', 'Volumen']

    col_radar, col_table = st.columns([1, 1])
    
    with col_radar:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=get_radar_data(v1), theta=categories, fill='toself', name=v1, line_color='#3B82F6'))
        fig_radar.add_trace(go.Scatterpolar(r=get_radar_data(v2), theta=categories, fill='toself', name=v2, line_color='#10B981'))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1], showticklabels=False), bgcolor='rgba(0,0,0,0)'),
            showlegend=True,
            height=350,
            font=dict(family="Inter, sans-serif", color="#334155"),
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col_table:
        st.markdown("##### 📋 Diferenciales Clave")
        comp_df = df_group[df_group['vendedor'].isin([v1, v2])].set_index('vendedor')
        comp_df = comp_df[['Venta', 'Margen_Pct', 'Cumplimiento']]
        comp_df['Venta'] = comp_df['Venta'].map('${:,.0f}'.format)
        comp_df['Margen_Pct'] = comp_df['Margen_Pct'].map('{:.1f}%'.format)
        comp_df['Cumplimiento'] = comp_df['Cumplimiento'].map('{:.1f}%'.format)
        
        st.table(comp_df.T)
        
        if df_group[df_group['vendedor']==v1]['Margen_Pct'].values[0] > df_group[df_group['vendedor']==v2]['Margen_Pct'].values[0]:
            st.success(f"💡 **{v1}** protege mejor el precio. Ideal para cerrar clientes difíciles.")
        else:
            st.info(f"💡 **{v2}** es más flexible en precio. Ideal para mover volumen rápido.")

# === TAB 4: REPORTES ===
with tab_export:
    st.markdown("#### 📥 Centro de Informes Oficiales")
    st.markdown("Genera el reporte para la Junta Directiva con formato Excel profesional (Semáforos, Barras de Datos).")
    
    excel_summary = df_group[['vendedor', 'Venta', 'meta', 'Cumplimiento', 'Margen_Pct']].copy()
    excel_summary.columns = ['Vendedor', 'Venta Real', 'Presupuesto', '% Cumplimiento', 'Margen %']
    
    excel_file = generar_excel_premium(df_mes[['fecha', 'cliente', 'vendedor', 'categoria', 'venta', 'margen_pct']], excel_summary)
    
    col_d1, col_d2 = st.columns([1,2])
    with col_d1:
        st.download_button(
            label="📄 DESCARGAR REPORTE .XLSX",
            data=excel_file,
            file_name=f"NEXUS_Reporte_Gerencial_{mes_sel}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )

st.divider()
st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 0.85rem;'>NEXUS INTELLIGENCE SYSTEM © 2025 | Powered by Datovate AI Core</div>", unsafe_allow_html=True)
