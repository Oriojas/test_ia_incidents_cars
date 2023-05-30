import pickle
import pandas as pd
import streamlit as st
from joblib import load
import plotly.express as px

st.set_page_config(page_title="Dashboard change parts",
                   page_icon="👨‍🔧",
                   layout="wide")

with open("model/all_columns.pickle", "rb") as f:
    all_columns = pickle.load(f)


def anio_group(anio):
    """
    this function calculate year range
    :param anio: int, year made
    :return: str, year range
    """
    if anio <= 2024 and anio >= 2021:
        anio_range = "2024 - 2021"
    elif anio <= 2020 and anio >= 2017:
        anio_range = "2020 - 2017"
    elif anio <= 2016 and anio >= 2013:
        anio_range = "2016 - 2013"
    elif anio <= 2012 and anio >= 2009:
        anio_range = "2012 - 2009"
    elif anio <= 2008 and anio >= 2005:
        anio_range = "2008 - 2005"
    else:
        anio_range = "2004 - atrás"

    return anio_range

st.markdown("## Modelo machine learning recambio de piezas siniestros")
st.markdown("### Estructura de archivo a subir ejemplo: ")

df_example = pd.read_csv("data/data.csv", nrows=5)
df_example = df_example.drop(columns=["accion", "accion_modelo"])

st.dataframe(df_example)

st.markdown("### Por favor suba sus datos en formato .csv teniendo en cuenta el ejemplo anterior:")
st.warning('Tener en cuenta que es un demo en la capa gratuita de AWS no soporta mas de 50 filas', icon="⚠️")
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

            anio_range_list = list(map(anio_group, list(df["anio"])))
            df["anio_range"] = anio_range_list
            df = df.drop(columns=["anio"])

            df["grupo"] = df["grupo"].astype(str)
            df["subgrupo"] = df["subgrupo"].astype(str)

            df_model = pd.get_dummies(df)

            for i in range(len(all_columns)):
                if all_columns[i] not in df_model.columns:
                    df_model[all_columns[i]] = 0

            X = df_model.values

            lr_model = load('model/lr_class.joblib')

            action = []
            for i in range(len(X)):
                temp = lr_model.predict(X[i].reshape(1, -1))[0]
                if temp:
                    temp2 = "cambiar"
                else:
                    temp2 = "reparar"
                action.append(temp2)

            df_user["action"] = action

            st.dataframe(df_user)

            st.markdown("### Resumen se recambios")

            fig = px.histogram(df_user,
                               x="action")

            fig.update_xaxes(tickangle=30)
            st.plotly_chart(fig, use_container_width=True)
