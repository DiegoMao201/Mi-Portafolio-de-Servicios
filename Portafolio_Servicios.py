# -*- coding: utf-8 -*-
# ======================================================================================
# PORTAFOLIO DE SERVICIOS ESTRATÉGICOS: GM-DATOVATE
# VERSIÓN: 2.0 (Demo Interactiva de Ecosistema Empresarial)
#
# DESCRIPCIÓN: Este portafolio interactivo simula un ecosistema empresarial
# completo (BI, Ventas, Operaciones, Finanzas, IA) para demostrar el
# valor y la capacidad técnica de GM-DATOVATE.
# ======================================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import base64
from datetime import datetime, timedelta
import urllib.parse
from fpdf import FPDF
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="GM-DATOVATE | Ecosistemas de Inteligencia Empresarial",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PALETA DE COLORES Y ESTILOS ---
COLOR_PRIMARIO = "#0D3B66"  # Azul profundo (Confianza, Inteligencia)
COLOR_SECUNDARIO = "#1A73E8" # Azul brillante (Tecnología, Innovación)
COLOR_ACENTO_ROJO = "#F94144"   # Rojo vivo (Acción, Alerta)
COLOR_ACENTO_VERDE = "#43AA8B"  # Verde (Finanzas, Crecimiento)
COLOR_FONDO = "#F7F9FC"    # Fondo gris muy claro
COLOR_FONDO_SIDEBAR = "#FFFFFF" # Sidebar clara
COLOR_TEXTO = "#2F2F2F"
COLOR_TEXTO_SIDEBAR = "#0D3B66"

st.markdown(f"""
<style>
    /* --- Contenedor Principal --- */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    .stApp {{
        background-color: {COLOR_FONDO};
        color: {COLOR_TEXTO};
    }}

    /* --- Títulos y Texto --- */
    h1, h2, h3 {{
        color: {COLOR_PRIMARIO};
        font-weight: 700;
    }}
    h1 {{
        font-size: 2.5rem;
    }}
    h2 {{
        font-size: 2rem;
        border-bottom: 3px solid {COLOR_ACENTO_ROJO};
        padding-bottom: 5px;
        margin-top: 2rem;
    }}
    h3 {{
        font-size: 1.5rem;
        color: {COLOR_SECUNDARIO};
        margin-top: 1.5rem;
    }}

    /* --- Barra Lateral --- */
    [data-testid="stSidebar"] {{
        background-color: {COLOR_FONDO_SIDEBAR};
        border-right: 1px solid #E0E0E0;
    }}
    [data-testid="stSidebar"] .stRadio > label {{
        font-size: 1.1rem;
        font-weight: 600;
        color: {COLOR_TEXTO_SIDEBAR};
        padding-top: 10px;
        padding-bottom: 10px;
    }}
    [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] span {{
        background-color: #DDEEFE;
        border-color: {COLOR_PRIMARIO};
    }}
    [data-testid="stSidebar"] .stRadio [data-baseweb="radio"] span[data-checked="true"] {{
        background-color: {COLOR_ACENTO_ROJO};
        border-color: {COLOR_ACENTO_ROJO};
    }}
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        color: {COLOR_PRIMARIO};
    }}

    /* --- Botones --- */
    .stButton>button {{
        border-radius: 8px;
        border: 2px solid {COLOR_PRIMARIO};
        background-color: {COLOR_PRIMARIO};
        color: white;
        font-weight: bold;
        transition: all 0.3s;
        padding: 0.5rem 1rem;
    }}
    .stButton>button:hover {{
        background-color: {COLOR_SECUNDARIO};
        border-color: {COLOR_SECUNDARIO};
        transform: scale(1.02);
    }}
    .stButton>button[kind="secondary"] {{
        background-color: transparent;
        color: {COLOR_PRIMARIO};
        border-color: {COLOR_PRIMARIO};
    }}
    .stButton>button[kind="secondary"]:hover {{
        background-color: {COLOR_FONDO};
        color: {COLOR_ACENTO_ROJO};
        border-color: {COLOR_ACENTO_ROJO};
    }}
    /* Botón especial de WhatsApp */
    .stButton>button.whatsapp-button {{
        background-color: {COLOR_ACENTO_VERDE};
        border-color: {COLOR_ACENTO_VERDE};
    }}
    .stButton>button.whatsapp-button:hover {{
        background-color: #368a73;
        border-color: #368a73;
    }}
    /* Botón especial de PDF */
    .stButton>button.pdf-button {{
        background-color: {COLOR_ACENTO_ROJO};
        border-color: {COLOR_ACENTO_ROJO};
    }}
    .stButton>button.pdf-button:hover {{
        background-color: #c23335;
        border-color: #c23335;
    }}

    /* --- Contenedores y Métricas --- */
    .stMetric {{
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #E0E0E0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        background-color: transparent;
        border-bottom: 3px solid #C0C0C0;
    }}
    .stTabs [aria-selected="true"] {{
        border-bottom: 3px solid {COLOR_ACENTO_ROJO};
        color: {COLOR_ACENTO_ROJO};
        font-weight: bold;
    }}
    [data-testid="stExpander"] {{
        background-color: #FFFFFF;
        border-radius: 10px;
        border: 1px solid #E0E0E0;
    }}
</style>
""", unsafe_allow_html=True)


# ======================================================================================
# --- DATOS DE EJEMPLO PARA LAS DEMOSTRACIONES ---
# ======================================================================================

@st.cache_data
def get_sample_data():
    """Crea y cachea todos los DataFrames de ejemplo para las demos."""
    data = {}

    # Para Demo 1: Inteligencia Comercial (BI Gerencial)
    data['ventas_vendedor'] = pd.DataFrame({
        'Vendedor': ['DIEGO GARCIA', 'ANGELA CONTRERAS', 'PABLO MAFLA', 'MARY LUZ TREJOS'],
        'Ventas ($)': [120_000_000, 95_000_000, 88_000_000, 75_000_000],
        'Meta ($)': [110_000_000, 100_000_000, 90_000_000, 80_000_000],
    })
    data['ventas_vendedor']['Avance (%)'] = (data['ventas_vendedor']['Ventas ($)'] / data['ventas_vendedor']['Meta ($)']) * 100

    # Para Demo 2: Operaciones (Sugerencia de Abastecimiento)
    data['sugerencia_abastecimiento'] = pd.DataFrame({
        'SKU': ['A-101', 'B-202', 'C-303', 'D-404'],
        'Producto': ['Disco Corte 4-1/2"', 'Tornillo Drywall 6x1', 'Electrodo 6013', 'Gafa de Seguridad'],
        'Stock (Total)': [500, 15000, 800, 120],
        'Stock Tránsito': [0, 5000, 0, 100],
        'Necesidad Real': [200, 10000, 500, 150],
        'Sugerencia Traslado': [0, 0, 300, 0],
        'Sugerencia Compra': [0, 0, 200, 50]
    })
    
    # Para Demo 3: Finanzas (Cartera por Antigüedad)
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

    # Para Demo 4: Integración (Simulación de Covinoc)
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
    def header(self):
        try:
            # Simula la carga de un logo (puedes reemplazar "LOGO.png" si tienes uno)
            # self.image("LOGO.png", 10, 8, 33) 
            pass
        except:
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'GM-DATOVATE (Logo)', 0, 1, 'L')
            
        self.set_font('Arial', 'B', 15)
        self.set_text_color(int(COLOR_PRIMARIO[1:3], 16), int(COLOR_PRIMARIO[3:5], 16), int(COLOR_PRIMARIO[5:7], 16))
        self.cell(0, 10, self.title, 0, 1, 'R')
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, f'Generado por GM-DATOVATE el {datetime.now().strftime("%Y-%m-%d")}', 0, 1, 'R')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Documento de demostración generado por el Ecosistema de Inteligencia GM-DATOVATE - Página %s' % self.page_no(), 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(int(COLOR_PRIMARIO[1:3], 16), int(COLOR_PRIMARIO[3:5], 16), int(COLOR_PRIMARIO[5:7], 16))
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, title, 0, 1, 'L', fill=True)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, body)
        self.ln()
        
    def add_table(self, df):
        # Header
        self.set_font('Arial', 'B', 9)
        self.set_fill_color(int(COLOR_SECUNDARIO[1:3], 16), int(COLOR_SECUNDARIO[3:5], 16), int(COLOR_SECUNDARIO[5:7], 16))
        self.set_text_color(255, 255, 255)
        col_widths = [self.w / 1.5 / len(df.columns)] * len(df.columns)
        
        for i, header in enumerate(df.columns):
            self.cell(col_widths[i], 7, str(header), 1, 0, 'C', fill=True)
        self.ln()

        # Body
        self.set_font('Arial', '', 9)
        self.set_text_color(0, 0, 0)
        self.set_fill_color(245, 245, 245)
        fill = False
        for _, row in df.iterrows():
            for i, item in enumerate(row):
                self.cell(col_widths[i], 6, str(item), 1, 0, 'L', fill=fill)
            self.ln()
            fill = not fill

@st.cache_data
def generar_demo_pdf(df, title, intro_text):
    """Genera un PDF de demostración en memoria."""
    pdf = DemoPDF()
    pdf.title = title
    pdf.add_page()
    pdf.chapter_body(intro_text)
    pdf.add_table(df)
    return pdf.output(dest='S').encode('latin-1')

@st.cache_data
def generar_demo_excel(df_dict):
    """Genera un Excel de demostración en memoria con múltiples hojas."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for sheet_name, df in df_dict.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name, startrow=1)
            
            # --- Formato Profesional ---
            ws = writer.sheets[sheet_name]
            
            # Estilos
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color=COLOR_PRIMARIO.replace("#",""), fill_type="solid")
            total_font = Font(bold=True)
            total_fill = PatternFill(start_color="E0E0E0", fill_type="solid")
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
                max_len = max(len(str(col)), df[col].astype(str).map(len).max())
                ws.column_dimensions[get_column_letter(i)].width = max_len + 2
                
                # Aplicar formatos
                if df[col].dtype == 'datetime64[ns]':
                    for c in ws[get_column_letter(i)][2:]:
                        c.number_format = date_format
                if 'Monto' in col or 'Valor' in col:
                    for c in ws[get_column_letter(i)][2:]:
                        c.number_format = currency_format

            # Título
            ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(df.columns))
            title_cell = ws.cell(row=1, column=1)
            title_cell.value = sheet_name
            title_cell.font = Font(size=16, bold=True, color=COLOR_PRIMARIO.replace("#",""))
            title_cell.alignment = Alignment(horizontal='center')
    
    return output.getvalue()


# ======================================================================================
# --- FUNCIONES DE RENDERIZADO DE PÁGINAS ---
# ======================================================================================

def render_pagina_inicio():
    """Renderiza la página de bienvenida y el pitch de valor."""
    st.title("De Datos Aislados a un Ecosistema de Negocios Inteligente.")
    st.markdown("### Su socio estratégico para la transformación digital y la inteligencia de negocios.")
    
    st.markdown(f"""
        En el entorno actual, la data no es solo un reporte; es el activo más valioso de su empresa.
        El problema es que, en la mayoría de las compañías, este activo está fragmentado:
        
        * Las **Ventas** están en un CRM o en Excels.
        * El **Inventario** está en el ERP.
        * Las **Finanzas** están en un software contable.
        * La **Operación** está en cuadernos, planillas y grupos de WhatsApp.
        
        **GM-DATOVATE** no solo construye 'apps' o 'dashboards'. Diseñamos y ejecutamos su **Sistema Operativo Central**: 
        un ecosistema digital que unifica este caos. 
        
        Conectamos cada pilar de su negocio en un solo cerebro digital
        inteligente, automatizado y accesible, que no solo le muestra lo que pasó, sino que le dice
        **qué hacer a continuación**.
    """)

    st.markdown("---")

    # Diagrama del Ecosistema
    st.graphviz_chart(f"""
        digraph "Ecosistema Digital GM-DATOVATE" {{
            node [shape=box, style="filled,rounded", fontname="Arial", fontsize=12];
            graph [bgcolor="transparent"];

            subgraph cluster_input {{
                label = "FUENTES DE DATOS";
                style = "rounded";
                color = "{COLOR_PRIMARIO}";
                fontcolor = "{COLOR_PRIMARIO}";
                
                erp [label="ERP / Archivos CSV\n(Dropbox, FTP, etc.)", shape=cylinder, fillcolor="#E3F2FD"];
                sheets [label="Bases de Datos en la Nube\n(Google Sheets)", shape=cylinder, fillcolor="#E3F2FD"];
                manual [label="Entrada Manual\n(Apps de Campo)", shape=cylinder, fillcolor="#E3F2FD"];
            }}

            subgraph cluster_core {{
                label = "ECOSISTEMA CENTRALIZADO (by GM-DATOVATE)";
                style = "rounded";
                color = "{COLOR_PRIMARIO}";
                fontcolor = "{COLOR_PRIMARIO}";

                node [fillcolor="#BBDEFB"];
                ventas [label="Módulo de Ventas\n(Cotizador, Catálogo)"];
                operaciones [label="Módulo de Operaciones\n(Inventario, Abastecimiento)"];
                finanzas [label="Módulo Financiero\n(Cartera, Tesorería, Integración)"];
                legal [label="Módulo Legal\n(Vinculación Digital, OTP, Firma)"];
            }}

            subgraph cluster_output {{
                label = "INTELIGENCIA ACCIONABLE";
                style = "rounded";
                color = "{COLOR_ACENTO_ROJO}";
                fontcolor = "{COLOR_ACENTO_ROJO}";

                node [fillcolor="#FFEBEE", shape=diamond, style="filled,rounded"];
                bi [label="Dashboards de BI\n(Gerencia, Ventas)"];
                ia [label="Agente IA\n(Chatbot WhatsApp)"];
                alertas [label="Recomendaciones Proactivas\n(Email, App)"];
            }}
            
            erp -> operaciones;
            erp -> finanzas;
            sheets -> ventas;
            sheets -> operaciones;
            manual -> operaciones;
            manual -> finanzas;
            legal -> ventas;

            ventas -> bi;
            operaciones -> bi;
            finanzas -> bi;
            
            bi -> alertas;
            ventas -> ia;
            operaciones -> ia;
            finanzas -> ia;
            alertas -> ia;
        }}
    """)
    
    st.markdown("---")
    st.subheader("Explore las demostraciones en el menú para ver este ecosistema en acción.")

def render_pagina_comercial():
    """Demo de la Suite de Inteligencia Comercial."""
    st.title("🚀 Suite de Inteligencia Comercial y Ventas")
    st.markdown("Deje que sus datos le digan cómo vender más. Automatizamos la prospección, la cotización y el análisis de rendimiento.")
    
    # --- Demo 1: Cotizador y Catálogo Interactivo ---
    st.header("Demo 1: Catálogo Interactivo y Cotizador Profesional")
    st.markdown("Transformamos sus listas de precios estáticas en una herramienta de ventas interactiva. El vendedor puede navegar, ver imágenes, consultar stock *real* de todas las bodegas y generar un PDF profesional en segundos.")
    
    with st.container(border=True):
        col1, col2 = st.columns([1.5, 1])
        with col1:
            st.subheader("Catálogo de Productos")
            # Simulación de una tarjeta de producto
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
            # Simulación del carrito
            st.info("🛒 Carrito de Cotización")
            st.dataframe(pd.DataFrame({
                'Referencia': ['A-101', 'B-202'],
                'Producto': ['Disco de Corte 4-1/2"', 'Tornillo Drywall 6x1'],
                'Cantidad': [50, 2000],
                'Vlr. Unitario': [1800, 150]
            }), use_container_width=True, hide_index=True)
            
            # --- Botón de descarga de PDF (Funcional) ---
            pdf_data = generar_demo_pdf(
                pd.DataFrame({'Producto': ['Disco de Corte'], 'Cant': [50], 'Valor': [1800]}),
                "Cotización de Ejemplo",
                "Este es un ejemplo de cotización profesional generada automáticamente."
            )
            st.download_button(
                label="📄 Descargar PDF Profesional (Demo)",
                data=pdf_data,
                file_name="Demo_Cotizacion_GM-DATOVATE.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    # --- Demo 2: BI Gerencial ---
    st.header("Demo 2: Dashboard de BI Gerencial (En Tiempo Real)")
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

    # --- Demo 3: Asistente Proactivo (IA) ---
    st.header("Demo 3: Asistente Proactivo (Análisis RFM y Venta Cruzada)")
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

def render_pagina_operaciones():
    """Demo de la Suite de Operaciones y Logística."""
    st.title("🏭 Suite de Operaciones y Logística")
    st.markdown("Automatización de la cadena de suministro, desde el proveedor hasta la bodega, con inteligencia de datos.")
    
    # --- Demo 1: Sincronización de Inventario (ETL) ---
    st.header("Demo 1: Sincronización Maestra de Inventario (ETL)")
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

    # --- Demo 2: Abastecimiento Inteligente ---
    st.header("Demo 2: Tablero de Abastecimiento Inteligente")
    st.markdown("Este módulo va más allá de mostrar el stock. Calcula la **Necesidad Real** (descontando lo que ya está en tránsito) y genera un **Plan de Traslados Inteligente** para ahorrar capital de trabajo antes de sugerir una compra.")
    
    with st.container(border=True):
        st.subheader("Sugerencias de Abastecimiento (Demo)")
        st.dataframe(
            SAMPLE_DATA['sugerencia_abastecimiento'].style
                .applymap(lambda x: f'background-color: {COLOR_ACENTO_VERDE}; color: white; font-weight: bold;' if x > 0 else '', subset=['Sugerencia Traslado'])
                .applymap(lambda x: f'background-color: {COLOR_ACENTO_ROJO}; color: white; font-weight: bold;' if x > 0 else '', subset=['Sugerencia Compra'])
                .format({"Stock Actual (Total)": "{:,.0f}", "Stock en Tránsito": "{:,.0f}", "Necesidad Real": "{:,.0f}", "Sugerencia Traslado": "{:,.0f}", "Sugerencia Compra": "{:,.0f}"}),
            use_container_width=True, hide_index=True
        )
        st.markdown("""
            * **Fila 2 (Tornillo):** El sistema ve que la necesidad (10,000) es cubierta por lo que hay en tránsito (5,000) y el stock (15,000). **Acción: No hacer nada.**
            * **Fila 3 (Electrodo):** El sistema detecta una necesidad de 500. Antes de comprar, encuentra 300 en otra tienda y sugiere un **Traslado (Ahorro)**. Solo pide comprar los 200 restantes.
        """)

    # --- Demo 3: Control de Inventario Móvil ---
    st.header("Demo 3: Aplicación Móvil de Conteo Físico")
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
            st.button("Registrar Cantidad", type="primary", use_container_width=True, help="En la app real, esto actualiza el total sin recargar.")

        with col2:
            st.subheader("Resumen de Conteo del Operario")
            st.dataframe(pd.DataFrame({
                'Producto': ['Gafa de Seguridad', 'Disco de Corte'],
                'Teórico': [120, 500],
                'Contado': [118, 505],
                'Historial Conteo': ["+50, +50, +10, +8", "+500, +5"],
                'Diferencia': [-2, 5]
            }), use_container_width=True, hide_index=True)
            st.button("Enviar Conteo Final para Revisión", use_container_width=True, help="En la app real, esto guarda en GSheets y notifica al gerente.")

def render_pagina_finanzas():
    """Demo de la Suite Financiera y de Tesorería."""
    st.title("🏦 Suite Financiera y de Tesorería")
    st.markdown("Controle el flujo de caja, automatice la contabilidad y gestione el riesgo de cartera como nunca antes.")
    
    # --- Demo 1: Automatización Contable ---
    st.header("Demo 1: Automatización Contable (Cuadres y Recibos)")
    st.markdown("Eliminamos la digitación manual y los errores. Las tiendas llenan un formulario digital (`Cuadre de Caja`) o procesan un Excel (`Recibos de Caja`). El sistema valida, asigna cuentas contables y genera el archivo `.txt` listo para el ERP.")

    with st.container(border=True):
        st.subheader("Simulación de Cuadre de Caja Digital")
        c1, c2 = st.columns(2)
        c1.text_input("Tienda", "Armenia", disabled=True, key="demo_tienda")
        # --- CORRECCIÓN DEL ERROR ---
        # Importar datetime al inicio del archivo: from datetime import datetime
        c2.date_input("Fecha", datetime.now().date(), disabled=True, key="demo_fecha")
        # --- FIN DE LA CORRECCIÓN ---
        st.number_input("Venta Total (Sistema)", 5_000_000, disabled=True, key="demo_venta_total")
        
        # Simulación de desglose
        st.dataframe(pd.DataFrame({
            'Tipo': ['Tarjetas', 'Consignaciones', 'Gastos', 'Efectivo Entregado'],
            'Valor': [2_500_000, 1_500_000, 200_000, 800_000]
        }), use_container_width=True, hide_index=True)

        st.metric("Total Desglose", "$ 5,000,000")
        st.metric("DIFERENCIA", "$ 0", delta="CUADRE PERFECTO", delta_color="off")
        
        # --- Botón de descarga de TXT (Funcional) ---
        demo_txt = "FECHA|CONSECUTIVO|CUENTA|...|DEBITO|CREDITO\n2025-11-05|1001|111005|...|2500000|0\n2025-11-05|1001|413501|...|0|2500000\n"
        st.download_button(
            label="1. 💾 Descargar .TXT para ERP (Demo)",
            data=demo_txt,
            file_name="Demo_Contable_GM-DATOVATE.txt",
            mime="text/plain",
            use_container_width=True
        )

    # --- Demo 2: Dashboard de Cartera y Cobranzas ---
    st.header("Demo 2: Dashboard de Gestión de Cartera (AR)")
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
        
        # --- Demostración de Gestión de Cliente ---
        st.subheader("Gestión de Cliente Individual (Demo)")
        cliente_demo = SAMPLE_DATA['cartera_detalle'][SAMPLE_DATA['cartera_detalle']['Días Vencido'] > 60].iloc[0]
        
        st.warning(f"**Cliente Seleccionado: {cliente_demo['Cliente']}**")
        st.dataframe(cliente_demo.to_frame().T[['Factura', 'Días Vencido', 'Monto']], use_container_width=True, hide_index=True)
        
        # Mensaje de WhatsApp pre-hecho
        mensaje_wa = (
            f"👋 ¡Hola {cliente_demo['Cliente']}! Te saludamos desde [Tu Empresa].\n\n"
            f"Te recordamos que tu factura *{cliente_demo['Factura']}* por *${cliente_demo['Monto']:,.0f}* "
            f"presenta *{cliente_demo['Días Vencido']} días* de vencimiento.\n\n"
            f"Agradecemos tu pronta gestión. Puedes pagar en nuestro portal: [Link de Pago]"
        )
        url_wa = f"https://wa.me/{cliente_demo['Teléfono']}?text={urllib.parse.quote(mensaje_wa)}"

        c1, c2, c3 = st.columns(3)
        # Botón PDF Funcional
        pdf_cartera = generar_demo_pdf(
            cliente_demo.to_frame().T[['Factura', 'Fecha Vencimiento', 'Días Vencido', 'Monto']],
            "Estado de Cuenta (Demo)",
            f"Estado de cuenta detallado para {cliente_demo['Cliente']}."
        )
        c1.download_button(
            label="📄 Descargar PDF (Demo)", data=pdf_cartera,
            file_name=f"Cartera_{cliente_demo['Cliente']}.pdf", mime="application/pdf",
            use_container_width=True
        )
        # Botón Email (Simulado)
        c2.button("✉️ Enviar Email (Demo)", use_container_width=True)
        # Botón WhatsApp (Funcional)
        st.markdown(f"""
        <style> .st-emotion-cache-s4p1ri {{ width: 100%; }} </style>
        <div class="st-emotion-cache-1jicfl2 e19lei0e1">
            <a href="{url_wa}" target="_blank" style="text-decoration: none;">
                <button class="st-emotion-cache-7ym5gk e19lei0e0 whatsapp-button" style="width: 100%;">
                    📲 Enviar WhatsApp (Demo)
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)


    # --- Demo 3: Integración de Riesgo (Covinoc) ---
    st.header("Demo 3: Automatización de Cobranza Legal (Integración)")
    st.markdown("El sistema cruza automáticamente nuestra cartera con reportes de agencias externas (como Covinoc). Identifica discrepancias y genera los archivos de acción masiva, automatizando la gestión de riesgo.")
    
    with st.container(border=True):
        st.subheader("Resultados del Cruce Automático con Covinoc (Demo)")
        tab1, tab2 = st.tabs(["Facturas a Subir (Nuevas en Cartera)", "Facturas a Exonerar (Pagadas)"])
        
        # --- Botones de descarga de Excel (Funcionales) ---
        excel_demo_data = generar_demo_excel({
            "Facturas_a_Subir": SAMPLE_DATA['covinoc_subir'],
            "Facturas_a_Exonerar": SAMPLE_DATA['covinoc_exonerar']
        })
        
        with tab1:
            st.warning("Acción: Estas facturas están en nuestra cartera pero no en Covinoc. Deben subirse.")
            st.dataframe(SAMPLE_DATA['covinoc_subir'], use_container_width=True, hide_index=True)
            st.download_button(
                "📥 Descargar Excel para Subida Masiva (Demo)", 
                excel_demo_data, 
                file_name="Demo_Reporte_Covinoc_GM-DATOVATE.xlsx", 
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                use_container_width=True
            )
        with tab2:
            st.success("Acción: Estas facturas ya fueron pagadas (no están en cartera) pero siguen activas en Covinoc. Deben exonerarse.")
            st.dataframe(SAMPLE_DATA['covinoc_exonerar'], use_container_width=True, hide_index=True)
            st.download_button(
                "📥 Descargar Excel para Exoneración Masiva (Demo)", 
                excel_demo_data, 
                file_name="Demo_Reporte_Covinoc_GM-DATOVATE.xlsx", 
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                use_container_width=True
            )

def render_pagina_integracion():
    """Demo de la Suite de Integración y Futuro (IA)."""
    st.title("🤖 Integración Total y Futuro con IA")
    st.markdown("Conectamos todos los procesos, desde la vinculación de un cliente hasta el servicio post-venta con IA.")

    # --- Demo 1: Vinculación Digital de Clientes ---
    st.header("Demo 1: Portal de Vinculación Digital de Clientes")
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
            st_canvas(
                stroke_width=3, stroke_color="#000000",
                background_color="#FFFFFF", height=130, width=400,
                key="canvas_demo"
            )
        
        st.text_input("Código OTP enviado a gerencia@miempresa.com", "******", max_chars=6, key="demo_otp")
        if st.button("Finalizar Vinculación y Generar PDF (Demo)", use_container_width=True, type="primary"):
            st.success("¡Vinculación Simulada! En una implementación real, esto generaría un PDF legal y lo archivaría en la nube.")
            st.balloons()

    # --- Demo 2: El Agente IA (Chatbot de WhatsApp) ---
    st.header("Demo 2: El Agente IA (Chatbot de WhatsApp)")
    st.markdown("Esta es la pieza que lo une todo. Un Chatbot con **Inteligencia Artificial (Gemini de Google)** conectado en tiempo real a su ecosistema de datos. Sus clientes y vendedores pueden auto-gestionar consultas 24/7.")
    
    with st.container(border=True):
        st.subheader("Simulación de Chat (WhatsApp)")
        
        st.chat_message("user").write("Hola, ¿cuál es mi deuda y tienen stock de 'Disco de Corte Inox'?")
        
        with st.chat_message("assistant"):
            st.write("¡Hola! Soy **DATO**, tu asistente de IA en **GM-DATOVATE**. Claro, estoy consultando tu información... 🕵️‍♂️")
            st.spinner("Consultando Base de Clientes, Cartera e Inventario...")
            
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
    st.title("Hablemos de su Transformación Digital 🚀")
    
    st.markdown(f"""
    Somos **GM-DATOVATE**, un equipo de arquitectos de soluciones de datos especializados en
    la creación de ecosistemas empresariales integrales.
    
    A diferencia de otros, no ofrecemos 'dashboards' aislados. Ofrecemos una **transformación operativa completa**:
    un sistema nervioso digital que conecta todas las áreas de su empresa, automatiza tareas críticas
    y le entrega la inteligencia que necesita para tomar decisiones ganadoras.
    
    Lo que ha visto en este portafolio no es una teoría; es una **demostración de sistemas reales, funcionales y probados**
    que ya están generando un valor incalculable.
    
    ¿Está listo para dejar de "administrar" su negocio y empezar a "dirigirlo"?
    """)
    
    st.divider()
    
    with st.form(key="contact_form"):
        st.subheader("Iniciemos la Conversación")
        col1, col2 = st.columns(2)
        nombre = col1.text_input("Su Nombre*")
        empresa = col2.text_input("Su Empresa*")
        email = col1.text_input("Su Correo Electrónico*")
        telefono = col2.text_input("Su Teléfono/WhatsApp")
        
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
                st.success(f"¡Gracias, {nombre}! He recibido su solicitud. Me pondré en contacto con usted en {email} muy pronto.")
                st.balloons()

# ======================================================================================
# --- NAVEGACIÓN PRINCIPAL (BARRA LATERAL) ---
# ======================================================================================

# --- Encabezado de la Barra Lateral ---
st.sidebar.markdown(f"""
<div style="text-align: center; padding: 1rem 0;">
    <h1 style="color: {COLOR_PRIMARIO}; font-size: 2.8rem; margin: 0; padding: 0;">GM-DATOVATE</h1>
    <p style="color: {COLOR_ACENTO_ROJO}; font-size: 1rem; margin: 0; padding: 0; font-weight: 700;">ECOSISTEMAS DE DATOS</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.header("Portafolio de Soluciones")

# Menú de navegación
paginas = {
    "🏠 Inicio": render_pagina_inicio,
    "🧠 Inteligencia Comercial": render_pagina_comercial,
    "🏭 Operaciones y Logística": render_pagina_operaciones,
    "🏦 Finanzas y Tesorería": render_pagina_finanzas,
    "🤖 Integración y Futuro (IA)": render_pagina_integracion,
    "✉️ Hablemos": render_pagina_contacto
}

seleccion = st.sidebar.radio(
    "Explore nuestro ecosistema:",
    list(paginas.keys())
)

st.sidebar.markdown("---")

# --- NUEVA SECCIÓN: SOBRE NOSOTROS ---
st.sidebar.header("Sobre Nosotros")
st.sidebar.markdown(f"""
<p style="color: {COLOR_TEXTO}; font-size: 0.9rem;">
    En **GM-DATOVATE**, transformamos datos en decisiones.
</p>
<ul style="color: {COLOR_TEXTO_SIDEBAR}; font-size: 0.9rem; padding-left: 20px;">
    <li><b>Diego Mauricio García</b><br><i>Arquitecto de Datos y Desarrollador Principal</i></li>
    <li style="margin-top: 10px;"><b>Pablo Cesar Mafla</b><br><i>Estratega Comercial y de Negocios</i></li>
</ul>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info(
    "Esta es una **demostración interactiva**."
    "Todos los datos son de ejemplo y simulan un ecosistema empresarial real."
)

# Renderiza la página seleccionada
paginas[seleccion]()
