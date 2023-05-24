import plotly.graph_objects as go
import numpy as np

def random_data_castter():
    np.random.seed(42)
    random_x=np.random.randint(0,101,100)
    random_y=np.random.randint(0,101,100)

    data= [go.Scatter(x=random_x,y=random_y,mode='markers', name='Random Data')]
    layout=go.Layout(title='My Graph on Dash')
    return go.Figure(data=data,layout=layout)

