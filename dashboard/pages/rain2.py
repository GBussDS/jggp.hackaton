import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, callback, Output, Input
import dash

from components.header import header
from components.apply import apply_updates
from components.container import create_container_graph

# Registrando a página
dash.register_page(__name__, path="/rain2", name="Chuva2")

# Função de callback para armazenar o DataFrame
@callback(
    Output('alagamento', 'data'),
    Input('alagamento', 'id')
)
def store_data(id):
    # Criando um DataFrame do zero
    df = pd.read_csv("dashboard/data/ponto_supervisionado_alagamento.csv")

    # Faça a consulta SQL
    # query = """
    # SELECT * FROM `rj-rioaguas.saneamento_drenagem.ponto_supervisionado_alagamento`
    # """
    # query_job = client.query(query)

    # df_alertario = query_job.to_dataframe()

    frequencia = dict(df.value_counts(df["bairro"])) # Convertendo o DataFrame para um dicionário

    filtered_dict = {k: v for k, v in frequencia.items() if v >= 5}

    return filtered_dict  

# Função de callback para atualizar o gráfico de pizza
@callback(
    Output('rain-graph-1B', 'figure'),
    Input('alagamento', 'data')
)
def update_column_graph(data):
    
    locations = list(data.keys())
    values = list(data.values())

    # Create a bar chart
    fig = px.bar(x=locations, y=values, title="Sales by Location")

    fig = apply_updates(fig)
    return fig

# Função de callback para atualizar o gráfico de linha
@callback(
    Output('rain-graph-2B', 'figure'),
    Input('alagamento', 'data')
)
def update_line_chart(data):
    df = pd.DataFrame(data)
    fig = px.line(df, x='Cidade', y='Chuva', title='Chuva no Rio de Janeiro')
    
    fig = apply_updates(fig)
    
    return fig

# Função de callback para atualizar o gráfico de barras
@callback(
    Output('rain-graph-3B', 'figure'),
    Input('alagamento', 'data')
)
def update_bar_chart(data):
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Cidade', y='Chuva', title='Chuva no Rio de Janeiro', color_discrete_sequence=["#0042AB"])
    
    fig = apply_updates(fig)
    
    return fig


# Função de callback para atualizar o gráfico
@callback(
    Output('rain-graph-4B', 'figure'),
    Input('alagamento', 'data')
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
        create_container_graph('rain-graph-1B', "Gráfico 1"),
        create_container_graph('rain-graph-2B', "Gráfico 2"),
        create_container_graph('rain-graph-3B', "Gráfico 3"),
        create_container_graph('rain-graph-4B', "Gráfico 4"),
    ], style={'display': 'flex', 'flex-wrap': 'wrap'}),
    
    dcc.Store(id='alagamento') 
],
)