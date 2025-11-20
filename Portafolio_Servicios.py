import streamlit as st
import base64
import os

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTADO GLOBAL ---
st.set_page_config(
    page_title="GM-DATOVATE | Ecosistema de Inteligencia",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. FUNCIONES DE ASSETS E IMÁGENES ---
@st.cache_data
def get_img_as_base64(file_path):
    """Convierte imágenes locales a base64 para usar en HTML/CSS"""
    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode()
    except Exception:
        pass
    return None

# Carga de imagen de perfil
current_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(current_dir, "assets", "foto_diego.png")
img_base64 = get_img_as_base64(img_path)
# Fallback si no encuentra la imagen local
foto_diego_src = f"data:image/png;base64,{img_base64}" if img_base64 else "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# --- 3. CSS PREMIUM (MEJORADO PARA CONTRASTE) ---
st.markdown(f"""
<style>
    /* IMPORTAR FUENTE MODERNA */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: #0E1117; /* Fondo Oscuro Profundo */
        color: #F0F2F6; /* Texto mucho más claro para contraste */
    }}

    /* --- HERO SECTION (ENCABEZADO) --- */
    .hero-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 80px 20px 50px 20px;
        background: radial-gradient(circle at center, #1a202c 0%, #0E1117 80%);
        border-radius: 0 0 50px 50px;
        margin-bottom: 60px;
        border-bottom: 1px solid #2d3748;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
    }}

    .company-tag {{
        background-color: rgba(6, 182, 212, 0.15);
        color: #22d3ee; /* Cian más brillante */
        padding: 6px 18px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
        border: 1px solid rgba(6, 182, 212, 0.4);
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.2);
    }}

    .main-title {{
        font-size: 5rem;
        font-weight: 900;
        margin: 0;
        line-height: 1.1;
        /* Degradado más brillante para el título */
        background: linear-gradient(90deg, #FFFFFF 20%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(255,255,255,0.1);
    }}

    .highlight-text {{
        /* Degradado azul eléctrico más intenso */
        background: linear-gradient(90deg, #3b82f6, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .subtitle {{
        font-size: 1.35rem;
        color: #E2E8F0; /* Gris muy claro */
        max-width: 800px;
        margin-top: 25px;
        line-height: 1.7;
        font-weight: 400;
    }}

    /* --- CARDS DE FLUJO (VIDRIO / NEON) --- */
    .flow-card {{
        background: rgba(30, 41, 59, 0.75); /* Un poco más opaco para legibilidad */
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 35px;
        border-radius: 24px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Efecto rebote sutil */
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}

    .flow-card:hover {{
        transform: translateY(-12px) scale(1.02);
        background: rgba(30, 41, 59, 1);
        border-color: #3b82f6;
        box-shadow: 0 25px 50px -12px rgba(37, 99, 235, 0.5);
    }}

    .card-icon {{ font-size: 3.5rem; margin-bottom: 20px; filter: drop-shadow(0 0 10px rgba(255,255,255,0.3)); }}
    .card-title {{ font-size: 1.6rem; font-weight: 700; color: #FFFFFF; margin-bottom: 12px; }}
    /* Descripción de la tarjeta mucho más clara */
    .card-desc {{ font-size: 1rem; color: #E2E8F0; margin-bottom: 25px; line-height: 1.6; }}

    /* --- PERFIL DE LIDERAZGO --- */
    .profile-box {{
        display: flex;
        align-items: center;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 45px;
        border-radius: 30px;
        border: 1px solid rgba(51, 65, 85, 0.7);
        margin-top: 80px;
        box-shadow: 0 20px 40px -10px rgba(0,0,0,0.4);
        position: relative;
        overflow: hidden;
    }}
    
    /* Efecto de luz sutil en el perfil */
    .profile-box::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.1) 0%, transparent 70%);
        pointer-events: none;
    }}
    
    .profile-img {{
        width: 160px;
        height: 160px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #06B6D4;
        margin-right: 35px;
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.5);
        z-index: 1;
    }}

    /* --- BOTONES PERSONALIZADOS --- */
    div.stButton > button {{
        width: 100%;
        /* Degradado más vibrante */
        background: linear-gradient(90deg, #2563EB 0%, #06B6D4 100%);
        color: white;
        border: none;
        padding: 14px 20px;
        font-weight: 700;
        letter-spacing: 0.5px;
        border-radius: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }}
    div.stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 20px -5px rgba(37, 99, 235, 0.6);
        background: linear-gradient(90deg, #1D4ED8 0%, #0891b2 100%);
    }}
    
    /* Estilo para el texto dentro de los modales (st.dialog) */
    .modal-highlight {{
        color: #06B6D4;
        font-weight: bold;
    }}
    .modal-text {{
        font-size: 1.1rem;
        line-height: 1.7;
        color: #E2E8F0;
    }}

</style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- 4. DEFINICIÓN DE MODALES DE VALOR (BI & IA PITCH) ---
# ==============================================================================

@st.dialog("📊 Inteligencia de Inventarios y Capital")
def open_inventory_modal():
    st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <span style='font-size: 4rem;'>🧠</span>
    </div>
    <h3 style='text-align: center; color: #FFFFFF;'>Del Caos Reactivo a la Precisión Predictiva</h3>
    <div class="modal-text">
        <p>La gestión tradicional de inventarios basada en "intuición" o Excel estático está costando millones en capital inmovilizado y ventas perdidas.
        Este módulo no es solo un registro; es un <b>cerebro analítico</b>.</p>
        <ul>
            <li><b>Análisis de Capital con IA:</b> Detecta automáticamente dónde está atrapado su dinero (excedentes) y dónde está perdiendo oportunidades (quiebres), sugiriendo acciones de liquidación o compra.</li>
            <li><b>Predicción de Demanda:</b> Algoritmos que analizan patrones históricos para anticipar necesidades futuras, optimizando el flujo de caja.</li>
            <li><b>Visión Gerencial 360°:</b> KPIs en tiempo real sobre la salud financiera de su stock.</li>
        </ul>
        <p><b>El Resultado:</b> Menos inventario obsoleto, mayor disponibilidad de productos clave y liberación significativa de capital de trabajo.</p>
    </div>
    <hr style="border-color: rgba(255,255,255,0.1);">
    """, unsafe_allow_html=True)
    
    # Botón de acción final dentro del modal
    if st.button("🚀 Ver Demo: Dashboard Gerencial", key="modal_btn_inv"):
        st.switch_page("pages/1_Inventario_Nexus.py")


@st.dialog("🚚 Logística Autónoma y Abastecimiento")
def open_logistics_modal():
    st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <span style='font-size: 4rem;'>⚡</span>
    </div>
    <h3 style='text-align: center; color: #FFFFFF;'>El Sistema Nervioso de su Cadena de Suministro</h3>
    <div class="modal-text">
        <p>Convertimos las necesidades detectadas por el módulo de inventario en acciones logísticas inmediatas. 
        Este es el motor operativo que asegura que el producto correcto esté en el lugar correcto.</p>
        <ul>
            <li><b>Compras Inteligentes:</b> Generación automática de órdenes de compra sugeridas basadas en la demanda real y tiempos de entrega del proveedor, eliminando el "yo creo que necesitamos X".</li>
            <li><b>Balanceo de Red (Traslados):</b> El sistema identifica que una sucursal tiene exceso mientras otra tiene escasez, sugiriendo traslados internos antes de comprar nuevo stock.</li>
            <li><b>Torre de Control:</b> Visibilidad centralizada del estado de todas las órdenes y movimientos en curso.</li>
        </ul>
        <p><b>El Valor:</b> Reducción de costos de compra, optimización de la red de distribución y agilidad operativa sin precedentes.</p>
    </div>
    <hr style="border-color: rgba(255,255,255,0.1);">
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Ver Demo: Centro de Operaciones", key="modal_btn_log"):
        st.switch_page("pages/2_Operaciones_Logistica.py")


@st.dialog("📥 Recepción Digital Sin Fricción (XML)")
def open_reception_modal():
    st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <span style='font-size: 4rem;'>🛡️</span>
    </div>
    <h3 style='text-align: center; color: #FFFFFF;'>Blindaje de la Entrada de Mercancía</h3>
    <div class="modal-text">
        <p>El 80% de los errores de inventario nacen en una mala recepción. Este módulo elimina la entrada manual de datos y utiliza la factura electrónica (XML DIAN) como única fuente de verdad.</p>
        <ul>
            <li><b>Homologación Automática:</b> El sistema lee el XML del proveedor y cruza automáticamente sus referencias con su catálogo interno, detectando productos nuevos o cambios de precio al instante.</li>
            <li><b>Conciliación Ciega Digital:</b> El equipo de bodega realiza el conteo físico en el sistema, y este lo compara automáticamente contra lo facturado en el XML, resaltando discrepancias (sobrantes/faltantes) en segundos.</li>
            <li><b>Integridad de Datos:</b> Garantiza que lo que se paga es exactamente lo que entró físicamente al almacén.</li>
        </ul>
        <p><b>El Impacto:</b> Eliminación de errores humanos de digitación, detección inmediata de fraudes o errores de proveedores y actualización del inventario en tiempo récord.</p>
    </div>
    <hr style="border-color: rgba(255,255,255,0.1);">
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Ver Demo: Recepción Inteligente", key="modal_btn_xml"):
        st.switch_page("pages/3_Recepcion_Inteligente.py")


# ==============================================================================
# --- 5. ESTRUCTURA VISUAL PRINCIPAL ---
# ==============================================================================

# >>> HERO SECTION (Centralizada y Brillante)
st.markdown("""
<div class="hero-container">
    <div class="company-tag">Arquitectura de Datos Empresarial & IA</div>
    <h1 class="main-title">GM-<span class="highlight-text">DATOVATE</span></h1>
    <p class="subtitle">
        Transformamos el caos operativo en <b>Ventaja Competitiva</b>.
        <br>Una suite integrada que utiliza Inteligencia Artificial para sincronizar Inventarios, Logística y Finanzas en tiempo real. El futuro no se reporta, se construye.
    </p>
</div>
""", unsafe_allow_html=True)

# >>> FLUJO DE TRABAJO (GRID)
st.write("")
st.markdown("<h3 style='text-align: center; margin-bottom: 50px; font-size: 2rem;'>🚀 Ecosistema NEXUS: Explore el Valor de Negocio</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

# --- CARD 1: INVENTARIOS ---
with col1:
    st.markdown("""
    <div class="flow-card">
        <div>
            <div class="card-icon">📊</div>
            <div class="card-title">1. Control & Estrategia</div>
            <p class="card-desc">
                El cerebro financiero de la operación. Análisis predictivo de capital de trabajo, detección de riesgos de quiebre y optimización de inventario con IA.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    # El botón ahora abre el MODAL, no cambia de página directamente
    if st.button("Explorar Valor e Inteligencia ➝", key="btn_open_inv"):
        open_inventory_modal()

# --- CARD 2: LOGÍSTICA ---
with col2:
    st.markdown("""
    <div class="flow-card">
        <div>
            <div class="card-icon">🚚</div>
            <div class="card-title">2. Abastecimiento Inteligente</div>
            <p class="card-desc">
                El brazo ejecutor táctico. Automatización de compras basada en demanda real y rebalanceo autónomo de stock entre bodegas.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explorar Valor Logístico ➝", key="btn_open_log"):
        open_logistics_modal()

# --- CARD 3: RECEPCIÓN XML ---
with col3:
    st.markdown("""
    <div class="flow-card">
        <div>
            <div class="card-icon">📥</div>
            <div class="card-title">3. Recepción Blindada (XML)</div>
            <p class="card-desc">
                La puerta de entrada digital. Procesamiento automático de facturas electrónicas (DIAN) y conciliación fiscal vs. física sin intervención manual.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explorar Valor de Automatización ➝", key="btn_open_xml"):
        open_reception_modal()

# >>> PERFIL DEL LÍDER (REDITADO PARA MAXIMO IMPACTO)
st.write("")
st.write("")
st.write("")

col_spacer_l, col_profile_main, col_spacer_r = st.columns([1, 6, 1])

with col_profile_main:
    st.markdown(f"""
    <div class="profile-box" style="z-index: 2;">
        <img src="{foto_diego_src}" class="profile-img" alt="Diego Mauricio García">
        <div>
            <h4 style="color: #06B6D4; margin:0 0 10px 0; font-weight: 800; letter-spacing:1.5px; text-transform: uppercase;">Visión & Arquitectura Tecnológica</h4>
            <h2 style="color: white; margin: 0 0 20px 0; font-size: 2.5rem; text-shadow: 0 0 20px rgba(6, 182, 212, 0.3);">Diego Mauricio García</h2>
            <p style="color: #E2E8F0; font-size: 1.15rem; line-height: 1.8; font-style: italic; border-left: 4px solid #06B6D4; padding-left: 20px; margin-bottom: 25px;">
                "En GM-Datovate no vendemos software, diseñamos el sistema nervioso central de su organización. Mi obsesión es eliminar la fricción operativa inútil mediante arquitecturas de datos que piensan, aprenden y actúan por sí mismas, liberando el potencial humano para la estrategia."
            </p>
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                <span style="background: rgba(15, 23, 42, 0.8); border: 1px solid #06B6D4; color: #06B6D4; padding: 8px 15px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">CEO & Founder</span>
                <span style="background: rgba(15, 23, 42, 0.8); border: 1px solid #06B6D4; color: #06B6D4; padding: 8px 15px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">Lead Data Architect</span>
                <span style="background: rgba(15, 23, 42, 0.8); border: 1px solid #06B6D4; color: #06B6D4; padding: 8px 15px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">AI & Python Expert</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #94A3B8; margin-top: 20px; margin-bottom: 40px;'>© 2025 GM-DATOVATE. Arquitectura de Sistemas Operativos Inteligentes.</div>", unsafe_allow_html=True)
