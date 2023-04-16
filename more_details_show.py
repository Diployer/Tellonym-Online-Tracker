from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    with open('online_status.txt', 'r') as file:
        data = file.readlines()

    online_events = []
    offline_events = []
    
    for line in data:
        timestamp, _, status = line.strip().partition(' Online Status: ')
        timestamp = datetime.datetime.strptime(timestamp.strip(), '%Y-%m-%d %H:%M:%S')

        if status == 'Online':
            online_events.append(timestamp)
        elif status == 'Offline':
            offline_events.append(timestamp)
            
    hourly_frequency = [0] * 24

    for event in online_events:
        hourly_frequency[event.hour] += 1

    most_popular_hour = hourly_frequency.index(max(hourly_frequency))

    online_durations = []
    offline_durations = []

    for online, offline in zip(online_events, offline_events):
        online_durations.append((offline - online).total_seconds())
        if len(offline_events) > len(online_events):
            offline_durations.append((online_events[1] - offline).total_seconds())

    for i in range(len(online_events) - 1):
        online_durations.append((offline_events[i] - online_events[i]).total_seconds())
        offline_durations.append((online_events[i + 1] - offline_events[i]).total_seconds())

    online_durations.append((offline_events[-1] - online_events[-1]).total_seconds())
    if len(offline_events) > len(online_events):
        offline_durations.append((online_events[0] - offline_events[-1]).total_seconds())

    average_online_duration = sum(online_durations) / len(online_durations)
    average_offline_duration = sum(offline_durations) / len(offline_durations)



    longest_online_duration = max(online_durations)
    longest_offline_duration = max(offline_durations)

    longest_online_duration_index = online_durations.index(longest_online_duration)
    longest_online_start = online_events[longest_online_duration_index]
    longest_online_end = offline_events[longest_online_duration_index]
    longest_offline_duration_index = offline_durations.index(longest_offline_duration)
    longest_offline_start = offline_events[longest_offline_duration_index]
    longest_offline_end = online_events[longest_offline_duration_index + 1]

   
    def format_time(seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours)} Hours {int(minutes)} minutes {int(seconds)} seconds"



    return render_template('index.html', 
        hourly_frequency=hourly_frequency,
        most_popular_hour=most_popular_hour,
        average_online_duration=format_time(average_online_duration),
        average_offline_duration=format_time(average_offline_duration),
        longest_online_duration_formatted=format_time(longest_online_duration),
        longest_online_start=longest_online_start,
        longest_online_end=longest_online_end,
        longest_offline_duration_formatted=format_time(longest_offline_duration),
        longest_offline_start=longest_offline_start,
        longest_offline_end=longest_offline_end)

@app.route('/about')
def about():
    return "<h1>About page</h1><p>This is a simple Flask web application for analyzing online and offline events.</p>"

if __name__ == '__main__':
    app.run(debug=True)
