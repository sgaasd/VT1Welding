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
#df_meta=df_meta.iloc[0]

#df=openfiles.updata_df(4)
df=openfiles.df_from_path(openfiles.col_to_list(df_meta,'Path_weld'),-1)

fig_vol=px.line(df,x="time [s]",y=' Voltage',
labels={
    "time [s]": "Time [ms]",
    " Voltage": "Voltage [V*10]"
},title='Voltage')
fig_vol.update_layout(
plot_bgcolor=colors['background'],
paper_bgcolor=colors['background'],
font_color=colors['text'],
margin=dict(l=20, r=20, t=35, b=20)
)

fig_cur=px.line(df,x="time [s]",y="Current",
labels={
    "time [s]": "Time [ms]",
    "Current": "Current [A*10]"
},title='Current')
fig_cur.update_layout(
plot_bgcolor=colors['background'],
paper_bgcolor=colors['background'],
font_color=colors['text'],
margin=dict(l=20, r=20, t=35, b=20)
)
fig_gas=px.line(df,x="time [s]",y=" Gas-flow",
labels={
    "time [s]": "Time [ms]",
    " Gas-flow": "Flow [L*10/min]"
},title='Gas flow')
fig_gas.update_layout(
plot_bgcolor=colors['background'],
paper_bgcolor=colors['background'],
font_color=colors['text'],
margin=dict(l=20, r=20, t=35, b=20)
)

fig_wir=px.line(df,x="time [s]",y=" Wire-feed",
labels={
    "time [s]": "Time [ms]",
    " Wire-feed": "Speed [m*10/min]"
},title='Wirer speed')
fig_wir.update_layout(
plot_bgcolor=colors['background'],
paper_bgcolor=colors['background'],
font_color=colors['text'],
margin=dict(l=20, r=20, t=35, b=20)
)

df=openfiles.df_from_path(openfiles.col_to_list(df_meta,'Path_sound'),-1)

fig_ch1=px.line(df,x="time [s]",y="Channel_1",
labels={
"time [s]": "Time [ms]",
"Channel_1": "Channel 1"
},title='Channel 1')
fig_ch1.update_layout(
plot_bgcolor=colors['background2'],
paper_bgcolor=colors['background2'],
font_color=colors['text'],
margin=dict(l=20, r=20, t=25, b=20)
)

fig_ch2=px.line(df,x="time [s]",y="Channel_2",
labels={
"time [s]": "Time [ms]",
"Channel_2": "Channel 2"
},title='Channel 2')
fig_ch2.update_layout(
plot_bgcolor=colors['background2'],
paper_bgcolor=colors['background2'],
font_color=colors['text'],
margin=dict(l=20, r=20, t=25, b=20)
)

fig_ch3=px.line(df,x="time [s]",y="Channel_3",
labels={
"time [s]": "Time [ms]",
"Channel_3": "Channel 3"
},title='Channel 3')
fig_ch3.update_layout(
plot_bgcolor=colors['background2'],
paper_bgcolor=colors['background2'],
font_color=colors['text'],
margin=dict(l=20, r=20, t=25, b=20)
)

fig_ch4=px.line(df,x="time [s]",y="Channel_4",
labels={
"time [s]": "Time [ms]",
"Channel_4": "Channel 4"
},title='Channel 4')
fig_ch4.update_layout(
plot_bgcolor=colors['background2'],
paper_bgcolor=colors['background2'],
font_color=colors['text'],
margin=dict(l=20, r=20, t=25, b=20)
)

#print(df_meta)
#print(df_meta.iat[0,0])

dropdown=dcc.Dropdown(openfiles.col_to_list(df_meta,'Test_number'),1,id='test_dropdown',style={'background-color': '#343434', 'border-radius': '0px'})

dash.register_page(__name__)
#Layout for page for looking at previous data
layout=([

    dcc.Interval(id='update_dropdown', disabled=False, interval=1*1000, n_intervals=0),
    html.Div(className="left_menu",children=[
    html.H1('Data Visualisation of Robotic Welding',style={'margin-top':   '5px','margin-left':  '10px'}),
    #html.Hr(style={'width': '95%'}),
    dcc.Graph(
    id='graph-vol2',
    figure=fig_vol,style={'width': '90%', 'height': '20vh','text-align': 'center','padding':'1rem'}),
    html.Hr(style={'width': '95%'}),
    dcc.Graph(
    id='graph-cur2',
    figure=fig_cur,style={'width': '90%', 'height': '20vh','text-align': 'center','padding':'1rem'}),
    html.Hr(style={'width': '95%'}),
    dcc.Graph(
    id='graph-gas2',
    figure=fig_gas,style={'width': '90%', 'height': '20vh','text-align': 'center','padding':'1rem'}),
    html.Hr(style={'width': '95%'}),
    dcc.Graph(
    id='graph-wir2',
    figure=fig_wir,style={'width': '90%', 'height': '20vh','text-align': 'center','padding':'1rem'})]),
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
            html.Div(id='meta_dat2',children=[
                dbc.Row([dbc.Col([
                    dbc.Row([
                        dbc.Col(html.Div(['Thickness bottom plate [mm]: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[0,10]), width="auto")
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(['Thickness vertical plate [mm]: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[0,11]), width="auto")
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(['Gas flow [L/min]: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[0,15]), width="auto")
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(['Wirer feed speed [m/min]: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[0,14]), width="auto")
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(['Input Current [A]: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[0,12]), width="auto")
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(['Input Voltage [V]']), width=8),
                        dbc.Col(html.Div(df_meta.iat[0,13]), width="auto")
                    ]),                
                    dbc.Row([
                        dbc.Col(html.Div(['Pass or fail: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[0,6]), width="auto")
                    ])
            ]),             
                dbc.Col([
                    html.H1("Description of test: ",style={
                               'margin-top':   '0px',
                               'margin-left':  '0px',
                               'font-size': '20px'}),
                    html.Div(df_meta.iat[0,16])
                
                ]),
                dbc.Col([
                    html.H1("Notes for test: ",style={
                               'margin-top':   '0px',
                               'margin-left':  '0px',
                               'font-size': '20px'}),
                    html.Div(df_meta.iat[0,17])
                
                ])
                
                ])

            
            ])
            ]

        ),
        html.Div(className="bottem_right_menu",children=[html.H3(' Microphone data'),
            dcc.Graph(
                id='graph-ch12',
                figure=fig_ch1,style={'width': '100%', 'height': '19.9vh','text-align': 'center','padding':'0rem',}
            ),
            dcc.Graph(
                id='graph-ch22',
                figure=fig_ch2,style={'width': '100%', 'height': '19.9vh','text-align': 'center','padding':'0rem'}
            ),
            dcc.Graph(
                id='graph-ch32',
                figure=fig_ch3,style={'width': '100%', 'height': '19.9vh','text-align': 'center','padding':'0rem'}
            ),
            dcc.Graph(
                id='graph-ch42',
                figure=fig_ch4,style={'width': '100%', 'height': '19.9vh','text-align': 'center','padding':'0rem'}
            )
        ]
            

        )]),
        dcc.Store(id='determine_update_drop'),
        dcc.Store(id='drop_value')
])
