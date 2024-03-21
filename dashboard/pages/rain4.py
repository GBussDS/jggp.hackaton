import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, callback, Output, Input
import dash

from components.header import header
from components.apply import apply_updates

# Registrando a página
dash.register_page(__name__, path="/rain4", name="Chuva4", svg="icons/rain.svg")

# Função de callback para armazenar o DataFrame
@callback(
    Output('map-data-store', 'data'),
    Input('map-data-store', 'id')
)
def store_map_data(id):
    # Criando um DataFrame do zero
    df = pd.read_csv('../data/drenagem.csv')

    return df.to_dict('records')  # Convertendo o DataFrame para um dicionário


# Função de callback para atualizar o gráfico de mapa
@callback(
    Output('map-graph', 'figure'),
    Input('map-data-store', 'data')
)
def update_map(data):
    df = pd.DataFrame(data)
    
    fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', hover_name='classe', hover_data=['data_atualizacao'], 
                            size=10, size_max=15, zoom=10, height=300)

    fig.update_traces(marker=dict(opacity=0.5))  # Define a opacidade do marcador para 50%


    fig.update_layout(mapbox_style="carto-positron")  # Usa um estilo de mapa menos detalhado
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

import pandas as pd
import geopandas as gpd
import plotly.express as px

@callback(
    Output('map-data-store', 'data'),
    Input('map-data-store', 'id')
)
def store_map_data(id):
    # Load the CSV file into a DataFrame
    df = pd.read_csv('../data/bairros.csv')

    # Convert the 'geometry_wkt' column to a GeoSeries
    df['geometry'] = gpd.GeoSeries.from_wkt(df['geometry_wkt'])

    # Convert the DataFrame to a GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry='geometry')

    return gdf.to_dict('records')  # Convert the GeoDataFrame to a dictionary

@callback(
    Output('map-graph', 'figure'),
    Input('map-data-store', 'data')
)
def update_map(data):
    # Convert the data back into a GeoDataFrame
    gdf = gpd.GeoDataFrame(data)

    # Create a scatter mapbox figure
    fig = px.scatter_mapbox(gdf, lat=gdf.geometry.y, lon=gdf.geometry.x, 
                            hover_name='classe', hover_data=['data_atualizacao'], 
                            size=10, size_max=15, zoom=10, height=300)

    fig.update_traces(marker=dict(opacity=0.5))  # Set the marker opacity to 50%

    fig.update_layout(mapbox_style="carto-positron")  # Use a less detailed map style
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig



# Função de callback para armazenar o DataFrame
@callback(
    Output('boxplot-data-store', 'data'),
    Input('boxplot-data-store', 'id')
)
def store_boxplot_data(id):
    # Criando um DataFrame do zero
    df = pd.DataFrame({
        'Cidade': ['Flamengo', 'Barra da Tijuca', 'Botafogo', 'Catete', 'Centro'],
        'Chuva': [120, 150, 170, 200, 180]
    })

    return df.to_dict('records')  # Convertendo o DataFrame para um dicionário

# Função de callback para atualizar o gráfico de boxplot
@callback(
    Output('boxplot-graph', 'figure'),
    Input('boxplot-data-store', 'data')
)
def update_boxplot(data):
    df = pd.DataFrame(data)
    fig = px.box(df, y='Chuva', title='Boxplot da Chuva no Rio de Janeiro')
    
    fig = apply_updates(fig)
    
    return fig


layout = html.Div([
    header("Chuva no Rio de Janeiro"),
    
    html.Div([
        html.Div([
            html.H1("Mapa do Rio de Janeiro", style={'textAlign': 'center', 'fontSize': '20px'}),
            dcc.Graph(id='map-graph', style={'width': '90%', 'height': '80vh', 'display': 'block', 'margin': 'auto', 'backgroundColor': '#000000', 'borderRadius': '15px'}),
        ], style={'backgroundColor': '#000000', 'borderRadius': '15px', 'margin': '0.5% 0.5%', 'padding': '20px', 'height': '88vh', 'width': '45vw'}),

        html.Div([
            html.H1("Boxplot da Chuva", style={'textAlign': 'center', 'fontSize': '20px'}),
            dcc.Graph(id='boxplot-graph', style={'width': '90%', 'height': '80vh', 'display': 'block', 'margin': 'auto', 'backgroundColor': '#000000', 'borderRadius': '15px'}),
        ], style={'backgroundColor': '#000000', 'borderRadius': '15px', 'margin': '0.5% 0.5%', 'padding': '20px', 'height': '88vh', 'width': '45vw'}),
    ], style={'display': 'flex'}),
    
    dcc.Store(id='map-data-store'),
    dcc.Store(id='boxplot-data-store')
],)

