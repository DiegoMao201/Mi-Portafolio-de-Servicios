import streamlit as st
import base64
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="GM-DATOVATE | Ecosystem",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. GESTIÓN DE ASSETS (Imágenes) ---
@st.cache_data
def get_img_as_base64(file_path):
    """Convierte imágenes locales a base64 para usar en HTML/CSS"""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return None

# Intentar cargar foto local, si no existe usa una de internet
img_path = os.path.join(os.path.dirname(__file__), "assets", "foto_diego.png")
img_base64 = get_img_as_base64(img_path)
foto_diego_src = f"data:image/png;base64,{img_base64}" if img_base64 else "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# --- 3. CSS PREMIUM (SUPER PODEROSO & CENTRADO) ---
st.markdown(f"""
<style>
    /* IMPORTAR FUENTE MODERNA */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: #0E1117; /* Fondo Oscuro Profundo */
        color: #E0E0E0;
    }}

    /* --- HERO SECTION (ENCABEZADO) --- */
    /* Flexbox para centrado absoluto */
    .hero-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 80px 20px 40px 20px;
        background: radial-gradient(circle at center, #1a202c 0%, #0E1117 70%);
        border-radius: 0 0 50px 50px;
        margin-bottom: 50px;
        border-bottom: 1px solid #2d3748;
    }}

    .company-tag {{
        background-color: rgba(6, 182, 212, 0.1);
        color: #06B6D4;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 15px;
        border: 1px solid rgba(6, 182, 212, 0.3);
    }}

    .main-title {{
        font-size: 4.5rem; /* Texto Gigante */
        font-weight: 900;
        margin: 0;
        line-height: 1.1;
        background: linear-gradient(90deg, #FFFFFF 0%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .highlight-text {{
        background: linear-gradient(90deg, #2563EB, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .subtitle {{
        font-size: 1.3rem;
        color: #94A3B8;
        max-width: 750px;
        margin-top: 20px;
        line-height: 1.6;
        font-weight: 300;
    }}

    /* --- CARDS DE FLUJO (VIDRIO / NEON) --- */
    .flow-card {{
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 20px;
        transition: all 0.4s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}

    .flow-card:hover {{
        transform: translateY(-10px);
        background: rgba(30, 41, 59, 1);
        border-color: #2563EB;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }}

    .card-icon {{ font-size: 3rem; margin-bottom: 15px; }}
    .card-title {{ font-size: 1.5rem; font-weight: 700; color: white; margin-bottom: 10px; }}
    .card-desc {{ font-size: 0.95rem; color: #94A3B8; margin-bottom: 20px; }}

    /* --- PERFIL DE LIDERAZGO --- */
    .profile-box {{
        display: flex;
        align-items: center;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 40px;
        border-radius: 24px;
        border: 1px solid #334155;
        margin-top: 60px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }}
    
    .profile-img {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #06B6D4;
        margin-right: 30px;
    }}

    /* --- BOTONES PERSONALIZADOS --- */
    div.stButton > button {{
        width: 100%;
        background: linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        border: none;
        padding: 12px 20px;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s;
    }}
    div.stButton > button:hover {{
        transform: scale(1.03);
        box-shadow: 0 0 15px rgba(37, 99, 235, 0.5);
    }}

</style>
""", unsafe_allow_html=True)

# --- 4. ESTRUCTURA VISUAL ---

# >>> HERO SECTION (Centralizada)
st.markdown("""
<div class="hero-container">
    <div class="company-tag">Arquitectura de Datos Empresarial</div>
    <h1 class="main-title">GM-<span class="highlight-text">DATOVATE</span></h1>
    <p class="subtitle">
        Transformamos el caos operativo en <b>Inteligencia de Negocios</b>.
        <br>Una suite integrada que sincroniza Inventarios, Logística y Finanzas en tiempo real.
    </p>
</div>
""", unsafe_allow_html=True)

# >>> FLUJO DE TRABAJO (GRID)
st.write("")
st.markdown("<h3 style='text-align: center; margin-bottom: 40px;'>🚀 Ecosistema NEXUS (Selecciona un Módulo)</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# --- CARD 1: INVENTARIOS ---
# Apunta a: pages/1_Inventario_Nexus.py
with col1:
    st.markdown("""
    <div class="flow-card">
        <div>
            <div class="card-icon">📊</div>
            <div class="card-title">1. Control & Inventario</div>
            <p class="card-desc">
                El tablero de mando gerencial. Análisis de KPIs, detección de quiebres de stock, 
                excedentes inmovilizados y predicción de demanda con IA.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("") # Espacio
    if st.button("Ir al Dashboard Gerencial ➝", key="btn_inv"):
        st.switch_page("pages/1_Inventario_Nexus.py")

# --- CARD 2: LOGÍSTICA ---
# Apunta a: pages/2_Operaciones_Logistica.py
with col2:
    st.markdown("""
    <div class="flow-card">
        <div>
            <div class="card-icon">🚚</div>
            <div class="card-title">2. Logística & Ops</div>
            <p class="card-desc">
                Operación táctica. Generación automática de órdenes de compra, gestión de traslados 
                entre bodegas y tracking de proveedores.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Ir a Logística & Compras ➝", key="btn_log"):
        st.switch_page("pages/2_Operaciones_Logistica.py")

# --- CARD 3: RECEPCIÓN XML ---
# Apunta a: pages/3_Recepcion_Inteligente.py
with col3:
    st.markdown("""
    <div class="flow-card">
        <div>
            <div class="card-icon">📥</div>
            <div class="card-title">3. Recepción XML</div>
            <p class="card-desc">
                La puerta de entrada. Escaneo de facturas electrónicas (DIAN), homologación de 
                referencias y conciliación de conteo físico vs. factura.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Ir a Recepción Inteligente ➝", key="btn_xml"):
        st.switch_page("pages/3_Recepcion_Inteligente.py")

# >>> PERFIL DEL LÍDER
st.write("")
st.write("")

col_spacer, col_profile, col_spacer2 = st.columns([0.5, 4, 0.5])

with col_profile:
    st.markdown(f"""
    <div class="profile-box">
        <img src="{foto_diego_src}" class="profile-img">
        <div>
            <h4 style="color: #06B6D4; margin:0; font-weight: 700; letter-spacing:1px;">LIDERAZGO TECNOLÓGICO</h4>
            <h2 style="color: white; margin: 5px 0 15px 0;">Diego Mauricio García</h2>
            <p style="color: #CBD5E1; font-size: 1.05rem; line-height: 1.6;">
                <i>"En GM-Datovate no solo organizamos datos, construimos el sistema nervioso de su empresa. 
                Mi misión es eliminar la fricción operativa mediante arquitecturas que piensan por sí mismas."</i>
            </p>
            <div style="margin-top: 15px;">
                <span style="background: #1e293b; border: 1px solid #334155; padding: 5px 12px; border-radius: 15px; font-size: 0.8rem; margin-right: 10px;">CEO & Founder</span>
                <span style="background: #1e293b; border: 1px solid #334155; padding: 5px 12px; border-radius: 15px; font-size: 0.8rem; margin-right: 10px;">Data Architect</span>
                <span style="background: #1e293b; border: 1px solid #334155; padding: 5px 12px; border-radius: 15px; font-size: 0.8rem;">Full Stack Python</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748B; font-size: 0.8rem;'>© 2025 GM-DATOVATE. Todos los sistemas operativos.</div>", unsafe_allow_html=True)
