import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
from plotly.figure_factory import create_table
import plotly.offline as py
import plotly.graph_objs as go


##############################################################################################################################################
#### LIMPIEZA BASE DE DATOS SINIESTROS####
siniestros= 'Siniestros.csv'
df_siniestros= pd.read_csv(siniestros, encoding='cp1252', sep=',', on_bad_lines='warn')
siniestros_limpio = df_siniestros.drop(['PLAN DE LA POLIZA','MODALIDAD DE LA POLIZA','VENCIMIENTOS','MONTO DE REASEGURO','CLAVE_INS','MONTO RECLAMADO','MONTO PAGADO'], axis=1)
siniestros_limpio =siniestros_limpio.dropna()
siniestros_limpio['NUMERO DE SINIESTROS'] = pd.to_numeric(siniestros_limpio['NUMERO DE SINIESTROS'], errors='coerce')
siniestroscompilados = siniestros_limpio.groupby(['ENTIDAD', 'CAUSA DEL SINIESTRO','EDAD','SEXO'])['NUMERO DE SINIESTROS'].sum().reset_index()
siniestroscompilados['EDAD'] = pd.to_numeric(siniestroscompilados['EDAD'], errors='coerce')
siniestroscompilados = siniestroscompilados[siniestroscompilados['EDAD'].notnull()]

##############################################################################################################################################
#### DF Siniestros por estados####
conteo_estados =  siniestroscompilados['ENTIDAD'].value_counts()
df_conteoestados = pd.DataFrame(list(conteo_estados.items()), columns=['Estado','Numero de incidentes'])

##############################################################################################################################################
#### BASES DE DATOS SINIESTROS POR MASCULINO Y FEMENINO ####
siniestrosF = siniestroscompilados.loc[siniestroscompilados['SEXO'] == 'Femenino']
siniestrosM = siniestroscompilados.loc[siniestroscompilados['SEXO'] == 'Masculino']

##############################################################################################################################################
#### HEAT MAP POR ESTADOS ####


siniestros_estados = siniestros_limpio.drop(['EDAD','COBERTURA', 'SEXO'], axis=1)
dfsiniestros_estados = pd.DataFrame(siniestros_estados)

conteo_estados =  siniestros_estados['ENTIDAD'].value_counts()

df_conteoestados = pd.DataFrame(list(conteo_estados.items()), columns=['Estado','Numero de incidentes'])
df_conteoestados.drop(32, inplace=True)
df_conteoestados.drop(33, inplace=True)
df_conteoestados.drop(34, inplace=True)

df_conteoestados.loc[0, 'Estado'] = 'Ciudad de México'
df_conteoestados.loc[1, 'Estado'] = 'México'
df_conteoestados.loc[5, 'Estado'] = 'Nuevo León'
df_conteoestados.loc[14, 'Estado'] = 'Michoacán'
df_conteoestados.loc[18, 'Estado'] = 'San Luis Potosí'
df_conteoestados.loc[22, 'Estado'] = 'Querétaro'
df_conteoestados.loc[23, 'Estado'] = 'Yucatán'
df_conteoestados.loc[0, 'Estado'] = 'Ciudad de México'


import requests
import plotly.express as px

def heat_map_estados():
    repo_url = 'https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json' #Archivo GeoJSON
    mx_regions_geo = requests.get(repo_url).json()

    fig = px.choropleth(data_frame=df_conteoestados, 
                        geojson=mx_regions_geo, 
                        locations='Estado', # nombre de la columna del Dataframe
                        featureidkey='properties.name',  # ruta al campo del archivo GeoJSON con el que se hará la relación (nombre de los estados)
                        color='Numero de incidentes', #El color depende de las cantidades
                        color_continuous_scale="burg", #greens
                    )
    fig.update_geos(showcountries=True, showcoastlines=True, showland=True, fitbounds="locations")

    fig.update_layout(
        title_text = 'Numero de Siniestros por Estado',
        font=dict(
            #family="Courier New, monospace",
            family="Ubuntu",
            size=18,
            color="#7f7f7f"
        ),
        annotations = [dict(
            x=0.55,
            y=-0.1,
            xref='paper',
            yref='paper',
            text='Fuente: "CNSF"',
            showarrow = False
        )]
    )

    return fig.show()

    
###############################################################################################################################################
#Log Scale on x-axis

tablasiniestros= create_table(siniestroscompilados.head(10))
tablasiniestros1= py.iplot(tablasiniestros)
