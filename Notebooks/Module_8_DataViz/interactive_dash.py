import pandas as pd
import numpy as np
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

df = airline_data.sample(n=500, random_state=42)

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('Airline Performance Dashboard', style={'text_align':'center','color':'black','font_size':40}),
                                html.Div(['Input Year: ', dcc.Input(id='input',value='2010',type='number', style={'height':'50px','font_size':35})], style={'font-size': 40}),
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id='line-plot'))])

@app.callback(Output(component_id='line-plot',component_property='figure'),
              Input(component_id='input', component_property='value'))
def update_yr(year):
    out_df = df[df['Year'] == int(year)].groupby('Month')['ArrDelay'].mean().reset_index()
    fig1 = go.Figure(data=go.Scatter(x=out_df['Month'], y=out_df['ArrDelay'], mode='lines',marker={'color':'green'}))
    fig1.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
    return fig1

if __name__ == '__main__':
    app.run_server()
