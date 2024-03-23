import pandas as pd
from dash import dcc, html, callback, Output, Input
import dash
import geopandas as gpd
from shapely.wkt import loads
import folium
from branca.colormap import linear
from shapely.geometry import Point
from components.header import header
import os
from google.cloud import bigquery

# Registrando a página
dash.register_page(__name__, path="/rain4", name="Chuva4")

# Crie uma instância do cliente BigQuery
client = bigquery.Client(project='hackaton-fgv-guris')

@callback(
    Output('map-data-store', 'data'),
    Output('chuva-data-store', 'data'),
    Output('estacoes-data-store', 'data'),
    Input('map-data-store', 'id')
)
def store_map_data(id):
    # Faça a consulta SQL
    # query = """
    # SELECT *
    # FROM datario.clima_pluviometro.taxa_precipitacao_inea
    # """
    # query_job = client.query(query)

    df = pd.read_csv('dashboard/data/bairros.csv')
    new_df = pd.DataFrame({'nome': df['nome'], 'geometry': df['geometry_wkt']})
    new_df['geometry'] = new_df['geometry']
    gdf_dict = new_df.to_dict()

    df_chuva = pd.read_csv('dashboard/data/acumulado_chuva_websirene.csv').dropna()
    df_chuva['horario'] = pd.to_datetime(df_chuva['horario'])  # Convert to datetime
    # Keep only the latest entry for each id_estacao
    df_chuva = df_chuva.sort_values('horario').groupby('id_estacao').tail(1)
    df_chuva = df_chuva.rename(columns={'acumulado_chuva_24_h': 'acumulado_chuva_24h'}).to_dict()
    df_estacoes = pd.read_csv('dashboard/data/estacoes_websirene.csv').to_dict()

    return gdf_dict, df_chuva, df_estacoes


@callback(
    Output('map-graph', 'srcDoc'),
    Input('map-data-store', 'data'),
    Input('chuva-data-store', 'data'),
    Input('estacoes-data-store', 'data'),
)
def update_map(map_data, chuva_data, estacoes_data):
    df = pd.DataFrame(map_data)
    df_chuva = pd.DataFrame(chuva_data)
    df_estacoes = pd.DataFrame(estacoes_data)

    merged_df = pd.merge(df_chuva, df_estacoes, on='id_estacao', how='inner')

    df['geometry'] = df['geometry'].apply(loads)
    gdf = gpd.GeoDataFrame(df, geometry='geometry')

    # Create a map centered around the center of your GeoDataFrame
    m = folium.Map(location=[gdf.geometry.centroid.y.mean()-0.07, gdf.geometry.centroid.x.mean()+0.04], zoom_start=11.5, tiles =None)

    # Define the tile layer URL
    tile_url = 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}.png'

    # Define attribution
    attribution = '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'

    # Add the tile layer
    folium.TileLayer(tile_url, attr=attribution, name='CartoDB Voyager Labels Under').add_to(m)

    # Sort thresholds for colormap
    sorted_thresholds = sorted(df_chuva['acumulado_chuva_24h'].unique())
    colormap = linear.YlGnBu_09.scale(min(sorted_thresholds), max(sorted_thresholds))

    # Add legend to the map
    colormap.caption = 'Rain Accumulation (24h)'
    m.add_child(colormap)

    # Create a mapping between polygons and stations inside them
    station_polygon_map = {}
    for _, station in df_estacoes.iterrows():
        station_point = Point(station['longitude'], station['latitude'])
        for _, r in gdf.iterrows():
            if station_point.within(r.geometry):
                if r.name not in station_polygon_map:
                    station_polygon_map[r.name] = []
                station_polygon_map[r.name].append(station['id_estacao'])

    for _, r in gdf.iterrows():
        # Create a shapely Point for the centroid of the polygon
        polygon_centroid = Point(r.geometry.centroid.x, r.geometry.centroid.y)

        # Get all stations inside this polygon
        stations_inside_polygon = station_polygon_map.get(r.name, [])
        
        if stations_inside_polygon:
            # Get the relevant data for these stations
            station_data = merged_df[merged_df['id_estacao'].isin(stations_inside_polygon)]
            # Calculate the mean of 'acumulado_chuva_24h' for these stations
            mean_chuva = station_data['acumulado_chuva_24h'].mean()
            # Determine color based on the mean
            color = colormap(mean_chuva)
            
            # Create GeoJSON for the polygon
            geo_j = folium.GeoJson(data=r.geometry.__geo_interface__,
                                style_function=lambda x, color=color: {'fillColor': color, 'fillOpacity': 1, 'color': 'black'})
            folium.Popup(f"{r['nome']}\n\nAcumulado:{mean_chuva}").add_to(geo_j)
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
    dcc.Store(id='estacoes-data-store'),
    dcc.Store(id='chuva-data-store'),

],style={'width':'100vw','height':'100vh'})
