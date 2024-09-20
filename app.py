import streamlit as st
import pandas as pd
import altair as alt

# Título de la aplicación
st.title("Análisis de Ventas de Videojuegos")

# Cargar el dataset
data = pd.read_csv("data/vgsales.csv")

# Mostrar los primeros datos del dataset
st.write("Vista previa de los datos", data.head())

# Crear un gráfico Altair y mostrarlo
cantidad_juegos_año = alt.Chart(data).mark_bar().encode(
    alt.X('Year:O', title='Año'),
    alt.Y('count()', title='Cantidad')
).properties(
    title='Distribución de Juegos por Año',
    width=800
)
st.altair_chart(cantidad_juegos_año)

plataformas_ventas2 = data.groupby("Platform")['Global_Sales'].sum().nlargest(10).reset_index()
chart2 = alt.Chart(plataformas_ventas2).mark_bar().encode(
    x='Platform',
    y='Global_Sales'
).properties(
    title="Plataformas con más ventas globales"
)
st.altair_chart(chart2)