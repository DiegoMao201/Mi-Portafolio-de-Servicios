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
    page_title="NEXUS COMMAND CENTER | Board Edition",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# --- 2. ESTILOS CSS "GLASSMORPHISM" & FUTURISTA ---
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap');

    .stApp {
        background-color: #090b10; /* Fondo Ultra Dark */
        color: #E0E0E0;
        font-family: 'Outfit', sans-serif;
    }

    /* HERO SECTION NEXUS */
    .nexus-hero {
        background: linear-gradient(90deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .nexus-badge {
        background-color: #00D4FF;
        color: #000;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* KPI CARDS REFINADAS */
    .metric-container {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.3s;
    }
    .metric-container:hover {
        transform: translateY(-5px);
        border-color: #00D4FF;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.1);
    }
    .metric-label { color: #94A3B8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }
    .metric-value { font-size: 2.2rem; font-weight: 700; color: #F8FAFC; margin: 8px 0; }
    .metric-delta { font-size: 0.9rem; display: flex; align-items: center; gap: 5px; }
    .delta-pos { color: #4ADE80; }
    .delta-neg { color: #F87171; }

    /* AI INSIGHT CARD */
    .ai-card {
        background: linear-gradient(145deg, #1a1f2e, #11141d);
        border-left: 4px solid #8B5CF6;
        border-radius: 8px;
        padding: 20px;
        margin-top: 20px;
    }
    .ai-title { color: #A78BFA; font-weight: bold; display: flex; align-items: center; gap: 10px; font-size: 1.1rem; }
    
    /* BOTONES */
    div.stButton > button {
        background: linear-gradient(45deg, #2563EB, #00D4FF);
        color: white;
        border: none;
        font-weight: 600;
        padding: 0.5rem 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- 3. MOTOR DE DATOS (SIMULACIÓN ALTA CALIDAD - 4 ACTORES) ---
# ==============================================================================
@st.cache_data
def generar_datos_nexus():
    np.random.seed(123)
    
    # SOLO 4 ACTORES CLAVE PARA CLARIDAD
    # 1. Carlos (Senior): Vende poco volumen, pero márgenes altísimos (experto técnico).
    # 2. Ana (Junior): Vende muchísimo volumen, pero quema precio (bajo margen).
    # 3. Mostrador Central: Equilibrio, atiende público general.
    # 4. Mostrador Norte: Nuevo punto, tráfico bajo pero ticket alto.
    
    vendedores = ["CARLOS (Senior)", "ANA (Junior)", "POS CENTRAL", "POS NORTE"]
    
    data = []
    fecha_inicio = datetime(2024, 1, 1)
    categorias = ["PINTURAS", "HERRAMIENTAS", "SOLVENTES", "IMPERMEABILIZANTES"]
    
    perfiles = {
        "CARLOS (Senior)": {"ticket_mu": 1500000, "margen_base": 0.40, "frecuencia": 0.6},
        "ANA (Junior)":    {"ticket_mu": 800000,  "margen_base": 0.18, "frecuencia": 1.5},
        "POS CENTRAL":     {"ticket_mu": 250000,  "margen_base": 0.30, "frecuencia": 2.0},
        "POS NORTE":       {"ticket_mu": 450000,  "margen_base": 0.35, "frecuencia": 0.8},
    }

    for i in range(1200): # Menos datos, más calidad
        fecha = fecha_inicio + timedelta(days=np.random.randint(0, 300))
        vendedor = np.random.choice(vendedores)
        perfil = perfiles[vendedor]
        
        # Probabilidad de venta basada en frecuencia
        if np.random.random() > 0.5: 
            
            # Generar Venta
            base_venta = np.random.lognormal(np.log(perfil['ticket_mu']), 0.6)
            margen_real = np.random.normal(perfil['margen_base'], 0.05)
            if margen_real < 0.05: margen_real = 0.05 # Cap mínimo
            
            costo = base_venta * (1 - margen_real)
            utilidad = base_venta - costo
            
            cat = np.random.choice(categorias)
            
            # Simulación de Inventario (Nexus Logic)
            # Si se vende mucho, el inventario baja.
            stock_impact = np.random.randint(1, 10)
            
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
                'margen_pct': margen_real * 100,
                'unidades': stock_impact
            })
            
    df = pd.DataFrame(data)
    
    # Metas Mensuales
    metas = {
        "CARLOS (Senior)": 80000000,
        "ANA (Junior)": 120000000, # Meta más alta por volumen
        "POS CENTRAL": 50000000,
        "POS NORTE": 30000000
    }
    
    df_metas = pd.DataFrame(list(metas.items()), columns=['vendedor', 'meta'])
    
    return df, df_metas

df, df_metas = generar_datos_nexus()

# ==============================================================================
# --- 4. GENERADOR DE EXCEL "CONSULTORÍA" (HIGH END) ---
# ==============================================================================
def generar_excel_premium(df_filtrado, df_resumen):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    
    # --- FORMATOS ---
    f_header = workbook.add_format({'bold': True, 'bg_color': '#0F172A', 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
    f_currency = workbook.add_format({'num_format': '$ #,##0', 'border': 1})
    f_pct = workbook.add_format({'num_format': '0.0%', 'border': 1, 'align': 'center'})
    f_text = workbook.add_format({'border': 1})
    f_alert_bad = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    f_alert_good = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
    f_title = workbook.add_format({'bold': True, 'font_size': 14, 'font_color': '#1E293B'})

    # --- HOJA 1: TABLERO DE MANDO ---
    sheet_name = 'Tablero Estratégico'
    df_resumen.to_excel(writer, sheet_name=sheet_name, startrow=3, index=False)
    ws = writer.sheets[sheet_name]
    
    # Títulos y Logos (Simulado)
    ws.merge_range('A1:F1', 'REPORTE DE RENDIMIENTO COMERCIAL - NEXUS SYSTEM', f_title)
    ws.write('A2', f"Generado: {datetime.now().strftime('%Y-%m-%d')}")
    
    # Aplicar formatos a columnas
    ws.set_column('A:A', 25) # Vendedor
    ws.set_column('B:C', 18, f_currency) # Ventas
    ws.set_column('D:E', 12, f_pct) # Margen
    
    # Formato Condicional (Barras de Datos para Ventas)
    ws.conditional_format('B4:B10', {'type': 'data_bar', 'bar_color': '#63C384'})
    
    # Formato Condicional (Semáforo para Margen)
    ws.conditional_format('E4:E10', {'type': 'cell', 'criteria': '<', 'value': 0.20, 'format': f_alert_bad})
    ws.conditional_format('E4:E10', {'type': 'cell', 'criteria': '>', 'value': 0.30, 'format': f_alert_good})

    # --- HOJA 2: DATA TRANSACCIONAL ---
    df_filtrado.to_excel(writer, sheet_name='Data Auditada', index=False)
    ws2 = writer.sheets['Data Auditada']
    ws2.set_column('A:Z', 15)

    writer.close()
    return output.getvalue()

# ==============================================================================
# --- 5. INTERFAZ DE USUARIO & LÓGICA ---
# ==============================================================================

# Sidebar
with st.sidebar:
    st.header("🎛️ Panel de Control")
    mes_sel = st.selectbox("Periodo de Análisis", df['mes_nombre'].unique(), index=len(df['mes_nombre'].unique())-1)
    st.divider()
    st.markdown("### 🤖 Nexus Status")
    st.caption("🟢 Conexión ERP: Estable")
    st.caption("🟢 Módulo Inventario: Sincronizado")
    st.caption("🟢 Motor IA: Activo")

# Filtrado
df_mes = df[df['mes_nombre'] == mes_sel].copy()

# --- HERO SECTION: EL VALOR DE NEXUS ---
st.markdown("""
<div class="nexus-hero">
    <div>
        <span class="nexus-badge">NEXUS OS v3.0</span>
        <h1 style="margin: 10px 0 5px 0; font-size: 1.8rem; color: white;">Centro de Inteligencia Comercial Unificado</h1>
        <p style="color: #94A3B8; margin: 0; max-width: 600px;">
            Este no es un simple reporte de ventas. NEXUS <strong>cruza en tiempo real</strong> sus transacciones comerciales 
            con los niveles de inventario y rentabilidad para detectar fugas de dinero invisibles al ojo humano.
        </p>
    </div>
    <div style="text-align: right; display: none; @media (min-width: 1000px) { display: block; }">
        <div style="font-size: 3rem;">🧠</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- KPIS MACRO ---
venta_total = df_mes['venta'].sum()
margen_global = (df_mes['utilidad'].sum() / venta_total * 100)
ticket_promedio = df_mes['venta'].mean()
trx_total = df_mes.shape[0]

c1, c2, c3, c4 = st.columns(4)

def kpi_card(col, label, value, sub_val, is_pos=True):
    color = "delta-pos" if is_pos else "delta-neg"
    icon = "▲" if is_pos else "▼"
    col.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-delta">
            <span class="{color}">{icon} {sub_val}</span> vs mes anterior
        </div>
    </div>
    """, unsafe_allow_html=True)

kpi_card(c1, "Venta Neta Cerrada", f"${venta_total/1e6:,.1f} M", "4.5%")
kpi_card(c2, "Margen de Utilidad Real", f"{margen_global:.1f}%", "1.2%")
kpi_card(c3, "Ticket Promedio", f"${ticket_promedio/1e3:,.0f} K", "0.8%", False) # False para probar rojo
kpi_card(c4, "Transacciones Totales", f"{trx_total}", "12%")

# --- CUERPO PRINCIPAL ---

tab_performance, tab_dna, tab_export = st.tabs(["📊 Rendimiento Estratégico", "🧬 ADN del Equipo (Comparativa)", "📥 Reportes Gerenciales"])

# === TAB 1: RENDIMIENTO ESTRATÉGICO ===
with tab_performance:
    col_main_chart, col_insight = st.columns([2, 1])
    
    # PREPARAR DATA PARA SCATTER (Cuadrante Mágico)
    df_group = df_mes.groupby('vendedor').agg(
        Venta=('venta', 'sum'),
        Margen_Pct=('margen_pct', 'mean'),
        Trx=('cliente', 'count')
    ).reset_index()
    
    df_group = df_group.merge(df_metas, on='vendedor')
    df_group['Cumplimiento'] = (df_group['Venta'] / df_group['meta']) * 100
    
    with col_main_chart:
        st.subheader("Matriz de Eficiencia: Volumen vs. Rentabilidad")
        
        fig = px.scatter(df_group, x="Cumplimiento", y="Margen_Pct", 
                         size="Venta", color="vendedor",
                         hover_name="vendedor",
                         text="vendedor",
                         size_max=60,
                         color_discrete_sequence=["#00D4FF", "#F43F5E", "#A78BFA", "#34D399"])
        
        # Líneas de referencia (Cuadrantes)
        fig.add_hline(y=25, line_width=1, line_dash="dash", line_color="gray", annotation_text="Margen Mínimo Saludable (25%)")
        fig.add_vline(x=100, line_width=1, line_dash="dash", line_color="gray", annotation_text="Meta (100%)")
        
        fig.update_traces(textposition='top center', marker=dict(line=dict(width=2, color='White')))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,0.03)',
            font=dict(color='#E0E0E0'),
            showlegend=False,
            height=450,
            xaxis_title="Cumplimiento de Presupuesto (%)",
            yaxis_title="Margen de Rentabilidad Promedio (%)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_insight:
        st.subheader("🧠 Diagnóstico de IA Nexus")
        
        # Lógica de recomendación real
        top_vendedor = df_group.sort_values('Venta', ascending=False).iloc[0]
        low_margin = df_group.sort_values('Margen_Pct').iloc[0]
        
        st.markdown(f"""
        <div class="ai-card">
            <div class="ai-title">🔎 ANÁLISIS DE LIDERAZGO</div>
            <p style="font-size: 0.9rem; margin-top: 10px;">
                <strong>{top_vendedor['vendedor']}</strong> domina la cuota de mercado con un cumplimiento del {top_vendedor['Cumplimiento']:.1f}%. 
                Nexus sugiere clonar su estrategia de cierre para el resto del equipo.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="ai-card" style="border-left-color: #F43F5E;">
            <div class="ai-title" style="color: #F43F5E;">⚠️ ALERTA DE FUGA DE MARGEN</div>
            <p style="font-size: 0.9rem; margin-top: 10px;">
                <strong>{low_margin['vendedor']}</strong> está sacrificando demasiada rentabilidad ({low_margin['Margen_Pct']:.1f}%) para lograr ventas. 
                <br><br>
                <em>Acción sugerida:</em> Bloquear descuentos superiores al 10% en el sistema POS para este usuario.
            </p>
        </div>
        """, unsafe_allow_html=True)

# === TAB 2: ADN DEL EQUIPO (COMPARATIVA) ===
with tab_dna:
    st.subheader("Comparativa de Habilidades: Vendedor vs. Vendedor")
    st.caption("Compare visualmente las fortalezas de dos miembros para equilibrar el equipo.")
    
    c_sel1, c_sel2 = st.columns(2)
    v1 = c_sel1.selectbox("Seleccionar Agente A", df_group['vendedor'].unique(), index=0)
    v2 = c_sel2.selectbox("Seleccionar Agente B", df_group['vendedor'].unique(), index=1)
    
    # Crear datos normalizados para Radar Chart
    # Ejes: Volumen, Margen, Ticket Promedio, Frecuencia (Trx)
    def get_radar_data(v_name):
        row = df_group[df_group['vendedor'] == v_name].iloc[0]
        # Normalizamos (min-max scaling simple para el ejemplo)
        max_vals = df_group[['Venta', 'Margen_Pct', 'Trx']].max()
        return [
            row['Venta'] / max_vals['Venta'],
            row['Margen_Pct'] / max_vals['Margen_Pct'],
            row['Trx'] / max_vals['Trx'],
            row['Venta'] / max_vals['Venta'] # Repetimos para cerrar o usar otro KPI
        ]

    categories = ['Capacidad de Volumen', 'Defensa del Precio (Margen)', 'Velocidad (Trx)', 'Impacto en Meta']

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=get_radar_data(v1), theta=categories, fill='toself', name=v1, line_color='#00D4FF'))
    fig_radar.add_trace(go.Scatterpolar(r=get_radar_data(v2), theta=categories, fill='toself', name=v2, line_color='#F43F5E'))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1], showticklabels=False, linecolor='#334155'), bgcolor='rgba(0,0,0,0)'),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=True,
        height=400
    )
    
    col_radar, col_table = st.columns([1, 1])
    col_radar.plotly_chart(fig_radar, use_container_width=True)
    
    with col_table:
        st.markdown("#### 📋 Tabla de Diferenciales")
        # Tabla comparativa directa
        comp_df = df_group[df_group['vendedor'].isin([v1, v2])].set_index('vendedor')
        comp_df = comp_df[['Venta', 'Margen_Pct', 'Cumplimiento']]
        comp_df['Venta'] = comp_df['Venta'].map('${:,.0f}'.format)
        comp_df['Margen_Pct'] = comp_df['Margen_Pct'].map('{:.1f}%'.format)
        comp_df['Cumplimiento'] = comp_df['Cumplimiento'].map('{:.1f}%'.format)
        
        st.table(comp_df.T)
        
        if df_group[df_group['vendedor']==v1]['Margen_Pct'].values[0] > df_group[df_group['vendedor']==v2]['Margen_Pct'].values[0]:
            st.success(f"💡 Insight: **{v1}** es más rentable. Pídale que capacite a {v2} en negociación.")
        else:
            st.info(f"💡 Insight: **{v2}** tiene mejores precios. Analice si está dando demasiados descuentos.")

# === TAB 3: EXPORTACIÓN GERENCIAL ===
with tab_export:
    st.markdown("### 📥 Centro de Descargas (Junta Directiva)")
    st.markdown("Este módulo genera el reporte oficial con formato condicional nativo de Excel.")
    
    # Preparar DataFrame final para Excel
    excel_summary = df_group[['vendedor', 'Venta', 'meta', 'Cumplimiento', 'Margen_Pct']].copy()
    excel_summary.columns = ['Vendedor/Punto', 'Venta Real', 'Presupuesto', '% Cumplimiento', 'Margen Real %']
    
    # Botón Mágico
    excel_file = generar_excel_premium(df_mes[['fecha', 'cliente', 'vendedor', 'categoria', 'venta', 'margen_pct']], excel_summary)
    
    col_d1, col_d2 = st.columns([1,2])
    with col_d1:
        st.download_button(
            label="📄 DESCARGAR INFORME AUDITADO (.XLSX)",
            data=excel_file,
            file_name=f"NEXUS_Reporte_Gerencial_{mes_sel}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Genera un Excel con formato condicional avanzado listo para presentar."
        )
    with col_d2:
        st.info("El archivo descargado incluye semáforos de rentabilidad y barras de datos automáticas.")

# Footer
st.divider()
st.markdown("<div style='text-align: center; color: #475569; font-size: 0.8rem;'>NEXUS INTELLIGENCE SYSTEM © 2025 | Powered by Datovate AI Core</div>", unsafe_allow_html=True)
