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

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


past_len=0


dash.register_page(__name__,path='/')
##Layout for the live page that updates whenever there is new data
layout=([
    dcc.Interval(id='update_interval', disabled=False, interval=1*10000, n_intervals=0),
    html.Div(className="left_menu",id="left_menu",children=["fetching data"]),
    html.Div(className="right_content",
    children=[
            html.Div(
            className="top_metrics",
            children=[html.Div(children=[
            html.H1(children='Weld Information:',style={
                               'margin-top':   '0px',
                               'margin-left':  '0px',
                               'margin-bottom':'0px',
                               'font-size': '25px'})]),
            html.Div([
                dbc.Row(id='meta_dat',children=["fetching data"])
            ])
            ]

        ),
        html.Div(className="bottem_right_menu",id="bottem_right_menu",children=["fetching data"]
        )]),
dcc.Store(id='determine_update')
])

