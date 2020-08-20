import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# load CSV file from Datasets folder
df = pd.read_csv('../Datasets/Olympic2016Rio.csv')

# removing empty spaces from state column to avoid errors
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# creating unrecovered column
# df['Unrecovered'] = df['Confirmed'] - df['Deaths'] - df['Recovered']

# creating sum of number of cases group by country column
new_df = df.groupby(['NOC']).agg(
    {'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'}).reset_index()

# sorting values and select 20 first values
new_df = new_df.sort_values(by=['Gold'], ascending=[False]).head(20).reset_index()

# preparing data
trace1 = go.Bar(x=new_df['NOC'], y=new_df['Bronze'], name='Bronze', marker={'color': '#CD7F32'})
trace2 = go.Bar(x=new_df['NOC'], y=new_df['Silver'], name='Silver', marker={'color': '#9EA0A1'})
trace3 = go.Bar(x=new_df['NOC'], y=new_df['Gold'], name='Gold', marker={'color': '#FFD700'})
data = [trace1, trace2, trace3]

# preparing layout
layout = go.Layout(title='Total medals of Olympic 2016 of 20 first top countries', xaxis_title="Country", yaxis_title="Medals", barmode='stack')

# plot the figure and saving in an html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='stackbarchart.html')