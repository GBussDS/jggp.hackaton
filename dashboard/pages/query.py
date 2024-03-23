import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, callback, Output, Input
import dash
from google.cloud import bigquery

from components.header import header
from components.apply import apply_updates
from components.container import create_large_container_graph

from data.data_query import df_precipitacao_inea

dash.register_page(__name__, path="/query", name="Query")

# Passa os dados
@callback(
    Output('query-data', 'data'),
    Input('query-data', 'id')
)
def store_data(id):
    # Converta o resultado da consulta em um DataFrame
    df = df_precipitacao_inea

    return df.to_dict('records')

# Faz o gráfico
@callback(
    Output('query-graph', 'figure'),
    Input('query-data', 'data')
)
def update_bar_chart(data):
    df = pd.DataFrame(data)
    fig = px.bar(df, x='id_estacao', y='acumulado_chuva_15_min', title='Acumulados por estação em 2023', color_discrete_sequence=["#0042AB"])
    return fig

# Layout of the dashboard
layout = html.Div([
    header("Chuva no Rio de Janeiro"),
    
    html.Div([
        create_large_container_graph('query-graph', "Por 15 minutos"),
    ], style={'display': 'flex', 'paddingRight': '5%'}),
    
    dcc.Store(id='query-data')
],)