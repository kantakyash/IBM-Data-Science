import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output
import plotly.graph_objects as go
import plotly.express as px

airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('Flight Delay Time Statistics', style={'text_align':'right',
                                                                               'color':'red',
                                                                               'font_size':50}),
                                html.Div(['Input Year: ', dcc.Input(id='input', value='2011', type='number', style={'height':'50px',
                                                                                                                    'font_size':35})], style={'font-size':35}),
                                html.Br(),
                                html.Br(),
                                html.Div([html.Div(dcc.Graph(id='avg_carrier_dly')),
                                          html.Div(dcc.Graph(id='avg_wthr_dly')),
                                          ], style={'display':'flex'}),
                                html.Div([html.Div(dcc.Graph(id='avg_nas_dly')),
                                          html.Div(dcc.Graph(id='avg_security_dly')),
                                          ], style={'display':'flex'}),
                                html.Div([html.Div(dcc.Graph(id='avg_crft_dly'))], style={'width':'65%'})                                                                                   
                                ])

@app.callback([Output(component_id='avg_carrier_dly', component_property='figure'), Output(component_id='avg_wthr_dly', component_property='figure'), Output(component_id='avg_nas_dly', component_property='figure'), 
               Output(component_id='avg_security_dly', component_property='figure'), Output(component_id='avg_crft_dly', component_property='figure')],
              Input(component_id='input', component_property='value'))
def update_year(year):
    out_df = airline_data[airline_data['Year'] == int(year)].groupby(['Month', 'Reporting_Airline'])[[col for col in airline_data.columns if col.endswith('Delay')]].mean().reset_index()

    fig1 = px.line(out_df, x='Month',y='CarrierDelay', color='Reporting_Airline', title='Avg. Carrier Delay')
    fig2 = px.line(out_df, x='Month',y='WeatherDelay', color='Reporting_Airline', title='Avg. Weather Delay')
    fig3 = px.line(out_df, x='Month',y='NASDelay', color='Reporting_Airline', title='Avg. NAS Delay')
    fig4 = px.line(out_df, x='Month',y='SecurityDelay', color='Reporting_Airline', title='Avg. Security Delay')
    fig5 = px.line(out_df, x='Month',y='LateAircraftDelay', color='Reporting_Airline', title='Avg. Late Aircraft Delay')

    return fig1, fig2, fig3, fig4, fig5 

if __name__ == '__main__':
    app.run_server()