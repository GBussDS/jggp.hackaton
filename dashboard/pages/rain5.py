import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, callback, Output, Input
import dash

from components.header import header
from components.apply import apply_updates
from components.container import create_container_graph

# Registrando a página
dash.register_page(__name__, path="/rain5", name="Chuva5")

# Função de callback para armazenar o DataFrame
@callback(
    Output('rain-data-store-4E', 'data'),
    Input('rain-data-store-4E', 'id')
)
def store_data(id):
    # Criando um DataFrame do zero
    df = pd.DataFrame({
        'Cidade': ['Flamengo', 'Barra da Tijuca', 'Botafogo', 'Catete', 'Centro'],
        'Chuva': [120, 150, 170, 200, 180]
    })

    return df.to_dict('records')  # Convertendo o DataFrame para um dicionário

# Função de callback para atualizar o gráfico de pizza
@callback(
    Output('rain-graph-1E', 'figure'),
    Input('rain-data-store-4E', 'data')
)
def update_pie_chart(data):
    df = pd.DataFrame(data)
    fig = px.pie(df, names='Cidade', values='Chuva', title='Chuva no Rio de Janeiro')
    fig = apply_updates(fig)
    return fig

# Função de callback para atualizar o gráfico de linha
@callback(
    Output('rain-graph-2E', 'figure'),
    Input('rain-data-store-4E', 'data')
)
def update_line_chart(data):
    df = pd.DataFrame(data)
    fig = px.line(df, x='Cidade', y='Chuva', title='Chuva no Rio de Janeiro')
    
    fig = apply_updates(fig)
    
    return fig

# Função de callback para atualizar o gráfico de barras
@callback(
    Output('rain-graph-3E', 'figure'),
    Input('rain-data-store-4E', 'data')
)
def update_bar_chart(data):
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Cidade', y='Chuva', title='Chuva no Rio de Janeiro', color_discrete_sequence=["#0042AB"])
    
    fig = apply_updates(fig)
    
    return fig


# Função de callback para atualizar o gráfico
@callback(
    Output('rain-graph-4E', 'figure'),
    Input('rain-data-store-4E', 'data')
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
        create_container_graph('rain-graph-1E', "Gráfico 1"),
        create_container_graph('rain-graph-2E', "Gráfico 2"),
        create_container_graph('rain-graph-3E', "Gráfico 3"),
        create_container_graph('rain-graph-4E', "Gráfico 4"),
    ], style={'display': 'flex', 'flex-wrap': 'wrap'}),
    
    dcc.Store(id='rain-data-store-4E') 
],
)
