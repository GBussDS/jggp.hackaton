import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, callback, Output, Input
import dash
from google.cloud import bigquery

from components.header import header
from components.apply import apply_updates
from components.container import create_large_container_graph

# Registrando a página
dash.register_page(__name__, path="/query", name="Query")

# Crie uma instância do cliente BigQuery
client = bigquery.Client(project='hackaton-fgv-guris')

# Faça a consulta SQL
query = """
SELECT *
FROM datario.clima_pluviometro.taxa_precipitacao_inea
"""
query_job = client.query(query)
    

# Função de callback para fazer a consulta e armazenar os dados
@callback(
    Output('query-data', 'data'),
    Input('query-data', 'id')
)
def store_data(id):
    # Converta o resultado da consulta em um DataFrame
    df_datario = query_job.to_dataframe()

    return df_datario.to_dict('records')  # Convertendo o DataFrame para um dicionário

# Função de callback para atualizar o gráfico de barras
@callback(
    Output('query-graph', 'figure'),
    Input('query-data', 'data')
)
def update_bar_chart(data):
    df = pd.DataFrame(data)  # Converta os dados de volta para um DataFrame
    fig = px.bar(df, x='id_estacao', y='acumulado_chuva_15_min', title='Acumulados por estação em 2023', color_discrete_sequence=["#0042AB"])
    return fig

# Layout of the dashboard
layout = html.Div([
    header("Chuva no Rio de Janeiro"),
    
    html.Div([
        create_large_container_graph('query-graph', "Boxplot da Chuva"),
    ], style={'display': 'flex', 'paddingRight': '5%'}),
    
    dcc.Store(id='query-data')
],)