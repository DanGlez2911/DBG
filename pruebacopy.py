import dash
from dash import dcc 
from dash import html
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
from graficascopy import *

app = dash.Dash()



app.layout = html.Div([
    html.H1("Dashboard 1", style={'textAlign':'center','color':'#600dd4','font-family':'Helvetica'}),
    html.Hr(),
    html.H3("Siniestros"),
    html.P("Esta base de datos contiene información "),
    html.Div(children='Siniestros Data Frame'),
    dash_table.DataTable(data=siniestroscompilados.to_dict('records'), page_size=10),
    html.Hr(),
    
        html.H4("Animated GDP and population over decades"),
        html.P("Select an animation:"),
        dcc.RadioItems(
            id="selection",
            options=["GDP - Scatter", "Population - Bar"],
            value="GDP - Scatter",
        ),
        dcc.Loading(dcc.Graph(id="graph"), type="cube"),

    
    ]
)


@app.callback(
    Output("graph", "figure"), Input("selection", "value")
)
def display_animated_graph(selection):
    animations = {
        "GDP - Scatter": px.scatter(
            siniestroscompilados,
            x="EDAD",
            y="NUMERO DE SINIESTROS",
            animation_group="ENTIDAD",
            size="NUMERO DE SINIESTROS",
            color="SEXO",
            hover_name="ENTIDAD",
        )
    }
    return animations[selection] 


if __name__ == '__main__':
    app.run_server()