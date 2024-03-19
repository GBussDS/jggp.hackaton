import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, callback, Output, Input
import dash

from components.header import header

# Registrando a página
dash.register_page(__name__, path="/rain", name="Chuva", svg="icons/rain.svg")

# Função de callback para armazenar o DataFrame
@callback(
    Output('rain-data-store', 'data'),
    Input('rain-data-store', 'id')
)
def store_data(id):
    # Criando um DataFrame do zero
    df = pd.DataFrame({
        'Cidade': ['Flamengo', 'Barra da Tijuca', 'Botafogo', 'Catete', 'Centro'],
        'Chuva': [120, 150, 170, 200, 180]
    })

    return df.to_dict('records')  # Convertendo o DataFrame para um dicionário

# Função de callback para atualizar o gráfico
@callback(
    Output('rain-graph', 'figure'),
    Input('rain-data-store', 'data')
)
def update_graph(data):
    df = pd.DataFrame(data)  # Convertendo o dicionário de volta para um DataFrame

    # Criando um gráfico com Plotly Express
    fig = px.bar(df, x='Cidade', y='Chuva', title='Chuva no Rio de Janeiro', color_discrete_sequence=["#0042AB"])

    # Atualizando as propriedades dos traços
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Chuva: %{y} mm",
        textfont=dict(color="white"),
        insidetextfont=dict(color="white"),
        hoverlabel=dict(font=dict(color="white")),
        marker_line_width=0
    )

    # Atualizando o layout
    fig.update_layout(
        title='',
        plot_bgcolor='rgba(0,0,0,0)',  # fundo transparente
        paper_bgcolor='rgba(0,0,0,0)',  # fundo transparente
        xaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.2)', zeroline=False, title_text=''),
        yaxis=dict(showgrid=True, gridcolor='rgba(200,200,200,0.2)', zeroline=False, title_text=''),
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(font=dict(color="white")),
        font=dict(color="white")
    )

    # Atualizando os eixos x
    fig.update_xaxes(
        showgrid=True, 
        gridcolor='rgba(200,200,200,0.2)', 
        zeroline=False, 
        title_text='',
        nticks=5,
        tickangle=0,
    )

    return fig

# Layout do dashboard
layout = html.Div([
    header("Chuva no Rio de Janeiro"),
    dcc.Graph(id='rain-graph'),
    dcc.Store(id='rain-data-store') 
])
