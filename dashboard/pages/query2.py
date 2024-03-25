import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, callback, Output, Input
import dash
from google.cloud import bigquery

from components.header import header
from components.apply import apply_updates
from components.container import create_large_container_graph

from data.data_query import df_ocorrencias

dash.register_page(__name__, path="/query2", name="Ocorrencias")

# Passa dados
@callback(
    Output('ocorrencias-data-store', 'data'),
    Input('ocorrencias-data-store', 'id')
)
def store_ocorrencias_data(id):
    df = df_ocorrencias

    return df.to_dict('records')  

# Faz o Gráfico
@callback(
    Output('ocorrencias-graph', 'figure'),
    Input('ocorrencias-data-store', 'data')
)
def update_ocorrencias_chart(data):
    df = pd.DataFrame(data)
    id_pop_list = ["32", "35", "28", "31", "6", "16", "33", "5"]
    df = df[df['id_pop'].isin(id_pop_list)] # Filtra pelos que importa
    df_grouped = df.groupby(['bairro', 'gravidade']).size().reset_index(name='count') # Agrupa os dados por bairro e gravidade
    
    # Crie o gráfico de barras
    fig = px.bar(df_grouped, x='bairro', y='count', 
                 color='gravidade', 
                 title='Número de ocorrências por bairro', 
                 color_discrete_sequence=["#0042AB"])
    
    fig = apply_updates(fig)
    return fig


# Defina o layout do aplicativo
layout = html.Div([
    header("Chuva no Rio de Janeiro"),
    
    html.Div([
        create_large_container_graph('ocorrencias-graph', "Gráfico de Ocorrências"),
    ], style={'display': 'flex', 'paddingRight': '5%'}),
    
    dcc.Store(id='ocorrencias-data-store'),
    dcc.Store(id='procedimento-data-store'),
])