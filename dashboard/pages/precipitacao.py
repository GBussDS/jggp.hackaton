import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, callback, Output, Input
import dash

from components.header import header
from components.apply import apply_updates
from components.container import create_container_graph

from google.cloud import bigquery

from data.data_query import df_ocorrencias, df_precipitacao_alertario_mensal

dfs = []

# Registrando a página
dash.register_page(__name__, path="/precipitacao", name="Precipitação")

# Crie uma instância do cliente BigQuery
client = bigquery.Client(project='hackaton-fgv-guris')

data_clean = df_precipitacao_alertario_mensal.drop(df_precipitacao_alertario_mensal['mes_ano'].idxmax())
dfs.append(data_clean)

# Função de callback para atualizar os gráficos com base no filtro selecionado
@callback(
    [Output('rain-graph-3B', 'figure')],
    [Input('filtro-ano', 'value')]
)
def update_graphs(selected_years):

    filtered_df_2 = data_clean[(data_clean["ano"] > selected_years[0]) & (data_clean["ano"] < selected_years[1])]
    fig2 = px.bar(filtered_df_2, x="mes_ano", y="soma_acumulado_chuva_24_h", title='Taxas de precipitação', color_discrete_sequence=["#0042AB"])
    fig2.update_layout(xaxis=dict(range=[filtered_df_2["mes_ano"].min(), filtered_df_2["mes_ano"].max()]),
                       height = 400)
    return fig2

# Layout do dashboard
layout = html.Div([
    header("Chuva no Rio de Janeiro"),

    dcc.RangeSlider(
        id='filtro-ano',
        min=1997,
        max=2024,
        marks={ano: str(ano) for ano in range(1997, 2025)},
        value=[1997,2024],
        step=1
    ),
    
    html.Div([
        html.Div([
                html.H1("Taxas de precipitação", style={'textAlign': 'center', 'fontSize': '20px'}),
                dcc.Graph(id='rain-graph-3B', style={'width': '90%', 'height': '75vh', 'display': 'block', 'margin': 'auto', 'backgroundColor': '#000000', 'borderRadius': '15px'}),
    ], style={'backgroundColor': '#000000', 'borderRadius': '15px', 'margin': '0.5% 0.5%', 'padding': '20px', 'height': '87.5vh', 'width': '92vw'}),
    ], style={'display': 'flex', 'flex-wrap': 'wrap'}),
    
    dcc.Store(id='alagamento2') 
],
)