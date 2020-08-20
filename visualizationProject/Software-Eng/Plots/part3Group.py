import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df1 = pd.read_csv('../Datasets/Olympic2016Rio.csv')
df2 = pd.read_csv('../Datasets/Weather2014-15.csv')

app = dash.Dash()

# Bar chart data
barchart_df = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
barchart_df = barchart_df.groupby(['NOC'])['Total'].sum().reset_index()
barchart_df = barchart_df.sort_values(by=['Total'], ascending=[False]).head(20)
data_barchart = [go.Bar(x=barchart_df['NOC'], y=barchart_df['Total'])]

# stack Bar chart data
stackbarchart_df = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
# stackbarchart_df['Unrecovered'] = stackbarchart_df['Confirmed'] - stackbarchart_df['Deaths'] - stackbarchart_df[
#     'Recovered']
newstackbarchart_df = df1.groupby(['NOC']).agg(
    {'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'}).reset_index()

newstackbarchart_df = newstackbarchart_df.sort_values(by=['Gold'], ascending=[False]).head(20).reset_index()

trace1 = go.Bar(x=newstackbarchart_df['NOC'], y=newstackbarchart_df['Bronze'], name='Bronze', marker={'color': '#CD7F32'})
trace2 = go.Bar(x=newstackbarchart_df['NOC'], y=newstackbarchart_df['Silver'], name='Silver', marker={'color': '#9EA0A1'})
trace3 = go.Bar(x=newstackbarchart_df['NOC'], y=newstackbarchart_df['Gold'], name='Gold', marker={'color': '#FFD700'})
data_stackbarchart = [trace1, trace2, trace3]

# line chart data
line_df = df2
line_df['date'] = pd.to_datetime(line_df['date'])
data_linechart = [go.Scatter(x=line_df['month'], y=line_df['actual_max_temp'], mode='lines', name='Month')]

# multi line chart data
multiline_df = df2
multiline_df['date'] = pd.to_datetime(multiline_df['date'])
trace1_multiline = go.Scatter(x=multiline_df['month'], y=multiline_df['actual_min_temp'], mode='lines', name='min')
trace2_multiline = go.Scatter(x=multiline_df['month'], y=multiline_df['actual_max_temp'], mode='lines', name='max')
trace3_multiline = go.Scatter(x=multiline_df['month'], y=multiline_df['actual_mean_temp'], mode='lines', name='mean')
data_multiline = [trace1_multiline, trace2_multiline, trace3_multiline]

# Bubble chart
bubble_df = df2

bubble_df = bubble_df.groupby(['month']).agg(
    {'average_min_temp': 'sum', 'average_max_temp': 'sum'}).reset_index()
data_bubblechart = [
    go.Scatter(x=bubble_df['average_min_temp'] / 30.42,
               y=bubble_df['average_max_temp'] / 30.42,
               text=bubble_df['month'],
               mode='markers',
               marker=dict(size=bubble_df['average_min_temp'] / 30, color=bubble_df['average_max_temp'] / 30, showscale=True))
]

# Heatmap
data_heatmap = [go.Heatmap(x=df2['day'],
                           y=df2['month'],
                           z=df2['record_max_temp'].values.tolist(),
                           colorscale='Jet')]


# Layout
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Part 3 plots', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represents the total medals of olympic 2016 of 20 first top countries'),
    dcc.Graph(id='graph1',
              figure={
                  'data': data_barchart,
                  'layout': go.Layout(title='Total medals of olypmic 2016 of 20 first top countries',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Medals'},
                                      barmode='stack')
              }),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Stack bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This stack bar chart represents the total medals of olypmic 2016 of 20 first top countries'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_stackbarchart,
                  'layout': go.Layout(title='Total medals of olypmic 2016 of 20 first top countries',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Medals'},
                                      barmode='stack')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Line chart', style={'color': '#df1e56'}),
    html.Div('This line chart represent the actual max temperature of each month'),
    dcc.Graph(id='graph3',
              figure={
                  'data': data_linechart,
                  'layout': go.Layout(title='Actual max temperature of each month',
                                      xaxis={'title': 'Month'}, yaxis={'title': 'Temperature'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Multi Line chart', style={'color': '#df1e56'}),
    html.Div(
        'This line chart represents the mean, max, and min temperatures for each month.'),
    dcc.Graph(id='graph4',
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(
                      title='mean, max, and min temperatures for each month',
                      xaxis={'title': 'Date'}, yaxis={'title': 'Temperature'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bubble chart', style={'color': '#df1e56'}),
    html.Div(
        'This bubble chart represent the average min/max temperature per month 2014/2015.'),
    dcc.Graph(id='graph5',
              figure={
                  'data': data_bubblechart,
                  'layout': go.Layout(title='average min/max temperature per month 2014/2015',
                                      xaxis={'title': 'average min'}, yaxis={'title': 'average max'},
                                      hovermode='closest')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Heat map', style={'color': '#df1e56'}),
    html.Div(
        'This heat map represent the recorded max temperature on day of week/month of year'),
    dcc.Graph(id='graph6',
              figure={
                  'data': data_heatmap,
                  'layout': go.Layout(title='recorded max temperature on day of week/month of year',
                                      xaxis={'title': 'Day of Week'}, yaxis={'title': 'Month of year'})
              }
              )
])

if __name__ == '__main__':
    app.run_server()