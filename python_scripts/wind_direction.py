import pandas as pd
import plotly.express as px

raw_df = pd.read_csv("weather_data/filtered_output.csv")

# Convert the date column to datetime format.
raw_df["date"] = pd.to_datetime(raw_df["time"])

# Create the main dataframe.
df = raw_df.copy()

# Create a day and year column.
df["day"] = df["date"].dt.day
df["year"] = df["date"].dt.year

df["hour_day"] = df["day"] + df["date"].dt.hour / 24

# Year as string for discrete data plotting.
df["year"] = df["year"].astype(str)

plot_dict = {
    year: df[df["year"] == year].reset_index()
    for year in df["year"].unique()
}

for frame in plot_dict:
    plot_dict[frame].dropna()
    plot_dict[frame]["wspd"] = plot_dict[frame]["wspd"].astype(float)

avg = df.groupby("hour_day")[["wspd", "wdir"]].mean()

fig = px.line(
    avg,
    x=avg.index,
    y="wspd",
    title="Wind Speed and Wind Direction in Sandusky, OH Past 10 Years",
    labels={
        "hour_day": "Day (in July)",
        "wspd": "Wind Speed (mph)",
    },
)

fig.update_traces(
    line=dict(color="black", width=4),
    mode="lines+markers",
    marker=dict(
        size=20,
        symbol="arrow",
        angle=avg["wdir"],
    ),
    zorder=1,
    name="Average Wind Speed"
)

for key in plot_dict:
    fig.add_scatter(
        x=plot_dict[key]["hour_day"],
        y=plot_dict[key]["wspd"],
        marker=dict(
            size=10,
            symbol="arrow",
            angle=plot_dict[key]["wdir"],
        ),
        connectgaps=True,
        mode="lines+markers",
        name=key,
        zorder=0,
    )

fig.update_xaxes(range=[18, 23], fixedrange=True)
fig.update_yaxes(range=[df["wspd"].min(), df["wspd"].max() + 1],
                 fixedrange=True)

fig.write_html("wind_direction.html")
fig.show()