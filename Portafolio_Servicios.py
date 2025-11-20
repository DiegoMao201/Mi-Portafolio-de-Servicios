import streamlit as st
import base64
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="GM-DATOVATE | Ecosistemas de Inteligencia",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LÓGICA DE IMÁGENES (Tu código blindado) ---
@st.cache_data
def get_image_base64(file_path):
    try:
        with open(file_path, "rb") as img_file:
            extension = file_path.split('.')[-1].lower()
            mime_type = 'image/jpeg' if extension in ['jpg', 'jpeg'] else 'image/png'
            return f"data:{mime_type};base64,{base64.b64encode(img_file.read()).decode('utf-8')}"
    except Exception:
        return "https://via.placeholder.com/150" # Fallback

# Rutas relativas seguras
try:
    _SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _SCRIPT_DIR = os.path.abspath(os.getcwd())
_ASSETS_PATH = os.path.join(_SCRIPT_DIR, "assets")

IMG_DIEGO = get_image_base64(os.path.join(_ASSETS_PATH, "foto_diego.png"))
IMG_PABLO = get_image_base64(os.path.join(_ASSETS_PATH, "foto_pablo.png"))

# --- CSS PROFESIONAL (ESTILO CORPORATIVO) ---
st.markdown("""
<style>
    /* Variables de Color */
    :root { --primary: #0D3B66; --accent: #F94144; --bg-light: #F0F2F6; }
    
    /* Tipografía y Reset */
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; color: var(--primary); }
    
    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #0D3B66 0%, #1A73E8 100%);
        padding: 4rem 2rem;
        border-radius: 0 0 20px 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hero h1 { color: white !important; font-size: 3.5rem; font-weight: 800; }
    .hero p { font-size: 1.2rem; opacity: 0.9; max-width: 800px; margin: 0 auto; }
    
    /* Tarjetas de Servicios */
    .service-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
        height: 100%;
        border: 1px solid #eee;
    }
    .service-card:hover { transform: translateY(-5px); border-color: var(--primary); }
    
    /* Botones Personalizados */
    div.stButton > button {
        background-color: var(--primary);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    /* Foto Equipo */
    .team-img {
        border-radius: 50%;
        border: 4px solid var(--primary);
        width: 120px;
        height: 120px;
        object-fit: cover;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. SECCIÓN HERO (Venta de Alto Impacto) ---
st.markdown("""
<div class="hero">
    <h1>GM-DATOVATE</h1>
    <h3>El Sistema Operativo de su Empresa, Impulsado por Datos.</h3>
    <br>
    <p>No hacemos simples reportes. Construimos Ecosistemas de Inteligencia que conectan Ventas, Inventario y Finanzas en un solo cerebro digital.</p>
</div>
""", unsafe_allow_html=True)

# --- 2. NAVEGACIÓN A DEMOS (El centro de la app) ---
st.markdown("### 🚀 Explore Nuestras Soluciones")
st.markdown("Seleccione un módulo para ver la demostración en tiempo real:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="service-card">
        <div style="font-size: 3rem;">📦</div>
        <h3>Inventario Inteligente</h3>
        <p>Optimización de stock, detección de quiebres y predicción de demanda con algoritmos avanzados.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("") # Espacio
    if st.button("👉 Ver Demo Inventario", key="btn_inv", use_container_width=True):
        st.switch_page("pages/1_Inventario_Nexus.py")

with col2:
    st.markdown("""
    <div class="service-card">
        <div style="font-size: 3rem;">💰</div>
        <h3>Finanzas & Cartera</h3>
        <p>Automatización de recaudo, flujo de caja y gestión de riesgo automatizada.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.button("🚧 Próximamente", key="btn_fin", disabled=True, use_container_width=True)

with col3:
    st.markdown("""
    <div class="service-card">
        <div style="font-size: 3rem;">🧠</div>
        <h3>Inteligencia Comercial</h3>
        <p>Segmentación de clientes y agentes de venta potenciados por Inteligencia Artificial.</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.button("🚧 Próximamente", key="btn_com", disabled=True, use_container_width=True)

st.divider()

# --- 3. QUIÉNES SOMOS (Tu equipo) ---
st.markdown("<h2 style='text-align: center;'>Arquitectos de Soluciones</h2>", unsafe_allow_html=True)
c_team1, c_team2 = st.columns(2)

with c_team1:
    st.markdown(f"""
    <div style="text-align: center;">
        <img src="{IMG_DIEGO}" class="team-img">
        <h3>Diego Mauricio García</h3>
        <p><strong>Arquitecto de Datos Líder</strong><br>
        Transformando procesos manuales en flujos automatizados.</p>
    </div>
    """, unsafe_allow_html=True)

with c_team2:
    st.markdown(f"""
    <div style="text-align: center;">
        <img src="{IMG_PABLO}" class="team-img">
        <h3>Pablo Cesar Mafla</h3>
        <p><strong>Estratega de Negocios</strong><br>
        Alineando la tecnología con la rentabilidad empresarial.</p>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>© 2025 GM-DATOVATE | Transformación Digital Real</div>", unsafe_allow_html=True)
