import streamlit as st
from PIL import Image
import base64

# ==============================================================================
# 1. CONFIGURACIÓN DEL NÚCLEO (SYSTEM CONFIG)
# ==============================================================================
st.set_page_config(
    page_title="GM-DATOVATE | Enterprise Intelligence Ecosystem",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. ARQUITECTURA DE DISEÑO (CSS PREMIUM)
# ==============================================================================
st.markdown("""
<style>
    /* IMPORTACIÓN DE FUENTES MODERNAS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    /* GLOBAL RESET */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        scroll-behavior: smooth;
    }

    /* OCULTAR ELEMENTOS NATIVOS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* FONDO SOFISTICADO */
    .stApp {
        background-color: #F8FAFC;
        background-image: 
            radial-gradient(at 0% 0%, rgba(37, 99, 235, 0.05) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(139, 92, 246, 0.05) 0px, transparent 50%);
    }

    /* HERO SECTION - TÍTULO PRINCIPAL */
    .hero-container {
        padding: 80px 20px 60px 20px;
        text-align: center;
        border-bottom: 1px solid rgba(226, 232, 240, 0.8);
        margin-bottom: 40px;
    }
    
    .company-badge {
        background: linear-gradient(90deg, #EFF6FF 0%, #DBEAFE 100%);
        color: #1E40AF;
        padding: 8px 20px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        border: 1px solid #BFDBFE;
        display: inline-block;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.1);
    }

    .main-headline {
        font-size: 4rem;
        font-weight: 900;
        color: #0F172A;
        letter-spacing: -2px;
        line-height: 1.1;
        margin-bottom: 20px;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #2563EB 0%, #0EA5E9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .sub-headline {
        font-size: 1.3rem;
        color: #64748B;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.6;
        font-weight: 300;
    }

    /* CARDS DE PRODUCTOS (GLASSMORPHISM) */
    .tech-card {
        background: white;
        border: 1px solid #F1F5F9;
        border-radius: 20px;
        padding: 40px 30px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.03);
    }
    
    .tech-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        border-color: #BAE6FD;
    }
    
    .card-icon-box {
        width: 60px;
        height: 60px;
        background: #F8FAFC;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        margin-bottom: 20px;
        border: 1px solid #E2E8F0;
    }

    .card-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 10px;
    }
    
    .card-text {
        color: #64748B;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 25px;
    }

    /* BOTONES PERSONALIZADOS */
    .stButton > button {
        width: 100%;
        background: #0F172A;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #334155;
        box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.2);
        transform: scale(1.02);
    }

    /* SECCIÓN PERFIL CEO */
    .ceo-section {
        margin-top: 80px;
        background: #0F172A;
        border-radius: 30px;
        padding: 60px;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    /* DETALLES FINALES */
    hr { border-color: #E2E8F0; margin: 60px 0; }

</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. INTERFAZ VISUAL (FRONTEND)
# ==============================================================================

# --- HERO HEADER ---
st.markdown("""
<div class="hero-container">
    <div class="company-badge">NEXUS PRO ENTERPRISE v3.0</div>
    <div class="main-headline">
        Arquitectura de Datos<br>
        <span class="gradient-text">Que Piensa por su Negocio</span>
    </div>
    <div class="sub-headline">
        GM-DATOVATE elimina la intuición y la reemplaza con precisión matemática. 
        Un ecosistema unificado de Inteligencia Artificial para Finanzas, Logística y Fiscalización.
    </div>
</div>
""", unsafe_allow_html=True)

# --- GRID DE SOLUCIONES (NAVIGATION HUB) ---
st.markdown("### 💠 Explore el Ecosistema")
st.write("") # Espaciador

col1, col2, col3 = st.columns(3, gap="medium")

# MÓDULO 1: ESTRATEGIA
with col1:
    st.markdown("""
    <div class="tech-card">
        <div class="card-icon-box">🧠</div>
        <div class="card-title">Nexus Strategy</div>
        <div class="card-text">
            El cerebro financiero. Algoritmos que detectan capital atrapado ("Huesos") y maximizan productos rentables ("Diamantes") conectados a Odoo ERP.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    # NAVEGACIÓN PRECISA: Debe coincidir con el nombre del archivo en 'pages/'
    if st.button("Iniciar Dashboard Financiero ➝", key="btn_strat"):
        st.switch_page("pages/1_Estrategia.py")

# MÓDULO 2: LOGÍSTICA
with col2:
    st.markdown("""
    <div class="tech-card">
        <div class="card-icon-box">⚡</div>
        <div class="card-title">Nexus Logistics</div>
        <div class="card-text">
            Torre de control de abastecimiento. Automatización de compras y rebalanceo de stock entre bodegas mediante predicción de demanda IA.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Iniciar Centro Logístico ➝", key="btn_log"):
        st.switch_page("pages/2_Logistica.py")

# MÓDULO 3: RECEPCIÓN
with col3:
    st.markdown("""
    <div class="tech-card">
        <div class="card-icon-box">🛡️</div>
        <div class="card-title">Nexus Guard</div>
        <div class="card-text">
            Auditoría fiscal blindada. Procesamiento automático de XML (DIAN) vs Recepción Física para eliminar fugas de dinero y errores humanos.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("Iniciar Auditoría Fiscal ➝", key="btn_guard"):
        st.switch_page("pages/3_Recepcion.py")

# --- PERFIL CORPORATIVO ---
st.markdown("""
<div class="ceo-section">
    <div style="text-align: center; max-width: 800px; margin: 0 auto;">
        <div style="color: #38BDF8; font-weight: 700; letter-spacing: 2px; font-size: 0.9rem; text-transform: uppercase; margin-bottom: 20px;">
            Visión & Arquitectura
        </div>
        <h2 style="font-size: 2.5rem; margin-bottom: 30px;">Diego Mauricio García</h2>
        <p style="font-size: 1.25rem; line-height: 1.8; color: #CBD5E1; font-style: italic;">
            "La verdadera transformación digital no es comprar software, es construir un sistema nervioso central para su empresa. 
            En GM-Datovate, no entregamos reportes; entregamos decisiones."
        </p>
        <div style="margin-top: 40px; display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
            <span style="background: rgba(255,255,255,0.1); padding: 8px 20px; border-radius: 20px; font-size: 0.85rem; border: 1px solid rgba(255,255,255,0.2);">CEO & Founder</span>
            <span style="background: rgba(255,255,255,0.1); padding: 8px 20px; border-radius: 20px; font-size: 0.85rem; border: 1px solid rgba(255,255,255,0.2);">Data Architect</span>
            <span style="background: rgba(255,255,255,0.1); padding: 8px 20px; border-radius: 20px; font-size: 0.85rem; border: 1px solid rgba(255,255,255,0.2);">Cloud Expert</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- FORMULARIO DE CONTACTO ---
st.write("")
st.write("")
st.markdown("### 🤝 Solicitar Acceso Enterprise")
c_contact, c_data = st.columns([2, 1])

with c_contact:
    with st.form("main_contact"):
        col_input1, col_input2 = st.columns(2)
        with col_input1:
            name = st.text_input("Nombre del Directivo")
        with col_input2:
            mail = st.text_input("Email Corporativo")
        
        challenge = st.text_area("Desafío Operativo Actual")
        
        if st.form_submit_button("Enviar Solicitud al Servidor"):
            st.success("✅ Solicitud procesada correctamente. El equipo de ingeniería lo contactará en breve.")

with c_data:
    st.info("""
    **GM-DATOVATE HQ**
    
    🌐 www.datovatenexuspro.com
    📧 gerencia@datovatenexuspro.com
    🔐 Servidor: DigitalOcean NYC1
    """)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94A3B8; font-size: 0.8rem;">
    © 2025 GM-DATOVATE | Infraestructura Segura Potenciada por Coolify & Docker
</div>
""", unsafe_allow_html=True)
