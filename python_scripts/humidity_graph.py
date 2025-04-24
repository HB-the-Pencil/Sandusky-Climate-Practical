from pathlib import Path
import csv
from datetime import datetime
import plotly.graph_objects as go
from collections import defaultdict

path = Path('weather_data/filtered_output.csv')
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)

year_to_label = {
    2015: "a", 2016: "b", 2017: "c", 2018: "d", 2019: "e",
    2020: "f", 2021: "g", 2022: "h", 2023: "i", 2024: "j"
}

lines = {label: {"x": [], "y": []} for label in year_to_label.values()}

#this is to create a list to store the humidity
#and number of counted hours to find the average
humidity_sum = defaultdict(list)
count_per_day_hour = defaultdict(int)

for row in reader:
    try:
        current_date_hour = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        current_year = current_date_hour.year
        humidity = float(row[1])

        current_time = current_date_hour.day + current_date_hour.hour / 24
    except ValueError:
        print(f"Missing data for {row[0]}")
        continue
    except Exception as exception:
        print(f"An error occured: {exception}")
        continue

    if current_year in year_to_label:
        label = year_to_label[current_year]
        lines[label]["x"].append(current_time)
        lines[label]["y"].append(humidity)

    humidity_sum[current_time].append(humidity)
    count_per_day_hour[current_time] += 1

average_x = []
average_y = []

print(count_per_day_hour)

for day_hour, humidity_list in humidity_sum.items():
    average_x.append(day_hour)
    average_y.append(sum(humidity_list) / count_per_day_hour[day_hour])

#this is so that I can flip the variables like a and 2015 back to the numbers
label_to_year = {v: k for k, v in year_to_label.items()}
traces = []

for label, data in lines.items():
    print('hello')
    print(len(data['y']))
    trace = {
        "type": 'scatter',
        'mode': 'lines',
        'name': str(label_to_year[label]),
        'x': data["x"],
        'y': data["y"],
    }
    traces.append(trace)

average_trace = {
    "type": 'scatter',
    'mode': 'lines',
    'name': 'Average',
    'x': average_x,
    'y': average_y,
    'line': {'width': 4, 'color': 'black', 'dash': 'solid'},
}
traces.append(average_trace)
print(traces)

fig = go.Figure(data=traces)
fig.update_layout(
    title="Humidity for the past 10 years with the average",
    xaxis_title="Day (in July)",
    yaxis_title="Humidity",
    xaxis=dict(
        tickangle=45,
        tickmode='array',
        ticks='inside'
    )
)
fig.write_html("humidity_graph.html")
fig.show()
