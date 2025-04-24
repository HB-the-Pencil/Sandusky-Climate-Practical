import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv('weather_data/water_temperature_data.csv')

# Convert the 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

df["Day"] = df["Date"].dt.day
df["Year"] = df["Date"].dt.year
df["Year"] = df["Year"].astype(str)

t_avg = [
    df[df["Day"] == i]["Temp"].mean() for i in range(17, 23)
]

# Create the plot
fig = px.line(
    df,
    x='Day',
    y='Temp',
    color="Year",
    color_discrete_sequence=px.colors.qualitative.Pastel,
    symbol="Year",
    title='Daily Temperatures',
    markers=True,
)

fig.add_scatter(
    x=df["Day"],
    y=t_avg,
    line=dict(width=4, color="red"),
    name="Average Water Temperature"
)

# Show the plot
fig.write_html("water_temp_graph.html")
fig.show()
