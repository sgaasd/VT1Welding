# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash,html, dcc
import plotly.express as px
import pandas as pd
import openfiles
from dash.dependencies import Input, Output
import plotly.graph_objects as go


app = Dash(__name__)

colors = {
    'background': '#343434',
    'text': '#f2f2f2',
    'background2': '#272727'

}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options




df=openfiles.updata_df(4)

fig_vol=px.line(df,x="time [s]",y=' Voltage')
fig_vol.update_layout(
plot_bgcolor=colors['background'],
paper_bgcolor=colors['background'],
font_color=colors['text'],
)

fig_cur=px.line(df,x="time [s]",y="Current")
fig_cur.update_layout(
plot_bgcolor=colors['background'],
paper_bgcolor=colors['background'],
font_color=colors['text'],
)

fig_wir=px.line(df,x="time [s]",y=" Wire-feed")
fig_wir.update_layout(
plot_bgcolor=colors['background'],
paper_bgcolor=colors['background'],
font_color=colors['text'],
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

#fig_scan.show()

app = Dash(__name__)

app.layout= html.Div(className="content", children=[
    dcc.Interval(id='update_interval', disabled=False, interval=1*5000, n_intervals=0),
    html.Div(className="left_menu",children=[
    html.H1('   Data Visualisation of welding data'),
    #html.Hr(style={'width': '95%'}),
    dcc.Graph(
    id='graph-vol',
    figure=fig_vol,style={'width': '90%', 'height': '25%','text-align': 'center','padding':'1rem'}),
    html.Hr(style={'width': '95%'}),
    dcc.Graph(
    id='graph-cur',
    figure=fig_cur,style={'width': '90%', 'height': '25%','text-align': 'center','padding':'1rem'}),
    html.Hr(style={'width': '95%'}),
    dcc.Graph(
    id='graph-wir',
    figure=fig_wir,style={'width': '90%', 'height': '25%','text-align': 'center','padding':'1rem'})]),
    html.Div(className="right_content",
    children=[
            html.Div(
            className="top_metrics",
            children=[
            'This is top metrics'
            ]
        ),
        html.Div(className="bottem_right_menu",children=[html.H3(' Microphone data'),
            dcc.Graph(
                id='graph-ch1',
                figure=fig_ch1,style={'width': '100%', 'height': '20vh','text-align': 'center','padding':'0rem',}
            ),
            dcc.Graph(
                id='graph-ch2',
                figure=fig_ch2,style={'width': '100%', 'height': '20vh','text-align': 'center','padding':'0rem'}
            ),
            dcc.Graph(
                id='graph-ch3',
                figure=fig_ch3,style={'width': '100%', 'height': '20vh','text-align': 'center','padding':'0rem'}
            ),
            dcc.Graph(
                id='graph-ch4',
                figure=fig_ch4,style={'width': '100%', 'height': '20vh','text-align': 'center','padding':'0rem'}
            )
        ]
            

        ),
    ])

])

@app.callback(Output('graph-vol','figure'),Output('graph-cur','figure'),Output('graph-wir','figure'),Output('graph-ch1','figure'),Output('graph-ch2','figure'),Output('graph-ch3','figure'),Output('graph-ch4','figure'),Input('update_interval','n_intervals'))

def update_figs_live(n):
    df=openfiles.updata_df(4)

    fig_vol=px.line(df,x="time [s]",y=' Voltage')
    fig_vol.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    )

    fig_cur=px.line(df,x="time [s]",y="Current")
    fig_cur.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    )

    fig_wir=px.line(df,x="time [s]",y=" Wire-feed")
    fig_wir.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
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


    return fig_vol,fig_cur,fig_wir,fig_ch1,fig_ch2,fig_ch3,fig_ch4



if __name__ == '__main__':
    app.run_server(debug=False)





