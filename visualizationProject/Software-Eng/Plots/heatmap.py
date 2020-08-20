import plotly.offline as pyo
import plotly.graph_objs as go
import pandas as pd
# Load CSV file from Datasets folder
df = pd.read_csv('../Datasets/Weather2014-15.csv')
# Preparing data
data = [go.Heatmap(x=df['Day'], y=df['WeekofMonth'], z=df['record_max_temp'].values.tolist(), colorscale='Jet')]
# Preparing layout
layout = go.Layout(title='Max temp on day of week and month of year', xaxis_title='Day of week', yaxis_title='month of year')
# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='heatmap.html')