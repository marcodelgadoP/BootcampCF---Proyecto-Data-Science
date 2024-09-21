import streamlit as st
import pandas as pd
import altair as alt


st.title("Análisis de Ventas de Videojuegos")
data = pd.read_csv("data/vgsales.csv")
st.write("Vista previa de los datos", data.head())


filtro_año2016 = data[data['Year']<=2016]
data_filtrada = data.dropna(subset=['Year'])

cantidad_juegos_año_area = alt.Chart(filtro_año2016).mark_area().encode(
    alt.X('Year:O', title='Año'),
    alt.Y('count()', title='Cantidad')
).properties(
    title='Cantidad de Juegos por Año',
    width=800
)
st.altair_chart(cantidad_juegos_año_area)

genero_canidad = alt.Chart(data).mark_bar().encode(
    alt.X('Genre:N', title='Género'),
    alt.Y('count()', title='Cantidad')
).properties(
    title='Distribución de Géneros',
    width=400  
).interactive()
st.altair_chart(genero_canidad)

mapa_calor = alt.Chart(data_filtrada).mark_rect().encode(
    x=alt.X('Platform:N', title='Plataforma'),
    y=alt.Y('Genre:N', title='Género'),
    color=alt.Color('count():Q', title='Cantidad de Juegos'),
    tooltip=['Platform', 'Genre', 'count()']
).properties(
    title='Cantidad de Juegos por Plataforma y Género',
    width=800
)
st.altair_chart(mapa_calor)

top_publishers = data['Publisher'].value_counts().nlargest(10).reset_index()
top_publishers.columns = ['Publisher', 'Count']

publisher_chart = alt.Chart(top_publishers).mark_bar().encode(
    x=alt.X('Publisher:N', sort='-y', title='Publisher'),
    y=alt.Y('Count:Q', title='Number of Publications'),
    tooltip=['Publisher', 'Count']
).properties(
    title='Top 10 Editoras con mas publicaciones',
    width=600,
    height=400
).interactive()
st.altair_chart(publisher_chart)

# filtro
data_filtrada_2008_2009 = data_filtrada[(data_filtrada['Year'] == 2008) | (data_filtrada['Year'] == 2009)]
publisher_counts_2008_2009 = data_filtrada_2008_2009.groupby('Publisher').size().reset_index(name='Cantidad')
#ordenar 
publishers_mas_publicaciones = publisher_counts_2008_2009.sort_values(by='Cantidad', ascending=False).head(10)

#gráfico
grafico_publishers = alt.Chart(publishers_mas_publicaciones).mark_bar().encode(
    x=alt.X('Publisher:N', sort='-y', title='Publisher'),
    y=alt.Y('Cantidad:Q', title='Cantidad de Juegos'),
    color=alt.Color('Publisher:N', legend=None)
).properties(
    title='Top 10 Publishers con más Publicaciones en 2008 y 2009',
    width=900
).configure_axisX(
    labelAngle=-45 
)
st.altair_chart(grafico_publishers)

# Contar la cantidad de publicaciones por cada publisher
publisher_counts = data_filtrada.groupby('Publisher').size().reset_index(name='Cantidad')
publishers_mas_de_500 = publisher_counts[publisher_counts['Cantidad'] > 300]

grafico_publishers = alt.Chart(publishers_mas_de_500).mark_bar().encode(
    x=alt.X('Publisher:N', sort='-y', title='Publisher'),
    y=alt.Y('Cantidad:Q', title='Cantidad de Publicaciones'),
    color=alt.Color('Publisher:N', legend=None)
).properties(
    title='Publishers con Más de 300 Publicaciones',
    width=900
).configure_axisX(
    labelAngle=-65  
)
st.altair_chart(grafico_publishers)

top_10_publishers = data.groupby('Publisher')['Global_Sales'].sum().nlargest(10).reset_index()
# Gráfico de barras para las 10 primeras editoras 
grafico_top_10_publishers = alt.Chart(top_10_publishers).mark_bar().encode(
    x=alt.X('Global_Sales:Q', title='Ventas Globales (en millones)'),
    y=alt.Y('Publisher:N', sort='-x', title='Publisher'),
    color=alt.Color('Publisher:N', legend=None),
    tooltip=['Publisher', 'Global_Sales']
).properties(
    title='Top 10 Publisher por Ventas Globales',
    width=600
)

st.altair_chart(grafico_top_10_publishers)

#filtro NA
top_5_na = data.groupby('Publisher')['NA_Sales'].sum().nlargest(5).reset_index()
#filtro JP
top_5_jp = data.groupby('Publisher')['JP_Sales'].sum().nlargest(5).reset_index()
#filtro EU
top_5_eu = data.groupby('Publisher')['EU_Sales'].sum().nlargest(5).reset_index()

grafico_na = alt.Chart(top_5_na).mark_bar().encode(
    x=alt.X('NA_Sales:Q', title='Ventas en NA (en millones)'),
    y=alt.Y('Publisher:N', sort='-x', title='Publisher'),
    color=alt.Color('Publisher:N', legend=None),
    tooltip=['Publisher', 'NA_Sales']
).properties(
    title='Top 5 Publishers por Ventas en NA',
    width=500
)
st.altair_chart(grafico_na)

#gráfico de barras para JP
grafico_jp = alt.Chart(top_5_jp).mark_bar().encode(
    x=alt.X('JP_Sales:Q', title='Ventas en JP (en millones)'),
    y=alt.Y('Publisher:N', sort='-x', title='Publisher'),
    color=alt.Color('Publisher:N', legend=None),
    tooltip=['Publisher', 'JP_Sales']
).properties(
    title='Top 5 Publishers por Ventas en JP',
    width=500
)

st.altair_chart(grafico_jp)

#gráfico de barras para EU
grafico_eu = alt.Chart(top_5_eu).mark_bar().encode(
    x=alt.X('EU_Sales:Q', title='Ventas en EU (en millones)'),
    y=alt.Y('Publisher:N', sort='-x', title='Publisher'),
    color=alt.Color('Publisher:N', legend=None),
    tooltip=['Publisher', 'EU_Sales']
).properties(
    title='Top 5 Publishers por Ventas en EU',
    width=500
)
st.altair_chart(grafico_eu)


ventas_por_genero = data.groupby('Genre')['Global_Sales'].sum().reset_index()

# Crear gráfico
grafico_generos_ventas = alt.Chart(ventas_por_genero).mark_bar().encode(
    x=alt.X('Global_Sales:Q', title='Ventas Globales (en millones)'),
    y=alt.Y('Genre:N', sort='-x', title='Género'),
    color=alt.Color('Genre:N', legend=None),
    tooltip=['Genre', 'Global_Sales']
).properties(
    title='Ventas Globales por Género de Videojuego',
    width=600
)
st.altair_chart(grafico_generos_ventas)

stacked_bar = alt.Chart(data_filtrada).mark_bar().encode(
    x=alt.X('Platform:N', title='Plataforma'),
    y=alt.Y('sum(Global_Sales):Q', title='Ventas Globales (en millones)'),
    color=alt.Color('Genre:N', title='Género'),
    tooltip=['Platform', 'Genre', 'sum(Global_Sales)']
).properties(
    title='Ventas Globales por Plataforma y Género',
    width=900
)
st.altair_chart(stacked_bar)

#agrupar las ventas globales por plataforma
ventas_por_plataforma = data_filtrada.groupby('Platform')['Global_Sales'].sum().reset_index()
ventas_por_plataforma = ventas_por_plataforma.sort_values(by='Global_Sales', ascending=False)

#gráfico de torta
grafico_torta = alt.Chart(ventas_por_plataforma).mark_arc().encode(
    theta=alt.Theta(field="Global_Sales", type="quantitative", title='Ventas Globales'),
    color=alt.Color(field="Platform", type="nominal", title='Plataforma'),
    tooltip=['Platform', 'Global_Sales']
).properties(
    title='Proporción de Ventas Globales por Plataforma'
)
st.altair_chart(grafico_torta)

ventas_por_plataforma = data_filtrada.groupby('Platform')['Global_Sales'].sum().reset_index()
ventas_por_plataforma = ventas_por_plataforma.sort_values(by='Global_Sales', ascending=False)
top_10_plataformas = ventas_por_plataforma.nlargest(10, 'Global_Sales')

grafico_torta_top_10 = alt.Chart(top_10_plataformas).mark_arc().encode(
    theta=alt.Theta(field="Global_Sales", type="quantitative", title='Ventas Globales'),
    color=alt.Color(field="Platform", type="nominal", title='Plataforma'),
    tooltip=['Platform', 'Global_Sales']
).properties(
    title='Proporción de Ventas Globales por Plataforma (Top 10)',
    width=500
)
st.altair_chart(grafico_torta_top_10)

box_plot = alt.Chart(data_filtrada).mark_boxplot().encode(
    x=alt.X('Genre:N', title='Género'),
    y=alt.Y('Global_Sales:Q', title='Ventas Globales (en millones)'),
    color='Genre:N'
).properties(
    title='Distribución de Ventas Globales por Género',
    width=800
)
st.altair_chart(box_plot)