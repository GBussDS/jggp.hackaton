import pandas as pd
from dash import dcc, html, callback, Output, Input
import dash
import geopandas as gpd
from shapely.wkt import loads
import folium
from branca.colormap import linear
from shapely.geometry import Point
from components.header import header

# Registrando a página
dash.register_page(__name__, path="/bairros", name="Bairros")

@callback(
    Output('map-data-store', 'data'),
    Output('chuva-data-store', 'data'),
    Output('estacoes-data-store', 'data'),
    Input('map-data-store', 'id')
)
def store_map_data(id):
    df = pd.read_csv('dashboard/data/bairros.csv')
    new_df = pd.DataFrame({'nome':df['nome'],'geometry': df['geometry_wkt']})
    new_df['geometry'] = new_df['geometry']
    gdf_dict = new_df.to_dict()

    df_chuva = pd.read_csv('dashboard/data/acumulado_chuva.csv').dropna().to_dict()
    df_estacoes = pd.read_csv('dashboard/data/estacoes_alertario.csv').to_dict()

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
    m = folium.Map(location=[gdf.geometry.centroid.y.mean()-0.1, gdf.geometry.centroid.x.mean()-0.12], zoom_start=11)
    
    # Sort thresholds for colormap
    sorted_thresholds = sorted(df_chuva['acumulado_chuva_24h'].unique())
    colormap = linear.YlGnBu_09.scale(min(sorted_thresholds), max(sorted_thresholds))

    # Add legend to the map
    colormap.caption = 'Rain Accumulation (24h)'
    m.add_child(colormap)

    for _, r in gdf.iterrows():
        # Create a shapely Point for the centroid of the polygon
        polygon_centroid = Point(r.geometry.centroid.x, r.geometry.centroid.y)
        
        # Iterate through stations to find stations inside the polygon
        for _, station in df_estacoes.iterrows():
            station_point = Point(station['longitude'], station['latitude'])
            if station_point.within(r.geometry):
                # Determine color based on 'acumulado_chuva_24_h'
                color = colormap(df_chuva.loc[df_chuva['id_estacao'] == station['id_estacao'], 'acumulado_chuva_24h'].iloc[0])
                # Create GeoJSON for the polygon
                geo_j = folium.GeoJson(data=r.geometry.__geo_interface__,
                                    style_function=lambda x: {'fillColor': color, 'fillOpacity': 0.7, 'color': 'black'})
                folium.Popup(r['nome']).add_to(geo_j)
                geo_j.add_to(m)
                break

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