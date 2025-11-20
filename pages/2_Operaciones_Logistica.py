import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import time
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="NEXUS OPS | Abastecimiento Inteligente",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #fafafa; }
    .metric-card {
        background: linear-gradient(145deg, #1e232a, #161b22);
        border-radius: 10px; padding: 15px; border-left: 5px solid #2E86C1;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-value { font-size: 24px; font-weight: bold; color: white; }
    .metric-label { font-size: 12px; color: #a0a0a0; text-transform: uppercase; }
    div[data-testid="stExpander"] { border: 1px solid #2E86C1; border-radius: 8px; }
    .success-box { padding: 10px; background-color: rgba(0, 204, 150, 0.1); border: 1px solid #00CC96; border-radius: 5px; color: #00CC96; }
</style>
""", unsafe_allow_html=True)

# --- 1. MOTOR DE SIMULACIÓN (BACKEND FALSO) ---
@st.cache_data
def init_mock_data():
    """Genera datos coherentes para el demo sin necesidad de archivos externos."""
    tiendas = ['Sede Principal', 'Norte', 'Sur', 'Occidente', 'Outlet']
    proveedores = ['DISTRIBUIDORA GLOBAL', 'IMPORTADOS S.A.', 'ACEROS DEL CARIBE', 'HERRAMIENTAS PRO']
    
    # Generar Inventario Maestro
    data = []
    for i in range(1001, 1051): # 50 productos
        sku = f"REF-{i}"
        costo = np.random.randint(5000, 150000)
        peso = round(np.random.uniform(0.1, 5.0), 2)
        
        for tienda in tiendas:
            demanda = np.random.randint(1, 50)
            stock = np.random.randint(0, 100)
            # Forzar algunos quiebres y excedentes para el demo
            if random.random() < 0.1: stock = 0 # Quiebre provocado
            if random.random() < 0.1: stock = 200 # Excedente provocado
            
            necesidad = max(0, (demanda * 45 / 30) - stock) # Stock objetivo 45 días
            excedente = max(0, stock - (demanda * 60 / 30)) # Excedente si > 60 días
            
            data.append({
                'SKU': sku,
                'Descripcion': f"Producto Industrial {i}",
                'Marca_Nombre': random.choice(['3M', 'Bosch', 'DeWalt', 'Stanley']),
                'Proveedor': random.choice(proveedores),
                'Almacen_Nombre': tienda,
                'Stock': stock,
                'Costo_Promedio_UND': costo,
                'Precio_Venta_Estimado': costo * 1.4,
                'Peso_Articulo': peso,
                'Demanda_Diaria_Promedio': demanda / 30,
                'Necesidad_Total': necesidad,
                'Excedente_Trasladable': excedente,
                'Stock_En_Transito': 0 if random.random() > 0.2 else np.random.randint(10, 50),
                'Segmento_ABC': random.choice(['A', 'A', 'B', 'C'])
            })
    return pd.DataFrame(data)

# Cargar datos en Session State (Persistencia durante la demo)
if 'df_maestro' not in st.session_state:
    st.session_state.df_maestro = init_mock_data()
    st.session_state.ordenes_generadas = [] # Historial de órdenes simulado

# --- 2. LÓGICA DE NEGOCIO (TRANSFERENCIAS Y COMPRAS) ---
def calcular_logica_abastecimiento(df):
    """Recalcula necesidades considerando tránsito y traslados."""
    df['Necesidad_Ajustada'] = (df['Necesidad_Total'] - df['Stock_En_Transito']).clip(lower=0)
    
    # Simulación simple de algoritmo de traslados
    # En un caso real, esto cruzaría excedentes vs necesidades
    df['Sugerencia_Traslado'] = df.apply(lambda x: min(x['Necesidad_Ajustada'], 10) if x['Necesidad_Ajustada'] > 0 else 0, axis=1)
    df['Sugerencia_Compra'] = (df['Necesidad_Ajustada'] - df['Sugerencia_Traslado']).clip(lower=0)
    
    return df

df_work = calcular_logica_abastecimiento(st.session_state.df_maestro.copy())

# --- UI: SIDEBAR ---
with st.sidebar:
    st.page_link("Portafolio_Servicios.py", label="🏠 Volver al Inicio", icon="🔙")
    st.divider()
    st.header("🎛️ Panel de Operaciones")
    
    tiendas_list = sorted(df_work['Almacen_Nombre'].unique())
    filtro_tienda = st.selectbox("Vista de Tienda:", ["Consolidado"] + tiendas_list)
    
    if filtro_tienda != "Consolidado":
        df_vista = df_work[df_work['Almacen_Nombre'] == filtro_tienda]
    else:
        df_vista = df_work
        
    st.info("🟢 Conexión ERP: Establecida\nLast Sync: Hace 2 min")

# --- UI: CABECERA ---
st.title("⚙️ NEXUS OPS | Centro de Abastecimiento")
st.markdown("Automatización de compras y traslados basada en análisis predictivo.")

# --- TABS PRINCIPALES ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Diagnóstico & KPIs", "🔄 Algoritmo de Traslados", "🛒 Generador de Compras", "✅ Tracking de Órdenes"])

# --- TAB 1: DIAGNÓSTICO ---
with tab1:
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    
    compra_total = (df_vista['Sugerencia_Compra'] * df_vista['Costo_Promedio_UND']).sum()
    traslado_ahorro = (df_vista['Sugerencia_Traslado'] * df_vista['Costo_Promedio_UND']).sum()
    venta_riesgo = df_vista[df_vista['Stock'] == 0]['Precio_Venta_Estimado'].sum() * 5 # Est. 5 días
    
    def kpi_box(col, label, val, prefix="$", color="#2E86C1"):
        col.markdown(f"""
        <div class="metric-card" style="border-left: 5px solid {color};">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{prefix}{val:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    kpi_box(col_kpi1, "Presupuesto de Compra Sugerido", compra_total, color="#EF553B")
    kpi_box(col_kpi2, "Ahorro Potencial (Traslados)", traslado_ahorro, color="#00CC96")
    kpi_box(col_kpi3, "Riesgo Venta Perdida (5 días)", venta_riesgo, color="#FFA15A")
    kpi_box(col_kpi4, "SKUs a Gestionar", len(df_vista[df_vista['Sugerencia_Compra'] > 0]), prefix="", color="#636EFA")
    
    st.markdown("### 📉 Análisis de Distribución")
    c1, c2 = st.columns(2)
    with c1:
        df_chart = df_vista.groupby('Marca_Nombre')['Sugerencia_Compra'].sum().reset_index().sort_values('Sugerencia_Compra', ascending=False).head(10)
        fig = px.bar(df_chart, x='Marca_Nombre', y='Sugerencia_Compra', title="Top Marcas a Reabastecer (Unidades)", color_discrete_sequence=['#2E86C1'])
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        # Scatter costo vs unidades
        fig2 = px.scatter(df_vista[df_vista['Sugerencia_Compra']>0], x="Sugerencia_Compra", y="Costo_Promedio_UND", size="Sugerencia_Compra", color="Segmento_ABC", title="Matriz de Compra (Volumen vs Costo)")
        st.plotly_chart(fig2, use_container_width=True)

# --- TAB 2: TRASLADOS ---
with tab2:
    st.subheader("🔄 Plan de Balanceo de Inventario (Inter-Tiendas)")
    st.markdown("El algoritmo ha detectado **Excedentes** en algunas tiendas que coinciden con **Necesidades** en otras. Mover stock es más barato que comprar.")
    
    # Simular dataframe de traslados
    df_traslados = df_vista[df_vista['Sugerencia_Traslado'] > 0].copy()
    if df_traslados.empty:
        st.success("✅ El inventario está balanceado. No se requieren traslados.")
    else:
        # Crear una vista amigable
        df_traslados['Origen_Sugerido'] = df_traslados['Almacen_Nombre'].apply(lambda x: random.choice([t for t in tiendas_list if t != x]))
        
        df_editor_traslado = df_traslados[['SKU', 'Descripcion', 'Origen_Sugerido', 'Almacen_Nombre', 'Sugerencia_Traslado', 'Peso_Articulo']].head(10)
        df_editor_traslado.columns = ['SKU', 'Producto', 'Desde (Origen)', 'Para (Destino)', 'Cant. a Enviar', 'Peso Unit.']
        df_editor_traslado['Confirmar'] = False
        
        st.info(f"💡 Se encontraron {len(df_traslados)} oportunidades de traslado. Ahorro proyectado: ${traslado_ahorro:,.0f}")
        
        edited_traslados = st.data_editor(
            df_editor_traslado,
            column_config={
                "Confirmar": st.column_config.CheckboxColumn(required=True),
                "Cant. a Enviar": st.column_config.NumberColumn(min_value=1, step=1)
            },
            use_container_width=True,
            hide_index=True,
            key="editor_traslados"
        )
        
        col_act1, col_act2 = st.columns([1, 3])
        if col_act1.button("🚀 Ejecutar Traslados", type="primary"):
            seleccionados = edited_traslados[edited_traslados['Confirmar']]
            if not seleccionados.empty:
                with st.spinner("Generando órdenes de transferencia en ERP..."):
                    time.sleep(1.5)
                    st.balloons()
                    st.markdown(f"""
                    <div class="success-box">
                        ✅ <b>{len(seleccionados)} Traslados Generados Exitosamente.</b><br>
                        Los jefes de bodega de <b>{', '.join(seleccionados['Desde (Origen)'].unique())}</b> han recibido la notificación por WhatsApp y Email.
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Seleccione al menos un ítem para trasladar.")

# --- TAB 3: COMPRAS ---
with tab3:
    st.subheader("🛒 Generador de Órdenes de Compra")
    st.markdown("Sugerencias basadas en *Punto de Reorden*, *Demanda Promedio* y *Lead Time* del proveedor.")
    
    filtro_prov = st.selectbox("Filtrar Proveedor para Orden:", ["Todos"] + sorted(df_work['Proveedor'].unique()))
    
    df_compras = df_work[df_work['Sugerencia_Compra'] > 0].copy()
    if filtro_prov != "Todos":
        df_compras = df_compras[df_compras['Proveedor'] == filtro_prov]
        
    df_compras['Subtotal'] = df_compras['Sugerencia_Compra'] * df_compras['Costo_Promedio_UND']
    
    # Preparar DF para editor
    df_editor_compra = df_compras[['SKU', 'Descripcion', 'Proveedor', 'Stock', 'Necesidad_Total', 'Sugerencia_Compra', 'Costo_Promedio_UND', 'Subtotal']].head(15)
    df_editor_compra['Seleccionar'] = True
    
    edited_compras = st.data_editor(
        df_editor_compra,
        column_config={
            "Sugerencia_Compra": st.column_config.NumberColumn(label="Cant. a Pedir", min_value=1, step=1),
            "Subtotal": st.column_config.ProgressColumn(format="$%.2f", min_value=0, max_value=int(df_editor_compra['Subtotal'].max())),
            "Costo_Promedio_UND": st.column_config.NumberColumn(format="$%.2f"),
            "Seleccionar": st.column_config.CheckboxColumn(required=True)
        },
        use_container_width=True,
        hide_index=True,
        key="editor_compras"
    )
    
    # Resumen de la orden
    items_pedir = edited_compras[edited_compras['Seleccionar']]
    total_orden = (items_pedir['Sugerencia_Compra'] * items_pedir['Costo_Promedio_UND']).sum()
    
    col_send1, col_send2 = st.columns([3, 1])
    with col_send1:
        st.markdown(f"### Total Orden Estimada: **${total_orden:,.0f}**")
    with col_send2:
        if st.button("📧 Enviar Orden de Compra", type="primary", use_container_width=True):
            if not items_pedir.empty:
                with st.spinner(f"Contactando API de {items_pedir['Proveedor'].iloc[0]}..."):
                    time.sleep(2) # Simular tiempo de envío
                    
                    # Guardar en historial simulado
                    nuevo_id = f"OC-{random.randint(10000, 99999)}"
                    st.session_state.ordenes_generadas.append({
                        "ID": nuevo_id,
                        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "Proveedor": items_pedir['Proveedor'].iloc[0] if filtro_prov != "Todos" else "Múltiples",
                        "Items": len(items_pedir),
                        "Total": total_orden,
                        "Estado": "Enviado 📨"
                    })
                    
                    st.success(f"✅ Orden {nuevo_id} enviada correctamente por Email y WhatsApp al proveedor.")
            else:
                st.warning("No hay ítems seleccionados.")

# --- TAB 4: TRACKING ---
with tab4:
    st.subheader("📡 Torre de Control (Tracking)")
    
    # Datos simulados de historial + los generados en la sesión
    historial_base = [
        {"ID": "OC-98123", "Fecha": "2023-10-20 09:30", "Proveedor": "DISTRIBUIDORA GLOBAL", "Items": 15, "Total": 15400000, "Estado": "Recibido ✅"},
        {"ID": "OC-98124", "Fecha": "2023-10-21 14:15", "Proveedor": "ACEROS DEL CARIBE", "Items": 4, "Total": 3200000, "Estado": "En Tránsito 🚚"},
        {"ID": "TR-4401", "Fecha": "2023-10-22 10:00", "Proveedor": "TRASLADO INTERNO (Norte->Sur)", "Items": 8, "Total": 0, "Estado": "Pendiente ⏳"}
    ]
    
    # Unir historial base con lo generado en esta sesión
    full_history = st.session_state.ordenes_generadas + historial_base
    df_track = pd.DataFrame(full_history)
    
    st.dataframe(
        df_track,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Total": st.column_config.NumberColumn(format="$ %d"),
            "Estado": st.column_config.Column(width="medium")
        }
    )
    
    if st.button("Actualizar Estados (Simulación API)"):
        with st.spinner("Consultando transportadoras..."):
            time.sleep(1)
            st.toast("Estados actualizados correctamente", icon="📡")
