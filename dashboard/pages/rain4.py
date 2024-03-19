import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, callback, Output, Input
import dash

from components.header import header

dash.register_page(__name__, path="/rain4", name="Chuva4", svg="icons/rain.svg")

# Função de callback para armazenar o DataFrame
@callback(
    Output('data-store4', 'data'),
    Input('data-store4', 'id')
)
def store_data(id):
    # Criando um DataFrame do zero
    df = pd.DataFrame({
        'Categoria': ['A', 'B', 'B', 'A', 'C', 'C', 'C', 'B', 'A', 'A'],
        'Valor': [10, 15, 7, 14, 10, 10, 7, 10, 11, 15]
    })

    # Limpeza básica e filtragem
    df = df[df['Valor'] > 10]  # Filtrando linhas onde Valor é maior que 10

    return df.to_dict('records')  # Convertendo o DataFrame para um dicionário

# Função de callback para atualizar o gráfico
@callback(
    Output('exemplo-grafico4', 'figure'),
    Input('data-store4', 'data')
)
def update_graph(data):
    df = pd.DataFrame(data)  # Convertendo o dicionário de volta para um DataFrame
    # Criando um gráfico com Plotly Express
    fig = px.bar(df, x='Categoria', y='Valor', title='Gráfico de Barras Simples')
    return fig

# Layout do dashboard
layout = html.Div([
    header("Header 4"),
    dcc.Graph(id='exemplo-grafico'),
    dcc.Store(id='data-store') 
])

