import streamlit as st
import base64
import os

# ==============================================================================
# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTADO GLOBAL ---
# ==============================================================================
st.set_page_config(
    page_title="GM-DATOVATE | Ecosistema de Inteligencia",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# --- 2. FUNCIONES UTILITARIAS (IMÁGENES Y ASSETS) ---
# ==============================================================================
@st.cache_data
def get_img_as_base64(file_path):
    """Convierte imágenes locales a base64 para usar en HTML/CSS."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                data = f.read()
            return base64.b64encode(data).decode()
    except Exception:
        pass
    return None

# Carga de imagen de perfil (Ajusta la ruta si es necesario)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Asegúrate de que esta carpeta y archivo existan, si no, usa el fallback
img_path = os.path.join(current_dir, "assets", "foto_diego.png")
img_base64 = get_img_as_base64(img_path)

# Fallback: Si no encuentra la foto local, usa un icono genérico
foto_diego_src = f"data:image/png;base64,{img_base64}" if img_base64 else "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# ==============================================================================
# --- 3. CSS ULTRA-PREMIUM (CORREGIDO PARA F-STRINGS) ---
# ==============================================================================
# NOTA: Usamos dobles llaves {{ }} en el CSS para evitar conflictos con f-strings de Python
st.markdown(f"""
<style>
    /* IMPORTAR FUENTE FUTURISTA */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800;900&family=Inter:wght@300;400;600&display=swap');

    /* --- ANIMACIONES KEYFRAMES --- */
    @keyframes gradient-bg {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    @keyframes float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
        100% {{ transform: translateY(0px); }}
    }}

    @keyframes pulse-glow {{
        0% {{ box-shadow: 0 0 0 0 rgba(6, 182, 212, 0.4); }}
        70% {{ box-shadow: 0 0 0 15px rgba(6, 182, 212, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(6, 182, 212, 0); }}
    }}

    @keyframes slide-up {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    /* ANIMACIÓN SHIMMER (BRILLO QUE PASA) */
    @keyframes text-shimmer {{
        0% {{ background-position: -200% center; }}
        100% {{ background-position: 200% center; }}
    }}

    /* ANIMACIÓN FLOTACIÓN 3D DEL TÍTULO */
    @keyframes title-float-3d {{
        0% {{ transform: perspective(1000px) rotateX(5deg) translateY(0); }}
        50% {{ transform: perspective(1000px) rotateX(5deg) translateY(-10px); }}
        100% {{ transform: perspective(1000px) rotateX(5deg) translateY(0); }}
    }}

    /* --- FONDO GENERAL --- */
    .stApp {{
        background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #000000);
        background-size: 400% 400%;
        animation: gradient-bg 15s ease infinite;
        color: #FFFFFF;
        font-family: 'Outfit', sans-serif;
    }}
    
    /* CLASE PARA ANIMAR ENTRADA */
    .animate-enter {{
        animation: slide-up 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    }}

    /* --- MODALES --- */
    .custom-modal-box {{
        background: rgba(17, 24, 39, 0.95);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(6, 182, 212, 0.3);
        box-shadow: 0 0 40px rgba(0,0,0,0.8);
    }}
    .modal-header-icon {{
        font-size: 3.5rem;
        text-align: center;
        display: block;
        margin-bottom: 15px;
        animation: float 3s ease-in-out infinite;
    }}
    .modal-title {{
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        font-size: 1.8rem;
        text-align: center;
        margin-bottom: 15px;
        background: linear-gradient(90deg, #22d3ee, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .modal-body-text {{
        color: #cbd5e1 !important;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 20px;
        text-align: justify;
        font-family: 'Inter', sans-serif;
    }}
    .modal-list-container {{
        background-color: rgba(0, 0, 0, 0.3);
        border-radius: 12px;
        padding: 20px;
        border-left: 3px solid #06B6D4;
    }}
    .modal-item {{
        display: flex;
        align-items: flex-start;
        margin-bottom: 12px;
        color: #D1D5DB;
        font-size: 0.95rem;
    }}
    .modal-bullet {{
        color: #06B6D4;
        font-size: 1.2rem;
        margin-right: 10px;
    }}
    .modal-highlight {{
        color: #38BDF8;
        font-weight: 700;
    }}
    .modal-quote {{
        text-align: center; 
        margin-top: 25px; 
        color: #94a3b8; 
        font-style: italic; 
        font-size: 0.9rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 15px;
    }}

    /* --- HERO SECTION (EL TÍTULO PRINCIPAL) --- */
    .hero-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 80px 20px 60px 20px;
        margin-bottom: 40px;
        position: relative;
        perspective: 1200px; 
    }}

    /* Efecto de luz detrás del título */
    .hero-container::before {{
        content: '';
        position: absolute;
        top: 40%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 80%;
        height: 150px;
        background: radial-gradient(ellipse at center, rgba(6, 182, 212, 0.25) 0%, rgba(0,0,0,0) 70%);
        filter: blur(60px);
        z-index: -1;
    }}

    .company-tag {{
        background: rgba(6, 182, 212, 0.05);
        color: #22d3ee;
        padding: 8px 24px;
        border-radius: 30px;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-bottom: 30px;
        border: 1px solid rgba(6, 182, 212, 0.4);
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.15);
        backdrop-filter: blur(5px);
    }}

    /* ESTILOS DEL TÍTULO 3D */
    .main-title-3d {{
        font-size: 6rem;
        font-weight: 900;
        margin: 0;
        line-height: 1.1;
        text-transform: uppercase;
        letter-spacing: -2px;
        
        /* Efecto Metálico */
        background: linear-gradient(
            110deg,
            #94a3b8 15%,
            #ffffff 25%,
            #94a3b8 35%,
            #64748b 45%
        );
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        
        animation: 
            title-float-3d 6s ease-in-out infinite,
            text-shimmer 5s linear infinite;
            
        filter: drop-shadow(0 15px 25px rgba(0,0,0,0.8));
    }}

    .highlight-text-3d {{
        /* Gradiente Cian Eléctrico */
        background: linear-gradient(
            110deg,
            #06B6D4 20%,
            #67e8f9 30%,
            #22d3ee 45%,
            #06B6D4 60%
        );
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: text-shimmer 3s linear infinite;
        filter: drop-shadow(0 0 20px rgba(34, 211, 238, 0.6));
    }}

    @media (max-width: 768px) {{
        .main-title-3d {{ font-size: 3.5rem; animation: none; transform: none; }}
    }}
    
    .subtitle {{
        font-size: 1.3rem;
        color: #cbd5e1;
        max-width: 800px;
        margin-top: 40px;
        line-height: 1.7;
        font-weight: 300;
        text-shadow: 0 2px 10px rgba(0,0,0,0.8);
        position: relative;
        z-index: 1;
    }}

    /* --- CARDS --- */
    .flow-card {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 35px 25px;
        border-radius: 24px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }}
    .flow-card:hover {{
        transform: translateY(-12px) scale(1.02);
        background: rgba(30, 41, 59, 0.6);
        border-color: rgba(6, 182, 212, 0.5);
        box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.5), 0 0 20px rgba(6, 182, 212, 0.2);
    }}
    .card-icon {{ 
        font-size: 3.5rem; 
        margin-bottom: 20px; 
        filter: drop-shadow(0 0 10px rgba(255,255,255,0.3));
        transition: transform 0.3s ease;
    }}
    .flow-card:hover .card-icon {{
        transform: scale(1.1) rotate(5deg);
    }}
    .card-title {{ 
        font-size: 1.5rem; 
        font-weight: 700; 
        color: #FFFFFF; 
        margin-bottom: 12px; 
    }}
    .card-desc {{ 
        font-size: 0.95rem; 
        color: #94a3b8; 
        margin-bottom: 25px; 
        line-height: 1.6; 
    }}

    /* --- PERFIL --- */
    .profile-box {{
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.4), rgba(15, 23, 42, 0.8));
        padding: 40px;
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 60px;
        display: flex;
        align-items: center;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
        overflow: hidden;
    }}
    .profile-img {{
        width: 160px;
        height: 160px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #06B6D4;
        margin-right: 40px;
        flex-shrink: 0;
        animation: pulse-glow 3s infinite;
    }}
    .profile-content {{
        flex: 1;
        z-index: 1;
    }}
    .profile-quote {{
        color: #e2e8f0; 
        font-size: 1.1rem; 
        line-height: 1.8; 
        font-style: italic; 
        border-left: 4px solid #06B6D4; 
        padding-left: 25px;
        font-weight: 300;
        background: linear-gradient(90deg, rgba(6,182,212,0.05) 0%, transparent 100%);
        padding-top: 10px; padding-bottom: 10px;
        border-radius: 0 10px 10px 0;
    }}
    .profile-tags {{
        margin-top: 25px; 
        display: flex; 
        gap: 12px; 
        flex-wrap: wrap;
    }}
    .tag-pill {{
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(6, 182, 212, 0.5);
        color: #22d3ee;
        padding: 8px 18px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    .tag-pill:hover {{
        background: rgba(6, 182, 212, 0.2);
        transform: translateY(-2px);
    }}
    
    /* RESPONSIVE */
    @media only screen and (max-width: 768px) {{
        .profile-box {{ flex-direction: column; text-align: center; }}
        .profile-img {{ margin-right: 0; margin-bottom: 25px; }}
        .profile-quote {{ border-left: none; border-top: 3px solid #06B6D4; padding-left: 0; padding-top: 20px; }}
        .profile-tags {{ justify-content: center; }}
    }}

    /* BOTONES */
    div.stButton > button {{
        width: 100%;
        background: transparent;
        color: #22d3ee;
        border: 1px solid #22d3ee;
        padding: 12px 24px;
        font-weight: 700;
        border-radius: 10px;
        transition: all 0.3s;
    }}
    div.stButton > button:hover {{
        color: white;
        border-color: #06B6D4;
        background: rgba(6, 182, 212, 0.2);
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
    }}
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 5rem;
    }}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- 4. DEFINICIÓN DE MODALES ---
# ==============================================================================

@st.dialog("📊 INVENTARIOS & ESTRATEGIA")
def open_inventory_modal():
    st.markdown("""
    <div class="custom-modal-box">
    <div class="modal-header-icon">🧠</div>
    <h2 class="modal-title">Del Caos Reactivo a la Precisión Predictiva</h2>
    <div class="modal-body-text">
    La gestión tradicional basada en "intuición" está costando millones. 
    Este módulo no es solo un registro; es un <b>cerebro financiero</b> que protege su capital.
    </div>
    <div class="modal-list-container">
    <div class="modal-item"><span class="modal-bullet">➤</span><div><span class="modal-highlight">Análisis de Capital (IA):</span> Detecta excedentes y quiebres.</div></div>
    <div class="modal-item"><span class="modal-bullet">➤</span><div><span class="modal-highlight">Predicción de Demanda:</span> Algoritmos que anticipan qué venderá mañana.</div></div>
    <div class="modal-item"><span class="modal-bullet">➤</span><div><span class="modal-highlight">Visión Gerencial 360°:</span> KPIs financieros en tiempo real.</div></div>
    </div>
    <div class="modal-quote">"El resultado: Menos stock obsoleto, más liquidez."</div>
    </div>
    """, unsafe_allow_html=True)
    st.write("") 
    if st.button("🚀 IR AL DEMO: DASHBOARD GERENCIAL", key="btn_go_inv"):
        st.switch_page("pages/1_Inventario_Nexus.py")

@st.dialog("🚚 LOGÍSTICA & ABASTECIMIENTO")
def open_logistics_modal():
    st.markdown("""
    <div class="custom-modal-box">
    <div class="modal-header-icon">⚡</div>
    <h2 class="modal-title">Sistema Nervioso de la Cadena de Suministro</h2>
    <div class="modal-body-text">
    Convertimos las necesidades en acciones. Motor operativo que asegura el producto correcto al menor costo.
    </div>
    <div class="modal-list-container">
    <div class="modal-item"><span class="modal-bullet">➤</span><div><span class="modal-highlight">Compras Inteligentes:</span> Órdenes basadas en consumo real.</div></div>
    <div class="modal-item"><span class="modal-bullet">➤</span><div><span class="modal-highlight">Balanceo de Red:</span> Traslados automáticos entre sedes.</div></div>
    <div class="modal-item"><span class="modal-bullet">➤</span><div><span class="modal-highlight">Torre de Control:</span> Visibilidad total de pedidos.</div></div>
    </div>
    <div class="modal-quote">"El resultado: Compras precisas y agilidad operativa."</div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("🚀 IR AL DEMO: CENTRO LOGÍSTICO", key="btn_go_log"):
        st.switch_page("pages/2_Operaciones_Logistica.py")

@st.dialog("📥 RECEPCIÓN INTELIGENTE (XML)")
def open_reception_modal():
    st.markdown("""
    <div class="custom-modal-box">
    <div class="modal-header-icon">🛡️</div>
    <h2 class="modal-title">Blindaje Total de Entrada de Mercancía</h2>
    <div class="modal-body-text">
    El 80% de los errores de inventario nacen en la recepción. Eliminamos la digitación manual usando la Factura Electrónica (XML).
    </div>
    <div class="modal-list-container">
    <div class="modal-item"><span class="modal-bullet">➤</span><div><span class="modal-highlight">Homologación Automática:</span> Cruce proveedor vs catálogo interno.</div></div>
    <div class="modal-item"><span class="modal-bullet">➤</span><div><span class="modal-highlight">Conciliación Ciega:</span> Conteo físico vs XML digital.</div></div>
    <div class="modal-item"><span class="modal-bullet">➤</span><div><span class="modal-highlight">Integridad de Datos:</span> Garantía fiscal total.</div></div>
    </div>
    <div class="modal-quote">"El resultado: Cero errores humanos, control fiscal total."</div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("🚀 IR AL DEMO: RECEPCIÓN XML", key="btn_go_xml"):
        st.switch_page("pages/3_Recepcion_Inteligente.py")

# ==============================================================================
# --- 5. ESTRUCTURA PRINCIPAL (AQUÍ ESTÁ LA CORRECCIÓN DEL TÍTULO) ---
# ==============================================================================

# EL HTML DEBE ESTAR DENTRO DE st.markdown CON unsafe_allow_html=True
st.markdown("""
<div class="hero-container animate-enter">
    <div class="company-tag">Arquitectura de Datos Empresarial & IA</div>
    
    <div style="transform-style: preserve-3d;">
        <h1 class="main-title-3d" style="display: inline-block;">
            GM-<span class="highlight-text-3d">DATOVATE</span>
        </h1>
    </div>

    <p class="subtitle">
        Transformamos el caos operativo en <b>Ventaja Competitiva</b>.
        <br>Una suite integrada que utiliza Inteligencia Artificial para sincronizar Inventarios, Logística y Finanzas en tiempo real.
    </p>
</div>
""", unsafe_allow_html=True)

# >>> GRID DE MÓDULOS
st.write("")
st.markdown("<h3 class='animate-enter' style='text-align: center; margin-bottom: 50px; font-size: 1.8rem; font-weight: 300; letter-spacing: 2px; color: #94a3b8;'>🚀 ECOSISTEMA NEXUS</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class="flow-card animate-enter" style="animation-delay: 0.1s;">
        <div>
            <div class="card-icon">📊</div>
            <div class="card-title">1. Control & Estrategia</div>
            <div class="card-desc">El cerebro financiero. Análisis predictivo de capital, detección de riesgos y optimización con IA.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explorar Módulo ➝", key="b1"):
        open_inventory_modal()

with col2:
    st.markdown("""
    <div class="flow-card animate-enter" style="animation-delay: 0.2s;">
        <div>
            <div class="card-icon">🚚</div>
            <div class="card-title">2. Logística Inteligente</div>
            <div class="card-desc">El brazo ejecutor. Automatización de compras y rebalanceo autónomo de stock entre bodegas.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explorar Módulo ➝", key="b2"):
        open_logistics_modal()

with col3:
    st.markdown("""
    <div class="flow-card animate-enter" style="animation-delay: 0.3s;">
        <div>
            <div class="card-icon">📥</div>
            <div class="card-title">3. Recepción Blindada</div>
            <div class="card-desc">La puerta de entrada. Procesamiento automático de XML (DIAN) y conciliación fiscal vs física.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explorar Módulo ➝", key="b3"):
        open_reception_modal()

# >>> PERFIL LÍDER
st.write("")
st.write("")

c_spacer_l, c_profile, c_spacer_r = st.columns([1, 6, 1])

with c_profile:
    st.markdown(f"""
    <div class="profile-box animate-enter" style="animation-delay: 0.4s;">
        <img src="{foto_diego_src}" class="profile-img" alt="Diego Mauricio García">
        <div class="profile-content">
            <h4 style="color: #06B6D4; margin:0 0 10px 0; font-weight: 800; letter-spacing:2px; font-size: 0.9rem;">ARQUITECTURA & VISIÓN</h4>
            <h2 style="color: white; margin: 0 0 20px 0; font-size: 2.5rem; font-weight: 700;">Diego Mauricio García</h2>
            <p class="profile-quote">
                "En GM-Datovate no vendemos software, diseñamos el sistema nervioso de su organización. 
                Mi obsesión es eliminar la fricción operativa mediante arquitecturas de datos que piensan, aprenden y actúan por sí mismas."
            </p>
            <div class="profile-tags">
                <div class="tag-pill">CEO & Founder</div>
                <div class="tag-pill">Data Architect</div>
                <div class="tag-pill">Python Expert</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748B; margin-bottom: 40px; font-size: 0.8rem; letter-spacing: 1px;'>© 2025 GM-DATOVATE. POWERED BY INTELLIGENCE.</div>", unsafe_allow_html=True)
