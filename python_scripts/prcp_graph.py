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

# Create a day and year column.
df["DAY"] = df["DATE"].dt.day
df["YEAR"] = df["DATE"].dt.year

# Convert year to a string for discrete data plotting.
df["YEAR"] = df["YEAR"].astype(str)

# Find the average precipitation each day.
prcp_avg = [df[df["DAY"] == i]["PRCP"].mean() for i in range(17, 23)]

title = "Average Precipitation in Sandusky, OH Past 10 Years"
labels = {"DAY": "Day (in July)", "PRCP": "Precipitation (in)"}

# Plot the high and low temperatures each year.
fig = px.bar(df,
    x="DAY", y="PRCP",
    color="YEAR",
    color_discrete_sequence=px.colors.qualitative.Pastel,
    barmode="group",
    text_auto=True,
    title=title,
    labels=labels,
)
fig.add_bar(
    x=df["DAY"],
    y=prcp_avg,
    marker_color="lightblue",
    marker_line=dict(width=2, color="black"),
    text=prcp_avg,
    name="Average Precipitation",
)

fig.update_xaxes(showgrid=True, gridwidth=2, range=[16.5, 22.5], dtick=0.5,
                 ticklabelstep=2)
fig.update_yaxes(showgrid=True, gridwidth=2, range=[0, df["PRCP"].max() + 0.1])

fig.write_html("prcp_graph.html")
fig.show()