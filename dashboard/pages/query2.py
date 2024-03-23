import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, callback, Output, Input
import dash
from google.cloud import bigquery

from components.header import header
from components.apply import apply_updates
from components.container import create_container_graph

# Crie uma instância do cliente BigQuery
client = bigquery.Client(project='hackaton-fgv-guris')

# Faça a consulta SQL
query = """
SELECT *
FROM `datario.adm_cor_comando.ocorrencias`
"""
query_job = client.query(query)


# Registrando a página
dash.register_page(__name__, path="/query2", name="Sou uma query")

# Função de callback para fazer a consulta e armazenar os dados das ocorrências
@callback(
    Output('ocorrencias-data-store', 'data'),
    Input('ocorrencias-data-store', 'id')
)
def store_ocorrencias_data(id):
    # Converta o resultado da consulta em um DataFrame
    df_ocorrencias = query_job.to_dataframe()

    return df_ocorrencias.to_dict('records')  # Convertendo o DataFrame para um dicionário

# Função de callback para atualizar o gráfico de barras das ocorrências
@callback(
    Output('ocorrencias-graph', 'figure'),
    Input('ocorrencias-data-store', 'data')
)
def update_ocorrencias_chart(data):
    df = pd.DataFrame(data)  # Converta os dados de volta para um DataFrame
    
    # Agrupe os dados por bairro e gravidade e conte o número de ocorrências
    df_grouped = df.groupby(['bairro', 'gravidade']).size().reset_index(name='count')
    
    print(df_grouped)
    
    # Crie o gráfico de barras
    fig = px.bar(df_grouped, x='bairro', y='count', color='gravidade', title='Número de ocorrências por gravidade e bairro', color_discrete_sequence=["#0042AB"])
    
    return fig


# Defina o layout do aplicativo
layout = html.Div([
    header("Chuva no Rio de Janeiro"),
    
    dcc.Graph(id='ocorrencias-graph'),
    
    dcc.Store(id='ocorrencias-data-store'),
    dcc.Store(id='procedimento-data-store'),
])