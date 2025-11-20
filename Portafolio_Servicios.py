import streamlit as st
import base64
import os

# --- CONFIGURACIÓN INICIAL DE PÁGINA ---
st.set_page_config(
    page_title="GM-DATOVATE | Arquitectura de Datos",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- GESTIÓN DE ASSETS (IMÁGENES) ---
@st.cache_data
def get_image_base64(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as img_file:
                extension = file_path.split('.')[-1].lower()
                mime_type = 'image/jpeg' if extension in ['jpg', 'jpeg'] else 'image/png'
                return f"data:{mime_type};base64,{base64.b64encode(img_file.read()).decode('utf-8')}"
    except Exception:
        pass
    return "https://img.freepik.com/free-vector/blue-futuristic-networking-technology_53876-100679.jpg" # Fallback Tech Image

# Definición de rutas
try:
    _SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _SCRIPT_DIR = os.path.abspath(os.getcwd())
_ASSETS_PATH = os.path.join(_SCRIPT_DIR, "assets")

# Cargar fotos (Asegúrate de tener 'foto_diego.png' en la carpeta assets)
IMG_DIEGO = get_image_base64(os.path.join(_ASSETS_PATH, "foto_diego.png"))
IMG_BG_TECH = "https://img.freepik.com/free-vector/gradient-network-connection-background_23-2148879892.jpg"

# --- CSS AVANZADO: HIGH-END TECH STYLE ---
st.markdown(f"""
<style>
    /* --- FUENTES Y COLORES GLOBALES --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    :root {{
        --primary-dark: #0F172A;
        --primary-blue: #2563EB;
        --accent-cyan: #06B6D4;
        --text-light: #F8FAFC;
        --card-bg: #ffffff;
    }}

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: #1E293B;
    }}

    /* --- FONDO Y AMBIENTE --- */
    .stApp {{
        background-color: #F8FAFC;
        background-image: radial-gradient(#E2E8F0 1px, transparent 1px);
        background-size: 20px 20px;
    }}

    /* --- HERO SECTION (Títulos) --- */
    .hero-container {{
        text-align: center;
        padding: 60px 20px;
        margin-bottom: 40px;
        background: white;
        border-radius: 24px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.05);
        border: 1px solid rgba(255,255,255,0.5);
    }}

    .gradient-text {{
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--accent-cyan) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -1px;
    }}

    .subtitle {{
        font-size: 1.25rem;
        color: #64748B;
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.6;
    }}

    /* --- TARJETAS DE SERVICIOS (GLASSMORPHISM) --- */
    .tech-card {{
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 30px;
        border: 1px solid rgba(255,255,255,0.6);
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        transition: all 0.3s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }}

    .tech-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 15px 30px rgba(37, 99, 235, 0.15);
        border-color: var(--primary-blue);
    }}
    
    .tech-card::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 4px;
        background: linear-gradient(90deg, var(--primary-blue), var(--accent-cyan));
    }}

    /* --- PERFIL LÍDER --- */
    .profile-section {{
        background: linear-gradient(145deg, #0F172A, #1E293B);
        color: white;
        border-radius: 20px;
        padding: 40px;
        margin-top: 60px;
        box-shadow: 0 20px 40px rgba(15, 23, 42, 0.3);
        display: flex;
        align-items: center;
        gap: 30px;
    }}

    .profile-img {{
        width: 180px;
        height: 180px;
        border-radius: 20px;
        object-fit: cover;
        border: 4px solid var(--accent-cyan);
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
    }}

    /* --- BOTONES --- */
    div.stButton > button {{
        background: linear-gradient(90deg, var(--primary-blue) 0%, #1D4ED8 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: 0.2s;
        width: 100%;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
    }}
    div.stButton > button:hover {{
        transform: scale(1.02);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
    }}
    
</style>
""", unsafe_allow_html=True)

# --- 1. HERO SECTION: IMPACTO VISUAL ---
st.markdown("""
<div class="hero-container">
    <h4 style="color: #2563EB; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px;">Tecnología Empresarial</h4>
    <h1 style="font-size: 4rem; line-height: 1.1; margin-bottom: 20px;">
        Bienvenido a <span class="gradient-text">GM-DATOVATE</span>
    </h1>
    <p class="subtitle">
        Transformamos el caos de datos en <b>Inteligencia de Negocios</b>. 
        Nuestras soluciones no solo reportan el pasado, <br>construyen el futuro operativo de su empresa.
    </p>
</div>
""", unsafe_allow_html=True)

# --- 2. ECOSISTEMA DE SOLUCIONES (GRID) ---
st.write("")
st.markdown("### ⚡ Nuestras Soluciones")
st.write("")

col1, col2, col3 = st.columns(3)

# --- Módulo 1: NEXUS (El que acabamos de programar) ---
with col1:
    st.markdown("""
    <div class="tech-card">
        <div style="font-size: 2.5rem; margin-bottom: 15px;">🧬</div>
        <h3 style="margin-top:0;">NEXUS Recepción</h3>
        <p style="color: #64748B; font-size: 0.95rem;">
            El estándar de oro en logística de entrada. Procesamiento automático de XML (DIAN), 
            homologación inteligente de SKUs y detección de precios en tiempo real.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    # NOTA: Asegúrate de que el archivo se llame 'Nexus_Recepcion.py'
    if st.button("🚀 Iniciar Nexus Engine", use_container_width=True):
        try:
            st.switch_page("Nexus_Recepcion.py")
        except Exception:
            st.error("⚠️ Archivo 'Nexus_Recepcion.py' no encontrado. Verifique la ruta.")

# --- Módulo 2: FINANZAS ---
with col2:
    st.markdown("""
    <div class="tech-card">
        <div style="font-size: 2.5rem; margin-bottom: 15px;">💎</div>
        <h3 style="margin-top:0;">Tesorería 4.0</h3>
        <p style="color: #64748B; font-size: 0.95rem;">
            Control total del flujo de caja. Algoritmos de predicción de recaudo, 
            gestión de riesgo de cartera y automatización de cuentas por pagar.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.button("🔒 Acceso Restringido", disabled=True, use_container_width=True)

# --- Módulo 3: CRM / IA ---
with col3:
    st.markdown("""
    <div class="tech-card">
        <div style="font-size: 2.5rem; margin-bottom: 15px;">🧠</div>
        <h3 style="margin-top:0;">Cortex AI</h3>
        <p style="color: #64748B; font-size: 0.95rem;">
            Inteligencia Artificial aplicada a ventas. Segmentación dinámica de clientes, 
            recomendación de productos y agentes de venta autónomos.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    st.button("🛠️ En Desarrollo", disabled=True, use_container_width=True)

# --- 3. LA MENTE MAESTRA (PERFIL SOLO DIEGO) ---
st.write("")
st.write("")

# Diseño responsive para la sección de perfil
col_prof_spacer, col_prof_content, col_prof_spacer2 = st.columns([0.5, 5, 0.5])

with col_prof_content:
    st.markdown(f"""
    <div class="profile-section">
        <div style="flex-shrink: 0;">
            <img src="{IMG_DIEGO}" class="profile-img" alt="Diego Mauricio García">
        </div>
        <div>
            <h4 style="color: #06B6D4; text-transform: uppercase; letter-spacing: 1px; margin: 0;">Liderazgo Tecnológico</h4>
            <h2 style="color: white; margin: 10px 0;">Diego Mauricio García</h2>
            <p style="color: #CBD5E1; font-size: 1.1rem; margin-bottom: 20px;">
                CEO & Lead Data Architect
            </p>
            <p style="color: #94A3B8; font-size: 0.95rem; line-height: 1.6;">
                "En GM-Datovate no escribimos código, diseñamos ecosistemas. Mi visión es eliminar la fricción operativa 
                mediante arquitecturas de datos que piensan por sí mismas. Cada módulo que desarrollamos es un paso 
                hacia la empresa autónoma del futuro."
            </p>
            <div style="margin-top: 20px; display: flex; gap: 15px;">
                <span style="background: rgba(255,255,255,0.1); padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; color: #06B6D4; border: 1px solid #06B6D4;">Python Expert</span>
                <span style="background: rgba(255,255,255,0.1); padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; color: #06B6D4; border: 1px solid #06B6D4;">Data Science</span>
                <span style="background: rgba(255,255,255,0.1); padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; color: #06B6D4; border: 1px solid #06B6D4;">Cloud Architecture</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.write("")
st.write("")
st.divider()
col_ft1, col_ft2 = st.columns([1, 1])
with col_ft1:
    st.markdown("<small style='color: #94A3B8;'>© 2025 GM-DATOVATE. Todos los derechos reservados.</small>", unsafe_allow_html=True)
with col_ft2:
    st.markdown("<div style='text-align: right;'><small style='color: #94A3B8;'>Potenciado por Streamlit & Python</small></div>", unsafe_allow_html=True)
