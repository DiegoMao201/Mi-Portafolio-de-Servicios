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

# Fallback: Si no encuentra la foto local, usa un icono genérico profesional
foto_diego_src = f"data:image/png;base64,{img_base64}" if img_base64 else "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

# ==============================================================================
# --- 3. CSS PREMIUM (ESTILO CLARO / LIGHT THEME) ---
# ==============================================================================
st.markdown(f"""
<style>
    /* IMPORTAR FUENTE */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&display=swap');

    /* --- FONDO GENERAL (LIGHT THEME) --- */
    .stApp {{
        background-color: #FFFFFF; /* Fondo Blanco Puro */
        background-image: radial-gradient(#F1F5F9 1px, transparent 1px); /* Puntos sutiles */
        background-size: 20px 20px;
        color: #1E293B; /* Texto Gris Oscuro (Slate 800) */
        font-family: 'Inter', sans-serif;
    }}
    
    /* MODALES (Ventanas emergentes) */
    .custom-modal-box {{
        background: #FFFFFF;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); /* Sombra suave */
    }}
    
    .modal-header-icon {{
        font-size: 3rem;
        text-align: center;
        display: block;
        margin-bottom: 10px;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
    }}

    .modal-title {{
        color: #0F172A !important; /* Texto casi negro */
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 1.6rem;
        text-align: center;
        margin-bottom: 15px;
    }}

    .modal-body-text {{
        color: #475569 !important; /* Gris medio para lectura */
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 25px;
        text-align: justify;
    }}

    .modal-list-container {{
        background-color: #F8FAFC; /* Gris muy claro */
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #E2E8F0;
    }}

    .modal-item {{
        display: flex;
        align-items: flex-start;
        margin-bottom: 12px;
        color: #334155;
        font-size: 0.95rem;
    }}

    .modal-bullet {{
        color: #2563EB; /* Azul Royal */
        font-size: 1.1rem;
        margin-right: 10px;
        line-height: 1.2;
    }}
    
    .modal-highlight {{
        color: #0369A1; /* Azul oscuro fuerte */
        font-weight: 700;
    }}

    .modal-quote {{
        text-align: center; 
        margin-top: 25px; 
        color: #64748B; 
        font-style: italic; 
        font-size: 0.9rem;
        border-top: 1px solid #E2E8F0;
        padding-top: 15px;
    }}

    /* HERO SECTION (Encabezado) */
    .hero-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 60px 20px 40px 20px;
        background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 50px;
    }}

    .company-tag {{
        background-color: #E0F2FE; /* Azul muy pálido */
        color: #0284C7; /* Azul corporativo */
        padding: 6px 18px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 20px;
        border: 1px solid #BAE6FD;
    }}

    .main-title {{
        font-size: 4rem;
        font-weight: 900;
        margin: 0;
        line-height: 1.1;
        color: #0F172A; /* Slate 900 */
        letter-spacing: -2px;
    }}

    /* Ajuste tamaño título en móvil */
    @media (max-width: 768px) {{
        .main-title {{
            font-size: 2.5rem;
        }}
    }}

    .highlight-text {{
        background: linear-gradient(90deg, #2563EB, #0891B2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    .subtitle {{
        font-size: 1.25rem;
        color: #64748B; /* Gris elegante */
        max-width: 750px;
        margin-top: 25px;
        line-height: 1.6;
        font-weight: 400;
    }}

    /* CARDS (Tarjetas de Módulos) */
    .flow-card {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 35px;
        border-radius: 20px;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }}
    
    .flow-card:hover {{
        transform: translateY(-8px);
        border-color: #2563EB;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }}

    .card-icon {{ font-size: 3rem; margin-bottom: 20px; }}
    
    .card-title {{ 
        font-size: 1.5rem; 
        font-weight: 700; 
        color: #1E293B; 
        margin-bottom: 12px; 
    }}
    
    .card-desc {{ 
        font-size: 1rem; 
        color: #64748B; 
        margin-bottom: 25px; 
        line-height: 1.5; 
    }}

    /* --- PERFIL (RESPONSIVE FIX) --- */
    .profile-box {{
        background: #FFFFFF;
        padding: 40px;
        border-radius: 25px;
        border: 1px solid #E2E8F0;
        margin-top: 60px;
        display: flex;
        align-items: center; /* Centrado vertical en desktop */
        box-shadow: 0 10px 40px rgba(0,0,0,0.08); /* Sombra elegante */
        flex-direction: row; 
    }}
    
    .profile-img {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #FFFFFF;
        margin-right: 40px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        flex-shrink: 0; 
    }}

    .profile-content {{
        flex: 1;
    }}

    .profile-quote {{
        color: #475569; 
        font-size: 1.15rem; 
        line-height: 1.8; 
        font-style: italic; 
        border-left: 4px solid #0EA5E9; /* Borde cian/azul */
        padding-left: 25px;
    }}

    .profile-tags {{
        margin-top: 25px; 
        display: flex; 
        gap: 12px; 
        flex-wrap: wrap;
    }}

    .tag-pill {{
        background-color: #F1F5F9;
        color: #334155;
        border: 1px solid #CBD5E1;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }}

    /* --- MEDIA QUERY PARA MÓVILES --- */
    @media only screen and (max-width: 768px) {{
        .profile-box {{
            flex-direction: column; 
            text-align: center;     
            padding: 30px 20px;
        }}

        .profile-img {{
            margin-right: 0;       
            margin-bottom: 20px;    
            width: 120px;           
            height: 120px;
        }}

        .profile-quote {{
            border-left: none;      
            border-top: 3px solid #0EA5E9; 
            padding-left: 0;
            padding-top: 20px;
            font-size: 1rem;
        }}

        .profile-tags {{
            justify-content: center; 
        }}
    }}

    /* BOTONES */
    div.stButton > button {{
        width: 100%;
        background: linear-gradient(135deg, #2563EB 0%, #0284C7 100%);
        color: white;
        border: none;
        padding: 12px 20px;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
    }}
    
    div.stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.5);
    }}

</style>
""", unsafe_allow_html=True)

# ==============================================================================
# --- 4. DEFINICIÓN DE MODALES (CONTENIDO) ---
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
# --- 5. ESTRUCTURA PRINCIPAL DEL UI ---
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
st.markdown("<h3 style='text-align: center; margin-bottom: 50px; font-size: 1.8rem; color: #334155;'>🚀 Ecosistema NEXUS: Explore el Valor de Negocio</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

# --- CARD 1 ---
with col1:
    st.markdown("""
    <div class="flow-card">
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
    <div class="flow-card">
        <div>
            <div class="card-icon">🚚</div>
            <div class="card-title">2. Abastecimiento Con IA</div>
            <div class="card-desc">El brazo ejecutor. Automatización de compras y rebalanceo autónomo de stock entre bodegas.</div>
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
    <div class="profile-box">
        <img src="{foto_diego_src}" class="profile-img" alt="Diego Mauricio García">
        <div class="profile-content">
            <h4 style="color: #0284C7; margin:0 0 10px 0; font-weight: 800; letter-spacing:1px; font-size: 0.9rem;">ARQUITECTURA & VISIÓN</h4>
            <h2 style="color: #0F172A; margin: 0 0 20px 0; font-size: 2.2rem; font-weight: 900;">Diego Mauricio García</h2>
            <p class="profile-quote">
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
st.markdown("<div style='text-align: center; color: #94A3B8; margin-bottom: 40px; font-size: 0.85rem;'>© 2025 GM-DATOVATE. Todos los derechos reservados.</div>", unsafe_allow_html=True)
