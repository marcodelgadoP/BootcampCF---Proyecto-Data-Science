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

st.markdown("**Cantidad de Juegos por Plataforma y Género**.")
st.markdown('''
            Este gráfico de calor muestra la cantidad de juegos distribuidos por plataformas y géneros. 
            El color indica la densidad de juegos en cada combinación de plataforma y género, donde los colores más oscuros muestran una mayor cantidad de juegos y los colores más claros indican una menor cantidad. Este tipo de visualización es útil para identificar patrones de popularidad de géneros en diferentes plataformas.
''')
mapa_calor = alt.Chart(data_filtrada).mark_rect().encode(
    x=alt.X('Platform:N', title='Plataforma'),
    y=alt.Y('Genre:N', title='Género'),
    color=alt.Color('count():Q', title='Cantidad de Juegos'),
    tooltip=['Platform', 'Genre', 'count()']
).properties(
    width=800
)
st.altair_chart(mapa_calor)

st.markdown("**Top 10 Editoras con mas publicaciones**.")
st.markdown('''
            Este gráfico de barras presenta las 10 editoras de videojuegos con mayor cantidad de publicaciones.  
            Se observa que Electronic Arts es la editora con mayor cantidad de juegos publicados, seguida de Activision y Namco Bandai Games. 
            Este gráfico ayuda a identificar las editoras más activas en la industria de videojuegos, permitiendo comparaciones claras entre ellas.
''')
top_publishers = data['Publisher'].value_counts().nlargest(10).reset_index()
top_publishers.columns = ['Publisher', 'Count']

publisher_chart = alt.Chart(top_publishers).mark_bar().encode(
    x=alt.X('Publisher:N', sort='-y', title='Publisher'),
    y=alt.Y('Count:Q', title='Number of Publications'),
    tooltip=['Publisher', 'Count']
).properties(
    width=600,
    height=400
).interactive()
st.altair_chart(publisher_chart)

# filtro
data_filtrada_2008_2009 = data_filtrada[(data_filtrada['Year'] == 2008) | (data_filtrada['Year'] == 2009)]
publisher_counts_2008_2009 = data_filtrada_2008_2009.groupby('Publisher').size().reset_index(name='Cantidad')
#ordenar 
publishers_mas_publicaciones = publisher_counts_2008_2009.sort_values(by='Cantidad', ascending=False).head(10)
st.markdown("**Top 10 Publishers con más Publicaciones en 2008 y 2009**.")
st.markdown('''
            Este gráfico de barras muestra las 10 editoras que publicaron más videojuegos en los años 2008 y 2009.  
            Electronic Arts, Ubisoft y Activision encabezan la lista con la mayor cantidad de lanzamientos en ese periodo. Este gráfico es útil para identificar las editoras más activas durante esos años específicos, lo que puede reflejar una tendencia en el mercado de los videojuegos en esa época.
''')
#gráfico
grafico_publishers = alt.Chart(publishers_mas_publicaciones).mark_bar().encode(
    x=alt.X('Publisher:N', sort='-y', title='Publisher'),
    y=alt.Y('Cantidad:Q', title='Cantidad de Juegos'),
    color=alt.Color('Publisher:N', legend=None)
).properties(
    width=900
).configure_axisX(
    labelAngle=-45 
)
st.altair_chart(grafico_publishers)

#cantidad de publicaciones por cada publisher
publisher_counts = data_filtrada.groupby('Publisher').size().reset_index(name='Cantidad')
publishers_mas_de_500 = publisher_counts[publisher_counts['Cantidad'] > 300]
st.markdown("**Publishers con Más de 300 Publicaciones**.")
st.markdown('''
            Este gráfico muestra todas las editoras que han lanzado más de 300 publicaciones en total. 
            Electronic Arts lidera ampliamente con más de 1,000 publicaciones, seguida por editoras como Activision, Namco Bandai Games, y Ubisoft. 
            Este gráfico permite identificar las editoras más prolíficas a lo largo del tiempo, dándonos una visión clara de los actores más importantes en la industria de videojuegos.
''')
grafico_publishers = alt.Chart(publishers_mas_de_500).mark_bar().encode(
    x=alt.X('Publisher:N', sort='-y', title='Publisher'),
    y=alt.Y('Cantidad:Q', title='Cantidad de Publicaciones'),
    color=alt.Color('Publisher:N', legend=None)
).properties(
    width=900
).configure_axisX(
    labelAngle=-65  
)
st.altair_chart(grafico_publishers)

st.markdown("**Top 10 Publisher por Ventas Globales**.")
st.markdown('''
            Este gráfico muestra las diez editoras de videojuegos con mayores ventas a nivel mundial. 
            Permite identificar qué compañías han dominado el mercado global en términos de ventas.
''')
top_10_publishers = data.groupby('Publisher')['Global_Sales'].sum().nlargest(10).reset_index()
# Gráfico de barras para las 10 primeras editoras 
grafico_top_10_publishers = alt.Chart(top_10_publishers).mark_bar().encode(
    x=alt.X('Global_Sales:Q', title='Ventas Globales (en millones)'),
    y=alt.Y('Publisher:N', sort='-x', title='Publisher'),
    color=alt.Color('Publisher:N', legend=None),
    tooltip=['Publisher', 'Global_Sales']
).properties(
    width=600
)

st.altair_chart(grafico_top_10_publishers)

#filtro NA
top_5_na = data.groupby('Publisher')['NA_Sales'].sum().nlargest(5).reset_index()
#filtro JP
top_5_jp = data.groupby('Publisher')['JP_Sales'].sum().nlargest(5).reset_index()
#filtro EU
top_5_eu = data.groupby('Publisher')['EU_Sales'].sum().nlargest(5).reset_index()

st.markdown("**Top 5 Publishers por Ventas en NA**.")
st.markdown('''
            Visualiza las cinco principales editoras por ventas en Norteamérica. Ayuda a entender qué editoras tienen mayor impacto en esta región específica.
''')
grafico_na = alt.Chart(top_5_na).mark_bar().encode(
    x=alt.X('NA_Sales:Q', title='Ventas en NA (en millones)'),
    y=alt.Y('Publisher:N', sort='-x', title='Publisher'),
    color=alt.Color('Publisher:N', legend=None),
    tooltip=['Publisher', 'NA_Sales']
).properties(
    width=500
)
st.altair_chart(grafico_na)

#gráfico de barras para JP
st.markdown("**Top 5 Publishers por Ventas en JP**.")
st.markdown('''
            Enfocado en el mercado japonés, este gráfico muestra las cinco editoras que lideran las ventas en Japón. Es útil para comparar con otras regiones.
''')
grafico_jp = alt.Chart(top_5_jp).mark_bar().encode(
    x=alt.X('JP_Sales:Q', title='Ventas en JP (en millones)'),
    y=alt.Y('Publisher:N', sort='-x', title='Publisher'),
    color=alt.Color('Publisher:N', legend=None),
    tooltip=['Publisher', 'JP_Sales']
).properties(
    width=500
)

st.altair_chart(grafico_jp)

#gráfico de barras para EU
st.markdown("**Top 5 Publishers por Ventas en EU**.")
st.markdown('''
            Muestra las cinco editoras con más ventas en Europa. Es interesante para evaluar la diferencia en preferencias de los consumidores europeos.
''')
grafico_eu = alt.Chart(top_5_eu).mark_bar().encode(
    x=alt.X('EU_Sales:Q', title='Ventas en EU (en millones)'),
    y=alt.Y('Publisher:N', sort='-x', title='Publisher'),
    color=alt.Color('Publisher:N', legend=None),
    tooltip=['Publisher', 'EU_Sales']
).properties(
    width=500
)
st.altair_chart(grafico_eu)


ventas_por_genero = data.groupby('Genre')['Global_Sales'].sum().reset_index()

# Crear gráfico
st.markdown("**Ventas Globales por Género de Videojuego**.")
st.markdown('''
            Este gráfico categoriza las ventas globales de videojuegos por géneros (como Acción, Aventura, etc.). Ofrece una visión sobre los géneros más populares.
''')
grafico_generos_ventas = alt.Chart(ventas_por_genero).mark_bar().encode(
    x=alt.X('Global_Sales:Q', title='Ventas Globales (en millones)'),
    y=alt.Y('Genre:N', sort='-x', title='Género'),
    color=alt.Color('Genre:N', legend=None),
    tooltip=['Genre', 'Global_Sales']
).properties(
    width=600
)
st.altair_chart(grafico_generos_ventas)

st.markdown("**Ventas Globales por Plataforma y Género**.")
st.markdown('''
            Relaciona las ventas globales de videojuegos con sus géneros y las plataformas en las que se publicaron. Esto ayuda a entender la popularidad de cada género según la plataforma.
''')
stacked_bar = alt.Chart(data_filtrada).mark_bar().encode(
    x=alt.X('Platform:N', title='Plataforma'),
    y=alt.Y('sum(Global_Sales):Q', title='Ventas Globales (en millones)'),
    color=alt.Color('Genre:N', title='Género'),
    tooltip=['Platform', 'Genre', 'sum(Global_Sales)']
).properties(
    width=900
)
st.altair_chart(stacked_bar)

#agrupar las ventas globales por plataforma
ventas_por_plataforma = data_filtrada.groupby('Platform')['Global_Sales'].sum().reset_index()
ventas_por_plataforma = ventas_por_plataforma.sort_values(by='Global_Sales', ascending=False)

#gráfico de torta
st.markdown("**Proporción de Ventas Globales por Plataforma**.")
st.markdown('''
            Un gráfico de proporciones que muestra cómo se distribuyen las ventas globales entre las diferentes plataformas de videojuegos.
''')
grafico_torta = alt.Chart(ventas_por_plataforma).mark_arc().encode(
    theta=alt.Theta(field="Global_Sales", type="quantitative", title='Ventas Globales'),
    color=alt.Color(field="Platform", type="nominal", title='Plataforma'),
    tooltip=['Platform', 'Global_Sales']
).properties(
)
st.altair_chart(grafico_torta)

ventas_por_plataforma = data_filtrada.groupby('Platform')['Global_Sales'].sum().reset_index()
ventas_por_plataforma = ventas_por_plataforma.sort_values(by='Global_Sales', ascending=False)
top_10_plataformas = ventas_por_plataforma.nlargest(10, 'Global_Sales')

st.markdown("**Proporción de Ventas Globales por Plataforma (Top 10)**.")
st.markdown('''
            Similar al anterior, pero enfocado únicamente en las diez principales plataformas con mayores ventas globales.
''')
grafico_torta_top_10 = alt.Chart(top_10_plataformas).mark_arc().encode(
    theta=alt.Theta(field="Global_Sales", type="quantitative", title='Ventas Globales'),
    color=alt.Color(field="Platform", type="nominal", title='Plataforma'),
    tooltip=['Platform', 'Global_Sales']
).properties(
    width=500
)
st.altair_chart(grafico_torta_top_10)

st.markdown("**Distribución de Ventas Globales por Género**.")
st.markdown('''
            Este gráfico ilustra cómo se distribuyen las ventas globales en cada género de videojuego, dando una idea de la popularidad relativa entre géneros.
''')
box_plot = alt.Chart(data_filtrada).mark_boxplot().encode(
    x=alt.X('Genre:N', title='Género'),
    y=alt.Y('Global_Sales:Q', title='Ventas Globales (en millones)'),
    color='Genre:N'
).properties(
    width=800
)
st.altair_chart(box_plot)

ventas_por_region = data[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum().reset_index()
ventas_por_region.columns = ['Region', 'Sales']

st.markdown("**Proporción de Ventas Globales por Región**.")
st.markdown('''
            Un gráfico que muestra la proporción de las ventas globales distribuidas por regiones (NA, EU, JP y otras), lo que permite comparar el desempeño de ventas por zonas geográficas.
''')
grafico_ventas_region = alt.Chart(ventas_por_region).mark_arc().encode(
    theta=alt.Theta(field='Sales', type='quantitative'),
    color=alt.Color(field='Region', type='nominal'),
    tooltip=['Region', 'Sales']
).properties(
)
st.altair_chart(grafico_ventas_region)

#columnas necesarias
columnas_ventas = ['Name', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
#ordenar los juegos por las ventas globales y seleccionar los 10 primeros
juegos_mas_vendidos = data.sort_values('Global_Sales', ascending=False).head(10)
#transformar los datos a formato largo 
juegos_ventas_long = juegos_mas_vendidos.melt(
    id_vars='Name',
    value_vars=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales'],
    var_name='Region',
    value_name='Sales'
)
# Crear gráfico de barras apiladas
st.markdown("**10 Juegos Más Vendidos en Cada Región**.")
st.markdown('''
           Lista los diez juegos con mayores ventas en cada región (NA, EU, JP, etc.), permitiendo ver las diferencias de preferencias por región.
''')
grafico_juegos_mas_vendidos_regiones = alt.Chart(juegos_ventas_long).mark_bar().encode(
    x=alt.X('sum(Sales):Q', title='Ventas (en millones)', stack='normalize'),
    y=alt.Y('Name:N', sort='-x', title='Juego'),
    color=alt.Color('Region:N', title='Región'),
    tooltip=['Name', 'Region', 'Sales']
).properties(
    width=700,
    height=400
)

st.altair_chart(grafico_juegos_mas_vendidos_regiones)

ventas_por_año = data_filtrada.groupby('Year')['Global_Sales'].sum().reset_index()

st.markdown("**Ventas Globales de Videojuegos por Año**.")
st.markdown('''
           Muestra la evolución de las ventas globales de videojuegos a lo largo de los años. Es útil para analizar tendencias y ciclos en la industria del videojuego.
''')
grafico_lineas = alt.Chart(ventas_por_año).mark_line().encode(
    x=alt.X('Year:O', title='Año'),
    y=alt.Y('Global_Sales:Q', title='Ventas Globales (en millones)'),
    tooltip=['Year', 'Global_Sales']
).properties(
    width=800
)

st.altair_chart(grafico_lineas)