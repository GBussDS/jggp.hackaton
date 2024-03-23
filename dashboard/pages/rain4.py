import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, callback, Output, Input
import dash
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.wkt import loads, dumps
import json
import plotly.graph_objects as go
import folium

from components.header import header
from components.apply import apply_updates
from components.container import create_large_container_graph, create_container_graph

# Registrando a página
dash.register_page(__name__, path="/rain4", name="Chuva4")

# # Função de callback para armazenar o DataFrame
# @callback(
#     Output('map-data-store', 'data'),
#     Input('map-data-store', 'id')
# )
# def store_map_data(id):
#     # Criando um DataFrame do zero
#     df = pd.read_csv('dashboard/data/drenagem.csv')

#     return df.to_dict('records')  # Convertendo o DataFrame para um dicionário


# # Função de callback para atualizar o gráfico de mapa
# @callback(
#     Output('map-graph', 'figure'),
#     Input('map-data-store', 'data')
# )
# def update_map(data):
#     df = pd.DataFrame(data)
    
#     fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', hover_name='classe', hover_data=['data_atualizacao'], 
#                             size=10, size_max=15, zoom=10, height=300)

#     fig.update_traces(marker=dict(opacity=0.5))  # Define a opacidade do marcador para 50%


#     fig.update_layout(mapbox_style="carto-positron")  # Usa um estilo de mapa menos detalhado
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#     return fig

@callback(
    Output('map-data-store', 'data'),
    Input('map-data-store', 'id')
)
def store_map_data(id):
    df = pd.read_csv('dashboard/data/bairros.csv')
    new_df = pd.DataFrame({'nome':df['nome'],'geometry': df['geometry_wkt']})
    new_df['geometry'] = new_df['geometry']
    # gdf = gpd.GeoDataFrame(new_df, geometry='geometry')
    # gdf['geometry'] = gdf['geometry'].apply(dumps)
    gdf_dict = new_df.to_dict()
    return gdf_dict


@callback(
    Output('map-graph', 'srcDoc'),
    Input('map-data-store', 'data'),
)
def update_map(data):
    df = pd.DataFrame(data)
    df['geometry'] = df['geometry'].apply(loads)
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
     # Create a map centered around the center of your GeoDataFrame
    m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=13)

    # Add each polygon to the map
    for _, r in gdf.iterrows():
        # Create a string of the form 'POLYGON ((x1 y1, x2 y2, ...))'
        sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                            style_function=lambda x: {'fillColor': 'orange'})
        folium.Popup(r['nome']).add_to(geo_j)
        geo_j.add_to(m)

    # Display the map
    m_html = m._repr_html_()

    return m_html

# Layout of the dashboard
layout = html.Div([
    header("Chuva no Rio de Janeiro"),

    html.Div([
        html.H1('Mapa bairros RJ', style={'textAlign': 'center', 'fontSize': '20px',"color": "#FFFFFF"}),
        html.Iframe(id='map-graph', srcDoc='', width='100%', height='90%')
    ], style={'backgroundColor': '#000000', 'borderRadius': '15px', 'margin': '0.5% 0.5%', 'padding': '20px', 'height': '90vh', 'width': '85vw'}),
    
    dcc.Store(id='map-data-store'),
    dcc.Store(id='map-data-json'),
    dcc.Store(id='boxplot-data-store')

],style={'width':'100vw','height':'100vh'})