from dash import dcc, html

def create_container_graph(graph_id, title):
    return html.Div([
        html.H1(title, style={'textAlign': 'center', 'fontSize': '20px', "color": "#FFFFFF"}),
        dcc.Graph(id=graph_id, style={'width': '90%', 'height': '32vh', 'display': 'block', 'margin': 'auto', 'backgroundColor': '#000000', 'borderRadius': '15px'}),
    ], style={'backgroundColor': '#000000', 'borderRadius': '15px', 'margin': '0.5% 0.5%', 'padding': '20px', 'width': '41vw',}
)
    
def create_large_container_graph(graph_id, title):
    return html.Div([
        html.H1(title, style={'textAlign': 'center', 'fontSize': '20px'}),
        dcc.Graph(id=graph_id, style={'width': '90%', 'height': '75vh', 'display': 'block', 'margin': 'auto', 'backgroundColor': '#000000', 'borderRadius': '15px'}),
    ], style={'backgroundColor': '#000000', 'borderRadius': '15px', 'margin': '0.5% 0.5%', 'padding': '20px', 'height': '87.5vh', 'width': '46vw'}
)