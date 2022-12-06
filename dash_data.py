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

@app.callback(Output('graph-vol','figure'),Output('graph-cur','figure'),Output('graph-wir','figure'),Output('graph-ch1','figure'),Output('graph-ch2','figure'),Output('graph-ch3','figure'),Output('graph-ch4','figure'),Output('determine_update','data'),Input('update_interval','n_intervals'),Input('determine_update','data'))

def update_figs_live(n,past_len):
    if n==0:
        past_len=0
    df_meta=openfiles.updata_df(1)
    con,past_len=openfiles.new_measure_check(past_len,openfiles.col_to_list(df_meta,'Path_weld'))
    if con==True:
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


        return fig_vol,fig_cur,fig_wir,fig_ch1,fig_ch2,fig_ch3,fig_ch4,past_len
    
    return no_update,no_update,no_update,no_update,no_update,no_update,no_update,past_len

@app.callback(Output('test_dropdown','options'),Output('determine_update_drop','data'),Input('update_dropdown','n_intervals'),Input('determine_update_drop','data'))

def update_drop_live(n,past_len):
    if n==0:
        past_len=0
    df_meta=openfiles.updata_df(1)
    con,past_len=openfiles.new_measure_check(past_len,openfiles.col_to_list(df_meta,'Test_number'))
    if con==True:

        #dropdown=dcc.Dropdown(openfiles.col_to_list(df_meta,'Test_number'),id='test_dropdown',style={'background-color': '#343434', 'border-radius': '0px'})
        
        return openfiles.col_to_list(df_meta,'Test_number'),past_len
    
    return no_update,past_len


@app.callback(Output('drop_value','data'),Output('graph-vol2','figure'),Output('graph-cur2','figure'),Output('graph-wir2','figure'),Output('graph-ch12','figure'),Output('graph-ch22','figure'),Output('graph-ch32','figure'),Output('graph-ch42','figure'),Input('test_dropdown','value'))
def update_value(value):
    print(value)
    df_meta=openfiles.updata_df(1)

    #df=openfiles.updata_df(4)
    df=openfiles.df_from_path(openfiles.col_to_list(df_meta,'Path_weld'),value-1)

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

    df=openfiles.df_from_path(openfiles.col_to_list(df_meta,'Path_sound'),value-1)

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
    return value-1,fig_vol,fig_cur,fig_wir,fig_ch1,fig_ch2,fig_ch3,fig_ch4

if __name__ == '__main__':
    app.run_server(debug=False)





