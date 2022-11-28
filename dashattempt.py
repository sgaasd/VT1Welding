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
    'text': '#f2f2f2'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options




df=openfiles.updata_df(4)

fig_vol=px.scatter(df,x="time [s]",y="voltage[v]")
fig_vol.update_layout(
plot_bgcolor=colors['background'],
paper_bgcolor=colors['background'],
font_color=colors['text'],
)

fig_cur=px.scatter(df,x="time [s]",y="current[A]")
fig_cur.update_layout(
plot_bgcolor=colors['background'],
paper_bgcolor=colors['background'],
font_color=colors['text'],
)

df=openfiles.updata_df_sound(3)

fig_F=px.line(df,x="time [s]",y="Channel 1",title='Channel 1 data')
fig_F.update_layout(
plot_bgcolor=colors['background'],
paper_bgcolor=colors['background'],
font_color=colors['text'],
)

df=openfiles.open_scan()

#fig_scan = go.Figure(data=[go.Mesh3d(x=df['x'], y=df['x'], z=df['x'])])
fig_scan = px.scatter_3d(x=df['x'], y=df['x'], z=df['x'])
fig_scan.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    )

#fig_scan.show()

app = Dash(__name__)

app.layout= html.Div(className="content", children=[
    dcc.Interval(id='update_interval', disabled=False, interval=1*5000, n_intervals=0),
    html.Div(className="left_menu",children=[
    html.H1('Data Visualisation of welding data'),
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
    id='graph-F',
    figure=fig_F,style={'width': '90%', 'height': '25%','text-align': 'center','padding':'1rem'})]),
    html.Div(className="right_content",
    children=[
            html.Div(
            className="top_metrics",
            children=[
            'This is top metrics'
            ]
        ),
        html.Div(className="bottem_right_menu",children=['This is bottom metrics',
            dcc.Graph(
                id='graph-scan',
                figure=fig_scan,style={'width': '90%', 'height': '25%','text-align': 'center','padding':'1rem'}
            )
        ]
            

        ),
    ])

])

@app.callback(Output('graph-vol','figure'),Output('graph-cur','figure'),Output('graph-F','figure'),Output('graph-scan','figure'),Input('update_interval','n_intervals'))

def update_figs_live(n):
    df=openfiles.updata_df(4)

    fig_vol=px.scatter(df,x="time [s]",y="voltage[v]")
    fig_vol.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],)

    fig_cur=px.scatter(df,x="time [s]",y="current[A]")
    fig_cur.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    )

    df=openfiles.updata_df_sound(3)

    fig_F=px.line(df,x="time [s]",y="Channel 1",title='Channel 1 data')
    fig_F.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    )
    df=openfiles.open_scan()

    #fig_scan = go.Figure(data=[go.Mesh3d(x=df['x'], y=df['x'], z=df['x'])])
    fig_scan = px.scatter_3d(x=df['x'], y=df['x'], z=df['x'])
    fig_scan.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    )


    return fig_vol,fig_cur,fig_F,fig_scan



if __name__ == '__main__':
    app.run_server(debug=True)





