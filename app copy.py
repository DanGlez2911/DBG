import dash
from dash import dcc 
from dash import html
from graphs import *
from graficas import *

app = dash.Dash()

app.layout = html.Div([
    html.H1("Dashboard 1", style={'textAlign':'center','color':'#600dd4','font-family':'Helvetica'}),
    html.Hr(),
    html.H3("Siniestros"),
    html.P("Esta base de datos contiene información "),
    dcc.Graph(
        id= 'graph_1',
        figure=random_data_castter(),
    ),
    dcc.Graph(
        id= 'graph_2',
        figure=heat_map_estados(),
    ),
    html.Table([
        html.Tr([
            html.Th("Company"),
            html.Th("Contact"),
            html.Th("Country")
        ]),
        html.Tr([
            html.Td("BBVA"),
            html.Td("Bruno Rodrigo Haro Aupart"),
            html.Td("Yemen")
        ]),
        html.Tr([
            html.Td("Coca-Cola"),
            html.Td("Sebastian Rodriguez Flores"),
            html.Td("Sudáfrica")
        ])
    ]),
    html.H5("Cosas que le gustan a Sebastian"),
    html.Ul([
        html.Li("Coca"),
        html.Li("Coca"),
        html.Li("Coca")
    ]),
    html.H5("Cosas que le gustan a Bruno"),
    html.Ol([
        html.Li("Pepsi"),
        html.Li("Pepsi"),
        html.Li("Pepsi")
    ]),
    ])

if __name__ == '__main__':
    app.run_server()