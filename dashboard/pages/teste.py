import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import pysal as ps
from shapely.wkt import loads
# from pysal.contrib.viz import mapping as maps
import plotly.express as px

# # Load the data
# df = pd.read_csv('dashboard/data/bairros.csv')
# new_df = pd.DataFrame({'nome':df['nome'],'geometry': df['geometry_wkt']})
# new_df['geometry'] = new_df['geometry'].apply(loads)
# gdf = gpd.GeoDataFrame(new_df, geometry='geometry')

# # Convert the GeoDataFrame to a DataFrame for Plotly
# # df = pd.DataFrame(gdf)

# # Create the figure
# fig = px.choropleth(df, geojson=df['geometry'], locations=df.index, color='nome')

# # Add hover data
# fig.update_traces(hovertemplate='Nome: %{z}')

# # Show the figure
# fig.show()

# import folium
# import geopandas as gpd
# import pandas as pd
# from shapely.wkt import loads

# df = pd.read_csv('dashboard/data/bairros.csv')
# new_df = pd.DataFrame({'nome':df['nome'],'geometry': df['geometry_wkt']})
# new_df['geometry'] = new_df['geometry'].apply(loads)
# gdf = gpd.GeoDataFrame(new_df, geometry='geometry')

# # Create a map centered around the center of your GeoDataFrame
# m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=13)

# # Add each polygon to the map
# for _, r in gdf.iterrows():
#     # Create a string of the form 'POLYGON ((x1 y1, x2 y2, ...))'
#     sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
#     geo_j = sim_geo.to_json()
#     geo_j = folium.GeoJson(data=geo_j,
#                            style_function=lambda x: {'fillColor': 'orange'})
#     folium.Popup(r['nome']).add_to(geo_j)
#     geo_j.add_to(m)

# # Display the map
# m.save('map.html')



# df = pd.read_csv('dashboard/data/bairros.csv')
# new_df = pd.DataFrame({'nome':df['nome'],'geometry': df['geometry_wkt']})
# new_df['geometry'] = new_df['geometry'].apply(loads)
# gdf = gpd.GeoDataFrame(new_df, geometry='geometry')

# # gdf.to_file("bairros.shp")
# #https://darribas.org/gds15/content/labs/lab_03.html
# # lsoas = gpd.read_file('dashboard/data/bairros.shp')

# # Criar a figura e os eixos
# f, ax = plt.subplots(1, figsize=(12, 12))

# # Plotar o GeoDataFrame, usando a coluna 'nome' para colorir os polígonos
# ax = gdf.plot(column='nome', cmap='Set3', linewidth=0.8, ax=ax, edgecolor='0.8')

# plt.show()

# import plotly.graph_objects as go
# import geopandas as gpd
# import plotly.express as px
# import pandas as pd
# from shapely.wkt import loads

# df = pd.read_csv('dashboard/data/bairros.csv')
# new_df = pd.DataFrame({'nome':df['nome'],'geometry': df['geometry_wkt']})
# new_df['geometry'] = new_df['geometry'].apply(loads)
# gdf = gpd.GeoDataFrame(new_df, geometry='geometry')

# # Convert the GeoDataFrame to a GeoJSON format that Plotly can understand
# geojson = gdf.geometry.__geo_interface__

# fig = px.choropleth(gdf, geojson=gdf.geometry, 
#                     locations=gdf.index, 
#                     color='nome',
#                     projection="mercator")
# fig.update_geos(showcountries=False, showcoastlines=True, showland=True, fitbounds="locations")

# fig.show()

import dash
import dash_html_components as html
import folium
import geopandas as gpd
import pandas as pd
from shapely.wkt import loads

df = pd.read_csv('dashboard/data/bairros.csv')
new_df = pd.DataFrame({'nome':df['nome'],'geometry': df['geometry_wkt']})
new_df['geometry'] = new_df['geometry'].apply(loads)
gdf = gpd.GeoDataFrame(new_df, geometry='geometry')

# Create a map centered around the center of your GeoDataFrame
m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=13)

# Add each polygon to the map
for _, r in gdf.iterrows():
    sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data=geo_j,
                           style_function=lambda x: {'fillColor': 'orange'})
    folium.Popup(r['nome']).add_to(geo_j)
    geo_j.add_to(m)

# Save the map to an HTML file
m.save('map.html')

# Create a Dash app
app = dash.Dash(__name__)

# Add the HTML file to the Dash app layout
app.layout = html.Div([
    html.Iframe(srcDoc=open('map.html', 'r').read(), width='100%', height='600')
])

if __name__ == '__main__':
    app.run_server(debug=True)
