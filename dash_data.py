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


#fig_scan.show()

df_meta=openfiles.updata_df(1)
print(df_meta)
print(df_meta.iat[0,0])
#app = Dash(__name__)
#df_meta['Thickness_hor'],df_meta['Thickness_ver'],df_meta['Rating'],df_meta['Describtion'],df_meta['Notes']
app.layout= html.Div(className="content", children=[html.Div("this is test",style={'text-align': 'right','margin-right':  '10px'}),
dash.page_container

])

@app.callback(Output('graph-vol','figure'),Output('graph-cur','figure'),Output('graph-wir','figure'),Output('graph-ch1','figure'),Output('graph-ch2','figure'),Output('graph-ch3','figure'),Output('graph-ch4','figure'),Output('determine_update','data'),Input('update_interval','n_intervals'),Input('determine_update','data'))

def update_figs_live(n,past_len):
    if n==0:
        past_len=0
    
    con,past_len=openfiles.new_measure_check(past_len)
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

        df=openfiles.updata_df_sound(3)

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


if __name__ == '__main__':
    app.run_server(debug=False)





