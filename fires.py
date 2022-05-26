import pandas as pd
import numpy as np
import plotly.express as px
import plotly
from dash import Dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
from datetime import date

df = pd.read_csv("greek_fires_data.csv") #read dataset from a csv.
df = df[["latitude","longitude","brightness","bright_t31","frp","acq_date"]]
df['acq_date'] = pd.to_datetime(df['acq_date'])
df['year'] = df['acq_date'].dt.year #keep on the year

#################### Creating App Object ############################               
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(name = __name__,external_stylesheets=external_stylesheets)
server = app.server

#Create a rangeslider

rangeslider = dcc.RangeSlider(
        id = "my-range-slider",
        min = 2000,
        max = 2021,
        value = [2005,2015],
        step = 1,
        marks = {
            2001:"2001",
            2002:"2002",
            2003:"2003",
            2004:"2004",
            2005:"2005",
            2006:"2006",
            2007:"2007",
            2008:"2008",
            2009:"2009",
            2010:"2010",
            2011:"2011",
            2012:"2012",
            2013:"2013",
            2014:"2014",
            2015:"2015",
            2016:"2016",
            2017:"2017",
            2018:"2018",
            2019:"2019",
            2020:"2020",
            2021:"2021",
        })

# Create a Radio Selector for the type of data we will be using
radio = dcc.RadioItems( ['frp', 'brightness','bright_t31'],'frp',
                    id = "heat-filter")

#app layout and calback function Range Slider and Radio Selector

app.layout = html.Div(children=[
    
    html.H1(children='Fires in Greece 2000-2021 from Satellite Data'),
    
    html.P(["made by ", html.A("Dimitrios Vogias", href ="https://www.linkedin.com/in/dimitrisvogias/")]),
    
    html.Br(),
    
    html.P(["This is my first attempt to create a Dashboard by using Plotly Dash. The data used is from Kaggle.com and ", html.A("Baris Dincer", href ="https://www.kaggle.com/datasets/brsdincer/2000-2021-tunisiaisraelgreeceitaly-nasa")]),           
           
    html.Br(),
    
    html.P("This Dashboard comes with three selections about the brightness data that you could like to create a map with."),
    html.P("FRP is the Fire Radiative Power (MW - megawatts). It depicts the pixel-integrated fire radiative power in MW (megawatts)"),
    html.P("The Brightness selection is the brightness temperature of the fire pixel measured in Kelvin."),
    html.P("The Bright_T31 Brightness is the Channel 31 brightness temperature of the fire pixel measured in Kelvin."),
    html.Br(),
    
    html.Label("Choose a feature:"),
    
    radio,
    
    html.Br(),
    
    html.Label("Choose a range of years by using the Range Slider:"),
       
    rangeslider,
    
    dcc.Graph(id='graph',figure={}),
  
])

@app.callback(Output("graph", "figure"),[Input("my-range-slider","value"), Input("heat-filter","value")])

def update_graph(option1, option2):

    dff = df.copy()
    dff = dff[(dff["year"] >= option1[0]) & (dff["year"] <= option1[1])]
    
    heat = px.density_mapbox(dff, lat='latitude', lon='longitude', z=option2, radius=10,
                        center=dict(lat=38, lon=23), zoom=5.1,
                        mapbox_style="stamen-terrain",height = 700)

    return heat

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)