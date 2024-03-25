# from dash import dcc, html, Dash, callback, Output, Input, dash
# import pandas as pd
# import dash
# from components.header import header
# from pages.bairros import store_map_data

# # Registrando a página
# dash.register_page(__name__, path="/downloads", name="Downloads")

# #bairros
# @callback(
#     Output("download-dataframe-mapa", "data"),
#     [Input("btn_mapa", "n_clicks")],
#     prevent_initial_call=True
# )
# def download_dados_mapa(n_clicks):
#     gdf_dict, df_chuva_dict, df_estacoes_dict = store_map_data("id")
#     if n_clicks:
#         df_bairros = pd.DataFrame(gdf_dict)
#         df_chuva = pd.DataFrame(df_chuva_dict)
#         df_estacoes = pd.DataFrame(df_estacoes_dict)
#         return dcc.send_data_frame(df_bairros.to_excel, "bairros.xlsx", index=False), dcc.send_data_frame(df_chuva.to_excel, "chuva.xlsx", index=False), dcc.send_data_frame(df_estacoes.to_excel, "estacoes_websirene.xlsx", index=False)

# @callback(
#     Output("download-dataframe-xlsx", "data"),
#     [Input("btn_mapa", "n_clicks")],
#     prevent_initial_call=True
# )
# def download_dados_mapa(n_clicks):
    
#     if n_clicks:
#         df = pd.DataFrame(gdf_dict)
#         return dcc.send_data_frame(df.to_excel, "bairros.xlsx", index=False)
    

# # Layout do dashboard
# layout = html.Div([
#     header("Downloads"),
#     html.Div([
#         html.Button("Download Dados Mapa", id="btn_mapa"),
#         dcc.Download(id="download-dataframe-mapa"),
#     ]),
#     html.Div([], style={'display': 'flex', 'paddingRight': '5%'}),
# ])
