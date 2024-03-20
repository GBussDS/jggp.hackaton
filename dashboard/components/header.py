import dash
from dash import html
import dash_bootstrap_components as dbc
import dash_dangerously_set_inner_html

def header(nome):
    header =  html.Div(
        [
            dbc.Nav(
                [
                    html.H1(nome, style={'color': '#fff', 'textTransform': 'Uppercase', 'fontSize': '30px'}),
                    html.H1("filtro", style={'color': '#fff', 'textTransform': 'Uppercase', 'fontSize': '30px'}),
                    html.H1("filtro", style={'color': '#fff', 'textTransform': 'Uppercase', 'fontSize': '30px'}),
                ],
                style={
                    "display": "flex",
                    "flexDirection": "row",
                    "gap": "0.5rem",
                    'alignItems':'center',
                    'justifyContent':'space-between',
                    'margin':'0 2.5vw',
                }
            ),
        ],
        className="header container-style",
        style={
            "padding": "0.1rem",
            "borderRadius": "10px",
            "backgroundColor": "#000000",
            "width": "92vw",
            "height": "60px",
            "marginRight": "10px",
            "marginTop": "5px",
            'alignItems':'center',
            'justifyContent':'center',
        } 
    )

    return header
