import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Dashboard change parts",
                   page_icon="👨‍🔧",
                   layout="wide")

st.markdown("## Modelo machine learning recambio de piezas siniestros")
st.markdown("### Estructura de archivo a subir ejemplo: ")

df_example = pd.read_csv("data/data.csv", nrows=5)
df_example = df_example.drop(columns=["accion", "accion_modelo"])

st.dataframe(df_example)

st.markdown("### Por favor suba sus datos en formato .csv teniendo en cuenta el ejemplo anterior:")
st.warning('Tener en cuenta que es un demo en la capa gratuita de AWS no soporta mas de 100 filas', icon="⚠️")
data_user = st.file_uploader("Datos a analizar:", type={"csv", "txt"})
if data_user is not None:
    df_user = pd.read_csv(data_user)
else:
    df_user = None

if df_user is not None:
    st.markdown("Primeras 20 filas de sus datos:")
    st.dataframe(df_user.head())
    fig = px.histogram(df_user,
                       x="marca")
    st.markdown(f"Usted **subió {len(df_user)} partes** de las siguientes marcas: ")

    fig.update_xaxes(tickangle=30)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Pulse Calcular para hacer las predicciones")
    fit_model = st.button("Calcular")

    if fit_model:
        with st.spinner("Analizando .."):
            df = df_user.drop(columns=["numero_aviso",
                                       "marca",
                                       "linea",
                                       "nombre"])

            df_user["grupo"] = df_user["grupo"].astype(str)
            df_user["subgrupo"] = df_user["subgrupo"].astype(str)

            df_model = pd.get_dummies(df_user)

            X = df_model.values



