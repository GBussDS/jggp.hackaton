import dash
from dash import html
import dash_bootstrap_components as dbc

def sidebar():
    sidebar =  html.Div(
        [
            html.Img(src='/assets/logo-prefeitura.png', style={'width':'80%'}),
            dbc.Nav(
                [
                    dbc.NavLink(
                        [
                            html.H1(page["name"], className="navbar-title")
                        ], 
                        href=page["relative_path"], 
                        active="exact"
                    ) for page in dash.page_registry.values()
                ],
                vertical=True,
                pills=True
            ),
        ],
        className="my_sidebar"
    )

    return sidebar
