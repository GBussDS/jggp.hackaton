import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, callback, Output, Input
import dash
from google.cloud import bigquery

from components.header import header
from components.apply import apply_updates
from components.container import create_large_container_graph

# Registrando a página
dash.register_page(__name__, path="/rain4", name="Chuva4")

# Crie uma instância do cliente BigQuery
client = bigquery.Client(project='hackaton-fgv-guris')

# Função de callback para fazer a consulta e armazenar os dados
@callback(
    Output('rain-data-store-7A', 'data'),
    Input('rain-data-store-7A', 'id')
)
def store_data(id):
    # Faça a consulta SQL
    query = """
    SELECT *
    FROM `datario.clima_pluviometro.taxa_precipitacao_inea`
    """
    query_job = client.query(query)

    # Converta o resultado da consulta em um DataFrame
    df_datario = query_job.to_dataframe()

    return df_datario.to_dict('records')  # Convertendo o DataFrame para um dicionário

# Função de callback para atualizar o gráfico de barras
@callback(
    Output('rain-graph-7A', 'figure'),
    Input('rain-data-store-7A', 'data')
)
def update_bar_chart(data):
    df = pd.DataFrame(data)  # Converta os dados de volta para um DataFrame
    fig = px.bar(df, x='id_estacao', y='acumulado_chuva_15_min', title='Acumulados por estação em 2023', color_discrete_sequence=["#0042AB"])
    return fig


# Função de callback para armazenar o DataFrame
@callback(
    Output('map-data-store', 'data'),
    Input('map-data-store', 'id')
)
def store_map_data(id):
    # Criando um DataFrame do zero
    df = pd.DataFrame({
        'Cidade': ['Flamengo', 'Barra da Tijuca', 'Botafogo', 'Catete', 'Centro'],
        'Latitude': [-22.933, -23.012, -22.951, -22.926, -22.906],
        'Longitude': [-43.175, -43.304, -43.184, -43.176, -43.181],
        'Chuva': [100, 150, 25, 200, 80],
    })

    return df.to_dict('records')  # Convertendo o DataFrame para um dicionário


# Função de callback para atualizar o gráfico de mapa
@callback(
    Output('map-graph', 'figure'),
    Input('map-data-store', 'data')
)
def update_map(data):
    df = pd.DataFrame(data)
    
    fig = px.scatter_mapbox(df, lat='Latitude', lon='Longitude', hover_name='Cidade', hover_data=['Chuva'], 
                            size='Chuva', size_max=15, zoom=10, height=300)

    fig.update_traces(marker=dict(opacity=0.5))  # Define a opacidade do marcador para 50%


    fig.update_layout(mapbox_style="carto-positron")  # Usa um estilo de mapa menos detalhado
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig


# Layout of the dashboard
layout = html.Div([
    header("Chuva no Rio de Janeiro"),
    
    html.Div([
        create_large_container_graph('map-graph', "Mapa do Rio de Janeiro"),
        create_large_container_graph('rain-graph-7A', "Boxplot da Chuva"),
    ], style={'display': 'flex', 'paddingRight': '5%'}),
    
    dcc.Store(id='map-data-store'),
    dcc.Store(id='rain-data-store-7A')
],)