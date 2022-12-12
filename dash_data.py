# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
from dash import Dash,html, dcc, no_update, exceptions
import plotly.express as px
import pandas as pd
import openfiles
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = Dash(__name__,external_stylesheets=external_stylesheets,use_pages=True)
#app = Dash(__name__)
colors = {
    'background': '#343434',
    'text': '#f2f2f2',
    'background2': '#272727'

}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


df_meta=openfiles.updata_df(1)
print(df_meta)
print(df_meta.iat[0,0])

app.layout= html.Div(className="content", children=[html.Div([dcc.Link(page['name']+" | ", href=page['path'])
for page in dash.page_registry.values()],
style={'text-align': 'right','margin-right':  '10px'}),

dash.page_container

])

@app.callback(Output('meta_dat', 'children'),Output('graph-vol','figure'),Output('graph-cur','figure'),Output('graph-gas','figure'),Output('graph-wir','figure'),Output('graph-ch1','figure'),Output('graph-ch2','figure'),Output('graph-ch3','figure'),Output('graph-ch4','figure'),Output('determine_update','data'),Input('update_interval','n_intervals'),Input('determine_update','data'))
##used for updating figures on the live page
def update_figs_live(n,past_len):
    if n==0:
        past_len=0
    df_meta=openfiles.updata_df(1)
    con,past_len=openfiles.new_measure_check(past_len,openfiles.col_to_list(df_meta,'Path_weld'))
    if con==True:
        df=openfiles.updata_df(4)

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

        df=openfiles.updata_df(3)

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


        df_meta=openfiles.updata_df(1)

        meta=[
                dbc.Row([dbc.Col([
                    dbc.Row([
                        dbc.Col(html.Div(['Thickness bottom plate [mm]: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[-1,10]), width="auto")
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(['Thickness vertical plate [mm]: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[-1,11]), width="auto")
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(['Gas flow [L/min]: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[-1,15]), width="auto")
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(['Wirer feed speed [m/min]: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[-1,14]), width="auto")
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(['Input Current [A]: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[-1,12]), width="auto")
                    ]),
                    dbc.Row([
                        dbc.Col(html.Div(['Input Voltage [V]']), width=8),
                        dbc.Col(html.Div(df_meta.iat[-1,13]), width="auto")
                    ]),                
                    dbc.Row([
                        dbc.Col(html.Div(['Pass or fail: ']), width=8),
                        dbc.Col(html.Div(df_meta.iat[-1,6]), width="auto")
                    ])
            ]),             
                dbc.Col([
                    html.H1("Description of test: ",style={
                               'margin-top':   '0px',
                               'margin-left':  '0px',
                               'font-size': '20px'}),
                    html.Div(df_meta.iat[-1,16])
                
                ]),
                dbc.Col([
                    html.H1("Notes for test: ",style={
                               'margin-top':   '0px',
                               'margin-left':  '0px',
                               'font-size': '20px'}),
                    html.Div(df_meta.iat[-1,17])
                
                ])
                
                ])

            
            ]

        return meta,fig_vol,fig_cur,fig_gas,fig_wir,fig_ch1,fig_ch2,fig_ch3,fig_ch4,past_len
    
    return no_update,no_update,no_update,no_update,no_update,no_update,no_update,no_update,past_len

@app.callback(Output('test_dropdown','options'),Output('determine_update_drop','data'),Input('update_dropdown','n_intervals'),Input('determine_update_drop','data'))
#updates the dropdown menu every time there is new data
def update_drop_live(n,past_len):
    if n==0:
        past_len=0
    df_meta=openfiles.updata_df(1)
    con,past_len=openfiles.new_measure_check(past_len,openfiles.col_to_list(df_meta,'Test_number'))
    if con==True:
        return openfiles.col_to_list(df_meta,'Test_number'),past_len
    
    return no_update,past_len


@app.callback(Output('meta_dat2', 'children'),Output('drop_value','data'),Output('graph-vol2','figure'),Output('graph-cur2','figure'),Output('graph-gas2','figure'),Output('graph-wir2','figure'),Output('graph-ch12','figure'),Output('graph-ch22','figure'),Output('graph-ch32','figure'),Output('graph-ch42','figure'),Input('test_dropdown','value'))
#updates the figures based on the option chosen in the dropdown menu
def update_value(value):
    print(value)
    df_meta=openfiles.updata_df(1)

    df=openfiles.df_from_path(openfiles.col_to_list(df_meta,'Path_weld'),value-1)

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

    df=openfiles.df_from_path(openfiles.col_to_list(df_meta,'Path_sound'),value-1)

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

    df_meta=openfiles.updata_df(1)
    meta=[
            dbc.Row([dbc.Col([
                dbc.Row([
                    dbc.Col(html.Div(['Thickness bottom plate [mm]: ']), width=8),
                    dbc.Col(html.Div(df_meta.iat[value-1,10]), width="auto")
                ]),
                dbc.Row([
                    dbc.Col(html.Div(['Thickness vertical plate [mm]: ']), width=8),
                    dbc.Col(html.Div(df_meta.iat[value-1,11]), width="auto")
                ]),
                dbc.Row([
                    dbc.Col(html.Div(['Gas flow [L/min]: ']), width=8),
                    dbc.Col(html.Div(df_meta.iat[value-1,15]), width="auto")
                ]),
                dbc.Row([
                    dbc.Col(html.Div(['Wirer feed speed [m/min]: ']), width=8),
                    dbc.Col(html.Div(df_meta.iat[value-1,14]), width="auto")
                ]),
                dbc.Row([
                    dbc.Col(html.Div(['Input Current [A]: ']), width=8),
                    dbc.Col(html.Div(df_meta.iat[value-1,12]), width="auto")
                ]),
                dbc.Row([
                    dbc.Col(html.Div(['Input Voltage [V]']), width=8),
                    dbc.Col(html.Div(df_meta.iat[value-1,13]), width="auto")
                ]),                
                dbc.Row([
                    dbc.Col(html.Div(['Pass or fail: ']), width=8),
                    dbc.Col(html.Div(df_meta.iat[value-1,6]), width="auto")
                ])
        ]),             
            dbc.Col([
                html.H1("Description of test: ",style={
                            'margin-top':   '0px',
                            'margin-left':  '0px',
                            'font-size': '20px'}),
                html.Div(df_meta.iat[value-1,16])
            
            ]),
            dbc.Col([
                html.H1("Notes for test: ",style={
                            'margin-top':   '0px',
                            'margin-left':  '0px',
                            'font-size': '20px'}),
                html.Div(df_meta.iat[value-1,17])
            
            ])
            
            ])

        
        ]

    return meta,value-1,fig_vol,fig_cur,fig_gas,fig_wir,fig_ch1,fig_ch2,fig_ch3,fig_ch4

if __name__ == '__main__':
    app.run_server(debug=False)





