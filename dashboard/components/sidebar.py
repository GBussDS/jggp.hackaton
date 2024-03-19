import dash
from dash import html
import dash_bootstrap_components as dbc
import dash_dangerously_set_inner_html

def get_css_variables():
    return {
        "color-bg": "#000000",
        "color-bg": "#000000",
        "color-bg": "#000000",
        "color-bg": "#000000",
        "color-bg": "#000000",
        "color-bg": "#000000",
    }


def svg(file_name, style=None):
    file_path = "dashboard/assets" + "/" + file_name
    with open(file_path, "r") as f:
        svg_string = f.read()
    
    if style:
        svg_style = ";".join([f"{k}: {v}" for k, v in style.items()])
        svg_string = svg_string.replace("<svg", f'<svg style="{svg_style}"')
    
    return dash_dangerously_set_inner_html.DangerouslySetInnerHTML(svg_string)


def sidebar():
    default_icon_color = get_css_variables()

    sidebar =  html.Div(
        [
            dbc.Nav(
                [
                    dbc.NavLink(
                        [
                            svg(page["svg"], page.get("svg_style", default_icon_color)),
                        ], 
                        href=page["relative_path"], 
                        active="exact",
                        style={
                            "padding": "0.5rem",
                            "color": "black",
                            "display": "flex",
                        }
                    ) for page in dash.page_registry.values()
                ],
                vertical=True,
                pills=True,
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "gap": "0.5rem",
                }
            ),
        ],
        className="my_sidebar container-style",
        style={
            "padding": "0.1rem",
            "borderRadius": "0 20px 20px 0",
            "backgroundColor": "#000000",
            "width": "75px",
            "marginRight": "10px"
        } 
    )

    return sidebar
