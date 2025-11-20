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
# Fallback si no encuentra la imagen
foto_diego_src = f"data:image/png;base64,{img_base64}" if img_base64 else "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# --- 3. CSS PREMIUM (CORREGIDO Y MEJORADO PARA MODALES) ---
st.markdown(f"""
<style>
    /* IMPORTAR FUENTE */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&display=swap');

    /* FONDO GENERAL */
    .stApp {{
        background-color: #0E1117;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }}
    
    /* =========================================
       ESTILOS ESPECÍFICOS DEL MODAL (CORRECCIÓN)
       ========================================= */
    
    /* Contenedor interno del modal para forzar el fondo oscuro */
    .custom-modal-box {{
        background: linear-gradient(145deg, #111827, #1f2937);
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #374151;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        color: white; /* Forzar texto base blanco */
    }}
    
    .modal-header-icon {{
        font-size: 4rem;
        text-align: center;
        display: block;
        margin-bottom: 10px;
        filter: drop-shadow(0 0 10px rgba(6, 182, 212, 0.5));
    }}

    .modal-title {{
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 1.8rem;
        text-align: center;
        margin-bottom: 20px;
        line-height: 1.2;
        background: -webkit-linear-gradient(0deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .modal-body-text {{
        color: #E2E8F0 !important;
        font-size: 1.05rem;
        line-height: 1.6;
        margin-bottom: 25px;
        text-align: center;
        font-weight: 300;
    }}

    /* Lista estilizada dentro del modal */
    .modal-list-container {{
        background-color: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.05);
    }}

    .modal-item {{
        display: flex;
        align-items: start;
        margin-bottom: 12px;
        color: #CBD5E1;
        font-size: 0.95rem;
    }}

    .modal-bullet {{
        color: #06B6D4;
        font-size: 1.2rem;
        margin-right: 10px;
        line-height: 1;
    }}
    
    .modal-highlight {{
        color: #38BDF8;
        font-weight: 700;
        margin-right: 5px;
    }}

    .modal-quote {{
        text-align: center; 
        margin-top: 15px; 
        color: #94a3b8; 
        font-style: italic; 
        font-size: 0.9rem;
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 15px;
    }}

    /* =========================================
       HERO SECTION & CARDS
       ========================================= */
    .hero-container {{
        text-align: center;
        padding: 80px 20px 60px 20px;
        background: radial-gradient(circle at top center, #1e293b 0%, #0E1117 60%);
        margin-bottom: 40px;
    }}

    .company-tag {{
        display: inline-block;
        background: rgba(6, 182, 212, 0.1);
        color: #22d3ee;
        padding: 8px 20px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 3px;
        border: 1px solid rgba(6, 182, 212, 0.3);
        margin-bottom: 25px;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.15);
    }}

    .main-title {{
        font-size: 4.5rem;
        font-weight: 900;
        margin: 0;
        line-height: 1.1;
        color: white;
        text-shadow: 0 0 40px rgba(37, 99, 235, 0.3);
    }}

    .highlight-text {{
        background: linear-gradient(90deg, #3b82f6, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    .subtitle {{
        font-size: 1.25rem;
        color: #94A3B8;
        max-width: 700px;
        margin: 30px auto 0 auto;
        line-height: 1.6;
    }}

    /* Cards */
    .flow-card {{
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 40px 30px;
        border-radius: 24px;
        height: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .flow-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 4px;
        background: linear-gradient(90deg, #2563EB, #06B6D4);
        opacity: 0;
        transition: opacity 0.3s ease;
    }}

    .flow-card:hover {{
        transform: translateY(-10px);
        background: rgba(30, 41, 59, 0.8);
        box-shadow: 0 20px 40px -10px rgba(0,0,0,0.5);
        border-color: rgba(56, 189, 248, 0.3);
    }}

    .flow-card:hover::before {{ opacity: 1; }}

    .card-icon {{ font-size: 3rem; margin-bottom: 20px; }}
    .card-title {{ font-size: 1.5rem; font-weight: 700; color: #FFF; margin-bottom: 15px; }}
    .card-desc {{ font-size: 0.95rem; color: #cbd5e1; line-height: 1.6; }}

    /* Perfil */
    .profile-box {{
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 40px;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.05);
        margin-top: 80px;
        display: flex;
        align-items: center;
        gap: 40px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    }}
    
    .profile-img {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #06B6D4;
        box-shadow: 0 0 30px rgba(6, 182, 212, 0.2);
    }}

    /* Botones Streamlit */
    div.stButton > button {{
        width: 100%;
        background: linear-gradient(90deg, #1e293b, #334155);
        color: #38BDF8;
        border: 1px solid #38BDF8;
        padding: 12px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
        margin-top: 15px;
    }}
    
    div.stButton > button:hover {{
        background: #38BDF8;
        color: #0f172a;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
    }}

</style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- 4. DEFINICIÓN DE MODALES (HTML PURO DENTRO DE MARKDOWN) ---
# ==============================================================================
# El truco para que no salga el texto crudo es usar st.markdown(..., unsafe_allow_html=True)

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
    
    # Espacio visual
    st.write("") 
    if st.button("🚀 IR AL DEMO: DASHBOARD GERENCIAL", key="btn_inv"):
        try:
            st.switch_page("pages/1_Inventario_Nexus.py")
        except:
            st.error("Página no encontrada. Verifica la carpeta 'pages'.")

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
                <div><span class="modal-highlight">Balanceo de Red:</span> Detecta excesos en la Sede A y faltantes en la Sede B, sugiriendo traslados.</div>
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
    if st.button("🚀 IR AL DEMO: CENTRO LOGÍSTICO", key="btn_log"):
        try:
            st.switch_page("pages/2_Operaciones_Logistica.py")
        except:
            st.error("Página no encontrada.")

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
                <div><span class="modal-highlight">Conciliación Ciega:</span> Compara el conteo físico real contra el XML digital, alertando faltantes.</div>
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
    if st.button("🚀 IR AL DEMO: RECEPCIÓN XML", key="btn_xml"):
        try:
            st.switch_page("pages/3_Recepcion_Inteligente.py")
        except:
            st.error("Página no encontrada.")

# ==============================================================================
# --- 5. ESTRUCTURA PRINCIPAL (LAYOUT) ---
# ==============================================================================

# >>> HERO SECTION
st.markdown("""
<div class="hero-container">
    <div class="company-tag">Arquitectura de Datos Empresarial & IA</div>
    <h1 class="main-title">GM-<span class="highlight-text">DATOVATE</span></h1>
    <p class="subtitle">
        Transformamos el caos operativo en <b>Ventaja Competitiva</b>.
        <br>Una suite integrada que utiliza Inteligencia Artificial para sincronizar Inventarios, Logística y Finanzas en tiempo real.
    </p>
</div>
""", unsafe_allow_html=True)

# >>> GRID DE MÓDULOS
st.write("")
st.markdown("<h3 style='text-align: center; margin-bottom: 40px; color: white;'>🚀 Ecosistema NEXUS: Explore el Valor de Negocio</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

# --- CARD 1 ---
with col1:
    st.markdown("""
    <div class="flow-card">
        <div class="card-icon">📊</div>
        <div class="card-title">1. Control & Estrategia</div>
        <p class="card-desc">El cerebro financiero. Análisis predictivo de capital, detección de riesgos y optimización con IA.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explorar Módulo ➝", key="b1"):
        open_inventory_modal()

# --- CARD 2 ---
with col2:
    st.markdown("""
    <div class="flow-card">
        <div class="card-icon">🚚</div>
        <div class="card-title">2. Logística Inteligente</div>
        <p class="card-desc">El brazo ejecutor. Automatización de compras y rebalanceo autónomo de stock entre bodegas.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explorar Módulo ➝", key="b2"):
        open_logistics_modal()

# --- CARD 3 ---
with col3:
    st.markdown("""
    <div class="flow-card">
        <div class="card-icon">📥</div>
        <div class="card-title">3. Recepción Blindada</div>
        <p class="card-desc">La puerta de entrada. Procesamiento automático de XML (DIAN) y conciliación fiscal vs física.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explorar Módulo ➝", key="b3"):
        open_reception_modal()

# >>> PERFIL LÍDER (LAYOUT OPTIMIZADO)
st.write("")
st.write("")

# Usamos columnas para centrar el perfil sin que ocupe el 100% del ancho si la pantalla es muy grande
c_spacer_l, c_profile, c_spacer_r = st.columns([1, 8, 1])

with c_profile:
    st.markdown(f"""
    <div class="profile-box">
        <img src="{foto_diego_src}" class="profile-img" alt="Diego Mauricio García">
        <div style="flex: 1;">
            <h4 style="color: #06B6D4; margin:0 0 5px 0; font-weight: 800; letter-spacing:1.5px; font-size: 0.9rem;">ARQUITECTURA & VISIÓN</h4>
            <h2 style="color: white; margin: 0 0 15px 0; font-size: 2.2rem; font-weight: 800;">Diego Mauricio García</h2>
            <p style="color: #CBD5E1; font-size: 1.05rem; line-height: 1.7; font-style: italic; border-left: 4px solid #06B6D4; padding-left: 20px; margin-bottom: 20px;">
                "En GM-Datovate no vendemos software, diseñamos el sistema nervioso de su organización. 
                Mi obsesión es eliminar la fricción operativa mediante arquitecturas de datos que piensan, aprenden y actúan por sí mismas."
            </p>
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                <span style="background: rgba(15,23,42,0.6); border: 1px solid #334155; color: #94A3B8; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem;">CEO & Founder</span>
                <span style="background: rgba(15,23,42,0.6); border: 1px solid #334155; color: #94A3B8; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem;">Data Architect</span>
                <span style="background: rgba(15,23,42,0.6); border: 1px solid #334155; color: #94A3B8; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem;">Python Expert</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align: center; color: #475569; margin-bottom: 40px; font-size: 0.8rem;'>© 2025 GM-DATOVATE. Todos los derechos reservados.</div>", unsafe_allow_html=True)
