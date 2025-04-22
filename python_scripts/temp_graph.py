import pandas as pd
import plotly.express as px

raw_df = pd.read_csv(
    "weather_data/sandusky_temp_prcp_2014_2024.csv",
)

# Convert the date column to datetime format.
raw_df["DATE"] = pd.to_datetime(raw_df["DATE"])

# Save just the dates in July (and remove the 2014 dates, I made a mistake).
time_mask = (raw_df["DATE"].dt.month == 7) & (raw_df["DATE"].dt.year > 2014)
df = raw_df.loc[time_mask]

# Save just the dates between the 17th and the 22nd.
date_mask = (17 <= raw_df["DATE"].dt.day) & (raw_df["DATE"].dt.day <= 22)
df = df.loc[date_mask]

df = df.reset_index()

# Create an average temperature column.
df["TAVG"] = (df["TMAX"] + df["TMIN"]) / 2

# Create a day and year column.
df["DAY"] = df["DATE"].dt.day
df["YEAR"] = df["DATE"].dt.year

# Convert year to a string for discrete data plotting.
df["YEAR"] = df["YEAR"].astype(str)

# Find the average temperature each day.
t_avg = [df[df["DAY"] == i]["TAVG"].mean() for i in range(17, 23)]

title = "Average Temperature in Sandusky, OH Past 10 Years"
labels = {"DAY": "Day (in July)", "TAVG": "Average Temperature (F)"}

# Plot the high and low temperatures each year.
fig = px.scatter(df,
    x="DAY", y="TAVG",
    color="YEAR",
    color_discrete_sequence=px.colors.qualitative.Bold,
    symbol="YEAR",
    title=title,
    labels=labels,
)
fig.add_scatter(
    x=df["DAY"],
    y=t_avg,
    line=dict(width=4, color="red"),
    name="Average Temperature",
)

fig.update_xaxes(range=[16.5, 22.5])
fig.update_yaxes(range=[df["TAVG"].min() - 1, df["TAVG"].max() + 1])

fig.write_html("temp_graph.html")
fig.show()
