import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI & Vida Estudiantil — Pakistan 2026",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Paleta de color ───────────────────────────────────────────────────────────
# Impacto en notas
IMPACT_ORDER  = ["Improved", "No Change", "Slight Decline"]
IMPACT_COLORS = {
    "Improved":       "#2563EB",   # azul
    "No Change":      "#F59E0B",   # ámbar
    "Slight Decline": "#EF4444",   # rojo
}

# Herramientas
TOOL_COLORS = {
    "ChatGPT":  "#2563EB",
    "Copilot":  "#7C3AED",
    "Grammarly":"#059669",
    "Gemini":   "#D97706",
    "Notion AI":"#DB2777",
}

# Género
GENDER_COLORS = {"Male": "#2563EB", "Female": "#DB2777"}

# Nivel educativo
EDU_COLORS = {
    "School":     "#059669",
    "College":    "#D97706",
    "University": "#7C3AED",
}

# Ciudades
CITY_COLORS = {
    "Karachi":   "#2563EB",
    "Lahore":    "#7C3AED",
    "Islamabad": "#059669",
    "Multan":    "#D97706",
    "Faisalabad":"#DB2777",
}

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  html, body,
  [data-testid="stAppViewContainer"], [data-testid="stApp"],
  .stApp, .main, section.main, [data-testid="stMain"] {
      background-color: #ffffff !important;
  }
  [data-testid="stHeader"] { background-color: #ffffff !important; }

  body, p, li, label, input, button, textarea, select,
  h1, h2, h3, h4, h5, h6,
  .stMarkdown, .stText, [data-testid="stMarkdownContainer"] {
      font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif !important;
  }
  /* NO tocar span ni div para no romper fuentes de iconos de Streamlit */

  h1 {
      font-size: 1.65rem !important; font-weight: 700 !important;
      color: #0f172a !important; letter-spacing: -0.02em !important;
      margin-bottom: 0.1rem !important;
  }
  h2 {
      font-size: 1.05rem !important; font-weight: 600 !important;
      color: #0f172a !important; letter-spacing: -0.01em !important;
      margin-bottom: 0.4rem !important;
  }
  p, li, .stMarkdown p {
      color: #334155 !important;
      font-size: 0.88rem !important;
      line-height: 1.6 !important;
  }

  [data-testid="stWidgetLabel"] p,
  .stRadio    > label,
  .stCheckbox > label,
  .stSelectbox  label,
  .stMultiSelect label,
  .stSlider     label {
      color: #0f172a !important;
      font-size: 0.85rem !important;
      font-weight: 500 !important;
  }

  .stRadio [data-testid="stMarkdownContainer"] p    { color: #0f172a !important; }
  .stCheckbox [data-testid="stMarkdownContainer"] p { color: #0f172a !important; }

  [data-baseweb="select"] > div {
      background-color: #ffffff !important;
      border-color: #cbd5e1 !important;
  }
  [data-baseweb="select"] span:not([data-baseweb="tag"]),
  [data-baseweb="select"] input {
      color: #0f172a !important;
  }
  [data-baseweb="popover"],
  [data-baseweb="menu"],
  ul[data-baseweb="menu"] {
      background-color: #ffffff !important;
  }
  [data-baseweb="menu"] li,
  [data-baseweb="option"] {
      background-color: #ffffff !important;
      color: #0f172a !important;
  }
  [data-baseweb="option"]:hover { background-color: #f1f5f9 !important; }

  .stSlider [data-testid="stTickBarMin"],
  .stSlider [data-testid="stTickBarMax"] { color: #64748b !important; }

  hr { border: none; border-top: 1px solid #e2e8f0 !important; margin: 2rem 0 !important; }

  [data-testid="stMetric"] {
      background: #f8fafc !important;
      border: 1px solid #e2e8f0 !important;
      border-radius: 10px !important;
      padding: 1rem 1.2rem !important;
  }
  [data-testid="stMetricLabel"] p { color: #64748b !important; font-size: 0.78rem !important; }
  [data-testid="stMetricValue"]   { color: #0f172a !important; font-size: 1.4rem !important; }

  [data-testid="stExpander"] {
      border: 1px solid #e2e8f0 !important;
      border-radius: 10px !important;
      background-color: #f8fafc !important;
  }
  [data-testid="stExpander"] summary {
      background-color: #f8fafc !important;
  }
  [data-testid="stExpander"] summary p,
  [data-testid="stExpander"] summary span {
      color: #0f172a !important;
      font-weight: 500 !important;
  }
  [data-testid="stExpanderToggleIcon"] svg {
      fill: #0f172a !important;
      display: inline-block !important;
  }
  [data-testid="stExpanderDetails"] { background-color: #f8fafc !important; }
  [data-testid="stExpanderDetails"] p { color: #334155 !important; }

  [data-testid="stDataFrame"] {
      border: 1px solid #e2e8f0 !important;
      border-radius: 8px !important; overflow: hidden;
  }

  [data-testid="stAlert"] p { color: #1e40af !important; }
</style>
""", unsafe_allow_html=True)

# ── Datos ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    csv_path = Path(__file__).parent / "AI_Student_Life_Pakistan_2026.csv"
    return pd.read_csv(csv_path)

df = load_data()

# ── Layout base de figuras ────────────────────────────────────────────────────
def clean_fig(fig, height=380):
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=36, b=20),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(family="Inter, Helvetica Neue, Arial", color="#0f172a", size=12),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="left", x=0,
            font=dict(size=11, color="#0f172a"),
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            showgrid=False, linecolor="#cbd5e1",
            tickcolor="#cbd5e1", tickfont=dict(color="#334155"),
            title_font=dict(color="#334155"),
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#f1f5f9",
            linecolor="#cbd5e1", zeroline=False,
            tickfont=dict(color="#334155"),
            title_font=dict(color="#334155"),
        ),
    )
    return fig

# ── CABECERA ──────────────────────────────────────────────────────────────────
st.markdown("# IA y Vida Estudiantil &mdash; Pakistan 2026", unsafe_allow_html=True)
st.markdown(
    "<p style='color:#64748b; margin-top:-4px;'>"
    "Análisis de herramientas de inteligencia artificial y su impacto en el rendimiento académico.</p>",
    unsafe_allow_html=True,
)

total        = len(df)
pct_improved = round(df[df["Impact_on_Grades"] == "Improved"].shape[0] / total * 100, 1)
pct_decline  = round(df[df["Impact_on_Grades"] == "Slight Decline"].shape[0] / total * 100, 1)
avg_hours    = round(df["Daily_Usage_Hours"].mean(), 2)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Estudiantes",          total)
c2.metric("Notas mejoradas",      f"{pct_improved}%")
c3.metric("Notas en declive",     f"{pct_decline}%")
c4.metric("Horas diarias promedio", avg_hours)

st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 — Impacto por herramienta · filtro ciudad
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("## Impacto en notas por herramienta de IA")
st.markdown(
    "<p>Distribución porcentual del impacto académico por herramienta. "
    "Filtra por ciudad para ver diferencias regionales.</p>",
    unsafe_allow_html=True,
)

cities   = ["Todas las ciudades"] + sorted(df["City"].unique().tolist())
city_sel = st.selectbox("Filtrar por ciudad", cities, key="city_sel")

df1 = df if city_sel == "Todas las ciudades" else df[df["City"] == city_sel]

counts1 = (
    df1.groupby(["AI_Tool_Used", "Impact_on_Grades"])
    .size().reset_index(name="Count")
)
counts1["Pct"] = (
    counts1["Count"] / counts1.groupby("AI_Tool_Used")["Count"].transform("sum") * 100
).round(1)

fig1 = px.bar(
    counts1,
    x="AI_Tool_Used", y="Pct",
    color="Impact_on_Grades",
    category_orders={"Impact_on_Grades": IMPACT_ORDER},
    color_discrete_map=IMPACT_COLORS,
    barmode="stack", text="Pct",
    labels={"Pct": "Porcentaje (%)", "AI_Tool_Used": "Herramienta",
            "Impact_on_Grades": "Impacto"},
)
fig1.update_traces(
    texttemplate="%{text:.0f}%", textposition="inside",
    textfont=dict(size=11, color="#ffffff"),
)
clean_fig(fig1)
st.plotly_chart(fig1, width="stretch")

st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 — Propósito de uso
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("## Notas según el propósito de uso")
st.markdown(
    "<p>Selecciona un propósito para ver cómo se distribuye el impacto "
    "entre las herramientas disponibles.</p>",
    unsafe_allow_html=True,
)

purposes    = sorted(df["Purpose"].unique().tolist())
purpose_sel = st.radio("Propósito de uso", purposes, horizontal=True, key="purpose_sel")

df2 = df[df["Purpose"] == purpose_sel]
counts2 = (
    df2.groupby(["AI_Tool_Used", "Impact_on_Grades"])
    .size().reset_index(name="Count")
)

fig2 = px.bar(
    counts2,
    x="AI_Tool_Used", y="Count",
    color="Impact_on_Grades",
    category_orders={"Impact_on_Grades": IMPACT_ORDER},
    color_discrete_map=IMPACT_COLORS,
    barmode="group",
    labels={"Count": "Estudiantes", "AI_Tool_Used": "Herramienta",
            "Impact_on_Grades": "Impacto"},
    title=f"Propósito: {purpose_sel}",
)
clean_fig(fig2)
st.plotly_chart(fig2, width="stretch")

st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 — Anomalía: alta satisfacción, notas en declive
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("## Anomalia: alta satisfaccion, notas en declive")
st.markdown(
    "<p>Estudiantes con satisfaccion alta pero cuyas notas bajaron. "
    "Ajusta el slider para ver si las horas de uso influyen.</p>",
    unsafe_allow_html=True,
)

anomaly      = df[(df["Satisfaction_Level"] == "High") &
                  (df["Impact_on_Grades"]   == "Slight Decline")].copy()
total_anomaly = len(anomaly)

st.metric("Estudiantes en esta condicion", total_anomaly)

min_h, max_h = float(df["Daily_Usage_Hours"].min()), float(df["Daily_Usage_Hours"].max())
hour_range   = st.slider(
    "Horas de uso diario",
    min_value=min_h, max_value=max_h,
    value=(min_h, max_h), step=0.1, key="hour_slider",
)

anomaly_filtered = anomaly[
    anomaly["Daily_Usage_Hours"].between(hour_range[0], hour_range[1])
]

tool_counts3 = (
    anomaly_filtered.groupby("AI_Tool_Used")
    .size().reset_index(name="Estudiantes")
    .sort_values("Estudiantes", ascending=False)
)
tool_counts3["color"] = tool_counts3["AI_Tool_Used"].map(TOOL_COLORS)

col_left, col_right = st.columns(2)

with col_left:
    fig3 = px.bar(
        tool_counts3,
        x="AI_Tool_Used", y="Estudiantes",
        color="AI_Tool_Used",
        color_discrete_map=TOOL_COLORS,
        labels={"AI_Tool_Used": "Herramienta"},
        title="Herramientas del grupo anomalo",
    )
    fig3.update_layout(showlegend=False)
    clean_fig(fig3, height=320)
    st.plotly_chart(fig3, width="stretch")

with col_right:
    display_cols = ["Student_ID", "Age", "Gender", "Education_Level",
                    "City", "AI_Tool_Used", "Daily_Usage_Hours", "Purpose"]
    st.dataframe(
        anomaly_filtered[display_cols].reset_index(drop=True),
        width="stretch", height=320,
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4 — Demografía y horas de uso
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("## Horas de uso diario por demografia")
st.markdown(
    "<p>Activa los desgloses para comparar el promedio de horas "
    "entre grupos demograficos.</p>",
    unsafe_allow_html=True,
)

by_gender = st.checkbox("Desglosar por genero",          key="chk_gender")
by_edu    = st.checkbox("Desglosar por nivel educativo", key="chk_edu")

if not by_gender and not by_edu:
    avg_data = (
        df.groupby("AI_Tool_Used")["Daily_Usage_Hours"]
        .mean().reset_index(name="Promedio de horas")
    )
    fig4 = px.bar(
        avg_data.sort_values("Promedio de horas"),
        x="Promedio de horas", y="AI_Tool_Used",
        orientation="h",
        color="AI_Tool_Used",
        color_discrete_map=TOOL_COLORS,
        labels={"AI_Tool_Used": "Herramienta"},
        title="Promedio de horas diarias por herramienta",
    )
    fig4.update_layout(showlegend=False)

elif by_gender and not by_edu:
    avg_data = (
        df.groupby(["AI_Tool_Used", "Gender"])["Daily_Usage_Hours"]
        .mean().reset_index(name="Promedio de horas")
    )
    fig4 = px.bar(
        avg_data, x="AI_Tool_Used", y="Promedio de horas",
        color="Gender", barmode="group",
        color_discrete_map=GENDER_COLORS,
        labels={"AI_Tool_Used": "Herramienta", "Gender": "Genero"},
        title="Promedio de horas por herramienta y genero",
    )

elif not by_gender and by_edu:
    edu_order = ["School", "College", "University"]
    avg_data  = (
        df.groupby(["AI_Tool_Used", "Education_Level"])["Daily_Usage_Hours"]
        .mean().reset_index(name="Promedio de horas")
    )
    fig4 = px.bar(
        avg_data, x="AI_Tool_Used", y="Promedio de horas",
        color="Education_Level", barmode="group",
        category_orders={"Education_Level": edu_order},
        color_discrete_map=EDU_COLORS,
        labels={"AI_Tool_Used": "Herramienta", "Education_Level": "Nivel educativo"},
        title="Promedio de horas por herramienta y nivel educativo",
    )

else:
    avg_data = (
        df.groupby(["AI_Tool_Used", "Gender", "Education_Level"])["Daily_Usage_Hours"]
        .mean().reset_index()
    )
    avg_data.columns = ["AI_Tool_Used", "Gender", "Education_Level", "Promedio de horas"]
    avg_data["Grupo"] = avg_data["Gender"] + " / " + avg_data["Education_Level"]
    COMBO_COLORS = {
        "Female / College":    "#DB2777",
        "Female / School":     "#F472B6",
        "Female / University": "#9D174D",
        "Male / College":      "#2563EB",
        "Male / School":       "#60A5FA",
        "Male / University":   "#1E3A8A",
    }
    fig4 = px.bar(
        avg_data, x="AI_Tool_Used", y="Promedio de horas",
        color="Grupo", barmode="group",
        color_discrete_map=COMBO_COLORS,
        labels={"AI_Tool_Used": "Herramienta"},
        title="Promedio de horas por herramienta, genero y nivel educativo",
    )

clean_fig(fig4)
st.plotly_chart(fig4, width="stretch")

st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 5 — Rendimiento regional
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("## Rendimiento regional")
st.markdown(
    "<p>Compara el porcentaje de notas mejoradas en las ciudades que selecciones.</p>",
    unsafe_allow_html=True,
)

all_cities = sorted(df["City"].unique().tolist())
cities_sel = st.multiselect(
    "Selecciona ciudades para comparar",
    all_cities, default=all_cities, key="cities_multi",
)

if cities_sel:
    city_perf = (
        df[df["City"].isin(cities_sel)]
        .groupby(["City", "Impact_on_Grades"])
        .size().reset_index(name="Count")
    )
    city_perf["Pct"] = (
        city_perf["Count"] /
        city_perf.groupby("City")["Count"].transform("sum") * 100
    ).round(1)

    fig5 = px.bar(
        city_perf,
        x="City", y="Pct",
        color="Impact_on_Grades",
        category_orders={"Impact_on_Grades": IMPACT_ORDER},
        color_discrete_map=IMPACT_COLORS,
        barmode="stack", text="Pct",
        labels={"Pct": "Porcentaje (%)", "City": "Ciudad",
                "Impact_on_Grades": "Impacto"},
    )
    fig5.update_traces(
        texttemplate="%{text:.0f}%", textposition="inside",
        textfont=dict(size=11, color="#ffffff"),
    )
    clean_fig(fig5)
    st.plotly_chart(fig5, width="stretch")

    improved_pct = (
        df[df["City"].isin(cities_sel)]
        .groupby("City")
        .apply(lambda x: round(
            (x["Impact_on_Grades"] == "Improved").sum() / len(x) * 100, 1
        ))
        .reset_index(name="% Notas mejoradas")
        .sort_values("% Notas mejoradas", ascending=False)
    )
    st.dataframe(improved_pct.reset_index(drop=True), width="content")
else:
    st.info("Selecciona al menos una ciudad para ver el análisis.")

st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FASE 2 — Descubrimientos clave
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("## Descubrimientos clave")

with st.expander("Descubrimiento 1 — El uso intensivo no garantiza mejores notas"):
    st.markdown("""
Los estudiantes con mas de **3.5 horas diarias** de uso muestran una proporcion mayor
de notas en declive que quienes usan la IA entre 1 y 2 horas. Esto sugiere que
la IA funciona mejor como herramienta de apoyo puntual que como sustituto del
aprendizaje activo. El volumen de uso, por si solo, no predice el beneficio academico.
    """)

with st.expander("Descubrimiento 2 — La anomalia de alta satisfaccion y notas bajas"):
    anomaly_pct = round(total_anomaly / total * 100, 1)
    st.markdown(f"""
Aproximadamente el **{anomaly_pct}%** de los estudiantes reporta satisfaccion alta con
su herramienta de IA pero, al mismo tiempo, experimenta un descenso en sus notas.
ChatGPT concentra la mayor parte de este grupo. Una posible explicacion es que los
estudiantes valoran la experiencia conversacional y la inmediatez de las respuestas,
sin notar que esto puede estar reemplazando el esfuerzo cognitivo necesario para
consolidar el aprendizaje.
    """)

with st.expander("Descubrimiento 3 — Diferencias por nivel educativo en el uso diario"):
    st.markdown("""
Los estudiantes universitarios destinan en promedio mas tiempo diario al uso de IA
que los de preparatoria o secundaria. Sin embargo, su tasa de mejora en notas no es
proporcionalmente mayor. Los estudiantes de nivel escolar, con menos horas de uso,
muestran resultados relativamente comparables, lo que indica que la intencion y el
contexto de uso importan mas que la cantidad de tiempo invertido.
    """)

with st.expander("Descubrimiento 4 — Grammarly destaca en impacto positivo para Writing"):
    st.markdown("""
Al filtrar por el proposito **Writing**, Grammarly tiene la mayor proporcion de
estudiantes con notas mejoradas entre todas las herramientas. Esto tiene sentido dado
que su funcion principal (correccion y mejora de redaccion) esta directamente alineada
con las tareas de escritura academica. Cuando existe una correspondencia clara entre
la herramienta y la tarea, el impacto positivo en el rendimiento es mas consistente.
    """)

st.markdown(
    "<p style='color:#94a3b8; font-size:0.75rem; margin-top:2rem;'>"
    "Fuente: AI Student Life Pakistan 2026 — 100 registros</p>",
    unsafe_allow_html=True,
)