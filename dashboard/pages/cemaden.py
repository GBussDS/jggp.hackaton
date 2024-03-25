from dash import dcc, html, Dash, callback, Output, Input
import dash
import pandas as pd
import plotly.express as px
from data.data_query import df_cemaden, df_precipitacao_cemaden

from components.header import header
from components.apply import apply_updates
from components.container import create_container_graph

# Registrando a página
dash.register_page(__name__, path="/cemaden", name="Cemaden")

# Função de callback para atualizar o gráfico de precipitação de 24 horas
@callback(
    Output('graph-24h-precipitation', 'figure'),
    Input('rain-data-store', 'data')
)
def update_24h_precipitation_graph(data):
    # Filtramos os dados para o último mês
    df_last_month = df_precipitacao_cemaden[df_precipitacao_cemaden['data_medicao'] > pd.Timestamp.now() - pd.DateOffset(days=30)]

    # Ordenamos o DataFrame por 'data_medicao'
    df_last_month = df_last_month.sort_values('data_medicao')

    # Mesclamos os dois dataframes em 'id_estacao'
    df = pd.merge(df_cemaden, df_last_month, on='id_estacao')

    # Criamos o gráfico de linha
    fig = px.line(df, x='data_medicao', y='acumulado_chuva_24_h', color='id_estacao', title='Precipitação horária por estação no último mês')
    fig = apply_updates(fig)
    # Remover a legenda
    fig.update_layout(showlegend=False)

    return fig

# Função de callback para atualizar o gráfico de precipitação de 1 hora
@callback(
    Output('graph-1h-precipitation', 'figure'),
    Input('rain-data-store', 'data')
)
def update_1h_precipitation_graph(data):
    # Filtramos os dados para o último mês
    df_last_month = df_precipitacao_cemaden[df_precipitacao_cemaden['data_medicao'] > pd.Timestamp.now() - pd.DateOffset(days=2)]

    # Ordenamos o DataFrame por 'data_medicao'
    df_last_month = df_last_month.sort_values('data_medicao')

    # Mesclamos os dois dataframes em 'id_estacao'
    df = pd.merge(df_cemaden, df_last_month, on='id_estacao')

    # Criamos o gráfico de linha
    fig = px.line(df, x='data_medicao', y='acumulado_chuva_1_h', color='id_estacao', title='Precipitação horária por estação no último mês')
    fig = apply_updates(fig)
    # Remover a legenda
    fig.update_layout(showlegend=False)
    return fig


# Função de callback para atualizar o gráfico de precipitação de 96 horas
@callback(
    Output('graph-96h-precipitation', 'figure'),
    Input('rain-data-store', 'data')
)
def update_96h_precipitation_graph(data):
    # Filtramos os dados para os últimos 4 meses
    df_last_4_months = df_precipitacao_cemaden[df_precipitacao_cemaden['data_medicao'] > pd.Timestamp.now() - pd.DateOffset(months=4)]

    # Ordenamos o DataFrame por 'data_medicao'
    df_last_4_months = df_last_4_months.sort_values('data_medicao')

    # Mesclamos os dois dataframes em 'id_estacao'
    df = pd.merge(df_cemaden, df_last_4_months, on='id_estacao')

    # Criamos o gráfico de linha
    fig = px.line(df, x='data_medicao', y='acumulado_chuva_96_h', color='id_estacao', title='Precipitação a cada 96 horas por estação nos últimos 4 meses')
    fig = apply_updates(fig)
    # Remover a legenda
    fig.update_layout(showlegend=False)
    return fig

# Função de callback para atualizar o gráfico de precipitação de 10 minutos
@callback(
    Output('graph-10min-precipitation', 'figure'),
    Input('rain-data-store', 'data')
)
def update_10min_precipitation_graph(data):
    # Filtramos os dados para o último mês
    df_last_month = df_precipitacao_cemaden[df_precipitacao_cemaden['data_medicao'] > pd.Timestamp.now() - pd.DateOffset(hours=6)]

    # Ordenamos o DataFrame por 'data_medicao'
    df_last_month = df_last_month.sort_values('data_medicao')

    # Mesclamos os dois dataframes em 'id_estacao'
    df = pd.merge(df_cemaden, df_last_month, on='id_estacao')

    # Criamos o gráfico de linha
    fig = px.line(df, x='data_medicao', y='acumulado_chuva_15_min', color='id_estacao', title='Precipitação a cada 10 minutos por estação no último mês')
    fig = apply_updates(fig)
    # Remover a legenda
    fig.update_layout(showlegend=False)
    return fig



# Layout do dashboard
layout = html.Div([
    header("Chuva no Rio de Janeiro"),
    
    html.Div([
        create_container_graph('graph-24h-precipitation', "Gráfico de Precipitação de 24 Horas"),
        create_container_graph('graph-1h-precipitation', "Gráfico de Precipitação de 1 Hora"),
    ], style={'display': 'flex', 'paddingRight': '5%'}),
    html.Div([
        create_container_graph('graph-96h-precipitation', "Gráfico de Precipitação de 96 Horas"),
        create_container_graph('graph-10min-precipitation', "Gráfico de Precipitação de 10 Minutos"),
    ], style={'display': 'flex', 'paddingRight': '5%'}),
    
    dcc.Store(id='rain-data-store')
],)
