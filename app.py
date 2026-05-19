import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página
st.set_page_config(page_title="Dashboard IA y Estudiantes", layout="wide")

# Cargar los datos
@st.cache_data
def load_data():
    # Asegúrate de que el CSV esté en la misma ruta que este script
    return pd.read_csv('AI_Student_Life_Pakistan_2026.csv')

df = load_data()

st.title("Análisis del Uso de IA en Estudiantes")

# =====================================================================
# 1. Análisis de Impacto por Herramienta (Filtros de Área Geográfica)
# =====================================================================
st.header("1. Análisis de Impacto por Herramienta")

# La interactividad: Selectbox para ciudades
opciones_ciudades = ["Todas las ciudades"] + list(df['City'].unique())
ciudad_seleccionada = st.selectbox("Selecciona una Ciudad:", opciones_ciudades)

# Filtrar datos según selección
if ciudad_seleccionada == "Todas las ciudades":
    df_city = df
else:
    df_city = df[df['City'] == ciudad_seleccionada]

# El componente visual: Gráfico de barras apiladas
df_city_grouped = df_city.groupby(['AI_Tool_Used', 'Impact_on_Grades']).size().reset_index(name='Cantidad')
fig1 = px.bar(df_city_grouped, x='AI_Tool_Used', y='Cantidad', color='Impact_on_Grades', 
              title=f"Impacto en Notas por Herramienta - {ciudad_seleccionada}",
              barmode='stack')
st.plotly_chart(fig1, use_container_width=True)

st.divider()

# =====================================================================
# 2. Comparativa de Propósitos: Coding vs. Writing 
# =====================================================================
st.header("2. Comparativa por Propósitos de Uso")

# La interactividad: Radio buttons para propósitos
propositos = df['Purpose'].unique()
proposito_seleccionado = st.radio("Selecciona el Propósito de Uso:", propositos, horizontal=True)

df_purpose = df[df['Purpose'] == proposito_seleccionado]

# El componente visual: Gráfico de cambio de notas
fig2 = px.histogram(df_purpose, x='Impact_on_Grades', 
                    title=f"Cambio en Notas usando la IA para: {proposito_seleccionado}",
                    color='Impact_on_Grades')
st.plotly_chart(fig2, use_container_width=True)

st.divider()

# =====================================================================
# 3. Análisis de Anomalías: Alta Satisfacción, Notas en Declive
# =====================================================================
st.header("3. Análisis de Anomalías: Alta Satisfacción pero Notas en Declive")

# Filtro base de anomalía
df_anomaly = df[(df['Satisfaction_Level'] == 'High') & (df['Impact_on_Grades'] == 'Slight Decline')]

# La interactividad: Slider numérico de horas de uso
min_horas = float(df_anomaly['Daily_Usage_Hours'].min()) if not df_anomaly.empty else 0.0
max_horas = float(df_anomaly['Daily_Usage_Hours'].max()) if not df_anomaly.empty else 24.0

if not df_anomaly.empty:
    horas_filtro = st.slider("Filtra por máximo de Horas de Uso Diario:", 
                             min_value=min_horas, max_value=max_horas, value=max_horas, step=0.5)
    
    # Filtrar dataframe con el slider
    df_anomaly_filtered = df_anomaly[df_anomaly['Daily_Usage_Hours'] <= horas_filtro]
    
    # El componente visual: Conteo y tabla
    st.warning(f"**Se encontraron {len(df_anomaly_filtered)} estudiantes** con alta satisfacción pero que bajaron sus notas (Usando la IA hasta {horas_filtro} horas diarias).")
    
    st.write("Detalle de las herramientas usadas por estos estudiantes:")
    # st.dataframe detallando los resultados
    st.dataframe(df_anomaly_filtered[['Student_ID', 'City', 'AI_Tool_Used', 'Daily_Usage_Hours', 'Purpose']])
else:
    st.success("No hay registros que cumplan con la condición de anomalía.")

st.divider()

# =====================================================================
# 4. Demografía y Uso (Filtros de Activación)
# =====================================================================
st.header("4. Demografía y Promedio de Horas de Uso")

# La interactividad: Checkboxes para desglosar información
col1, col2 = st.columns(2)
with col1:
    desglosar_genero = st.checkbox("Desglosar por Género (Gender)")
with col2:
    desglosar_educacion = st.checkbox("Desglosar por Nivel Educativo (Education_Level)")

# El componente visual: Boxplot dinámico
x_col = "City" # Base X axis
color_col = None

if desglosar_genero and desglosar_educacion:
    x_col = "Gender"
    color_col = "Education_Level"
elif desglosar_genero:
    x_col = "Gender"
elif desglosar_educacion:
    x_col = "Education_Level"

fig4 = px.box(df, x=x_col, y="Daily_Usage_Hours", color=color_col,
              title="Distribución de Horas de Uso Diario")
st.plotly_chart(fig4, use_container_width=True)

st.divider()

# =====================================================================
# 5. Rendimiento Regional (Selección Múltiple)
# =====================================================================
st.header("5. Rendimiento Regional")

# Preprocesar datos: % de notas mejoradas ('Improved') por ciudad
df_improved = df[df['Impact_on_Grades'] == 'Improved'].groupby('City').size()
df_total = df.groupby('City').size()
df_percent = ((df_improved / df_total) * 100).fillna(0).reset_index(name='Mejora_Porcentaje')

# El componente visual: Indicadores
ciudad_max = df_percent.loc[df_percent['Mejora_Porcentaje'].idxmax()]
ciudad_min = df_percent.loc[df_percent['Mejora_Porcentaje'].idxmin()]

col_ind1, col_ind2 = st.columns(2)
col_ind1.metric("Ciudad con Mayor % de Mejora", ciudad_max['City'], f"{ciudad_max['Mejora_Porcentaje']:.1f}%")
col_ind2.metric("Ciudad con Menor % de Mejora", ciudad_min['City'], f"{ciudad_min['Mejora_Porcentaje']:.1f}%")

# La interactividad: Multiselect para comparar
ciudades_disponibles = list(df['City'].unique())
ciudades_comparar = st.multiselect("Selecciona ciudades para comparar el rendimiento ('Improved' %):", 
                                   ciudades_disponibles, 
                                   default=ciudades_disponibles[:2])

if ciudades_comparar:
    df_comparar = df_percent[df_percent['City'].isin(ciudades_comparar)]
    fig5 = px.bar(df_comparar, x='City', y='Mejora_Porcentaje', color='City',
                  title="Comparativa de Porcentaje de Mejora de Notas por Ciudad",
                  labels={'Mejora_Porcentaje': '% de Notas Mejoradas'})
    st.plotly_chart(fig5, use_container_width=True)
else:
    st.info("Selecciona al menos una ciudad para ver la comparativa.")