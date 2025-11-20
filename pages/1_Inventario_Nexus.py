import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Nexus AI | Inventario",
    page_icon="📦",
    layout="wide"
)

# --- ESTILOS COMPARTIDOS (Para mantener identidad de marca) ---
st.markdown("""
<style>
    :root { --primary: #0D3B66; --bg-light: #F0F2F6; }
    .metric-card {
        background-color: white;
        border: 1px solid #e0e0e0;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    h1, h2, h3 { color: var(--primary); }
</style>
""", unsafe_allow_html=True)

# --- GENERADOR DE DATOS (Tu Motor de Simulación) ---
@st.cache_data
def generar_data_demo():
    tiendas = ['Sede Principal', 'Sucursal Norte', 'Sucursal Sur', 'Outlet Centro']
    categorias = ['Herramientas', 'Construcción', 'Pinturas', 'Eléctricos', 'Plomería']
    
    data = []
    # 500 Productos simulados
    for i in range(100, 600):
        cat = np.random.choice(categorias)
        sku = f"SKU-{i}"
        costo = np.random.uniform(5000, 150000)
        precio = costo * 1.4 
        
        for tienda in tiendas:
            factor_demanda = np.random.choice([0.1, 0.5, 1.0, 3.0], p=[0.1, 0.4, 0.4, 0.1])
            demanda_diaria = np.random.poisson(lam=2) * factor_demanda
            stock_actual = int(demanda_diaria * np.random.uniform(0, 60))
            lead_time = np.random.choice([3, 7, 15, 30])
            ventas_60_dias = int(demanda_diaria * 60)
            
            item = {
                'SKU': sku, 'Descripcion': f"Producto Premium {cat} {i}", 'Categoria': cat,
                'Tienda': tienda, 'Costo_Unitario': round(costo, 2), 'Precio_Venta': round(precio, 2),
                'Stock': stock_actual, 'Ventas_60_Dias': ventas_60_dias, 'Lead_Time_Dias': lead_time,
                'Proveedor': f"Proveedor {np.random.choice(['Alpha', 'Beta', 'Gamma'])}"
            }
            data.append(item)
            
    df = pd.DataFrame(data)
    df['Demanda_Diaria'] = df['Ventas_60_Dias'] / 60
    df['Valor_Inventario'] = df['Stock'] * df['Costo_Unitario']
    
    # Lógica ABC
    total_ventas = df['Ventas_60_Dias'] * df['Costo_Unitario']
    df = df.sort_values('Ventas_60_Dias', ascending=False)
    df['Acumulado'] = (df['Ventas_60_Dias'] * df['Costo_Unitario']).cumsum()
    df['Porcentaje_Acum'] = df['Acumulado'] / total_ventas.sum()
    df['Clasificacion_ABC'] = df['Porcentaje_Acum'].apply(lambda x: 'A' if x <= 0.80 else ('B' if x <= 0.95 else 'C'))
    
    # Lógica Estados
    df['Dias_Inventario'] = np.where(df['Demanda_Diaria'] > 0, df['Stock'] / df['Demanda_Diaria'], 999)
    conditions = [
        (df['Stock'] == 0) & (df['Demanda_Diaria'] > 0),
        (df['Dias_Inventario'] > 90),
        (df['Stock'] < (df['Demanda_Diaria'] * df['Lead_Time_Dias']) * 1.5)
    ]
    choices = ['🔴 Quiebre Crítico', '🔵 Excedente', '🟡 Riesgo']
    df['Estado'] = np.select(conditions, choices, default='✅ Saludable')
    
    return df

# --- UI PRINCIPAL ---
st.title("📦 NEXUS AI | Optimización de Inventarios")
st.markdown("Módulo avanzado para la detección de quiebres y optimización de capital de trabajo.")

# Sidebar
with st.sidebar:
    st.header("Filtros de Análisis")
    df_master = generar_data_demo()
    filtro_tienda = st.selectbox("Sede:", ["Todas"] + list(df_master['Tienda'].unique()))
    
    st.info("💡 **Tip:** Este módulo simula la conexión con su ERP en tiempo real.")
    if st.button("🏠 Volver al Inicio"):
        st.switch_page("0_Inicio.py")

# Filtrado
df = df_master[df_master['Tienda'] == filtro_tienda] if filtro_tienda != "Todas" else df_master.copy()

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Valor Inventario", f"${df['Valor_Inventario'].sum()/1e6:,.1f} M")
col2.metric("SKUs en Quiebre", len(df[df['Estado'] == '🔴 Quiebre Crítico']))
col3.metric("Excedente Capital", f"${df[df['Estado'] == '🔵 Excedente']['Valor_Inventario'].sum()/1e6:,.1f} M")
col4.metric("Rotación Promedio", f"{df['Dias_Inventario'].median():.0f} días")

st.divider()

# Gráficos
tab1, tab2 = st.tabs(["📊 Diagnóstico Visual", "📋 Acciones Sugeridas"])

with tab1:
    c1, c2 = st.columns([2,1])
    with c1:
        st.subheader("Distribución ABC del Inventario")
        fig = px.sunburst(df, path=['Clasificacion_ABC', 'Categoria'], values='Valor_Inventario', color='Clasificacion_ABC')
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Estado de Salud")
        fig2 = px.pie(df, names='Estado', title='Proporción de SKUs por Estado', hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("🚨 Prioridad Alta: Productos a Reabastecer")
    st.dataframe(
        df[df['Estado'] == '🔴 Quiebre Crítico'][['SKU', 'Descripcion', 'Proveedor', 'Demanda_Diaria']].head(10),
        use_container_width=True,
        hide_index=True
    )
    
    st.subheader("💸 Oportunidad: Productos para Liquidar (Excedentes)")
    st.dataframe(
        df[df['Estado'] == '🔵 Excedente'][['SKU', 'Descripcion', 'Stock', 'Dias_Inventario', 'Valor_Inventario']].sort_values('Valor_Inventario', ascending=False).head(10),
        use_container_width=True,
        hide_index=True
    )
