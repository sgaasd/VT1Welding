import dash
from dash import Dash,html, dcc, no_update, exceptions
import plotly.express as px
import pandas as pd
import openfiles
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
external_stylesheets = [dbc.themes.BOOTSTRAP]

colors = {
    'background': '#343434',
    'text': '#f2f2f2',
    'background2': '#272727'

}
past_len=0
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df_meta=openfiles.updata_df(1)


dropdown=dcc.Dropdown(openfiles.col_to_list(df_meta,'Test_number'),id='test_dropdown',style={ 'border-radius': '0px'})
dash.register_page(__name__)
#Layout for page for looking at previous data
layout=([

    dcc.Interval(id='update_dropdown', disabled=False, interval=1*1000, n_intervals=0),
    html.Div(className="left_menu",id="weld_drop",
    children=[html.H1('Data Visualisation of Robotic Welding',
    style={'margin-top':   '5px','margin-left':  '10px'})]),
    html.Div(className="right_content",
    children=[
            html.Div(
            className="top_metrics",
            children=[html.Div(children=[dbc.Row([dbc.Col(
            html.H1(children='Weld Information:',style={
                               'margin-top':   '0px',
                               'margin-left':  '0px',
                               'margin-bottom':'0px',
                               'font-size': '25px'}),width=3),
                               dbc.Col(dropdown
                               
                               ,width=3)])
                               ]),
            html.Div(id='meta_dat2',children=[])
            ]

        ),
        html.Div(className="bottem_right_menu",id="mic_drop",children=[]
            

        )]),
        dcc.Store(id='determine_update_drop'),
        dcc.Store(id='drop_value')
])
