import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import random
import io
from fpdf import FPDF
import xlsxwriter

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="NEXUS OPS | Abastecimiento Estratégico",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ESTILOS CSS (TEMA CLARO Y CORPORATIVO) ---
st.markdown("""
<style>
    /* Fondo General y Tipografía */
    .stApp {
        background-color: #FFFFFF;
        color: #333333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Tarjetas de Métricas (KPIs) */
    .metric-card {
        background-color: #F8F9FA;
        border: 1px solid #E9ECEF;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #2E86C1;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 10px;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #2E86C1;
    }
    .metric-label {
        font-size: 13px;
        color: #666666;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Bloques de Guía Estratégica (Narrativa de Venta) */
    .guide-box {
        background-color: #E8F4FD;
        border-left: 4px solid #2E86C1;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 25px;
        color: #0C3658;
        font-size: 15px;
    }
    .guide-title {
        font-weight: 700;
        font-size: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }
    
    /* Personalización de Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.0rem;
        font-weight: 600;
    }
    
    /* Botones */
    div.stButton > button:first-child {
        border-radius: 6px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE SIMULACIÓN DE DATOS (BACKEND SIMULADO) ---
@st.cache_data
def init_mock_data():
    """Genera datos base realistas para la demostración."""
    tiendas = ['Sede Principal', 'Norte', 'Sur', 'Occidente', 'Outlet']
    proveedores = ['DISTRIBUIDORA GLOBAL', 'IMPORTADOS S.A.', 'ACEROS DEL CARIBE', 'HERRAMIENTAS PRO', 'ELECTRO-MUNDO']
    categorias = ['Herramientas', 'Construcción', 'Eléctricos', 'Pinturas', 'Seguridad Ind.']
    
    data = []
    for i in range(1001, 1081): # 80 productos simulados
        cat = random.choice(categorias)
        sku = f"{cat[:3].upper()}-{i}"
        costo = np.random.randint(5000, 250000)
        
        for tienda in tiendas:
            demanda = np.random.randint(0, 60)
            stock = np.random.randint(0, 120)
            
            # Lógica para forzar escenarios interesantes para el demo
            if random.random() < 0.15: stock = 0 # Quiebre forzado
            if random.random() < 0.10: stock = 300 # Excedente forzado
            
            # Cálculo de necesidades (Lógica de negocio)
            necesidad = max(0, (demanda * 1.5) - stock) # Cobertura ideal 1.5 meses
            excedente = max(0, stock - (demanda * 3)) # Excedente si supera 3 meses
            
            # Clasificación ABC basada en valor
            valor_movimiento = demanda * costo
            abc = 'A' if valor_movimiento > 5000000 else ('B' if valor_movimiento > 1000000 else 'C')

            data.append({
                'SKU': sku,
                'Descripcion': f"Item {cat} Profesional {i}",
                'Categoria': cat,
                'Marca_Nombre': random.choice(['Makita', 'Bosch', '3M', 'Pintuco', 'Schneider']),
                'Proveedor': random.choice(proveedores),
                'Almacen_Nombre': tienda,
                'Stock': stock,
                'Costo_Promedio_UND': costo,
                'Precio_Venta': costo * 1.4,
                'Peso_Articulo': round(random.uniform(0.5, 10.0), 2),
                'Demanda_Mes': demanda,
                'Necesidad_Total': int(necesidad),
                'Excedente_Trasladable': int(excedente),
                'Stock_En_Transito': 0,
                'Segmento_ABC': abc
            })
    return pd.DataFrame(data)

# Inicializar estado
if 'df_maestro' not in st.session_state:
    st.session_state.df_maestro = init_mock_data()

# Lógica de abastecimiento (Separa qué se puede trasladar vs comprar)
def calcular_abastecimiento(df):
    # Si hay necesidad, intentamos cubrir hasta 12 unidades con traslados (simulación)
    df['Sugerencia_Traslado'] = df.apply(lambda x: min(x['Necesidad_Total'], 12) if x['Necesidad_Total'] > 0 else 0, axis=1)
    # Lo que falte, se compra
    df['Sugerencia_Compra'] = (df['Necesidad_Total'] - df['Sugerencia_Traslado']).clip(lower=0)
    return df

df_work = calcular_abastecimiento(st.session_state.df_maestro.copy())

# --- 4. FUNCIONES GENERADORAS DE ARCHIVOS (EXCEL Y PDF) ---

def generar_excel(df, hoja="Reporte"):
    """Genera un archivo Excel en memoria bytes."""
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name=hoja)
    
    workbook = writer.book
    worksheet = writer.sheets[hoja]
    
    # Formatos profesionales
    header_fmt = workbook.add_format({'bold': True, 'fg_color': '#2E86C1', 'font_color': 'white', 'border': 1})
    money_fmt = workbook.add_format({'num_format': '$#,##0'})
    
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_fmt)
        # Ajustar ancho
        worksheet.set_column(col_num, col_num, 20)
        
    writer.close()
    return output.getvalue()

class PDFReport(FPDF):
    """Clase personalizada para el PDF."""
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(46, 134, 193) # Azul corporativo
        self.cell(0, 10, 'NEXUS OPS - Reporte Operativo', 0, 1, 'C')
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

def generar_pdf(df, titulo):
    """Genera un PDF simple con tabla en memoria bytes."""
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(0)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"{titulo}", 0, 1, 'L')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 10, f"Fecha Generación: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'L')
    pdf.ln(5)
    
    # Tabla simple
    # Calculamos ancho dinámico
    num_cols = len(df.columns)
    col_width = 190 / num_cols if num_cols > 0 else 10
    row_height = 7
    
    # Encabezados
    pdf.set_font("Arial", 'B', 8)
    pdf.set_fill_color(232, 244, 253) # Azul muy claro
    for col in df.columns:
        # Truncar nombre de columna si es muy largo
        clean_col = str(col)[:15]
        pdf.cell(col_width, row_height, clean_col, 1, 0, 'C', True)
    pdf.ln()
    
    # Filas
    pdf.set_font("Arial", '', 8)
    for i, row in df.iterrows():
        for col in df.columns:
            txt = str(row[col])
            # Truncar texto de celda si es muy largo
            pdf.cell(col_width, row_height, txt[:18], 1, 0, 'C')
        pdf.ln()
    
    # --- CORRECCIÓN DEL ERROR ---
    # Devolvemos los bytes directamente.
    return bytes(pdf.output())

# --- 5. UI: BARRA LATERAL DE NAVEGACIÓN ---
with st.sidebar:
    st.page_link("Portafolio_Servicios.py", label="🏠 Volver al Inicio", icon="🔙")
    st.divider()
    
    # Simulación de logo
    st.markdown("<h2 style='text-align: center; color: #2E86C1;'>NEXUS OPS</h2>", unsafe_allow_html=True)
    
    st.subheader("Filtros Globales")
    
    lista_tiendas = ["Todas"] + sorted(df_work['Almacen_Nombre'].unique())
    filtro_tienda = st.selectbox("Sede / Almacén:", lista_tiendas)
    
    lista_marcas = sorted(df_work['Marca_Nombre'].unique())
    filtro_marca = st.multiselect("Filtrar Marcas:", lista_marcas, default=lista_marcas[:3])
    
    st.divider()
    st.info("🟢 **Conexión ERP:** Establecida\n📅 **Datos:** Tiempo Real")

# Aplicar Filtros Globales
if filtro_tienda != "Todas":
    df_vista = df_work[df_work['Almacen_Nombre'] == filtro_tienda]
else:
    df_vista = df_work

if filtro_marca:
    df_vista = df_vista[df_vista['Marca_Nombre'].isin(filtro_marca)]

# --- 6. UI: ENCABEZADO PRINCIPAL ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🏭 Centro de Control Logístico")
    st.markdown("Gestión unificada de abastecimiento, inventarios y distribución.")
with col_h2:
    if st.button("🔄 Actualizar Análisis"):
        st.toast("Recalculando algoritmos de abastecimiento...", icon="🤖")
        time.sleep(1)
        st.rerun()

# --- 7. PESTAÑAS DE CONTENIDO ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Diagnóstico Estratégico", 
    "🚚 Gestión de Traslados", 
    "🛒 Gestión de Compras", 
    "📡 Torre de Control"
])

# === TAB 1: DIAGNÓSTICO ===
with tab1:
    st.markdown("""
    <div class="guide-box">
        <div class="guide-title">💡 Guía Estratégica: Diagnóstico</div>
        Esta vista le permite identificar en segundos dónde está atrapado su capital y dónde está perdiendo ventas por quiebres.
        <br>Utilice el gráfico de <b>Nivel de Servicio</b> para medir la calidad de su inventario actual.
    </div>
    """, unsafe_allow_html=True)

    # KPIs Principales
    c1, c2, c3, c4 = st.columns(4)
    
    total_inv = (df_vista['Stock'] * df_vista['Costo_Promedio_UND']).sum()
    total_compra = (df_vista['Sugerencia_Compra'] * df_vista['Costo_Promedio_UND']).sum()
    total_ahorro = (df_vista['Sugerencia_Traslado'] * df_vista['Costo_Promedio_UND']).sum()
    skus_quiebre = len(df_vista[df_vista['Stock'] == 0])

    with c1: st.markdown(f'<div class="metric-card"><div class="metric-label">Valor Inventario Actual</div><div class="metric-value">${total_inv/1e6:,.1f} M</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card" style="border-color:#EF553B;"><div class="metric-label">Inversión Requerida</div><div class="metric-value" style="color:#EF553B">${total_compra/1e6:,.1f} M</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-card" style="border-color:#00CC96;"><div class="metric-label">Ahorro x Traslados</div><div class="metric-value" style="color:#00CC96">${total_ahorro/1e6:,.1f} M</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-card"><div class="metric-label">SKUs en Quiebre</div><div class="metric-value">{skus_quiebre}</div></div>', unsafe_allow_html=True)

    # Gráficos Avanzados
    st.markdown("---")
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.subheader("Distribución de Inversión (Interactivo)")
        # Sunburst Chart: Categoría -> Marca
        fig_sun = px.sunburst(
            df_vista, 
            path=['Categoria', 'Marca_Nombre'], 
            values='Costo_Promedio_UND',
            color='Segmento_ABC',
            color_discrete_map={'A':'#EF553B', 'B':'#FFA15A', 'C':'#00CC96'},
            title="Haga clic en los sectores para profundizar (Drill-down)"
        )
        fig_sun.update_layout(height=450, margin=dict(t=30, l=0, r=0, b=0))
        st.plotly_chart(fig_sun, use_container_width=True)
        
    with col_chart2:
        st.subheader("Salud del Inventario")
        # Gauge Chart (Velocímetro)
        eficiencia = 100 - (skus_quiebre / len(df_vista) * 100)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = eficiencia,
            title = {'text': "Nivel de Servicio (%)"},
            gauge = {'axis': {'range': [None, 100]},
                     'bar': {'color': "#2E86C1"},
                     'steps': [
                         {'range': [0, 85], 'color': "#F9EBEA"},
                         {'range': [85, 100], 'color': "#E8F8F5"}],
                     'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}}))
        fig_gauge.update_layout(height=350, margin=dict(t=50, l=20, r=20, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.info("✅ **Meta:** Mantener el nivel de servicio por encima del 90% para asegurar la satisfacción del cliente.")

# === TAB 2: TRASLADOS ===
with tab2:
    st.markdown("""
    <div class="guide-box">
        <div class="guide-title">🚚 Guía Estratégica: Centro de Traslados</div>
        El sistema detecta automáticamente dónde sobra mercancía y dónde falta.
        <br><b>Acción:</b> Seleccione los productos en la tabla, descargue la orden y envíela a bodega para ahorrar capital de compra.
    </div>
    """, unsafe_allow_html=True)
    
    df_traslados = df_vista[df_vista['Sugerencia_Traslado'] > 0].copy()
    
    if df_traslados.empty:
        st.success("✅ Excelente. El inventario está balanceado. No se requieren traslados.")
    else:
        # Preparar datos para edición
        # Simulamos un origen lógico
        df_traslados['Origen_Sugerido'] = df_traslados['Almacen_Nombre'].apply(lambda x: "Sede Principal" if x != "Sede Principal" else "Norte")
        
        df_display_tras = df_traslados[['SKU', 'Descripcion', 'Origen_Sugerido', 'Almacen_Nombre', 'Sugerencia_Traslado', 'Costo_Promedio_UND']].head(20)
        df_display_tras.columns = ['SKU', 'Producto', 'Origen', 'Destino', 'Cantidad', 'Costo Unit.']
        df_display_tras['Seleccionar'] = False
        
        # Editor interactivo
        edited_traslados = st.data_editor(
            df_display_tras,
            column_config={
                "Seleccionar": st.column_config.CheckboxColumn(required=True),
                "Cantidad": st.column_config.NumberColumn(min_value=1, step=1),
                "Costo Unit.": st.column_config.NumberColumn(format="$%d")
            },
            use_container_width=True,
            hide_index=True,
            key="editor_traslados_principal"
        )
        
        seleccionados_tras = edited_traslados[edited_traslados['Seleccionar']]
        
        st.markdown("---")
        
        # Panel de Acciones
        if not seleccionados_tras.empty:
            cant_total = seleccionados_tras['Cantidad'].sum()
            valor_total = (seleccionados_tras['Cantidad'] * seleccionados_tras['Costo Unit.']).sum()
            
            col_res, col_exp, col_act = st.columns([1, 1, 1])
            
            with col_res:
                st.markdown("#### Resumen")
                st.info(f"📦 **{len(seleccionados_tras)} Referencias**\n\n📊 **{cant_total} Unidades**\n\n💰 Valor: **${valor_total:,.0f}**")
            
            with col_exp:
                st.markdown("#### Exportar Documentos")
                
                # Generar Excel
                excel_data = generar_excel(seleccionados_tras, "Orden_Traslado")
                st.download_button(
                    label="📥 Descargar Excel (Bodega)",
                    data=excel_data,
                    file_name="Orden_Traslado.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                
                # Generar PDF
                # Aseguramos que el nombre no sea muy largo
                pdf_data = generar_pdf(seleccionados_tras, "ORDEN DE TRASLADO INTERNO")
                st.download_button(
                    label="📄 Descargar PDF (Legal)",
                    data=pdf_data,
                    file_name="Orden_Traslado.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
            with col_act:
                st.markdown("#### Ejecución")
                if st.button("🚀 Procesar Traslado y Notificar", type="primary", use_container_width=True):
                    with st.spinner("Enviando notificaciones a Jefes de Bodega..."):
                        time.sleep(2)
                        st.success(f"¡Orden procesada! Se notificó a {seleccionados_tras['Origen'].iloc[0]} y {seleccionados_tras['Destino'].iloc[0]}.")
                        st.balloons()
        else:
            st.warning("👆 Por favor, seleccione al menos un ítem en la tabla para activar las opciones de exportación y envío.")

# === TAB 3: COMPRAS ===
with tab3:
    st.markdown("""
    <div class="guide-box">
        <div class="guide-title">🛒 Guía Estratégica: Generador de Compras</div>
        Aquí convertimos las "Sugerencias del Algoritmo" en "Órdenes de Compra" reales.
        <br>1. Seleccione un proveedor.
        <br>2. Ajuste las cantidades sugeridas si es necesario.
        <br>3. Genere el PDF para firma o envíe el email directamente.
    </div>
    """, unsafe_allow_html=True)
    
    df_compras = df_vista[df_vista['Sugerencia_Compra'] > 0].copy()
    
    # Filtro de Proveedor
    col_filtro_prov, col_info_prov = st.columns([1, 2])
    
    with col_filtro_prov:
        list_prov = sorted(df_compras['Proveedor'].unique())
        if not list_prov:
            st.success("No hay necesidades de compra pendientes.")
            st.stop()
            
        sel_prov = st.selectbox("Seleccionar Proveedor para Orden:", list_prov)
    
    # Filtrar datos
    df_prov = df_compras[df_compras['Proveedor'] == sel_prov].head(20)
    df_prov['Total_Linea'] = df_prov['Sugerencia_Compra'] * df_prov['Costo_Promedio_UND']
    
    with col_info_prov:
        total_sug = df_prov['Total_Linea'].sum()
        st.info(f"El sistema sugiere **{len(df_prov)} referencias** para **{sel_prov}** por un valor total de **${total_sug:,.0f}**")
    
    # Preparar tabla
    df_display_compra = df_prov[['SKU', 'Descripcion', 'Stock', 'Sugerencia_Compra', 'Costo_Promedio_UND', 'Total_Linea']]
    df_display_compra.columns = ['SKU', 'Producto', 'Stock Actual', 'Cant. Sugerida', 'Costo Unit.', 'Total Estimado']
    df_display_compra['Incluir'] = True # Checkbox por defecto activado
    
    st.markdown("##### Detalle de la Orden")
    edited_compras = st.data_editor(
        df_display_compra,
        column_config={
            "Incluir": st.column_config.CheckboxColumn(required=True),
            "Cant. Sugerida": st.column_config.NumberColumn(min_value=1, step=1),
            "Costo Unit.": st.column_config.NumberColumn(format="$%d"),
            "Total Estimado": st.column_config.ProgressColumn(format="$%d", min_value=0, max_value=int(df_display_compra['Total Estimado'].max()))
        },
        use_container_width=True,
        hide_index=True,
        key="editor_compra_principal"
    )
    
    seleccionados_compra = edited_compras[edited_compras['Incluir']]
    
    st.markdown("---")
    
    if not seleccionados_compra.empty:
        c_buy1, c_buy2 = st.columns([1, 1])
        
        with c_buy1:
            total_oc = (seleccionados_compra['Cant. Sugerida'] * seleccionados_compra['Costo Unit.']).sum()
            st.subheader(f"Total Orden: ${total_oc:,.0f}")
            st.markdown(f"Items Seleccionados: **{len(seleccionados_compra)}**")
            
            if st.button("📧 Enviar Orden al Proveedor", type="primary", use_container_width=True):
                with st.spinner(f"Enviando correo a pedidos@{sel_prov.lower().replace(' ', '')}.com..."):
                    time.sleep(1.5)
                    st.success("✅ Orden enviada exitosamente.")
                    st.toast("Copia enviada a compras@tuempresa.com", icon="📨")
            
        with c_buy2:
            st.markdown("#### Descargar Archivos")
            # Excel
            excel_oc = generar_excel(seleccionados_compra, "Orden_Compra")
            st.download_button("📥 Descargar Excel (Formato Proveedor)", data=excel_oc, file_name=f"OC_{sel_prov}.xlsx", use_container_width=True)
            
            # PDF
            pdf_oc = generar_pdf(seleccionados_compra, f"ORDEN DE COMPRA - {sel_prov}")
            st.download_button("📄 Descargar PDF (Formato Firma)", data=pdf_oc, file_name=f"OC_{sel_prov}.pdf", use_container_width=True)
    else:
        st.warning("Seleccione al menos un producto para generar la orden.")

# === TAB 4: TRACKING ===
with tab4:
    st.subheader("📡 Torre de Control: Seguimiento en Vivo")
    st.markdown("Monitoreo en tiempo real del estado de todas las órdenes generadas (Simulación).")
    
    # Datos Mock de Tracking mejorados
    tracking_data = [
        {"ID": "OC-2024-101", "Fecha": "2024-05-20", "Tipo": "Compra", "Destino/Origen": "DISTRIBUIDORA GLOBAL", "Estado": "🟢 Recibido (100%)", "Total": "$15,400,000"},
        {"ID": "OC-2024-102", "Fecha": "2024-05-21", "Tipo": "Compra", "Destino/Origen": "IMPORTADOS S.A.", "Estado": "🟡 En Tránsito (Llega Hoy)", "Total": "$8,200,000"},
        {"ID": "TR-2024-088", "Fecha": "2024-05-22", "Tipo": "Traslado", "Destino/Origen": "Tienda Norte -> Sur", "Estado": "🔵 Despachado", "Total": "$0"},
        {"ID": "OC-2024-103", "Fecha": "2024-05-22", "Tipo": "Compra", "Destino/Origen": "HERRAMIENTAS PRO", "Estado": "⚪ Pendiente Aprobación", "Total": "$4,500,000"},
        {"ID": "TR-2024-089", "Fecha": "2024-05-23", "Tipo": "Traslado", "Destino/Origen": "Sede Ppal -> Occidente", "Estado": "⚪ Pendiente Picking", "Total": "$0"},
    ]
    df_track = pd.DataFrame(tracking_data)
    
    st.dataframe(
        df_track,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Estado": st.column_config.Column(width="medium"),
            "Total": st.column_config.TextColumn(width="small"),
            "Tipo": st.column_config.Column(width="small")
        }
    )
    
    c_refresh, c_void = st.columns([1, 4])
    if c_refresh.button("🔄 Actualizar Estados (API Transportadora)"):
        with st.spinner("Consultando GPS de transportadoras..."):
            time.sleep(1.5)
            st.success("Estados actualizados correctamente.")
