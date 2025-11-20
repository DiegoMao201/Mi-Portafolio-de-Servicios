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
img_path = os.path.join(current_dir, "assets", "foto_diego.png")
img_base64 = get_img_as_base64(img_path)

# Fallback: Si no encuentra la foto local, usa un icono genérico
foto_diego_src = f"data:image/png;base64,{img_base64}" if img_base64 else "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# ==============================================================================
# --- 3. CSS PREMIUM (ESTILOS AVANZADOS 3D) ---
# ==============================================================================
st.markdown(f"""
<style>
    /* IMPORTAR FUENTE */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&display=swap');

    /* FONDO GENERAL */
    .stApp {{
        background-color: #0E1117;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        overflow-x: hidden; /* Evitar scroll horizontal por animaciones */
    }}
    
    /* --- ANIMACIONES KEYFRAMES --- */
    
    /* 1. Flujo de Gradiente (Liquid Effect) */
    @keyframes textShine {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* 2. Levitación 3D (Floating) */
    @keyframes float {{
        0% {{ transform: translateY(0px) perspective(1000px) rotateX(0deg); }}
        50% {{ transform: translateY(-15px) perspective(1000px) rotateX(2deg); }}
        100% {{ transform: translateY(0px) perspective(1000px) rotateX(0deg); }}
    }}

    /* 3. Pulso de Neon */
    @keyframes glowPulse {{
        0% {{ filter: drop-shadow(0 0 15px rgba(6, 182, 212, 0.3)); }}
        50% {{ filter: drop-shadow(0 0 35px rgba(6, 182, 212, 0.8)); }}
        100% {{ filter: drop-shadow(0 0 15px rgba(6, 182, 212, 0.3)); }}
    }}

    /* --- ESTILOS DE MODALES --- */
    .custom-modal-box {{
        background: linear-gradient(145deg, #111827, #1f2937);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #374151;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
    }}
    
    .modal-header-icon {{
        font-size: 3rem;
        text-align: center;
        display: block;
        margin-bottom: 10px;
        text-shadow: 0 0 15px rgba(6, 182, 212, 0.6);
    }}

    .modal-title {{
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 15px;
        background: -webkit-linear-gradient(0deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .modal-body-text {{
        color: #E5E7EB !important;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 20px;
        text-align: justify;
    }}

    .modal-list-container {{
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        padding: 15px;
        border: 1px solid rgba(255,255,255,0.05);
    }}

    .modal-item {{
        display: flex;
        align-items: flex-start;
        margin-bottom: 8px;
        color: #D1D5DB;
        font-size: 0.9rem;
    }}

    .modal-bullet {{
        color: #06B6D4;
        font-size: 1.1rem;
        margin-right: 8px;
        line-height: 1.2;
    }}
    
    .modal-highlight {{
        color: #38BDF8;
        font-weight: 700;
    }}

    .modal-quote {{
        text-align: center; 
        margin-top: 20px; 
        color: #94a3b8; 
        font-style: italic; 
        font-size: 0.85rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 10px;
    }}

    /* --- HERO SECTION MEJORADA (3D & MOVIMIENTO) --- */
    .hero-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 70px 20px 50px 20px; /* Más espacio */
        background: radial-gradient(circle at center, #1e293b 0%, #0E1117 80%);
        border-bottom: 1px solid #2d3748;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
    }}

    .company-tag {{
        background-color: rgba(6, 182, 212, 0.1);
        color: #22d3ee;
        padding: 8px 20px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 25px;
        border: 1px solid rgba(6, 182, 212, 0.3);
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.15);
        backdrop-filter: blur(5px);
    }}

    /* TÍTULO 3D IMPACTANTE */
    .super-title-container {{
        perspective: 1000px; /* Da la profundidad 3D */
    }}

    .super-title {{
        font-size: 5.5rem; /* Muy grande e impactante */
        font-weight: 900;
        margin: 0;
        line-height: 1.1;
        letter-spacing: -2px;
        
        /* Gradiente Metálico Animado */
        background: linear-gradient(
            225deg, 
            #FFFFFF 0%, 
            #94a3b8 25%, 
            #FFFFFF 50%, 
            #94a3b8 75%, 
            #FFFFFF 100%
        );
        background-size: 200% auto;
        color: #fff;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        
        /* Animaciones combinadas */
        animation: textShine 4s linear infinite, float 6s ease-in-out infinite;
        
        /* Sombra 3D CSS pura (simula extrusión) */
        filter: drop-shadow(0px 0px 0px rgba(0,0,0,0)); /* Reset base */
    }}

    /* Parte coloreada del título */
    .super-highlight {{
        background: linear-gradient(
            90deg, 
            #22d3ee 0%, 
            #3b82f6 50%, 
            #22d3ee 100%
        );
        background-size: 200% auto;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: textShine 3s linear infinite;
        
        /* Glow específico para la parte de color */
        text-shadow: 0 0 30px rgba(34, 211, 238, 0.5);
    }}

    /* Subtítulo elegante */
    .subtitle {{
        font-size: 1.3rem;
        color: #cbd5e1;
        max-width: 750px;
        margin-top: 30px;
        line-height: 1.7;
        font-weight: 300;
        opacity: 0.9;
    }}
    
    .subtitle b {{
        color: #38BDF8;
        font-weight: 600;
    }}

    /* --- CARDS --- */
    .flow-card {{
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 30px;
        border-radius: 20px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
    }}
    
    .flow-card::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, #06B6D4, transparent);
        opacity: 0;
        transition: opacity 0.4s;
    }}

    .flow-card:hover {{
        transform: translateY(-10px) scale(1.02);
        background: rgba(30, 41, 59, 0.8);
        border-color: #3b82f6;
        box-shadow: 0 20px 40px -12px rgba(6, 182, 212, 0.3);
    }}
    
    .flow-card:hover::before {{
        opacity: 1;
    }}

    .card-icon {{ font-size: 3rem; margin-bottom: 15px; }}
    .card-title {{ font-size: 1.4rem; font-weight: 700; color: #FFFFFF; margin-bottom: 10px; }}
    .card-desc {{ font-size: 0.95rem; color: #cbd5e1; margin-bottom: 20px; line-height: 1.5; }}

    /* --- PERFIL --- */
    .profile-box {{
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 40px;
        border-radius: 25px;
        border: 1px solid rgba(51, 65, 85, 0.7);
        margin-top: 50px;
        display: flex;
        align-items: center;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        position: relative;
    }}
    
    .profile-img {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #06B6D4;
        margin-right: 30px;
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.4);
        transition: transform 0.3s;
    }}
    
    .profile-img:hover {{
        transform: scale(1.05) rotate(5deg);
    }}

    /* --- BOTONES --- */
    div.stButton > button {{
        width: 100%;
        background: linear-gradient(90deg, #2563EB 0%, #06B6D4 100%);
        color: white;
        border: none;
        padding: 12px 20px;
        font-weight: 700;
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.9rem;
    }}
    
    div.stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(6, 182, 212, 0.6);
        background: linear-gradient(90deg, #3b82f6 0%, #22d3ee 100%);
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
    <div class="modal-item">
    <span class="modal-bullet">➤</span>
    <div><span class="modal-highlight">Análisis de Capital (IA):</span> Detecta dónde está atrapado el dinero (excedentes) y dónde pierde ventas (quiebres).</div>
    </div>
    <div class="modal-item">
    <span class="modal-bullet">➤</span>
    <div><span class="modal-highlight">Predicción de Demanda:</span> Algoritmos que anticipan qué venderá mañana, optimizando el flujo de caja hoy.</div>
    </div>
    <div class="modal-item">
    <span class="modal-bullet">➤</span>
    <div><span class="modal-highlight">Visión Gerencial 360°:</span> KPIs en tiempo real sobre la salud financiera de su stock.</div>
    </div>
    </div>
    <div class="modal-quote">
    "El resultado: Menos stock obsoleto, más liquidez."
    </div>
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
    Convertimos las necesidades en acciones. Este es el motor operativo que asegura 
    que el producto correcto esté en el lugar correcto, al menor costo posible.
    </div>
    <div class="modal-list-container">
    <div class="modal-item">
    <span class="modal-bullet">➤</span>
    <div><span class="modal-highlight">Compras Inteligentes:</span> Generación automática de órdenes basadas en consumo real y Lead Time.</div>
    </div>
    <div class="modal-item">
    <span class="modal-bullet">➤</span>
    <div><span class="modal-highlight">Balanceo de Red:</span> Detecta excesos en la Sede A y faltantes en la Sede B, sugiriendo traslados automáticos.</div>
    </div>
    <div class="modal-item">
    <span class="modal-bullet">➤</span>
    <div><span class="modal-highlight">Torre de Control:</span> Visibilidad total del estado de pedidos y movimientos en curso.</div>
    </div>
    </div>
    <div class="modal-quote">
    "El resultado: Compras precisas y agilidad operativa."
    </div>
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
    El 80% de los errores de inventario nacen en la recepción. Este módulo elimina la digitación manual 
    usando la Factura Electrónica (XML DIAN) como única fuente de verdad.
    </div>
    <div class="modal-list-container">
    <div class="modal-item">
    <span class="modal-bullet">➤</span>
    <div><span class="modal-highlight">Homologación Automática:</span> Cruce instantáneo de referencias del proveedor vs. catálogo interno.</div>
    </div>
    <div class="modal-item">
    <span class="modal-bullet">➤</span>
    <div><span class="modal-highlight">Conciliación Ciega:</span> Compara el conteo físico real contra el XML digital, alertando faltantes al instante.</div>
    </div>
    <div class="modal-item">
    <span class="modal-bullet">➤</span>
    <div><span class="modal-highlight">Integridad de Datos:</span> Garantiza que lo que paga es exactamente lo que entró a bodega.</div>
    </div>
    </div>
    <div class="modal-quote">
    "El resultado: Cero errores humanos, control fiscal total."
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("🚀 IR AL DEMO: RECEPCIÓN XML", key="btn_go_xml"):
        st.switch_page("pages/3_Recepcion_Inteligente.py")

# ==============================================================================
# --- 5. ESTRUCTURA PRINCIPAL ---
# ==============================================================================

# >>> HERO SECTION (NUEVO DISEÑO IMPACTANTE 3D)
st.markdown("""
<div class="hero-container">
    <div class="company-tag">Arquitectura de Datos Empresarial & IA</div>
    
    <div class="super-title-container">
        <h1 class="super-title">
            GM-<span class="super-highlight">DATOVATE</span>
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
st.markdown("<h3 style='text-align: center; margin-bottom: 50px; font-size: 2rem; font-weight: 800; letter-spacing: -1px;'>🚀 Ecosistema NEXUS: Explore el Valor de Negocio</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

# --- CARD 1 ---
with col1:
    st.markdown("""
    <div class="flow-card">
        <div>
            <div class="card-icon">📊</div>
            <div class="card-title">1. Control & Estrategia</div>
            <p class="card-desc">El cerebro financiero. Análisis predictivo de capital, detección de riesgos y optimización con IA.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explorar Módulo ➝", key="b1"):
        open_inventory_modal()

# --- CARD 2 ---
with col2:
    st.markdown("""
    <div class="flow-card">
        <div>
            <div class="card-icon">🚚</div>
            <div class="card-title">2. Logística Inteligente</div>
            <p class="card-desc">El brazo ejecutor. Automatización de compras y rebalanceo autónomo de stock entre bodegas.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explorar Módulo ➝", key="b2"):
        open_logistics_modal()

# --- CARD 3 ---
with col3:
    st.markdown("""
    <div class="flow-card">
        <div>
            <div class="card-icon">📥</div>
            <div class="card-title">3. Recepción Blindada</div>
            <p class="card-desc">La puerta de entrada. Procesamiento automático de XML (DIAN) y conciliación fiscal vs física.</p>
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
    <div class="profile-box">
        <img src="{foto_diego_src}" class="profile-img" alt="Diego Mauricio García">
        <div style="flex: 1;">
            <h4 style="color: #06B6D4; margin:0 0 10px 0; font-weight: 800; letter-spacing:1.5px;">ARQUITECTURA & VISIÓN</h4>
            <h2 style="color: white; margin: 0 0 20px 0; font-size: 2.5rem; text-shadow: 0 0 20px rgba(0,0,0,0.5);">Diego Mauricio García</h2>
            <p style="color: #E2E8F0; font-size: 1.1rem; line-height: 1.8; font-style: italic; border-left: 4px solid #06B6D4; padding-left: 20px;">
                "En GM-Datovate no vendemos software, diseñamos el sistema nervioso de su organización. 
                Mi obsesión es eliminar la fricción operativa mediante arquitecturas de datos que piensan, aprenden y actúan por sí mismas."
            </p>
            <div style="margin-top: 20px; display: flex; gap: 10px; flex-wrap: wrap;">
                <span style="background: rgba(15,23,42,0.6); border: 1px solid #06B6D4; color: #06B6D4; padding: 6px 15px; border-radius: 20px; font-size: 0.8rem;">CEO & Founder</span>
                <span style="background: rgba(15,23,42,0.6); border: 1px solid #06B6D4; color: #06B6D4; padding: 6px 15px; border-radius: 20px; font-size: 0.8rem;">Data Architect</span>
                <span style="background: rgba(15,23,42,0.6); border: 1px solid #06B6D4; color: #06B6D4; padding: 6px 15px; border-radius: 20px; font-size: 0.8rem;">Python Expert</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748B; margin-bottom: 40px;'>© 2025 GM-DATOVATE. Todos los derechos reservados.</div>", unsafe_allow_html=True)
