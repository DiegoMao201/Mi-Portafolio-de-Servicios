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

# Carga de imagen de perfil
current_dir = os.path.dirname(os.path.abspath(__file__))
# Ajusta la ruta si tu carpeta de assets tiene otro nombre
img_path = os.path.join(current_dir, "assets", "foto_diego.png")
img_base64 = get_img_as_base64(img_path)

# Fallback: Si no encuentra la foto local, usa un icono genérico profesional
foto_diego_src = f"data:image/png;base64,{img_base64}" if img_base64 else "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# ==============================================================================
# --- 3. CSS "ULTRA-IMPACT" (3D REAL + NEBULOSA + CYBERPUNK) ---
# ==============================================================================
st.markdown(f"""
<style>
    /* --- IMPORTACIÓN DE FUENTES --- */
    /* Russo One: Para títulos gruesos e impactantes */
    /* Outfit: Para cuerpo de texto moderno y limpio */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800;900&family=Russo+One&display=swap');

    /* --- ANIMACIONES --- */
    
    /* Fondo Nebulosa: Movimiento lento y profundo */
    @keyframes nebula-move {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* Flote 3D del Título Principal */
    @keyframes float-3d {{
        0% {{ transform: perspective(1000px) rotateX(5deg) rotateY(-2deg) translateY(0); text-shadow: 0 10px 10px rgba(0,0,0,0.5), 0 20px 20px rgba(0,0,0,0.4), 0 0 30px rgba(6, 182, 212, 0.2); }}
        50% {{ transform: perspective(1000px) rotateX(5deg) rotateY(-2deg) translateY(-15px); text-shadow: 0 25px 15px rgba(0,0,0,0.5), 0 40px 30px rgba(0,0,0,0.4), 0 0 60px rgba(6, 182, 212, 0.6); }}
        100% {{ transform: perspective(1000px) rotateX(5deg) rotateY(-2deg) translateY(0); text-shadow: 0 10px 10px rgba(0,0,0,0.5), 0 20px 20px rgba(0,0,0,0.4), 0 0 30px rgba(6, 182, 212, 0.2); }}
    }}

    /* Entrada suave desde abajo */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(40px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Pulso de neón para bordes */
    @keyframes neon-pulse {{
        0%, 100% {{ border-color: rgba(6, 182, 212, 0.5); box-shadow: 0 0 15px rgba(6, 182, 212, 0.2); }}
        50% {{ border-color: rgba(6, 182, 212, 1); box-shadow: 0 0 30px rgba(6, 182, 212, 0.6); }}
    }}

    /* --- ESTILOS GLOBALES DE LA APP --- */
    .stApp {{
        /* Gradiente complejo Dark Matter */
        background: linear-gradient(-45deg, #000000, #0f172a, #1e1b4b, #312e81, #020617);
        background-size: 400% 400%;
        animation: nebula-move 12s ease infinite;
        color: #FFFFFF;
        font-family: 'Outfit', sans-serif;
        overflow-x: hidden; /* Evita scroll horizontal por animaciones 3D */
    }}
    
    /* Overlay de textura "Scanline" (Efecto Tech sutil) */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background: repeating-linear-gradient(
            to bottom,
            transparent 0px,
            transparent 2px,
            rgba(0, 0, 0, 0.2) 3px
        );
        pointer-events: none;
        z-index: 0;
    }}

    /* CLASE UTILITARIA: Entrada Animada */
    .animate-enter {{
        animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        opacity: 0; /* Inicia invisible */
        animation-delay: 0.1s;
        animation-fill-mode: forwards;
    }}

    /* --- HERO SECTION (TITULO 3D) --- */
    .hero-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 80px 20px 60px 20px;
        margin-bottom: 30px;
        position: relative;
        z-index: 1;
    }}

    .company-tag {{
        background: rgba(6, 182, 212, 0.15);
        color: #67e8f9;
        padding: 8px 20px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-bottom: 30px;
        border: 1px solid rgba(6, 182, 212, 0.5);
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
        backdrop-filter: blur(10px);
    }}

    /* Wrapper para activar la perspectiva 3D */
    .title-3d-wrapper {{
        perspective: 1000px;
        display: inline-block;
    }}

    .main-title {{
        font-family: 'Russo One', sans-serif;
        font-size: 6rem; /* Tamaño gigante */
        margin: 0;
        line-height: 1;
        color: #ffffff;
        
        /* TRANSFORMACIÓN Y ANIMACIÓN 3D */
        transform-style: preserve-3d;
        animation: float-3d 6s ease-in-out infinite;
        
        /* SOMBRAS APILADAS PARA EFECTO VOLUMEN */
        text-shadow: 
            1px 1px 0 #0891b2,
            2px 2px 0 #0891b2,
            3px 3px 0 #0891b2,
            4px 4px 0 #0891b2,
            6px 10px 20px rgba(0,0,0,0.8),
            0 0 80px rgba(6, 182, 212, 0.5);
    }}
    
    .highlight-text {{
        color: #22d3ee; /* Cian Eléctrico */
        text-shadow: 
            1px 1px 0 #0e7490,
            2px 2px 0 #0e7490,
            3px 3px 0 #0e7490,
            0 0 50px #22d3ee; /* Glow intenso */
    }}

    /* Ajuste para móviles */
    @media (max-width: 768px) {{
        .main-title {{ font-size: 3.5rem; }}
    }}

    .subtitle {{
        font-size: 1.3rem;
        color: #e2e8f0;
        max-width: 800px;
        margin-top: 40px;
        line-height: 1.6;
        font-weight: 300;
        text-shadow: 0 2px 4px rgba(0,0,0,0.8);
        background: rgba(15, 23, 42, 0.6);
        padding: 15px 25px;
        border-radius: 15px;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255,255,255,0.05);
    }}

    /* --- TARJETAS (CARDS) GLASSMORPHISM --- */
    .flow-card {{
        background: linear-gradient(160deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 35px 25px;
        border-radius: 24px;
        height: 100%;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        z-index: 2;
    }}
    
    .flow-card:hover {{
        transform: translateY(-15px) scale(1.03);
        background: linear-gradient(160deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 1) 100%);
        border-color: #38bdf8;
        box-shadow: 0 20px 50px rgba(6, 182, 212, 0.25);
    }}
    
    /* Icono animado dentro de la tarjeta */
    .flow-card:hover .card-icon {{
        transform: scale(1.2) rotate(10deg);
        filter: drop-shadow(0 0 15px rgba(255,255,255,0.8));
    }}

    .card-icon {{ 
        font-size: 3.5rem; 
        margin-bottom: 20px; 
        transition: all 0.4s ease; 
        display: inline-block;
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
        line-height: 1.6; 
    }}

    /* --- PERFIL DEL LÍDER (ESTILO CYBER) --- */
    .profile-box {{
        background: rgba(17, 24, 39, 0.7);
        padding: 45px;
        border-radius: 30px;
        border: 1px solid rgba(6, 182, 212, 0.2);
        margin-top: 60px;
        display: flex;
        align-items: center;
        box-shadow: 0 0 40px rgba(0,0,0,0.5);
        backdrop-filter: blur(15px);
        position: relative;
        animation: neon-pulse 4s infinite; /* El borde respira */
    }}
    
    .profile-img {{
        width: 160px; height: 160px;
        border-radius: 50%; object-fit: cover;
        border: 4px solid #22d3ee;
        margin-right: 40px;
        box-shadow: 0 0 30px rgba(34, 211, 238, 0.4);
    }}

    .profile-content h2 {{ 
        font-family: 'Russo One', sans-serif; 
        letter-spacing: 1px; 
    }}

    .tag-pill {{
        background: linear-gradient(90deg, rgba(6,182,212,0.1), rgba(59,130,246,0.1));
        border: 1px solid #22d3ee;
        color: #22d3ee;
        padding: 6px 15px; border-radius: 20px;
        font-size: 0.8rem; font-weight: 700;
        text-transform: uppercase;
        box-shadow: 0 0 10px rgba(6,182,212,0.1);
        margin-right: 10px;
        margin-bottom: 10px;
        display: inline-block;
    }}

    /* Responsive Profile */
    @media only screen and (max-width: 768px) {{
        .profile-box {{ flex-direction: column; text-align: center; padding: 30px; }}
        .profile-img {{ margin-right: 0; margin-bottom: 20px; }}
        .profile-tags {{ justify-content: center; }}
    }}

    /* --- BOTONES PERSONALIZADOS (GRADIENTE ACTIVO) --- */
    div.stButton > button {{
        background: linear-gradient(90deg, #0ea5e9, #2563eb);
        color: white;
        border: none;
        padding: 14px 28px;
        font-weight: 700;
        border-radius: 12px;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4);
        width: 100%;
    }}
    
    div.stButton > button:hover {{
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 10px 30px rgba(14, 165, 233, 0.7);
        background: linear-gradient(90deg, #38bdf8, #3b82f6);
    }}

    /* --- MODALES (ADAPTADOS AL TEMA OSCURO) --- */
    .custom-modal-box {{
        background: #0f172a; 
        border: 1px solid #334155; 
        border-radius: 20px; 
        padding: 25px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
    }}
    .modal-header-icon {{ font-size: 3rem; text-align: center; margin-bottom: 10px; display:block; animation: float-3d 4s infinite; }}
    .modal-title {{ 
        color: #fff !important; 
        text-align: center; 
        font-size: 1.6rem; 
        font-weight: 800; 
        margin-bottom: 15px; 
        font-family: 'Russo One', sans-serif;
    }}
    .modal-body-text {{ color: #cbd5e1 !important; text-align: justify; margin-bottom: 20px; font-size: 0.95rem; }}
    .modal-list-container {{ background: rgba(255,255,255,0.03); padding: 15px; border-radius: 10px; border-left: 3px solid #0ea5e9; }}
    .modal-item {{ display: flex; margin-bottom: 10px; align-items: flex-start; }}
    .modal-bullet {{ color: #0ea5e9; margin-right: 10px; font-weight: bold; font-size: 1.2rem; }}
    .modal-highlight {{ color: #38bdf8; font-weight: 700; }}
    .modal-quote {{ text-align: center; margin-top: 15px; font-style: italic; color: #64748b; font-size: 0.85rem; }}

    /* Ajuste contenedores Streamlit */
    .block-container {{ padding-top: 2rem; padding-bottom: 5rem; }}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- 4. DEFINICIÓN DE MODALES (LÓGICA DE NEGOCIO) ---
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
            <div class="modal-item">
                <span class="modal-bullet">➤</span>
                <div><span class="modal-highlight">Análisis de Capital (IA):</span> Detecta dónde está atrapado el dinero (excedentes).</div>
            </div>
            <div class="modal-item">
                <span class="modal-bullet">➤</span>
                <div><span class="modal-highlight">Predicción de Demanda:</span> Algoritmos que anticipan qué venderá mañana.</div>
            </div>
            <div class="modal-item">
                <span class="modal-bullet">➤</span>
                <div><span class="modal-highlight">Visión Gerencial 360°:</span> KPIs en tiempo real sobre la salud financiera.</div>
            </div>
        </div>
        <div class="modal-quote">"Menos stock obsoleto, más liquidez inmediata."</div>
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
        <h2 class="modal-title">Sistema Nervioso de la Cadena</h2>
        <div class="modal-body-text">
        Convertimos las necesidades en acciones. Este es el motor operativo que asegura 
        que el producto correcto esté en el lugar correcto.
        </div>
        <div class="modal-list-container">
            <div class="modal-item">
                <span class="modal-bullet">➤</span>
                <div><span class="modal-highlight">Compras Inteligentes:</span> Generación automática de órdenes basadas en consumo.</div>
            </div>
            <div class="modal-item">
                <span class="modal-bullet">➤</span>
                <div><span class="modal-highlight">Balanceo de Red:</span> Detecta excesos y sugiere traslados automáticos.</div>
            </div>
            <div class="modal-item">
                <span class="modal-bullet">➤</span>
                <div><span class="modal-highlight">Torre de Control:</span> Visibilidad total del estado de pedidos.</div>
            </div>
        </div>
        <div class="modal-quote">"Compras precisas y agilidad operativa."</div>
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
        <h2 class="modal-title">Blindaje Total de Entrada</h2>
        <div class="modal-body-text">
        El 80% de los errores de inventario nacen en la recepción. Este módulo elimina la digitación manual 
        usando el XML DIAN como fuente de verdad.
        </div>
        <div class="modal-list-container">
            <div class="modal-item">
                <span class="modal-bullet">➤</span>
                <div><span class="modal-highlight">Homologación Automática:</span> Cruce instantáneo de referencias.</div>
            </div>
            <div class="modal-item">
                <span class="modal-bullet">➤</span>
                <div><span class="modal-highlight">Conciliación Ciega:</span> Compara conteo físico vs XML digital.</div>
            </div>
            <div class="modal-item">
                <span class="modal-bullet">➤</span>
                <div><span class="modal-highlight">Integridad de Datos:</span> Garantiza que lo que paga es lo que entró.</div>
            </div>
        </div>
        <div class="modal-quote">"Cero errores humanos, control fiscal total."</div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("🚀 IR AL DEMO: RECEPCIÓN XML", key="btn_go_xml"):
        st.switch_page("pages/3_Recepcion_Inteligente.py")

# ==============================================================================
# --- 5. ESTRUCTURA PRINCIPAL (LAYOUT) ---
# ==============================================================================

# >>> HERO SECTION (TITULO 3D + ANIMACION DE ENTRADA)
st.markdown("""
<div class="hero-container animate-enter">
    <div class="company-tag">Arquitectura de Datos Empresarial & IA</div>
    
    <div class="title-3d-wrapper">
        <h1 class="main-title">GM-<span class="highlight-text">DATOVATE</span></h1>
    </div>
    
    <p class="subtitle">
        Transformamos el caos operativo en <b>Ventaja Competitiva</b>.
        <br>Una suite integrada que utiliza Inteligencia Artificial para sincronizar Inventarios, Logística y Finanzas.
    </p>
</div>
""", unsafe_allow_html=True)

# >>> GRID DE MÓDULOS (CARDS GLASSMORPHISM)
st.write("")
st.markdown("<div class='animate-enter' style='text-align: center; margin-bottom: 50px; animation-delay: 0.3s;'><h3 style='font-family: \"Outfit\"; font-weight: 300; letter-spacing: 3px; color: #94a3b8;'>🚀 ECOSISTEMA NEXUS DE ALTO RENDIMIENTO</h3></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

# --- CARD 1 ---
with col1:
    st.markdown("""
    <div class="flow-card animate-enter" style="animation-delay: 0.4s;">
        <div>
            <div class="card-icon">📊</div>
            <div class="card-title">1. Control & Estrategia</div>
            <div class="card-desc">El cerebro financiero. Análisis predictivo de capital, detección de riesgos y optimización con IA.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explorar Módulo ➝", key="b1"):
        open_inventory_modal()

# --- CARD 2 ---
with col2:
    st.markdown("""
    <div class="flow-card animate-enter" style="animation-delay: 0.5s;">
        <div>
            <div class="card-icon">🚚</div>
            <div class="card-title">2. Logística Inteligente</div>
            <div class="card-desc">El brazo ejecutor. Automatización de compras y rebalanceo autónomo de stock entre bodegas.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explorar Módulo ➝", key="b2"):
        open_logistics_modal()

# --- CARD 3 ---
with col3:
    st.markdown("""
    <div class="flow-card animate-enter" style="animation-delay: 0.6s;">
        <div>
            <div class="card-icon">📥</div>
            <div class="card-title">3. Recepción Blindada</div>
            <div class="card-desc">La puerta de entrada. Procesamiento automático de XML (DIAN) y conciliación fiscal vs física.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explorar Módulo ➝", key="b3"):
        open_reception_modal()

# >>> PERFIL LÍDER (ESTÉTICA CYBER)
st.write("")
st.write("")

c_spacer_l, c_profile, c_spacer_r = st.columns([1, 6, 1])

with c_profile:
    st.markdown(f"""
    <div class="profile-box animate-enter" style="animation-delay: 0.7s;">
        <img src="{foto_diego_src}" class="profile-img" alt="Diego Mauricio García">
        <div class="profile-content">
            <h4 style="color: #22d3ee; margin:0 0 10px 0; font-weight: 800; letter-spacing:2px; font-size: 0.9rem; text-shadow: 0 0 10px rgba(34,211,238,0.5);">ARQUITECTURA & VISIÓN</h4>
            <h2 style="color: white; margin: 0 0 20px 0; font-size: 2.5rem; font-weight: 700;">Diego Mauricio García</h2>
            <p style="color: #cbd5e1; font-style: italic; line-height: 1.8; margin-bottom: 25px;">
                "En GM-Datovate no vendemos software, diseñamos el sistema nervioso de su organización. 
                Mi obsesión es eliminar la fricción operativa mediante arquitecturas de datos que piensan, aprenden y actúan por sí mismas."
            </p>
            <div class="profile-tags">
                <span class="tag-pill">CEO & Founder</span>
                <span class="tag-pill">Data Architect</span>
                <span class="tag-pill">Python Expert</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #64748B; margin-bottom: 40px; font-size: 0.8rem; letter-spacing: 1px; opacity: 0.7;'>
    © 2025 GM-DATOVATE. <span style='color: #0ea5e9;'>POWERED BY INTELLIGENCE.</span>
</div>
""", unsafe_allow_html=True)
