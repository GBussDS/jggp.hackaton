import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, callback, Output, Input
import dash

from components.header import header

# Registrando a página
dash.register_page(__name__, path="/rain", name="Chuva", svg="icons/rain.svg")

# Função de callback para armazenar o DataFrame
@callback(
    Output('data-store', 'data'),
    Input('data-store', 'id')
)
def store_data(id):
    # Criando um DataFrame do zero
    df = pd.DataFrame({
        'Categoria': ['A', 'B', 'B', 'A', 'C', 'C', 'C', 'B', 'A', 'A'],
        'Valor': [10, 15, 7, 10, 10, 15, 7, 10, 10, 15]
    })

    # Limpeza básica e filtragem
    df = df[df['Valor'] > 10]  # Filtrando linhas onde Valor é maior que 10

    return df.to_dict('records')  # Convertendo o DataFrame para um dicionário

# Função de callback para atualizar o gráfico
@callback(
    Output('exemplo-grafico', 'figure'),
    Input('data-store', 'data')
)
def update_graph(data):
    df = pd.DataFrame(data)  # Convertendo o dicionário de volta para um DataFrame

    # Criando um gráfico com Plotly Express
    fig = px.bar(df, x='Categoria', y='Valor', title='Gráfico de Barras Simples', color_discrete_sequence=["#0042AB"])

    # Atualizando as propriedades dos traços
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Quantidade: %{y} un.",
        textfont=dict(color="white"),  # Atualiza a cor do texto das fatias
        insidetextfont=dict(color="white"),  # Atualiza a cor do texto dentro das fatias
        hoverlabel=dict(font=dict(color="white")),  # Atualiza a cor do texto do hover
        marker_line_width=0
    )

    # Atualizando o layout
    fig.update_layout(
        title='',
        plot_bgcolor='rgba(0,0,0,0)',  # fundo transparente
        paper_bgcolor='rgba(0,0,0,0)',  # fundo transparente
        xaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.2)', zeroline=False, title_text=''), # grades suaves e sem título
        yaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.2)', zeroline=False, title_text=''), # grades suaves e sem título
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(font=dict(color="white")),  # Atualiza a cor do texto da legenda
        font=dict(color="white")  # Atualiza a cor do texto do título e dos eixos
    )

    # Atualizando os eixos x
    fig.update_xaxes(
        tickformat="%b", # formata os rótulos para exibir apenas o nome do mês
        showgrid=True, 
        gridcolor='rgba(200,200,200,0.2)', 
        zeroline=False, 
        title_text='', # remove o título do eixo x
        nticks=5,
        tickangle=0,
    )

    return fig


# Layout do dashboard
layout = html.Div([
    header("Header 1"),
    dcc.Graph(id='exemplo-grafico'),
    dcc.Store(id='data-store') 
])

