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
dash.register_page(__name__, path="/bairros", name="Bairros")

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
    df_chuva = df_chuva.sort_values('horario').groupby('id_estacao').tail(1).to_dict()
    df_estacoes = pd.read_csv('dashboard/data/estacoes_websirene.csv').to_dict()

    return gdf_dict, df_chuva, df_estacoes


@callback(
    Output('map-graph', 'srcDoc'),
    Input('map-data-store', 'data'),
    Input('chuva-data-store', 'data'),
    Input('estacoes-data-store', 'data'),
    Input('column-dropdown', 'value')
)
def update_map(map_data, chuva_data, estacoes_data, selected_column):
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
    sorted_thresholds = sorted(df_chuva[selected_column].unique())
    colormap = linear.YlGnBu_09.scale(1, 200)

    # Add legend to the map
    colormap.caption = f'Chuva Acumulada ({selected_column})'
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
            # Calculate the mean of the selected column for these stations
            mean_chuva = station_data[selected_column].mean()
            # Determine color based on the mean
            color = colormap(mean_chuva)
            
            # Create GeoJSON for the polygon
            geo_j = folium.GeoJson(data=r.geometry.__geo_interface__,
                                style_function=lambda x, color=color: {'fillColor': color, 'fillOpacity': 1, 'color': 'black'})

            folium.Popup(f"""
                <div>
                    <h2>{r['nome']}</h2>
                    <h4>Acumulado: {int(mean_chuva)}mm</h4>
                </div>
            """).add_to(geo_j)
            geo_j.add_to(m)

    # Display the map
    m_html = m._repr_html_()

    return m_html

# Layout of the dashboard
layout = html.Div([
    header("Acumulado de chuva por período", dcc.Dropdown(
            id='column-dropdown',
            options=[
                {'label': 'Últimas 24 h', 'value': 'acumulado_chuva_24_h'},
                {'label': 'Últimos 15 min', 'value': 'acumulado_chuva_15_min'},
                {'label': 'Últimas 1 h', 'value': 'acumulado_chuva_1_h'},
                {'label': 'Últimas 4 h', 'value': 'acumulado_chuva_4_h'},
                {'label': 'Últimas 96 h', 'value': 'acumulado_chuva_96_h'}
            ],
            value='acumulado_chuva_24_h',  # Default value
            clearable=False,
            style={'width':'10vw','zIndex':'999','overflow': 'visible'}
        )),
    
    html.Div([
        html.H1('mm Por Bairro', style={'textAlign': 'center', 'fontSize': '20px',"color": "#FFFFFF"}),
        html.Iframe(id='map-graph', srcDoc='', width='100%', height='90%')
    ], style={'backgroundColor': '#000000', 'borderRadius': '15px', 'margin': '0.5% 0.5%', 'padding': '20px', 'height': '90vh', 'width': '85vw'}),
    
    dcc.Store(id='map-data-store'),
    dcc.Store(id='map-data-json'),
    dcc.Store(id='estacoes-data-store'),
    dcc.Store(id='chuva-data-store'),

],style={'width':'90vw','height':'100vh'})
