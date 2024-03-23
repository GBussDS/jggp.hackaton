import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, callback, Output, Input
import dash
import os

from components.header import header
from components.apply import apply_updates
from components.container import create_container_graph

# Registrando a página
dash.register_page(__name__, path="/rain", name="Chuva1")

# Função de callback para armazenar o DataFrame
@callback(
    Output('rain-data-store-4A', 'data'),
    Input('rain-data-store-4A', 'id')
)
def store_data(id):
    # Criando um DataFrame do zero
    df = pd.DataFrame({
        'Cidade': ['Flamengo', 'Barra da Tijuca', 'Botafogo', 'Catete', 'Centro'],
        'Chuva': [120, 150, 170, 200, 150]
    })

    return df.to_dict('records')  # Convertendo o DataFrame para um dicionário

# Função de callback para atualizar o gráfico de pizza
@callback(
    Output('rain-graph-1A', 'figure'),
    Input('rain-data-store-4A', 'data')
)
def update_pie_chart(data):
    df = pd.DataFrame(data)
    fig = px.pie(df, names='Cidade', values='Chuva', title='Chuva no Rio de Janeiro')
    fig = apply_updates(fig)
    return fig

# Função de callback para atualizar o gráfico de linha
@callback(
    Output('rain-graph-2A', 'figure'),
    Input('rain-data-store-4A', 'data')
)
def update_line_chart(data):
    df = pd.DataFrame(data)
    fig = px.line(df, x='Cidade', y='Chuva', title='Chuva no Rio de Janeiro')
    
    fig = apply_updates(fig)
    
    return fig


# Função de callback para atualizar o gráfico de barras
@callback(
    Output('rain-graph-3A', 'figure'),
    Input('rain-data-store-4A', 'data')
)
def update_bar_chart(data):
    precipitacao_alertario = pd.read_csv("dashboard/data/taxa_precipitacao_alertario_2023.csv")
    precipitacao_alertario = precipitacao_alertario.groupby("id_estacao")["acumulado_chuva_15_min"].sum()
    estacoes = pd.read_csv("dashboard/data/estacoes.csv")
    estacoes = dict(zip(estacoes['id_estacao'], estacoes['estacao']))
    precipitacao_alertario = precipitacao_alertario.rename(estacoes)
    precipitacao_alertario = precipitacao_alertario.nlargest(5)
    fig = px.bar(precipitacao_alertario, x= precipitacao_alertario.index, y=precipitacao_alertario.values, title='Acumulados por estação em 2023', color_discrete_sequence=["#0042AB"])

    fig = apply_updates(fig)
    fig.update_layout(
        xaxis=dict(
            tickangle=-20  # Permite que os rótulos do eixo x ajustem automaticamente a margem para ajustar o texto
        )
    )
    fig.update_xaxes(
    title='Estação'
    )
    fig.update_yaxes(
        title='Precipitação (mm)',
        title_font=dict(size=13)
    )
    
    return fig


# Função de callback para atualizar o gráfico
@callback(
    Output('rain-graph-4A', 'figure'),
    Input('rain-data-store-4A', 'data')
)
def update_graph(data):
    df = pd.DataFrame(data)  # Convertendo o dicionário de volta para um DataFrame

    # Criando um gráfico com Plotly Express
    fig = px.bar(df, x='Cidade', y='Chuva', title='Chuva no Rio de Janeiro', color_discrete_sequence=["#0042AB"])

    fig = apply_updates(fig)

    return fig

# Layout do dashboard
layout = html.Div([
    header("Chuva no Rio de Janeiro"),
    
    html.Div([
        create_container_graph('rain-graph-1A', "Gráfico 1"),
        create_container_graph('rain-graph-2A', "Gráfico 2"),
        create_container_graph('rain-graph-3A', "Precipitação por estação"),
        create_container_graph('rain-graph-4A', "Gráfico 4"),
    ], style={'display': 'flex', 'flex-wrap': 'wrap'}),
    
    dcc.Store(id='rain-data-store-4A') 
])
