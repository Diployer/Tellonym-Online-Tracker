import datetime
from flask import Flask, render_template_string
from collections import defaultdict


app = Flask(__name__)

def parse_data(file_path):
    online_periods = []
    online_start = None
    with open(file_path, "r") as f:
        for line in f.readlines():
            if "Online Status:" in line:
                date_str, status_str = line.strip().split("  Online Status: ")
                dt = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                if "Online" in status_str:
                    online_start = dt
                elif "Offline" in status_str and online_start is not None:
                    online_periods.append((online_start, dt))
                    online_start = None
    return online_periods

file_path = "online_status.txt"
online_periods = parse_data(file_path)

@app.route("/")
def index():
    html_template = '''
    <html>
    <head>
        <style>
            .online { background-color: red; }
            table { border-collapse: collapse; }
            th, td { border: 1px solid black; padding: 4px; }
        </style>
    </head>
    <body>
    <table>
        <tr>
            <th></th>
            {% for day in days %}
                <th>{{ day.strftime('%Y-%m-%d') }}<br>{{ day.strftime('%A') }}</th>
            {% endfor %}
        </tr>
        {% for hour in range(0, 24) %}
            {% for minute in range(0, 60, 10) %}
                <tr>
                    <th>{{ '{:02d}:{:02d}'.format(hour, minute) }}</th>
                    {% for day in days %}
                        <td class="{% if (day, hour, minute) in online_cells %}online{% endif %}"></td>
                    {% endfor %}
                </tr>
            {% endfor %}
        {% endfor %}
    </table>
    '''
   
  

    days = sorted(list(set([period[0].date() for period in online_periods])))
    online_cells = []

    activity_counts = [0] * 24 * 60

    for period in online_periods:
        day = period[0].date()
        start_hour, start_minute = period[0].hour, period[0].minute
        end_hour, end_minute = period[1].hour, period[1].minute

        for hour in range(start_hour, end_hour + 1):
            if hour == start_hour:
                minute = start_minute
            else:
                minute = 0

            while minute < 60:
                if hour == end_hour and minute >= end_minute:
                    break
                online_cells.append((day, hour, minute))
                activity_counts[hour * 60 + minute] += 1
                minute += 1

    most_active_time = activity_counts.index(max(activity_counts))
    return render_template_string(html_template, days=days, online_cells=online_cells, most_active_time=most_active_time)


if __name__ == "__main__":
    app.run(debug=True)

