import streamlit as st
from PIL import Image
import base64

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="GM-DATOVATE | Enterprise AI Solutions",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed" # Ocultamos sidebar para parecer web corporativa
)

# --- CSS PROFESIONAL (ESTILO "SAAS" MODERNO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Ocultar elementos nativos de Streamlit para look Web */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* FONDO Y COLORES */
    .stApp {
        background-color: #ffffff;
        background-image: radial-gradient(#e2e8f0 1px, transparent 1px);
        background-size: 24px 24px;
    }

    /* HERO SECTION */
    .hero-section {
        padding: 80px 20px;
        text-align: center;
        background: linear-gradient(180deg, rgba(255,255,255,0) 0%, #F8FAFC 100%);
        border-bottom: 1px solid #e2e8f0;
    }
    
    .hero-tag {
        background: #EFF6FF;
        color: #2563EB;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 20px;
        border: 1px solid #BFDBFE;
    }

    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        color: #0F172A;
        line-height: 1.1;
        margin-bottom: 20px;
        letter-spacing: -2px;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: #64748B;
        max-width: 800px;
        margin: 0 auto 40px auto;
        line-height: 1.6;
    }

    /* CARDS DE PRODUCTO */
    .feature-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 30px;
        transition: all 0.3s ease;
        height: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        border-color: #3B82F6;
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 20px;
        background: #F1F5F9;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
    }

    /* BOTONES */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        height: 45px;
        background-color: #0F172A;
        color: white;
        border: none;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #334155;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* PERFIL CEO */
    .profile-section {
        background: #0F172A;
        color: white;
        border-radius: 24px;
        padding: 60px;
        margin-top: 80px;
        position: relative;
        overflow: hidden;
    }
    
    .profile-role {
        color: #38BDF8;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-size: 0.9rem;
    }

</style>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("""
<div class="hero-section">
    <div class="hero-tag">Nexus Pro Enterprise v3.0</div>
    <div class="hero-title">
        Inteligencia de Negocios<br>
        <span style="background: linear-gradient(90deg, #2563EB, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Que Toma Decisiones</span>
    </div>
    <div class="hero-subtitle">
        GM-DATOVATE transforma sus datos en activos líquidos. 
        Deje de usar Excel como base de datos y empiece a usar algoritmos como gerentes.
    </div>
</div>
""", unsafe_allow_html=True)

# --- PRODUCTOS (GRID) ---
st.markdown("### 🚀 Nuestra Suite de Soluciones")
st.write("")

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">🧠</div>
        <h3 style="margin:0; color:#0F172A;">NEXUS STRATEGY</h3>
        <p style="color:#64748B; margin-top:10px;">
            Dashboard financiero conectado a Odoo/ERP. Detecta capital atrapado (Huesos) y productos estrella (Diamantes) en tiempo real.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Ver Demo Estrategia ➝", key="btn1"):
        st.switch_page("pages/1_📊_Inventario_Nexus.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">⚡</div>
        <h3 style="margin:0; color:#0F172A;">NEXUS LOGISTICS</h3>
        <p style="color:#64748B; margin-top:10px;">
            Torre de control de abastecimiento. Sugiere compras automáticas y traslados entre bodegas para evitar quiebres de stock.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Ver Demo Logística ➝", key="btn2"):
        st.switch_page("pages/2_🚚_Logistica_IA.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="card-icon">🛡️</div>
        <h3 style="margin:0; color:#0F172A;">NEXUS XML GUARD</h3>
        <p style="color:#64748B; margin-top:10px;">
            Auditoría fiscal automática. Cruza el XML de la DIAN contra la recepción física para eliminar pérdidas y errores humanos.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Ver Demo Recepción ➝", key="btn3"):
        st.switch_page("pages/3_📥_Recepcion_Blindada.py")

# --- PERFIL CEO ---
st.write("")
st.markdown("""
<div class="profile-section">
    <div style="max-width: 800px; margin: 0 auto; text-align: center;">
        <div class="profile-role">Arquitectura & Visión</div>
        <h2 style="font-size: 2.5rem; margin: 15px 0 25px 0;">Diego Mauricio García</h2>
        <p style="font-size: 1.2rem; line-height: 1.8; color: #E2E8F0; font-style: italic;">
            "La tecnología sin estrategia es solo un gasto. En GM-Datovate diseñamos arquitecturas de datos que no solo almacenan información, 
            sino que piensan por su negocio las 24 horas del día."
        </p>
        <div style="margin-top: 30px; display: flex; gap: 10px; justify-content: center;">
            <span style="background: rgba(255,255,255,0.1); padding: 5px 15px; border-radius: 20px; font-size: 0.8rem;">Python Expert</span>
            <span style="background: rgba(255,255,255,0.1); padding: 5px 15px; border-radius: 20px; font-size: 0.8rem;">Data Architect</span>
            <span style="background: rgba(255,255,255,0.1); padding: 5px 15px; border-radius: 20px; font-size: 0.8rem;">Cloud Infrastructure</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- CONTACTO (SIMULADO POR AHORA) ---
st.write("")
st.write("")
st.markdown("### 📬 ¿Listo para escalar?")
c_form, c_info = st.columns([2,1])

with c_form:
    with st.form("contact_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("Nombre Completo")
        with col_b:
            email = st.text_input("Correo Corporativo")
        msg = st.text_area("¿Qué desafío operativo quiere resolver hoy?")
        
        submitted = st.form_submit_button("Solicitar Consultoría")
        if submitted:
            st.success("✅ Solicitud enviada al servidor de GM-DATOVATE. Nos pondremos en contacto pronto.")
            # AQUÍ ES DONDE CONECTAREMOS TU BASE DE DATOS POSTGRES MÁS ADELANTE

with c_info:
    st.info("""
    **Oficina Central**
    
    🏢 GM-DATOVATE HQ
    🌐 panel.datovatenexuspro.com
    📧 gerencia@datovatenexuspro.com
    """)

st.markdown("---")
st.caption("© 2025 GM-DATOVATE | Infraestructura potenciada por DigitalOcean & Coolify")
