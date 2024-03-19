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
    Output('rain-data-store-4', 'data'),
    Input('rain-data-store-4', 'id')
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
    Output('rain-graph-1', 'figure'),
    Input('rain-data-store-4', 'data')
)
def update_pie_chart(data):
    df = pd.DataFrame(data)
    fig = px.pie(df, names='Cidade', values='Chuva', title='Chuva no Rio de Janeiro')
    fig = apply_updates(fig)
    return fig

# Função de callback para atualizar o gráfico de linha
@callback(
    Output('rain-graph-2', 'figure'),
    Input('rain-data-store-4', 'data')
)
def update_line_chart(data):
    df = pd.DataFrame(data)
    fig = px.line(df, x='Cidade', y='Chuva', title='Chuva no Rio de Janeiro')
    
    fig = apply_updates(fig)
    
    return fig

# Função de callback para atualizar o gráfico de barras
@callback(
    Output('rain-graph-3', 'figure'),
    Input('rain-data-store-4', 'data')
)
def update_bar_chart(data):
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Cidade', y='Chuva', title='Chuva no Rio de Janeiro', color_discrete_sequence=["#0042AB"])
    
    fig = apply_updates(fig)
    
    return fig


# Função de callback para atualizar o gráfico
@callback(
    Output('rain-graph-4', 'figure'),
    Input('rain-data-store-4', 'data')
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
    
    # Div superior com dois gráficos
    html.Div([
        dcc.Graph(id='rain-graph-1', style={'width': '46%', 'height': '40vh', 'display': 'inline-block', 'backgroundColor': '#000000', 'borderRadius': '15px', 'margin': '1% 2%'}),
        dcc.Graph(id='rain-graph-2', style={'width': '46%', 'height': '40vh', 'display': 'inline-block', 'backgroundColor': '#000000', 'borderRadius': '15px', 'margin': '1% 2%'}),
    ]),
    
    # Div inferior com dois gráficos
    html.Div([
        dcc.Graph(id='rain-graph-3', style={'width': '46%', 'height': '40vh', 'display': 'inline-block', 'backgroundColor': '#000000', 'borderRadius': '15px', 'margin': '1% 2%'}),
        dcc.Graph(id='rain-graph-4', style={'width': '46%', 'height': '40vh', 'display': 'inline-block', 'backgroundColor': '#000000', 'borderRadius': '15px', 'margin': '1% 2%'}),
    ]),
    
    dcc.Store(id='rain-data-store-4') 
],)

