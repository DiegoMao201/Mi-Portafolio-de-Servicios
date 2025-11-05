# -*- coding: utf-8 -*-
# ======================================================================================
# PORTAFOLIO DE SERVICIOS ESTRATÉGICOS: GM-DATOVATE
# VERSIÓN: 3.2 (Diseño Web Moderno + Corrección de Errores PDF y Canvas)
# ======================================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import urllib.parse
from fpdf import FPDF
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
# --- CORRECCIÓN 1: Importar st_canvas ---
from streamlit_drawable_canvas import st_canvas

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="GM-DATOVATE | Ecosistemas de Inteligencia Empresarial",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed" # La barra lateral se oculta por defecto
)

# --- PALETA DE COLORES Y ESTILOS ---
COLOR_PRIMARIO = "#0D3B66"  # Azul profundo (Confianza, Inteligencia)
COLOR_SECUNDARIO = "#1A73E8" # Azul brillante (Tecnología, Innovación)
COLOR_ACENTO_ROJO = "#F94144"    # Rojo vivo (Acción, Alerta)
COLOR_ACENTO_VERDE = "#43AA8B"  # Verde (Finanzas, Crecimiento)
COLOR_FONDO = "#FFFFFF"     # Fondo Blanco Limpio
COLOR_FONDO_SECUNDARIO = "#F7F9FC" # Fondo gris muy claro para secciones
COLOR_TEXTO = "#2F2F2F"
COLOR_TEXTO_SECUNDARIO = "#555555"

# --- INYECCIÓN DE CSS GLOBAL ---
st.markdown(f"""
<style>
    /* --- Ocultar elementos de Streamlit --- */
    #MainMenu {{display: none;}} /* Oculta el menú hamburguesa */
    footer {{display: none;}} /* Oculta el pie de página "Made with Streamlit" */
    [data-testid="stHeader"] {{display: none;}} /* Oculta la cabecera de Streamlit */
    [data-testid="stSidebar"] {{display: none;}} /* Oculta la barra lateral por completo */

    /* --- Reseteo y Fuentes --- */
    body {{
        font-family: 'Arial', sans-serif;
        color: {COLOR_TEXTO};
    }}

    /* --- Contenedor Principal --- */
    .main .block-container {{
        padding-top: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
        padding-bottom: 0rem;
    }}
    .stApp {{
        background-color: {COLOR_FONDO};
    }}

    /* --- Clases de Diseño Personalizadas --- */
    .section-container {{
        padding: 4rem 2rem;
    }}
    .section-container-dark {{
        background-color: {COLOR_FONDO_SECUNDARIO};
        border-top: 1px solid #E0E0E0;
        border-bottom: 1px solid #E0E0E0;
    }}
    .section-container-darker {{
        background-color: {COLOR_PRIMARIO};
        color: white;
    }}
    .section-container-darker h1, .section-container-darker h2, .section-container-darker h3, .section-container-darker p {{
        color: white;
    }}

    /* --- Héroe (Banner Principal) --- */
    .hero-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 6rem 2rem;
        background: linear-gradient(135deg, {COLOR_PRIMARIO} 0%, {COLOR_SECUNDARIO} 100%);
        color: white;
    }}
    .hero-container h1 {{
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        margin: 0;
    }}
    .hero-container h3 {{
        font-size: 1.5rem;
        font-weight: 400;
        color: {COLOR_ACENTO_ROJO};
        margin-top: 0.5rem;
    }}
    .hero-container p {{
        font-size: 1.1rem;
        max-width: 700px;
        margin: 1rem auto;
        color: #E0E0E0;
    }}
    .hero-button {{
        display: inline-block;
        padding: 0.8rem 2rem;
        background-color: {COLOR_ACENTO_ROJO};
        color: white;
        font-weight: bold;
        text-decoration: none;
        border-radius: 8px;
        transition: all 0.3s;
        margin-top: 1.5rem;
    }}
    .hero-button:hover {{
        background-color: #FFFFFF;
        color: {COLOR_ACENTO_ROJO};
        transform: scale(1.05);
    }}

    /* --- Tarjetas de Servicios --- */
    .service-card {{
        background-color: {COLOR_FONDO};
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        height: 100%;
    }}
    .service-card-icon {{
        font-size: 3rem;
    }}
    .service-card h3 {{
        margin-top: 1rem;
        color: {COLOR_PRIMARIO};
    }}

    /* --- Pestañas de Demo --- */
    /* Contenedor de las pestañas */
    .stTabs {{
        background-color: {COLOR_FONDO_SECUNDARIO};
        padding: 2rem 2rem 4rem 2rem;
        border-top: 1px solid #E0E0E0;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
        padding-left: 1rem;
        padding-right: 1rem;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        background-color: transparent;
        border-bottom: 3px solid #C0C0C0;
        font-size: 1.1rem;
        font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        border-bottom: 3px solid {COLOR_ACENTO_ROJO};
        color: {COLOR_ACENTO_ROJO};
        font-weight: bold;
    }}
    
    /* --- Tarjetas de Equipo --- */
    .team-card {{
        background-color: {COLOR_FONDO};
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #E0E0E0;
    }}
    .team-card img {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        border: 4px solid {COLOR_PRIMARIO};
    }}
    .team-card h3 {{ color: {COLOR_PRIMARIO}; margin-top: 1rem; }}
    .team-card p {{
        color: {COLOR_ACENTO_ROJO};
        font-weight: bold;
        font-size: 1rem;
    }}

    /* --- Formulario de Contacto --- */
    .contact-form-container {{
        padding: 4rem 2rem;
    }}
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        background-color: #FFFFFF;
        border: 1px solid #DDD;
    }}
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {{
        border-color: {COLOR_PRIMARIO};
        box-shadow: 0 0 0 1px {COLOR_PRIMARIO};
    }}
    .stButton>button {{
        border-radius: 8px;
        border: 2px solid {COLOR_PRIMARIO};
        background-color: {COLOR_PRIMARIO};
        color: white;
        font-weight: bold;
        transition: all 0.3s;
        padding: 0.75rem 1.5rem;
    }}
    .stButton>button:hover {{
        background-color: {COLOR_SECUNDARIO};
        border-color: {COLOR_SECUNDARIO};
        transform: scale(1.02);
    }}
    
    /* Media Query para móviles */
    @media (max-width: 768px) {{
        .hero-container h1 {{ font-size: 2.5rem; }}
        .hero-container h3 {{ font-size: 1.2rem; }}
        .section-container {{ padding: 2rem 1rem; }}
        .service-card {{ margin-bottom: 1rem; }}
        .team-card {{ margin-bottom: 1rem; }}
    }}
</style>
""", unsafe_allow_html=True)


# ======================================================================================
# --- DATOS DE EJEMPLO PARA LAS DEMOS (Igual que antes) ---
# ======================================================================================
@st.cache_data
def get_sample_data():
    """Crea y cachea todos los DataFrames de ejemplo para las demos."""
    data = {}
    data['ventas_vendedor'] = pd.DataFrame({
        'Vendedor': ['DIEGO GARCIA', 'ANGELA CONTRERAS', 'PABLO MAFLA', 'MARY LUZ TREJOS'],
        'Ventas ($)': [120_000_000, 95_000_000, 88_000_000, 75_000_000],
        'Meta ($)': [110_000_000, 100_000_000, 90_000_000, 80_000_000],
    })
    data['ventas_vendedor']['Avance (%)'] = (data['ventas_vendedor']['Ventas ($)'] / data['ventas_vendedor']['Meta ($)']) * 100
    data['sugerencia_abastecimiento'] = pd.DataFrame({
        'SKU': ['A-101', 'B-202', 'C-303', 'D-404'],
        'Producto': ['Disco Corte 4-1/2"', 'Tornillo Drywall 6x1', 'Electrodo 6013', 'Gafa de Seguridad'],
        'Stock (Total)': [500, 15000, 800, 120],
        'Stock Tránsito': [0, 5000, 0, 100],
        'Necesidad Real': [200, 10000, 500, 150],
        'Sugerencia Traslado': [0, 0, 300, 0],
        'Sugerencia Compra': [0, 0, 200, 50]
    })
    data['cartera_antiguedad'] = pd.DataFrame({
        'Rango': ['Al día', '1-15 días', '16-30 días', '31-60 días', 'Más de 60 días'],
        'Valor ($)': [250_000_000, 80_000_000, 45_000_000, 25_000_000, 70_000_000],
        'Color': [COLOR_ACENTO_VERDE, '#FBC02D', '#F57C00', COLOR_ACENTO_ROJO, '#a71919']
    })
    data['cartera_detalle'] = pd.DataFrame({
        'Cliente': ['Cliente A', 'Cliente B (Vencido)', 'Cliente B (Vencido)', 'Cliente C', 'Cliente D (Vencido)'],
        'NIT': ['800.123.456-1', '800.987.654-2', '800.987.654-2', '800.222.333-4', '900.555.444-5'],
        'Cod. Cliente': ['1001', '1002', '1002', '1003', '1004'],
        'Factura': ['FV-1001', 'FV-901', 'FV-902', 'FV-1002', 'FV-850'],
        'Fecha Vencimiento': [datetime.now().date() + timedelta(days=15), datetime.now().date() - timedelta(days=45), datetime.now().date() - timedelta(days=12), datetime.now().date() + timedelta(days=30), datetime.now().date() - timedelta(days=70)],
        'Días Vencido': [-15, 45, 12, -30, 70],
        'Monto': [2_500_000, 1_200_000, 850_000, 3_100_000, 4_500_000],
        'Email': ['pagos@clientea.com', 'pagos@clienteb.com', 'pagos@clienteb.com', 'pagos@clientec.com', 'pagos@cliented.com'],
        'Teléfono': ['573001234567', '573019876543', '573019876543', '573022223333', '573035554444']
    })
    
    # Datos para Covinoc (Demo 3 Finanzas)
    data['covinoc_subir'] = pd.DataFrame({
        'Factura': ['FV-1001', 'FV-1002', 'FV-1003'],
        'Cliente': ['Cliente A', 'Cliente B', 'Cliente C'],
        'Días Vencido': [35, 40, 28],
        'Monto': [1_200_000, 850_000, 2_100_000]
    })
    data['covinoc_exonerar'] = pd.DataFrame({
        'Factura': ['FV-901', 'FV-902'],
        'Cliente': ['Cliente D', 'Cliente E'],
        'Estado Covinoc': ['Pendiente', 'Pendiente'],
        'Estado Cartera': ['PAGADA', 'PAGADA']
    })
    
    return data

SAMPLE_DATA = get_sample_data()


# ======================================================================================
# --- CLASES DE GENERACIÓN DE DOCUMENTOS (PDF Y EXCEL) ---
# ======================================================================================

class DemoPDF(FPDF):
    """Crea un PDF profesional de ejemplo para las demos."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = "Documento de Demostración"

    def header(self):
        self.set_fill_color(int(COLOR_PRIMARIO[1:3], 16), int(COLOR_PRIMARIO[3:5], 16), int(COLOR_PRIMARIO[5:7], 16))
        self.rect(0, 0, self.w, 30, 'F')
        # self.image("LOGO.png", 10, 8, 33) # Descomentar si tienes un logo
        self.set_font('Arial', 'B', 20)
        self.set_text_color(255, 255, 255)
        
        # --- CORRECCIÓN 2: Se eliminó el argumento 'ln=False' que causaba el TypeError ---
        self.cell(0, 20, 'GM-DATOVATE', 0, 1, 'L') 
        # Esta línea tenía (..., ln=False) al final, lo cual es un error. 
        # El '1' ya actúa como ln=1. Al quitarlo, se soluciona el error.
        # PERO, la lógica siguiente (set_xy) implica que NO queríamos un salto de línea.
        # La corrección correcta es poner ln=0 y quitar el '1'.
        
        # --- RE-CORRECCIÓN 2.1 (La correcta) ---
        # Reseteamos el cursor al inicio para la primera celda
        self.set_xy(self.l_margin, 10) 
        # Escribimos 'GM-DATOVATE' SIN salto de línea (ln=0)
        self.cell(0, 10, 'GM-DATOVATE', 0, 0, 'L') 

        # Ahora, nos movemos a la posición Y correcta para el TÍTULO
        self.set_xy(self.l_margin, 18)
        self.set_font('Arial', 'B', 15)
        self.set_text_color(int(COLOR_ACENTO_ROJO[1:3], 16), int(COLOR_ACENTO_ROJO[3:5], 16), int(COLOR_ACENTO_ROJO[5:7], 16))
        # Escribimos el título CON salto de línea (ln=1)
        self.cell(0, 10, self.title, 0, 1, 'R')
        self.ln(15) # Salto de línea final para el contenido

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Documento de demostración generado por el Ecosistema de Inteligencia GM-DATOVATE - Página %s' % self.page_no(), 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(int(COLOR_FONDO_SECUNDARIO[1:3], 16), int(COLOR_FONDO_SECUNDARIO[3:5], 16), int(COLOR_FONDO_SECUNDARIO[5:7], 16))
        self.set_text_color(int(COLOR_PRIMARIO[1:3], 16), int(COLOR_PRIMARIO[3:5], 16), int(COLOR_PRIMARIO[5:7], 16))
        self.cell(0, 10, f" {title}", 0, 1, 'L', fill=True)
        self.ln(4)
        
    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, body)
        self.ln()

    def add_table(self, df):
        self.set_font('Arial', 'B', 9)
        self.set_fill_color(int(COLOR_SECUNDARIO[1:3], 16), int(COLOR_SECUNDARIO[3:5], 16), int(COLOR_SECUNDARIO[5:7], 16))
        self.set_text_color(255, 255, 255)
        
        # Calcular anchos de columna dinámicamente
        col_widths = []
        for col in df.columns:
            # Encontrar el ancho máximo del contenido de la columna o del header
            max_len_col = df[col].astype(str).map(len).max()
            max_len = max(len(str(col)), max_len_col if pd.notna(max_len_col) else 0)
            col_widths.append(max_len * 2.5 + 6) # Factor de escala + padding
        
        total_width = sum(col_widths)
        page_width = self.w - 2 * self.l_margin
        
        # Escalar anchos si exceden la página
        if total_width > page_width:
            scale_factor = page_width / total_width
            col_widths = [w * scale_factor for w in col_widths]
        
        for i, header in enumerate(df.columns):
            self.cell(col_widths[i], 7, str(header), 1, 0, 'C', fill=True)
        self.ln()

        self.set_font('Arial', '', 9)
        self.set_text_color(0, 0, 0)
        self.set_fill_color(245, 245, 245)
        fill = False
        for _, row in df.iterrows():
            for i, item in enumerate(row):
                if isinstance(item, (int, float)):
                    # Formato de moneda para columnas relevantes
                    if "Monto" in df.columns[i] or "Valor" in df.columns[i] or "Total" in df.columns[i] or "Vlr. Unitario" in df.columns[i]:
                        item_str = f"${item:,.0f}"
                    else:
                        item_str = str(item)
                    align = 'R'
                else:
                    item_str = str(item)
                    align = 'L'
                self.cell(col_widths[i], 6, item_str, 1, 0, align, fill=fill)
            self.ln()
            fill = not fill

@st.cache_data
def generar_demo_pdf(df, title, intro_text):
    """Genera un PDF genérico de demostración en memoria."""
    pdf = DemoPDF()
    pdf.title = title
    pdf.add_page()
    pdf.chapter_title("Resumen del Reporte")
    pdf.chapter_body(intro_text)
    pdf.ln(5)
    pdf.chapter_title("Datos de Ejemplo")
    pdf.add_table(df)
    return pdf.output(dest='S').encode('latin-1')

@st.cache_data
def generar_demo_pdf_cartera(df, cliente_info):
    """Genera un PDF de estado de cuenta profesional en memoria."""
    pdf = DemoPDF()
    pdf.title = "Estado de Cuenta"
    pdf.add_page()
    
    pdf.chapter_title("Información del Cliente")
    pdf.set_font('Arial', '', 10)
    pdf.cell(40, 6, "Cliente:")
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, cliente_info['Cliente'])
    pdf.ln()
    pdf.set_font('Arial', '', 10)
    pdf.cell(40, 6, "NIT:")
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, cliente_info['NIT'])
    pdf.ln()
    pdf.set_font('Arial', '', 10)
    pdf.cell(40, 6, "Teléfono:")
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, cliente_info['Teléfono'])
    pdf.ln()
    pdf.set_font('Arial', '', 10)
    pdf.cell(40, 6, "Email:")
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 6, cliente_info['Email'])
    pdf.ln(10)

    pdf.chapter_title("Detalle de Facturas Vencidas")
    pdf.add_table(df[['Factura', 'Fecha Vencimiento', 'Días Vencido', 'Monto']])
    pdf.ln(10)
    
    total_vencido = df['Monto'].sum()
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(int(COLOR_ACENTO_ROJO[1:3], 16), int(COLOR_ACENTO_ROJO[3:5], 16), int(COLOR_ACENTO_ROJO[5:7], 16))
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, f"TOTAL VENCIDO: ${total_vencido:,.0f}", 1, 1, 'C', fill=True)
    
    return pdf.output(dest='S').encode('latin-1')

@st.cache_data
def generar_demo_excel(df_dict):
    """Genera un Excel de demostración en memoria con múltiples hojas y formato profesional."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for sheet_name, df in df_dict.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name, startrow=1)
            
            ws = writer.sheets[sheet_name]
            
            # Estilos
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color=COLOR_PRIMARIO.replace("#",""), fill_type="solid")
            total_font = Font(bold=True)
            total_fill = PatternFill(start_color="F7F9FC", fill_type="solid")
            currency_format = '$ #,##0'
            date_format = 'dd/mm/yyyy'
            
            # Aplicar estilo a cabecera
            for i, col in enumerate(df.columns, 1):
                cell = ws.cell(row=2, column=i)
                cell.value = col
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal='center', vertical='center')
                
                # Autoajustar ancho
                try:
                    max_len_col = df[col].astype(str).map(len).max()
                    max_len = max(len(str(col)), max_len_col if pd.notna(max_len_col) else 0)
                except:
                    max_len = len(str(col))
                ws.column_dimensions[get_column_letter(i)].width = max(max_len + 2, 12)
                
                # Aplicar formatos
                if df[col].dtype == 'datetime64[ns]':
                    for c in ws[get_column_letter(i)][2:]:
                        c.number_format = date_format
                if 'Monto' in col or 'Valor' in col or 'Total' in col or 'Vlr. Unitario' in col:
                    for c in ws[get_column_letter(i)][2:]:
                        c.number_format = currency_format

            # Título
            ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(df.columns))
            title_cell = ws.cell(row=1, column=1)
            title_cell.value = sheet_name.replace("_", " ")
            title_cell.font = Font(size=16, bold=True, color=COLOR_PRIMARIO.replace("#",""))
            title_cell.alignment = Alignment(horizontal='center')
    
    return output.getvalue()


# ======================================================================================
# --- FUNCIONES DE RENDERIZADO DE PÁGINAS ---
# (Estas funciones ahora renderizan el contenido de cada sección/demo)
# ======================================================================================

def render_pagina_inicio():
    """Renderiza la página de bienvenida, el pitch de valor y el equipo."""
    
    # --- Sección Héroe ---
    st.markdown(f"""
    <div class="hero-container">
        <div>
            <h1>De Datos Aislados a un Ecosistema de Negocios Inteligente.</h1>
            <h3>Transformamos su operación con datos, automatización e IA.</h3>
            <p>
                Somos GM-DATOVATE. No construimos solo 'apps' o 'dashboards'. 
                Construimos el **Sistema Operativo Central** de su compañía, 
                conectando Ventas, Finanzas y Operaciones en un solo cerebro digital 
                que le dice exactamente qué hacer a continuación.
            </p>
            <a href="#contacto" class="hero-button">
                Solicitar Consulta Estratégica
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- Sección de Servicios/Pilares ---
    with st.container():
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; border: none; margin-bottom: 3rem;'>Un Ecosistema, Cuatro Pilares de Valor</h2>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="service-card">
                <div class="service-card-icon">🧠</div>
                <h3>Inteligencia Comercial</h3>
                <p style="color: {COLOR_TEXTO_SECUNDARIO};">
                    Deje de adivinar. Usamos IA para analizar su historial y decirle a quién llamar, 
                    qué producto ofrecer (venta cruzada) y qué clientes están en riesgo de irse.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="service-card">
                <div class="service-card-icon">🏭</div>
                <h3>Operaciones y Logística</h3>
                <p style="color: {COLOR_TEXTO_SECUNDARIO};">
                    Automatizamos su cadena de suministro. Desde la sincronización de inventario con el ERP
                    hasta el conteo físico en bodega con apps móviles y sugerencias de abastecimiento.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="service-card">
                <div class="service-card-icon">🏦</div>
                <h3>Finanzas y Tesorería</h3>
                <p style="color: {COLOR_TEXTO_SECUNDARIO};">
                    Digitalizamos su flujo de caja. Automatizamos cuadres de caja, procesamiento de recibos 
                    y generamos los archivos .txt para su ERP, eliminando la digitación manual.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class="service-card">
                <div class="service-card-icon">🤖</div>
                <h3>Integración y Automatización</h3>
                <p style="color: {COLOR_TEXTO_SECUNDARIO};">
                    Unimos todos los sistemas: vinculación de clientes con firma digital, gestión de riesgo 
                    con agencias externas (Covinoc) y un Agente IA en WhatsApp 24/7.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Sección "Quiénes Somos" ---
    with st.container():
        st.markdown('<div class="section-container section-container-dark">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; border: none; margin-bottom: 3rem;'>Nuestros Arquitectos de Soluciones</h2>", unsafe_allow_html=True)
        
        col_space1, col_team1, col_team2, col_space2 = st.columns([1, 2, 2, 1])
        
        with col_team1:
            st.markdown(f"""
            <div class="team-card">
                <img src="https://i.imgur.com/7bQyL4B.png" alt="Foto de Diego Garcia">
                <h3>Diego Mauricio García</h3>
                <p>Arquitecto de Datos y Desarrollador Líder</p>
                <span style="font-size: 0.9rem; color: {COLOR_TEXTO_SECUNDARIO};">
                    Especialista en la construcción de ecosistemas de datos complejos, 
                    transformando procesos manuales en flujos de trabajo automatizados 
                    e inteligentes.
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        with col_team2:
            st.markdown(f"""
            <div class="team-card">
                <img src="https://i.imgur.com/kF2bWpA.png" alt="Foto de Pablo Mafla">
                <h3>Pablo Cesar Mafla</h3>
                <p>Estratega Comercial y de Negocios</p>
                <span style="font-size: 0.9rem; color: {COLOR_TEXTO_SECUNDARIO};">
                    Experto en alinear la tecnología con los objetivos de negocio. 
                    Traduce las necesidades del mercado en herramientas de datos que 
                    impulsan el crecimiento y la rentabilidad.
                </span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

def render_pagina_comercial():
    """Demo de la Suite de Inteligencia Comercial."""
    
    st.markdown("Deje que sus datos le digan cómo vender más. Automatizamos la prospección, la cotización y el análisis de rendimiento.")
    st.divider()
    
    tab1, tab2, tab3 = st.tabs([
        "Demo 1: Dashboard de BI Gerencial",
        "Demo 2: Asistente Proactivo (IA)",
        "Demo 3: Catálogo y Cotizador"
    ])
    
    with tab1:
        st.subheader("Dashboard de BI Gerencial (En Tiempo Real)")
        st.markdown("Agregamos los datos de ventas de todas las fuentes y los presentamos en un dashboard de alto nivel para la toma de decisiones. Mida el rendimiento vs. metas, identifique a sus mejores vendedores y entienda la salud de su venta.")

        with st.container(border=True):
            df_ventas = SAMPLE_DATA['ventas_vendedor']
            total_ventas = df_ventas['Ventas ($)'].sum()
            total_meta = df_ventas['Meta ($)'].sum()
            avg_avance = (total_ventas / total_meta) * 100 if total_meta > 0 else 0

            col1, col2, col3 = st.columns(3)
            col1.metric("Ventas Totales del Mes", f"${total_ventas/1_000_000:.1f} M", f"{avg_avance - 100:.1f}% vs Meta")
            col2.metric("Meta del Mes", f"${total_meta/1_000_000:.1f} M")
            col3.metric("Avance General", f"{avg_avance:.1f}%")
            
            fig = px.bar(
                df_ventas, x='Vendedor', y=['Ventas ($)', 'Meta ($)'], barmode='group',
                title='Rendimiento de Ventas vs. Meta por Vendedor',
                color_discrete_map={'Ventas ($)': COLOR_SECUNDARIO, 'Meta ($)': COLOR_ACENTO_ROJO}
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Asistente Proactivo (Análisis RFM y Venta Cruzada)")
        st.markdown("Esto es inteligencia de negocios en acción. El sistema analiza el historial de compras y genera un plan de acción *automático* para el vendedor, diciéndole exactamente a quién llamar.")
        
        with st.container(border=True):
            st.subheader("Plan de Acción para: DIEGO GARCIA (Demo)")
            st.info(
                "**🎯 Oportunidad de Venta Cruzada (Demo):**\n"
                "Tus clientes **'Ferretería El Tornillo'** y **'Depósito Central'** compran 'Discos de Corte' (A-101) pero "
                "nunca han comprado 'Gafas de Seguridad' (D-404). ¡Ofréceles en su próximo pedido!"
            )
            st.warning(
                "**🔥 Cliente en Riesgo (Análisis RFM - Demo):**\n"
                "Tu cliente **'Construcciones Andinas'** no ha comprado en 62 días (Segmento: 'En Riesgo'). "
                "Su frecuencia de compra habitual es de 30 días. **¡Acción: Llama hoy!**"
            )
            st.success(
                "**💎 Cliente Campeón (Análisis RFM - Demo):**\n"
                "Tu cliente **'Maestro SAS'** es un 'Campeón' (Compra reciente, frecuente y de alto valor). "
                "**Acción: Agradécele** y ofrécele un producto nuevo de nicho."
            )

    with tab3:
        st.subheader("Catálogo Interactivo y Cotizador Profesional")
        st.markdown("Transformamos sus listas de precios estáticas en una herramienta de ventas interactiva. El vendedor puede navegar, ver imágenes, consultar stock *real* de todas las bodegas y generar un PDF profesional en segundos.")
        
        with st.container(border=True):
            col1, col2 = st.columns([1.5, 1])
            with col1:
                st.subheader("Catálogo de Productos")
                st.markdown(f"""
                <div style="background: #FFF; border: 1px solid #EEE; border-radius: 10px; padding: 1rem; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                    <h4 style="color: {COLOR_PRIMARIO}; margin-top: 0;">Disco de Corte 4-1/2" Inox</h4>
                    <p style="font-size: 0.9rem; color: {COLOR_TEXTO};">Ref: A-101</p>
                    <img src="https://i.imgur.com/gY5aM5A.png" style="width: 100%; border-radius: 5px; border: 1px solid #EEE;">
                    <h5 style="color: {COLOR_SECUNDARIO}; margin-top: 1rem;">Stock en Tiendas (Simulación):</h5>
                    <ul style="font-size: 0.9rem;">
                        <li><b>Bodega CEDI:</b> 5,200 uds</li>
                        <li><b>Tienda Armenia:</b> <span style="color: {COLOR_ACENTO_ROJO};">30 uds (Stock Bajo)</span></li>
                        <li><b>Tienda Pereira:</b> 450 uds</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.subheader("Cotización en Proceso")
                st.info("🛒 Carrito de Cotización")
                df_cotizacion = pd.DataFrame({
                    'Referencia': ['A-101', 'B-202'],
                    'Producto': ['Disco de Corte 4-1/2"', 'Tornillo Drywall 6x1'],
                    'Cantidad': [50, 2000],
                    'Vlr. Unitario': [1800, 150]
                })
                df_cotizacion['Total'] = df_cotizacion['Cantidad'] * df_cotizacion['Vlr. Unitario']
                st.dataframe(df_cotizacion, use_container_width=True, hide_index=True)
                
                # --- Botón de descarga de PDF (Funcional) ---
                pdf_data = generar_demo_pdf(
                    df_cotizacion[['Referencia', 'Producto', 'Cantidad', 'Vlr. Unitario', 'Total']],
                    "Cotización de Ejemplo",
                    "Este es un ejemplo de cotización profesional generada automáticamente por el sistema de GM-DATOVATE."
                )
                st.download_button(
                    label="📄 Descargar PDF Profesional (Demo)",
                    data=pdf_data,
                    file_name="Demo_Cotizacion_GM-DATOVATE.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )


def render_pagina_operaciones():
    """Demo de la Suite de Operaciones y Logística."""
    st.markdown("Automatización de la cadena de suministro, desde el proveedor hasta la bodega, con inteligencia de datos.")
    st.divider()
    
    tab1, tab2, tab3 = st.tabs([
        "Demo 1: Abastecimiento Inteligente",
        "Demo 2: Control de Inventario Móvil",
        "Demo 3: Sincronización (ETL)"
    ])

    with tab1:
        st.subheader("Tablero de Abastecimiento Inteligente")
        st.markdown("Este módulo va más allá de mostrar el stock. Calcula la **Necesidad Real** (descontando lo que ya está en tránsito) y genera un **Plan de Traslados Inteligente** para ahorrar capital de trabajo antes de sugerir una compra.")
        
        with st.container(border=True):
            st.subheader("Sugerencias de Abastecimiento (Demo)")
            st.dataframe(
                SAMPLE_DATA['sugerencia_abastecimiento'].style
                    .applymap(lambda x: f'background-color: {COLOR_ACENTO_VERDE}; color: white; font-weight: bold;' if x > 0 else '', subset=['Sugerencia Traslado'])
                    .applymap(lambda x: f'background-color: {COLOR_ACENTO_ROJO}; color: white; font-weight: bold;' if x > 0 else '', subset=['Sugerencia Compra'])
                    .format({"Stock (Total)": "{:,.0f}", "Stock Tránsito": "{:,.0f}", "Necesidad Real": "{:,.0f}", "Sugerencia Traslado": "{:,.0f}", "Sugerencia Compra": "{:,.0f}"}),
                use_container_width=True, hide_index=True
            )
            st.markdown("""
                * **Fila 2 (Tornillo):** El sistema ve que la necesidad (10,000) es cubierta por lo que hay en tránsito (5,000) y el stock (15,000). **Acción: No hacer nada.**
                * **Fila 3 (Electrodo):** El sistema detecta una necesidad de 500. Antes de comprar, encuentra 300 en otra tienda y sugiere un **Traslado (Ahorro)**. Solo pide comprar los 200 restantes.
            """)
            
            # --- Botones de acción (Funcionales) ---
            st.subheader("Generación de Órdenes (Demo)")
            df_orden = SAMPLE_DATA['sugerencia_abastecimiento'][SAMPLE_DATA['sugerencia_abastecimiento']['Sugerencia Compra'] > 0]
            
            pdf_data = generar_demo_pdf(
                df_orden[['SKU', 'Producto', 'Sugerencia Compra']],
                "Orden de Compra (Demo)",
                "Documento de ejemplo generado automáticamente para el proveedor, basado en las sugerencias del sistema."
            )
            excel_data = generar_demo_excel({
                "Orden_de_Compra": df_orden,
                "Detalle_Traslados": SAMPLE_DATA['sugerencia_abastecimiento'][SAMPLE_DATA['sugerencia_abastecimiento']['Sugerencia Traslado'] > 0]
            })

            c1, c2 = st.columns(2)
            c1.download_button(
                label="📄 Descargar Orden de Compra PDF (Demo)",
                data=pdf_data,
                file_name="Demo_Orden_de_Compra.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            c2.download_button(
                label="📊 Descargar Reporte Excel (Demo)",
                data=excel_data,
                file_name="Demo_Reporte_Abastecimiento.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

    with tab2:
        st.subheader("Aplicación Móvil de Conteo Físico")
        st.markdown("Digitalizamos el conteo en bodega. El gerente asigna tareas (basadas en datos o manualmente) y el operario las ejecuta en una app móvil con escáner, conteo parcial y manejo de sobrantes.")
        
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Vista del Operario (Móvil)")
                st.text_input("Buscar por Escáner o Referencia:", "770123456789", key="demo_scan")
                st.success("Producto Encontrado: 'Gafa de Seguridad'")
                st.metric("Stock Teórico", 120)
                
                st.markdown("**Conteo Parcial (Calculadora):**")
                qty = st.number_input("Añadir cantidad:", value=0, step=1, key="demo_qty")
                if st.button("Registrar Cantidad", type="primary", use_container_width=True):
                    st.toast(f"Se registraron {qty} unidades. El total se actualizará.", icon="✅")

            with col2:
                st.subheader("Resumen de Conteo del Operario")
                st.dataframe(pd.DataFrame({
                    'Producto': ['Gafa de Seguridad', 'Disco de Corte'],
                    'Teórico': [120, 500],
                    'Contado': [118, 505],
                    'Historial Conteo': ["+50, +50, +10, +8", "+500, +5"],
                    'Diferencia': [-2, 5]
                }), use_container_width=True, hide_index=True)
                if st.button("Enviar Conteo Final para Revisión (Demo)", use_container_width=True):
                    st.success("¡Conteo enviado! El gerente será notificado.")
                    st.balloons()
    
    with tab3:
        st.subheader("Sincronización Maestra de Inventario (ETL)")
        st.markdown("Desarrollamos un proceso que se conecta a su ERP (vía Dropbox, FTP, etc.), lee los archivos de inventario y costos, los transforma, y actualiza la base de datos central en la nube. **Detecta productos nuevos** y actualiza el stock de **todas las tiendas**.")
        
        st.graphviz_chart(f"""
            digraph "ETL Process" {{
                node [shape=box, style="filled,rounded", fontname="Arial", fontsize=12];
                graph [bgcolor="transparent"];

                erp [label="1. ERP Exporta CSV/XLSX\n(Ej: 'Rotacion.csv')", shape=cylinder, fillcolor="#E3F2FD"];
                script [label="2. Script de Sincronización\n(Python + Pandas)", shape=component, fillcolor="#D1C4E9"];
                nube [label="3. Base de Datos Maestra\n(Google Sheets)", shape=cylinder, fillcolor="#C8E6C9"];
                apps [label="4. Todo el Ecosistema\n(Cotizador, BI, App Móvil)", shape=display, fillcolor="#FFF9C4"];

                erp -> script [label=" Lee y Transforma"];
                script -> nube [label=" Actualiza y Añade Nuevos"];
                nube -> apps [label=" Alimenta Datos Vivos"];
            }}
        """)
        st.info("Esta demostración visualiza el flujo de datos. En una implementación real, este proceso se ejecuta automáticamente en un servidor.")

def render_pagina_finanzas():
    """Demo de la Suite Financiera y de Tesorería."""
    st.markdown("Controle el flujo de caja, automatice la contabilidad y gestione el riesgo de cartera como nunca antes.")
    st.divider()
    
    tab1, tab2, tab3 = st.tabs([
        "Demo 1: Dashboard de Cartera (AR)",
        "Demo 2: Automatización Contable",
        "Demo 3: Automatización de Riesgo"
    ])

    with tab1:
        st.subheader("Dashboard de Gestión de Cartera (AR)")
        st.markdown("Visibilidad total de su cartera. KPIs en tiempo real (DSO, CER, Morosidad), análisis de Pareto y **herramientas de gestión (Email/WhatsApp/PDF) para cada cliente.**")

        with st.container(border=True):
            df_cartera = SAMPLE_DATA['cartera_antiguedad']
            total_cartera = df_cartera['Valor ($)'].sum()
            total_vencido = df_cartera[df_cartera['Rango'] != 'Al día']['Valor ($)'].sum()

            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("Cartera Total", f"${total_cartera/1_000_000:.1f} M")
            kpi2.metric("Cartera Vencida", f"${total_vencido/1_000_000:.1f} M")
            kpi3.metric("Índice de Morosidad", f"{total_vencido/total_cartera*100:.1f}%")

            fig = px.pie(
                df_cartera, values='Valor ($)', names='Rango', title='Deuda por Antigüedad',
                hole=0.4, color='Rango', color_discrete_map=dict(zip(df_cartera['Rango'], df_cartera['Color']))
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Gestión de Cliente Individual (Demo Interactiva)")
            df_detalle = SAMPLE_DATA['cartera_detalle']
            cliente_demo_nombre = st.selectbox("Seleccione un cliente para gestionar:", df_detalle['Cliente'].unique())
            
            if cliente_demo_nombre:
                cliente_demo_data = df_detalle[df_detalle['Cliente'] == cliente_demo_nombre]
                cliente_info = cliente_demo_data.iloc[0]
                
                st.dataframe(cliente_demo_data[['Factura', 'Días Vencido', 'Monto']], use_container_width=True, hide_index=True)
                
                mensaje_wa = (
                    f"👋 ¡Hola {cliente_info['Cliente']}! Te saludamos desde GM-DATOVATE (Demo).\n\n"
                    f"Te recordamos tu saldo vencido. Tu factura *{cliente_info['Factura']}* por *${cliente_info['Monto']:,.0f}* "
                    f"presenta *{cliente_info['Días Vencido']} días* de vencimiento.\n\n"
                    f"Agradecemos tu pronta gestión."
                )
                url_wa = f"https://wa.me/{cliente_info['Teléfono']}?text={urllib.parse.quote(mensaje_wa)}"

                c1, c2, c3 = st.columns(3)
                
                pdf_cartera = generar_demo_pdf_cartera(cliente_demo_data, cliente_info)
                c1.download_button(
                    label="📄 Descargar PDF (Demo)", data=pdf_cartera,
                    file_name=f"Cartera_{cliente_info['Cliente']}.pdf", mime="application/pdf",
                    use_container_width=True
                )
                
                if c2.button("✉️ Enviar Email (Demo)", use_container_width=True):
                    st.toast("Simulación: Email enviado a " + cliente_info['Email'], icon="✉️")

                # Botón de WhatsApp funcional
                c3.link_button("📲 Enviar WhatsApp (Demo)", url_wa, use_container_width=True)

    with tab2:
        st.subheader("Automatización Contable (Cuadres y Recibos)")
        st.markdown("Eliminamos la digitación manual y los errores. Las tiendas llenan un formulario digital (`Cuadre de Caja`) o procesan un Excel (`Recibos de Caja`). El sistema valida, asigna cuentas contables y genera el archivo `.txt` listo para el ERP.")

        with st.container(border=True):
            st.subheader("Simulación de Cuadre de Caja Digital")
            c1, c2 = st.columns(2)
            c1.text_input("Tienda", "Armenia", disabled=True, key="demo_tienda_2")
            c2.date_input("Fecha", datetime.now().date(), disabled=True, key="demo_fecha_2")
            st.number_input("Venta Total (Sistema)", 5_000_000, disabled=True, key="demo_venta_total_2")
            
            st.dataframe(pd.DataFrame({
                'Tipo': ['Tarjetas', 'Consignaciones', 'Gastos', 'Efectivo Entregado'],
                'Valor': [2_500_000, 1_500_000, 200_000, 800_000]
            }), use_container_width=True, hide_index=True)

            st.metric("Total Desglose", "$ 5,000,000")
            st.metric("DIFERENCIA", "$ 0", delta="CUADRE PERFECTO", delta_color="off")
            
            demo_txt = "FECHA|CONSECUTIVO|CUENTA|...|DEBITO|CREDITO\n2025-11-05|1001|111005|...|2500000|0\n2025-11-05|1001|413501|...|0|2500000\n"
            st.download_button(
                label="💾 Descargar .TXT para ERP (Demo)",
                data=demo_txt,
                file_name="Demo_Contable_GM-DATOVATE.txt",
                mime="text/plain",
                use_container_width=True,
                type="primary"
            )

    with tab3:
        st.subheader("Automatización de Riesgo (Integración Externa)")
        st.markdown("El sistema cruza automáticamente nuestra cartera con reportes de agencias externas (como Covinoc). Identifica discrepancias y genera los archivos de acción masiva, automatizando la gestión de riesgo.")
        
        with st.container(border=True):
            st.subheader("Resultados del Cruce Automático (Demo)")
            
            excel_demo_data = generar_demo_excel({
                "1_Facturas_a_Subir": SAMPLE_DATA['covinoc_subir'],
                "2_Facturas_a_Exonerar": SAMPLE_DATA['covinoc_exonerar']
            })
            
            st.warning("Acción: Estas facturas están en nuestra cartera pero no en la agencia. Deben subirse.")
            st.dataframe(SAMPLE_DATA['covinoc_subir'], use_container_width=True, hide_index=True)
            
            st.success("Acción: Estas facturas ya fueron pagadas (no están en cartera) pero siguen activas en la agencia. Deben exonerarse.")
            st.dataframe(SAMPLE_DATA['covinoc_exonerar'], use_container_width=True, hide_index=True)

            st.download_button(
                "📥 Descargar Reporte de Acciones (Excel Demo)", 
                excel_demo_data, 
                file_name="Demo_Reporte_Riesgo_GM-DATOVATE.xlsx", 
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                use_container_width=True,
                type="primary"
            )

def render_pagina_integracion():
    """Demo de la Suite de Integración y Futuro (IA)."""
    st.markdown("Conectamos todos los procesos, desde la vinculación de un cliente hasta el servicio post-venta con IA.")
    st.divider()

    tab1, tab2 = st.tabs([
        "Demo 1: Portal de Vinculación Digital",
        "Demo 2: Agente IA (Chatbot WhatsApp)"
    ])

    with tab1:
        st.subheader("Portal de Vinculación Digital de Clientes")
        st.markdown("Un portal público para que sus nuevos clientes se registren. El sistema captura sus datos, obtiene su **firma digital**, valida su identidad con un **código OTP** por email, genera el **PDF legal** (Habeas Data) y lo archiva automáticamente en Google Drive y Google Sheets.")
        
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Razón Social*", "Mi Empresa S.A.S.", key="demo_rs")
                st.text_input("NIT*", "900.123.456-7", key="demo_nit")
                st.text_input("Email de Facturación*", "pagos@miempresa.com", key="demo_email_fact")
                st.text_input("Email de Notificaciones (para OTP)*", "gerencia@miempresa.com", key="demo_email_otp")
            with col2:
                st.text_input("Representante Legal*", "Juan Pérez", key="demo_rl")
                st.text_input("C.C. del Representante*", "1.234.567.890", key="demo_cc")
                st.info("Por favor, firme en el recuadro:")
                
                # --- CORRECCIÓN 3: Descomentar st_canvas ---
                st_canvas(
                    stroke_width=3, stroke_color="#000000",
                    background_color="#FFFFFF", height=130, width=400,
                    key="canvas_demo"
                )
            
            st.text_input("Código OTP enviado a gerencia@miempresa.com", "******", max_chars=6, key="demo_otp")
            if st.button("Finalizar Vinculación y Generar PDF (Demo)", use_container_width=True, type="primary"):
                st.success("¡Vinculación Simulada! En una implementación real, esto generaría un PDF legal y lo archivaría en la nube.")
                st.balloons()

    with tab2:
        st.subheader("El Agente IA (Chatbot de WhatsApp)")
        st.markdown("Esta es la pieza que lo une todo. Un Chatbot con **Inteligencia Artificial (Gemini de Google)** conectado en tiempo real a su ecosistema de datos. Sus clientes y vendedores pueden auto-gestionar consultas 24/7.")
        
        with st.container(border=True):
            st.subheader("Simulación de Chat (WhatsApp)")
            
            st.chat_message("user").write("Hola, ¿cuál es mi deuda y tienen stock de 'Disco de Corte Inox'?")
            
            with st.chat_message("assistant"):
                st.write("¡Hola! Soy **DATO**, tu asistente de IA en **GM-DATOVATE**. Claro, estoy consultando tu información... 🕵️‍♂️")
                # st.spinner("Consultando Base de Clientes, Cartera e Inventario...")
                
                # Simulación de la respuesta del bot
                st.markdown(f"""
                    ¡Listo!
                    
                    1.  **Estado de Cartera:** Tienes una deuda vencida de **$1,250,000**. La factura más antigua tiene 45 días.
                    2.  **Stock de 'Disco de Corte Inox' (Ref: A-101):**
                        * **Bodega CEDI:** 5,200 unidades
                        * **Tienda Pereira:** 450 unidades
                    
                    ¿Te gustaría que te envíe el estado de cuenta a tu correo o te ayude a encontrar otro producto?
                """)

        with st.expander("Ver el 'Cerebro' del Bot (Fragmento de Lógica)"):
            st.code("""
# El "cerebro" del bot: un prompt de sistema que le dice quién es y qué herramientas puede usar.
system_instruction = (
    "Eres DATO, el asistente experto de GM-DATOVATE."
    "Tu misión es ayudar a los clientes con sus consultas de forma amable, cercana y natural."
    
    "PROTOCOLO DE SEGURIDAD MÁXIMA:"
    "Nunca entregues información financiera (deudas o historial) sin validar al cliente con NIT y Código de Cliente usando las herramientas seguras."
    
    "HERRAMIENTAS DISPONIBLES:"
    "- verificar_cliente_existente(nit)"
    "- consultar_estado_cliente_seguro(nit, codigo_cliente)"
    "- consultar_stock_producto(nombre_producto)"
    "- consultar_precio_producto(nombre_producto)"
)
            """, language="python")

def render_pagina_contacto():
    """Renderiza la página final de Contacto / CTA."""
    
    # Ancla para el botón "Solicitar Consulta"
    st.markdown('<div id="contacto"></div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="section-container contact-form-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"""
            <h2 style="border: none; color: {COLOR_PRIMARIO};">Hablemos de su Transformación Digital 🚀</h2>
            <p style="font-size: 1.1rem; color: {COLOR_TEXTO_SECUNDARIO};">
                Lo que ha visto en este portafolio no es una teoría; es una 
                <strong>demostración de sistemas reales, funcionales y probados</strong>
                que ya están generando un valor incalculable.
                <br><br>
                ¿Está listo para dejar de "administrar" su negocio y empezar a "dirigirlo"? 
                Complete el formulario y uno de nuestros arquitectos de soluciones 
                se pondrá en contacto con usted.
            </p>
            """, unsafe_allow_html=True)
        
        with col2:
            with st.form(key="contact_form"):
                st.subheader("Iniciemos la Conversación")
                c1, c2 = st.columns(2)
                nombre = c1.text_input("Su Nombre*")
                empresa = c2.text_input("Su Empresa*")
                email = c1.text_input("Su Correo Electrónico*")
                telefono = c2.text_input("Su Teléfono/WhatsApp")
                
                desafio = st.text_area(
                    "¿Cuál es su mayor desafío operativo o de datos en este momento?*",
                    placeholder="Ej: 'Mi inventario nunca cuadra', 'Mi equipo de ventas es muy lento para cotizar', 'No tengo idea de mi cartera vencida en tiempo real'..."
                )
                
                submit = st.form_submit_button("Solicitar Consulta Estratégica", use_container_width=True, type="primary")
                
                if submit:
                    if not all([nombre, empresa, email, desafio]):
                        st.warning("Por favor, complete todos los campos marcados con *.")
                    else:
                        # Aquí iría tu lógica de envío de correo (usando yagmail, smtplib, o una API como Formspree)
                        st.success(f"¡Gracias, {nombre}! He recibido su solicitud. Nos pondremos en contacto con usted en {email} muy pronto.")
                        st.balloons()
                        
        st.markdown('</div>', unsafe_allow_html=True)

# ======================================================================================
# --- NAVEGACIÓN PRINCIPAL (NUEVA ESTRUCTURA) ---
# (Se elimina la barra lateral y se usa un flujo de página única)
# ======================================================================================

# 1. Renderiza la página de "Inicio" (Hero + Resumen + Equipo)
# Esta parte SIEMPRE es visible.
render_pagina_inicio()

# 2. Título para la sección de demos
st.markdown("<h2 style='text-align: center; border: none; margin-top: 4rem; margin-bottom: 0rem; padding-bottom: 0; color: #0D3B66;'>Explore las Demos Interactivas</h2>", unsafe_allow_html=True)

# 3. Pestañas (Tabs) para las demos interactivas
# Esta es la nueva navegación principal para las demos.
tab_com, tab_ops, tab_fin, tab_int = st.tabs([
    "🧠 Inteligencia Comercial",
    "🏭 Operaciones y Logística",
    "🏦 Finanzas y Tesorería",
    "🤖 Integración y Futuro (IA)"
])

with tab_com:
    render_pagina_comercial()

with tab_ops:
    render_pagina_operaciones()

with tab_fin:
    render_pagina_finanzas()

with tab_int:
    render_pagina_integracion()

# 4. Renderiza el formulario de contacto al final de la página.
st.divider()
render_pagina_contacto()

# --- Footer Personalizado ---
st.markdown(f"""
<div style="background-color: {COLOR_PRIMARIO}; color: {COLOR_FONDO_SECUNDARIO}; padding: 2rem; text-align: center; margin-top: 3rem;">
    <p style="color: white; margin: 0;">
        © {datetime.now().year} GM-DATOVATE. Todos los derechos reservados.<br>
        Transformando Datos en Decisiones Estratégicas.
    </p>
</div>
""", unsafe_allow_html=True)
