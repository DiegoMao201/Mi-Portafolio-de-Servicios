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
# Configuración inicial de la página
st.set_page_config(
    page_title="NEXUS | Commercial Board",
    page_icon="📈",
    layout="wide", # Usa el ancho completo de la pantalla
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# --- 2. ESTILOS CSS PREMIUM (LIGHT THEME / CORPORATIVO) ---
# ==============================================================================
# Aplicación de estilos CSS para un tema corporativo limpio (Slate y Azul)
st.markdown("""
<style>
    /* IMPORTAR FUENTE CORPORATIVA */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    /* FONDO Y TIPOGRAFÍA BASE */
    .stApp {
        background-color: #F8FAFC; /* Slate 50: Fondo muy claro */
        color: #334155; /* Slate 700: Color de texto base */
        font-family: 'Inter', sans-serif;
    }
    
    /* SIDEBAR GENERAL */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    /* HEADER HERO: Diseño de bienvenida al dashboard */
    .nexus-hero {
        background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%);
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 30px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); /* Sombra sutil */
    }
    .nexus-badge {
        background-color: #E0F2FE; /* Azul claro */
        color: #0369A1; /* Azul oscuro */
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 1px solid #BAE6FD;
    }

    /* KPI CARDS REFINADAS: Estilo para métricas clave */
    .metric-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        transition: all 0.2s ease;
        border-left: 5px solid #3B82F6; /* Azul Corporativo para acento */
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

    /* AI INSIGHT CARD: Estilo para el diagnóstico asistido */
    .ai-card {
        background: #F0F9FF;
        border: 1px solid #BAE6FD;
        border-left: 5px solid #0EA5E9; /* Borde izquierdo de acento Azul Cielo */
        border-radius: 10px;
        padding: 20px;
        margin-top: 15px;
    }
    .ai-title { color: #0369A1; font-weight: 800; display: flex; align-items: center; gap: 10px; font-size: 1rem; margin-bottom: 8px; }
    
    /* BOTONES PRIMARIOS: Estilo de degradado */
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #0284C7 100%); /* Degradado de Azul medio a cian */
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
    
    h1, h2, h3 { color: #0F172A; } /* Títulos oscuros y fuertes */
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- 3. MOTOR DE DATOS (SIMULACIÓN DE VENTAS) ---
# ==============================================================================
@st.cache_data # Caching para evitar recargar datos en cada interacción
def generar_datos_nexus():
    np.random.seed(123) # Para resultados reproducibles
    
    # 4 ACTORES CLAVE (Vendedores y Puntos de Venta)
    vendedores = ["CARLOS (Senior)", "ANA (Junior)", "POS CENTRAL", "POS NORTE"]
    
    data = []
    fecha_inicio = datetime(2024, 1, 1)
    # Categorías ampliadas para un análisis de producto más rico
    categorias = ["PINTURAS", "HERRAMIENTAS", "SOLVENTES", "IMPERMEABILIZANTES", "ELECTRICOS", "GRIFERIA"]
    
    # Perfiles de comportamiento de venta
    perfiles = {
        "CARLOS (Senior)": {"ticket_mu": 1500000, "margen_base": 0.40, "frecuencia": 0.6}, # Alto ticket, alto margen
        "ANA (Junior)":    {"ticket_mu": 800000,  "margen_base": 0.18, "frecuencia": 1.5}, # Ticket medio, bajo margen
        "POS CENTRAL":     {"ticket_mu": 250000,  "margen_base": 0.30, "frecuencia": 2.0}, # Bajo ticket, alta frecuencia
        "POS NORTE":       {"ticket_mu": 450000,  "margen_base": 0.35, "frecuencia": 0.8}, # Ticket medio, buen margen
    }

    # Generación de 1500 transacciones simuladas
    for i in range(1500): 
        fecha = fecha_inicio + timedelta(days=np.random.randint(0, 365))
        vendedor = np.random.choice(vendedores)
        perfil = perfiles[vendedor]
        
        # Simulación de probabilidad de venta (para tener días sin venta)
        if np.random.random() > 0.4: 
            
            # Generar Venta (Usando lognormal para simular colas de precios)
            base_venta = np.random.lognormal(np.log(perfil['ticket_mu']), 0.6)
            margen_real = np.random.normal(perfil['margen_base'], 0.05) # Margen con volatilidad
            if margen_real < 0.05: margen_real = 0.05 # Límite inferior de margen
            
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
                'margen_pct': margen_real * 100 # Guardado como porcentaje para fácil visualización
            })
            
    df = pd.DataFrame(data)
    
    # Definición de Metas Mensuales
    metas = {
        "CARLOS (Senior)": 80000000,
        "ANA (Junior)": 120000000, 
        "POS CENTRAL": 50000000,
        "POS NORTE": 30000000
    }
    
    df_metas = pd.DataFrame(list(metas.items()), columns=['vendedor', 'meta'])
    
    return df, df_metas

# Carga de datos
df, df_metas = generar_datos_nexus()

# ==============================================================================
# --- 4. GENERADOR DE EXCEL "CONSULTORÍA" (ROBUSTO) ---
# ==============================================================================
def generar_excel_premium(df_filtrado, df_resumen):
    """
    Genera un archivo Excel con dos hojas: un tablero estratégico formateado
    y la data cruda filtrada. Incluye formatos condicionales.
    """
    output = io.BytesIO()
    # Usamos xlsxwriter como engine para acceder a las funcionalidades avanzadas
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    
    # --- DEFINICIÓN DE FORMATOS ---
    f_header = workbook.add_format({'bold': True, 'bg_color': '#0F172A', 'font_color': 'white', 'border': 1, 'align': 'center', 'valign': 'vcenter'})
    f_currency = workbook.add_format({'num_format': '$ #,##0', 'border': 1})
    f_pct = workbook.add_format({'num_format': '0.0%', 'border': 1, 'align': 'center'})
    f_alert_bad = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006', 'border': 1}) # Rojo claro para bajo margen
    f_alert_good = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100', 'border': 1}) # Verde claro para buen margen
    f_title = workbook.add_format({'bold': True, 'font_size': 16, 'font_color': '#1E293B', 'align': 'center'})

    # --- HOJA 1: TABLERO DE MANDO (Resumen Ejecutivo) ---
    sheet_name = 'Tablero Estratégico'
    
    # Escribir el resumen de desempeño en la hoja (iniciando en la fila 3 para dejar espacio)
    df_resumen.to_excel(writer, sheet_name=sheet_name, startrow=3, header=False, index=False)
    ws = writer.sheets[sheet_name]
    
    # Escribir los encabezados de columna con formato
    for col_num, value in enumerate(df_resumen.columns.values):
        ws.write(3, col_num, value, f_header)
        
    # Título y metadatos
    ws.merge_range('A1:E1', 'REPORTE DE RENDIMIENTO COMERCIAL - NEXUS SYSTEM', f_title)
    ws.write('A2', f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Aplicar formatos a las columnas
    num_filas = len(df_resumen)
    ws.set_column('A:A', 25) # Vendedor
    ws.set_column('B:C', 18, f_currency) # Venta y Presupuesto
    ws.set_column('D:E', 15, f_pct) # Porcentajes

    # Formato Condicional (Rendimiento)
    # Barra de datos para el cumplimiento de venta (columna D)
    ws.conditional_format(4, 3, 3 + num_filas, 3, {'type': 'data_bar', 'bar_color': '#3B82F6'})

    # Formato Condicional (Margen)
    # Alerta si el margen es bajo (<20%) o bueno (>30%) (columna E)
    ws.conditional_format(4, 4, 3 + num_filas, 4, {'type': 'cell', 'criteria': '<', 'value': 0.20, 'format': f_alert_bad})
    ws.conditional_format(4, 4, 3 + num_filas, 4, {'type': 'cell', 'criteria': '>', 'value': 0.30, 'format': f_alert_good})

    # --- HOJA 2: DATA (Data Cruda Filtrada) ---
    df_filtrado.to_excel(writer, sheet_name='Data Auditada', index=False)
    ws_data = writer.sheets['Data Auditada']
    
    # Formatear la tabla de datos crudos
    ws_data.set_column('A:A', 15) # Fecha
    ws_data.set_column('E:E', 15, workbook.add_format({'num_format': '$ #,##0'})) # Venta
    ws_data.set_column('F:F', 15, workbook.add_format({'num_format': '0.0%'})) # Margen %
    
    # Escribir encabezados con formato
    for col_num, value in enumerate(df_filtrado.columns.values):
        ws_data.write(0, col_num, value.replace('_', ' ').title(), f_header)
    
    writer.close()
    return output.getvalue()

# ==============================================================================
# --- 5. INTERFAZ DE USUARIO (Funciones de Componentes) ---
# ==============================================================================

# Definición de la función para las tarjetas KPI
def kpi_card(col, label, value, sub_val, is_pos=True):
    """Genera una tarjeta KPI con estilos CSS."""
    style_class = "delta-pos" if is_pos else "delta-neg"
    icon = "▲" if is_pos else "▼"
    with col:
        # Uso de st.markdown con HTML para aplicar el estilo CSS
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

# --- SIDEBAR (PANEL DE CONTROL) ---
with st.sidebar:
    st.markdown("### 🧭 Panel de Control")
    # Selector de mes de análisis. El índice se establece en el último mes disponible.
    mes_sel = st.selectbox("Periodo de Análisis", df['mes_nombre'].unique(), index=len(df['mes_nombre'].unique())-1)
    
    st.divider()
    st.markdown("#### ⚙️ Configuración de Vista")
    # Checkboxes para configuraciones de visualización
    st.checkbox("Mostrar Proyecciones", value=True)
    st.checkbox("Incluir Notas de Crédito", value=False)
    
    st.markdown("---")
    st.caption("🟢 Conexión ERP: Estable")
    # Enlace de navegación
    st.page_link("Portafolio_Servicios.py", label="Volver al Inicio", icon="🏠")

# --- FILTRADO DE DATOS PRINCIPAL ---
df_mes = df[df['mes_nombre'] == mes_sel].copy()

# --- HERO SECTION (HEADER) ---
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

# --- KPIS MACRO (Calculados y mostrados con la función kpi_card) ---
venta_total = df_mes['venta'].sum()
margen_global = (df_mes['utilidad'].sum() / venta_total * 100) if venta_total > 0 else 0
ticket_promedio = df_mes['venta'].mean()
trx_total = df_mes.shape[0]

c1, c2, c3, c4 = st.columns(4)

# Presentación de KPIs Macro
kpi_card(c1, "Venta Neta Cerrada", f"${venta_total/1e6:,.1f} M", "4.5%")
kpi_card(c2, "Margen Utilidad Real", f"{margen_global:.1f}%", "1.2%")
kpi_card(c3, "Ticket Promedio", f"${ticket_promedio/1e3:,.0f} K", "0.8%", False) # Ejemplo de delta negativo
kpi_card(c4, "Transacciones", f"{trx_total}", "12%")

# --- CUERPO PRINCIPAL (TABS) ---
st.write("")
tab_performance, tab_trends, tab_dna, tab_export = st.tabs(["📊 Rendimiento & Matriz", "📈 Tendencias & Categorías", "🧬 ADN Comparativo", "📥 Reportes"])

# === TAB 1: MATRIZ DE EFICIENCIA (Scatter Plot y Diagnóstico AI) ===
with tab_performance:
    st.markdown("## 🥇 Rendimiento de Agentes")
    col_main_chart, col_insight = st.columns([2, 1])
    
    # 1. Agrupación de Datos por Vendedor
    df_group = df_mes.groupby('vendedor').agg(
        Venta=('venta', 'sum'),
        Margen_Pct=('margen_pct', 'mean'),
        Trx=('cliente', 'count')
    ).reset_index()
    
    # 2. Cruce con Metas
    df_group = df_group.merge(df_metas, on='vendedor', how='left')
    df_group['Cumplimiento'] = (df_group['Venta'] / df_group['meta']) * 100
    
    # --- GRÁFICO DE BURBUJAS (Matriz de Eficiencia) ---
    with col_main_chart:
        st.markdown("##### 🎯 Matriz de Eficiencia: Volumen vs. Rentabilidad")
        
        # Creación del Scatter Plot con Plotly Express
        fig = px.scatter(df_group, x="Cumplimiento", y="Margen_Pct", 
                         size="Venta", color="vendedor", # El tamaño de la burbuja es la Venta
                         hover_name="vendedor", text="vendedor",
                         size_max=50,
                         color_discrete_sequence=px.colors.qualitative.Prism) # Esquema de colores profesional
        
        # Líneas de referencia para fácil interpretación del cuadrante
        fig.add_hline(y=df_group['Margen_Pct'].mean(), line_width=1, line_dash="dot", line_color="#F97316", annotation_text=f"Margen Prom. ({df_group['Margen_Pct'].mean():.1f}%)")
        fig.add_vline(x=100, line_width=1, line_dash="dash", line_color="#94A3B8", annotation_text="Meta (100%)")
        
        # Ajustes de visualización del gráfico
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

    # --- DIAGNÓSTICO AI (Basado en Reglas Simples) ---
    with col_insight:
        st.markdown("##### 🧠 Diagnóstico IA")
        
        top_vendedor = df_group.sort_values('Venta', ascending=False).iloc[0]
        low_margin = df_group.sort_values('Margen_Pct').iloc[0]
        
        # Insight de Liderazgo (Card Azul)
        st.markdown(f"""
        <div class="ai-card">
            <div class="ai-title">🌟 LIDERAZGO DE MERCADO</div>
            <p style="font-size: 0.95rem; color: #475569; margin-top: 5px;">
                <strong>{top_vendedor['vendedor']}</strong> lidera con un cumplimiento del <strong>{top_vendedor['Cumplimiento']:.1f}%</strong>. 
                Su capacidad de venta es alta, enfocarse en mantener el margen.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Insight de Alerta (Card Rojo)
        st.markdown(f"""
        <div class="ai-card" style="border-left-color: #EF4444; background-color: #FEF2F2; border-color: #FECACA;">
            <div class="ai-title" style="color: #991B1B;">⚠️ FUGA DE MARGEN</div>
            <p style="font-size: 0.95rem; color: #7F1D1D; margin-top: 5px;">
                <strong>{low_margin['vendedor']}</strong> tiene una rentabilidad del <strong>{low_margin['Margen_Pct']:.1f}%</strong> (Bajo promedio).
                <br><em>Acción:</em> Revisar política de descuentos manuales y precios de costo.
            </p>
        </div>
        """, unsafe_allow_html=True)

# === TAB 2: TENDENCIAS & CATEGORÍAS (Solución del error y mejora visual) ===
with tab_trends:
    st.markdown("## 📊 Análisis Temporal y de Producto")
    
    c_trend1, c_trend2 = st.columns([2, 1])
    
    with c_trend1:
        # GRÁFICO DE LINEAS (VENTAS DIARIAS)
        df_daily = df_mes.groupby('fecha').agg({'venta': 'sum'}).reset_index()
        st.markdown("##### 📈 Evolución Diaria de Ventas")
        
        fig_line = px.line(df_daily, x='fecha', y='venta', markers=True)
        
        # Configuración del gráfico de líneas
        fig_line.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title=None,
            yaxis_title="Venta ($)",
            height=350,
            font=dict(family="Inter, sans-serif", color="#334155"),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        # Aplicación de estilo a la línea - NO HAY ERROR AQUÍ
        fig_line.update_traces(line=dict(color='#2563EB', width=3)) 
        st.plotly_chart(fig_line, use_container_width=True)
        
    with c_trend2:
        # GRÁFICO DE DONA (CATEGORÍAS)
        df_cat = df_mes.groupby('categoria').agg({'utilidad': 'sum'}).reset_index()
        st.markdown("##### 💰 Rentabilidad por Categoría")
        
        # CORRECCIÓN: El error AttributeError: 'Figure' object has no attribute 'line_dict'
        # o el error genérico en esa sección puede ocurrir si se pasa un dataframe vacío o hay un conflicto
        # de versiones. El código es conceptualmente correcto, lo reforzamos.
        
        if not df_cat.empty:
             fig_pie = px.pie(df_cat, values='utilidad', names='categoria', hole=0.6)
             # Título movido al markdown para mejor control de espacio
             fig_pie.update_layout(
                 height=350, 
                 showlegend=True, # Mostrar la leyenda es útil para categorías
                 font=dict(family="Inter, sans-serif", color="#334155"),
                 margin=dict(l=20, r=20, t=20, b=20),
                 # Añadir anotación central si se desea:
                 # annotations=[dict(text='Rentabilidad', x=0.5, y=0.5, font_size=12, showarrow=False)]
             )
             fig_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=2)))
             st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("No hay datos de utilidad para este mes y categorías.")

# === TAB 3: ADN COMPARATIVO (Radar Chart) ===
with tab_dna:
    st.markdown("## 🧬 Comparativa 1 a 1: Fortalezas y Debilidades")
    
    c_sel1, c_sel2 = st.columns(2)
    vendedores_unicos = df_group['vendedor'].unique()
    
    # Seleccionadores para los agentes a comparar
    v1 = c_sel1.selectbox("Agente A", vendedores_unicos, index=0)
    v2 = c_sel2.selectbox("Agente B", vendedores_unicos, index=1 if len(vendedores_unicos) > 1 else 0)
    
    # Lógica del Radar Chart: Normalización de métricas
    def get_radar_data(v_name):
        """Calcula los valores normalizados (0-1) para el gráfico de radar."""
        row = df_group[df_group['vendedor'] == v_name].iloc[0]
        # Se calcula el máximo para normalizar
        max_vals = df_group[['Venta', 'Margen_Pct', 'Trx']].max() 
        # Evitar división por cero
        max_vals = max_vals.replace(0, 1) 
        return [
            row['Venta'] / max_vals['Venta'],
            row['Margen_Pct'] / max_vals['Margen_Pct'],
            row['Trx'] / max_vals['Trx'],
            row['Venta'] / max_vals['Venta'] # Repetir el primero para cerrar el polígono
        ]

    categories = ['Volumen', 'Rentabilidad', 'Velocidad (Trx)', 'Volumen']

    col_radar, col_table = st.columns([1, 1])
    
    with col_radar:
        st.markdown("##### 🕸️ Matriz de Competencias Normalizada")
        
        fig_radar = go.Figure()
        
        # Trazas de los dos agentes
        fig_radar.add_trace(go.Scatterpolar(r=get_radar_data(v1), theta=categories, fill='toself', name=v1, line_color='#3B82F6', opacity=0.6))
        fig_radar.add_trace(go.Scatterpolar(r=get_radar_data(v2), theta=categories, fill='toself', name=v2, line_color='#10B981', opacity=0.6))

        # Configuración del eje polar
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1], showticklabels=False), # Ocultar etiquetas numéricas radiales
                bgcolor='rgba(0,0,0,0)'
            ),
            showlegend=True,
            height=350,
            font=dict(family="Inter, sans-serif", color="#334155"),
            margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col_table:
        st.markdown("##### 📋 Diferenciales Clave")
        # Prepara el DataFrame para la tabla comparativa
        comp_df = df_group[df_group['vendedor'].isin([v1, v2])].set_index('vendedor')
        comp_df = comp_df[['Venta', 'Margen_Pct', 'Cumplimiento']]
        
        # Aplicar formato de visualización
        comp_df['Venta'] = comp_df['Venta'].map('${:,.0f}'.format)
        comp_df['Margen_Pct'] = comp_df['Margen_Pct'].map('{:.1f}%'.format)
        comp_df['Cumplimiento'] = comp_df['Cumplimiento'].map('{:.1f}%'.format)
        
        st.table(comp_df.T)
        
        # Análisis de texto simple
        if df_group[df_group['vendedor']==v1]['Margen_Pct'].values[0] > df_group[df_group['vendedor']==v2]['Margen_Pct'].values[0]:
            st.success(f"💡 **{v1}** protege mejor el precio. Ideal para el entrenamiento en rentabilidad.")
        else:
            st.info(f"💡 **{v2}** es más flexible en precio. Ideal para estrategias de penetración de mercado.")

# === TAB 4: REPORTES (Descarga de Excel) ===
with tab_export:
    st.markdown("## 📥 Centro de Informes Oficiales")
    st.markdown("Genera el reporte para la Junta Directiva con formato Excel profesional (Semáforos, Barras de Datos).")
    
    # 1. Preparación de los datos para el resumen de Excel
    excel_summary = df_group[['vendedor', 'Venta', 'meta', 'Cumplimiento', 'Margen_Pct']].copy()
    excel_summary.columns = ['Vendedor', 'Venta Real', 'Presupuesto', '% Cumplimiento', 'Margen %']
    
    # 2. Generación del archivo Excel (llama a la función mejorada)
    excel_file = generar_excel_premium(
        df_mes[['fecha', 'cliente', 'vendedor', 'categoria', 'venta', 'margen_pct']], # Data Cruda
        excel_summary # Resumen Estratégico
    )
    
    col_d1, col_d2 = st.columns([1,2])
    with col_d1:
        # Botón de descarga
        st.download_button(
            label="📄 DESCARGAR REPORTE .XLSX",
            data=excel_file,
            file_name=f"NEXUS_Reporte_Gerencial_{mes_sel}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )
    with col_d2:
        st.caption("El reporte incluye el resumen ejecutivo con formatos condicionales y la data cruda subyacente del periodo seleccionado.")

# --- FOOTER ---
st.divider()
st.markdown("<div style='text-align: center; color: #94A3B8; font-size: 0.85rem;'>NEXUS INTELLIGENCE SYSTEM © 2025 | Powered by Datovate AI Core</div>", unsafe_allow_html=True)
