import dash
from dash import html
import dash_bootstrap_components as dbc
import dash_dangerously_set_inner_html

def header(nome, filtro=None, baixar_dados =None, baixar_fig = None):
    header =  html.Div(
        [
            dbc.Nav(
                [
                    html.H1(nome, style={'color': '#fff', 'textTransform': 'Uppercase', 'fontSize': '30px'}),
                    filtro,
                    baixar_dados,
                    baixar_fig
                ],
                style={
                    "display": "flex",
                    "flexDirection": "row",
                    "gap": "0.5rem",
                    'alignItems':'center',
                    'justifyContent':'space-between',
                    'margin':'0 2.5vw',
                    'overflow': 'visible',
                    'zIndex':'999',
                }
            ),
        ],
        className="header",
        style={
            "padding": "0.1rem",
            "borderRadius": "10px",
            "backgroundColor": "#000000",
            "width": "97%",
            "marginRight": "0%",
            "marginTop": "5px",
            'zIndex':'999',
        } 
    )

    return header
