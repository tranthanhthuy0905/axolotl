import pandas as pd                       #to perform data manipulation and analysis
import numpy as np                        #to cleanse data
from datetime import datetime             #to manipulate dates
import plotly.express as px               #to create interactive charts
import plotly.graph_objects as go         #to create interactive charts
from dash import dcc        #to get components for interactive user interfaces
from dash import html       #to compose the dash layout using Python structures
# import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import datetime
from dash import dash_table
import json
import calendar
import dash

app = dash.Dash(__name__)
server = app.server

def display_map(location_database):
    px.set_mapbox_access_token('pk.eyJ1IjoibGFtbGVvMDMwOCIsImEiOiJja3Z5bmlxMm85YXJ6MzBxcG82cm5ndTZjIn0.dKy0r5isHevflHEBb5REyQ')

    fig = px.scatter_mapbox(
        location_database,
        lat=location_database.lat,
        lon=location_database.lon,
        hover_name = "location",
        zoom=4,
        mapbox_style = 'mapbox://styles/mapbox/streets-v11'
    )

    fig.update_layout(height=int(800))
    return fig

location_database = pd.read_csv('https://raw.githubusercontent.com/tranthanhthuy0905/data_file/main/data_file.csv', sep=",")

# Build App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app.layout = html.Div([
    html.Div([
        html.H2(f"Hotline"),
                    
        dcc.Graph(figure=display_map(location_database))

    ]),
    
])

app.run_server()
