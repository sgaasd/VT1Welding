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
df=openfiles.updata_df(4)

fig_vol=px.line(df,x="time [s]",y=' Voltage',title='Voltage data')
fig_vol.update_layout(
plot_bgcolor=colors['background'],
paper_bgcolor=colors['background'],
font_color=colors['text'],
margin=dict(l=20, r=20, t=35, b=20)
)

fig_cur=px.line(df,x="time [s]",y="Current",title='Current data')
fig_cur.update_layout(
plot_bgcolor=colors['background'],
paper_bgcolor=colors['background'],
font_color=colors['text'],
margin=dict(l=20, r=20, t=35, b=20)
)

fig_wir=px.line(df,x="time [s]",y=" Wire-feed",title='Wirer data')
fig_wir.update_layout(
plot_bgcolor=colors['background'],
paper_bgcolor=colors['background'],
font_color=colors['text'],
margin=dict(l=20, r=20, t=35, b=20)
)

df=openfiles.updata_df(3)

fig_ch1=px.line(df,x="time [s]",y="Channel_1",title='Channel 1 data')
fig_ch1.update_layout(
plot_bgcolor=colors['background2'],
paper_bgcolor=colors['background2'],
font_color=colors['text'],
margin=dict(l=20, r=20, t=25, b=20)
)

fig_ch2=px.line(df,x="time [s]",y="Channel_2",title='Channel 2 data')
fig_ch2.update_layout(
plot_bgcolor=colors['background2'],
paper_bgcolor=colors['background2'],
font_color=colors['text'],
margin=dict(l=20, r=20, t=25, b=20)
)

fig_ch3=px.line(df,x="time [s]",y="Channel_3",title='Channel 3 data')
fig_ch3.update_layout(
plot_bgcolor=colors['background2'],
paper_bgcolor=colors['background2'],
font_color=colors['text'],
margin=dict(l=20, r=20, t=25, b=20)
)

fig_ch4=px.line(df,x="time [s]",y="Channel_4",title='Channel 4 data')
fig_ch4.update_layout(
plot_bgcolor=colors['background2'],
paper_bgcolor=colors['background2'],
font_color=colors['text'],
margin=dict(l=20, r=20, t=25, b=20)
)

#fig_scan.show()

df_meta=openfiles.updata_df(1)
print(df_meta)
print(df_meta.iat[0,0])

dash.register_page(__name__,path='/')

layout=([

    dcc.Interval(id='update_interval', disabled=False, interval=1*1000, n_intervals=0),
    html.Div(className="left_menu",children=[
    html.H1('Data Visualisation of Robotic Welding',style={'margin-top':   '5px','margin-left':  '10px'}),
    #html.Hr(style={'width': '95%'}),
    dcc.Graph(
    id='graph-vol',
    figure=fig_vol,style={'width': '90%', 'height': '20vh','text-align': 'center','padding':'1rem'}),
    html.Hr(style={'width': '95%'}),
    dcc.Graph(
    id='graph-cur',
    figure=fig_cur,style={'width': '90%', 'height': '20vh','text-align': 'center','padding':'1rem'}),
    html.Hr(style={'width': '95%'}),
    dcc.Graph(
    id='graph-cur',
    figure=fig_cur,style={'width': '90%', 'height': '20vh','text-align': 'center','padding':'1rem'}),
    html.Hr(style={'width': '95%'}),
    dcc.Graph(
    id='graph-wir',
    figure=fig_wir,style={'width': '90%', 'height': '20vh','text-align': 'center','padding':'1rem'})]),
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
                dbc.Row([dbc.Col([
                    dbc.Row([
                        dbc.Col(html.Div(['Thickness bottom plate [mm]: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[0,9]), width="auto")
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(['Thickness vertical plate [mm]: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[0,10]), width="auto")
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(['Gas flow [L/min]: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[0,14]), width="auto")
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(['Wirer feed speed [m/min]: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[0,13]), width="auto")
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(['Input Current [A]: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[0,11]), width="auto")
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(['Input Voltage [V]']), width=8),
                        dbc.Col(html.Div(df_meta.iat[0,12]), width="auto")
                    ]),                
                    dbc.Row([
                        dbc.Col(html.Div(['Pass or fail: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[0,5]), width="auto")
                    ])
            ]),             
                dbc.Col([
                    html.H1("Description of test: ",style={
                               'margin-top':   '0px',
                               'margin-left':  '0px',
                               'font-size': '20px'}),
                    html.Div(df_meta.iat[0,15])
                
                ]),
                dbc.Col([
                    html.H1("Notes for test: ",style={
                               'margin-top':   '0px',
                               'margin-left':  '0px',
                               'font-size': '20px'}),
                    html.Div(df_meta.iat[0,16])
                
                ])
                
                ])

            
            ])
            ]

        ),
        html.Div(className="bottem_right_menu",children=[html.H3(' Microphone data'),
            dcc.Graph(
                id='graph-ch1',
                figure=fig_ch1,style={'width': '100%', 'height': '19.9vh','text-align': 'center','padding':'0rem',}
            ),
            dcc.Graph(
                id='graph-ch2',
                figure=fig_ch2,style={'width': '100%', 'height': '19.9vh','text-align': 'center','padding':'0rem'}
            ),
            dcc.Graph(
                id='graph-ch3',
                figure=fig_ch3,style={'width': '100%', 'height': '19.9vh','text-align': 'center','padding':'0rem'}
            ),
            dcc.Graph(
                id='graph-ch4',
                figure=fig_ch4,style={'width': '100%', 'height': '19.9vh','text-align': 'center','padding':'0rem'}
            )
        ]
            

        )]),
dcc.Store(id='determine_update')
])

