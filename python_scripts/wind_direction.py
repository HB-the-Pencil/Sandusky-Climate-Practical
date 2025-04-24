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

# Drop null data.
df.dropna()
df["wspd"] = df["wspd"].astype(float)

# Create an average list
avg = df.groupby("hour_day")[["wspd", "wdir"]].mean()

fig = px.line(
    df,
    x="hour_day",
    y="wspd",
    color="year",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig.update_traces(
    mode="lines+markers",
    marker=dict(
        size=10,
        symbol="arrow",
        angle=df["wdir"]
    ),
)

fig.add_scattergl(
    x=avg.index,
    y=avg["wspd"],
    line=dict(width=4, color="black"),
    marker=dict(
        symbol="arrow",
        size=20,
        angle=avg["wdir"],
    ),
    mode="lines+markers",
    name="Average Wind Speed",
)

fig.update_xaxes(range=[18, 23])
fig.update_yaxes(range=[df["wspd"].min(), df["wspd"].max() + 1],)

fig.write_html("wind_direction.html")
fig.show()