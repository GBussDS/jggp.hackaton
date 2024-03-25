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
dash.register_page(__name__, path="/alagamentos", name="Alagamentos")

# Crie uma instância do cliente BigQuery
client = bigquery.Client(project='hackaton-fgv-guris')

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
    # df = query_job.to_dataframe()

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


df_alagamentos_por_dia = df_ocorrencias[df_ocorrencias["id_pop"].isin(["32", "31", "6"])]
df_alagamentos_por_dia = df_alagamentos_por_dia.groupby("data_particao").size()

df_alagamentos_por_dia.index = pd.to_datetime(df_alagamentos_por_dia.index)
df = df_alagamentos_por_dia.reset_index()
df.rename(columns={0: 'ocorrencias'}, inplace=True)
df['ano'] = df['data_particao'].dt.year

dfs.append(df)

# # Função de callback para atualizar o gráfico de barras
# @callback(
#     Output('rain-graph-3B', 'figure'),
#     Input('alagamento', 'data')
# )
# def update_bar_chart(data):
#     # df = pd.DataFrame(data)

#     fig = px.bar(data_clean, x=data_clean["mes_ano"], y=data_clean["soma_acumulado_chuva_24_h"], title='Taxas de precipitação', color_discrete_sequence=["#0042AB"])
    
#     fig = apply_updates(fig)
#     fig.update_layout(xaxis=dict(range=[data_clean["mes_ano"].min(), data_clean["mes_ano"].max()]))
    

#     return fig

data_clean = df_precipitacao_alertario_mensal.drop(df_precipitacao_alertario_mensal['mes_ano'].idxmax())
dfs.append(data_clean)

# Função de callback para atualizar os gráficos com base no filtro selecionado
@callback(
    Output('rain-graph-2B', 'figure'),
    Input('filtro-ano', 'value')
)
def update_graphs(selected_years):
    filtered_df_1 = df[(df["ano"] > selected_years[0]) & (df["ano"] < selected_years[1])]

    fig1 = px.line(filtered_df_1, x="data_particao", y="ocorrencias")
    fig1 = apply_updates(fig1)
    return fig1

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
                html.H1("Casos de Alagamento por Bairro", style={'textAlign': 'center', 'fontSize': '20px', "color": "#FFFFFF"}),
                dcc.Graph(id='rain-graph-1B', style={'width': '90%', 'height': '75vh', 'display': 'block', 'margin': 'auto', 'backgroundColor': '#000000', 'borderRadius': '15px'}),
    ], style={'backgroundColor': '#000000', 'borderRadius': '15px', 'margin': '0.5% 0.5%', 'padding': '20px', 'height': '87.5vh', 'width': '46vw'}),
        html.Div([
                html.H1("Número de eventos de enchente/inundação", style={'textAlign': 'center', 'fontSize': '20px', "color": "#FFFFFF"}),
                dcc.Graph(id='rain-graph-2B', style={'width': '90%', 'height': '75vh', 'display': 'block', 'margin': 'auto', 'backgroundColor': '#000000', 'borderRadius': '15px'}),
    ], style={'backgroundColor': '#000000', 'borderRadius': '15px', 'margin': '0.5% 0.5%', 'padding': '20px', 'height': '87.5vh', 'width': '46vw'}),
    ], style={'display': 'flex','flexDirection': 'row', 'flex-direction': 'row'}),
    
    dcc.Store(id='alagamento') 
],
)