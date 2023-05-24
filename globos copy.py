import dash
from dash import dcc 
from dash import html
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
from collections import OrderedDict
from graficas import *
from graphs import *


app = dash.Dash()

app.layout = html.Div([
    html.H1("Análisis cuantitativo y proyecciones CNSF", style={'textAlign':'center','color':'#162b4e','font-family':'Helvetica'}),
    html.Hr(),
    html.H3("Objetivo del proyecto"),
    html.P("La Comisión Nacional de Seguros y Fianzas se encarga de supervisar las operaciones de las instituciones encargadas de brindar servicios de dicha índole. Este trabajo estará basado en datos reales, de usuarios que han hecho uso de algún tipo de cobertura derivada de siniestros. El enfoque de nuestro proyecto se basa en buscar la relación existente entre el volumen de incidencia por siniestro y el género del asegurado, para ello, realizaremos un análisis usando procesos como la creación de series de tiempo, complementados con la proyección basada en modelos de medias móviles autorregresivas."),
    html.Div(children='Siniestros Data Frame'),
    dash_table.DataTable(data=siniestroscompilados.to_dict('records'),
                         columns=[{'id':c,'name':c} for c in siniestroscompilados.columns],
                          
                         style_header={
                             'backgroundColor': 'rgb(30,30,30)',
                             'color': 'white'
                         },
                           page_size=15),
    html.Hr(),

    html.H3("Representación de Siniestros por Estado"),
    html.P("Al reaizar un conteo de los siniestros por estado, se puede generar un gráfico de frecuencia donde se observa de mayor a menor, los estados con más incidentes a nivel nacional. "),
    dcc.Graph(figure=px.histogram(df_conteoestados, x='Estado', y='Numero de incidentes', histfunc='avg')),

    html.Hr(),

    dcc.Graph(
        id= 'graph_1',
        figure=random_data_castter(),
    ),


    html.Hr(),

        html.H4("Volumen de Siniestros agrupado por Edad, Entidad y Género"),
        html.P("Al hacer un análisis más avanzado de los datos se puede llevar a cabo una rapresentación con más de 4 variables, en este caso se cuenta con la variable EDAD en el eje X, el número de siniestros en el eje Y, el color representará el género, azul para femenino y rojo masulino, por último el tamaño de las figuras será mayor al tener incidencia de siniestros mayor "),
        html.P("Seleccciona la animación:"),
        dcc.RadioItems(
            id="selection",
            options=["Volumen de Siniestros EEG"],
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