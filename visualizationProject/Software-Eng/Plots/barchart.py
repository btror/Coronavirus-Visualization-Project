import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df = pd.read_csv('../Datasets/CoronavirusTotal.csv')

# Removing empty spaces from State column to avoid errors
df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Creating sum of number of medals group by country Column
new_df = df.groupby(['Country'])['Confirmed'].sum().reset_index()

# Sorting values and select first 20 countries with highest total
new_df = new_df.sort_values(by=['Confirmed'], ascending=[False]).head(20)

# Preparing data
data = [go.Bar(x=new_df['Country'], y=new_df['Confirmed'])]

# Preparing layout
layout = go.Layout(title='Total cases of coronavirus per country', xaxis_title="Country",
                   yaxis_title="Total cases")

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='barchart.html')
