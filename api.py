import flask
import db_config

from flask import request, jsonify, render_template

app = flask.Flask(__name__)
app.config['DEBUG'] = True

hours_ms = 3600000
day_ms = 24 * hours_ms
INVALID_QUERY = ['invalid query args', ]
START_EVENT = 'FEVER_START_EVENT'
END_EVENT = 'FEVER_END_EVENT'


def median(values):
    n = len(values)
    s = sorted(values)
    return (sum(s[n // 2 - 1:n // 2 + 1]) / 2.0, s[n // 2])[n % 2] if n else None

def get_temp_by_duration(start, end, duration):
    connection = db_config.connect_to_db()
    c = connection.cursor()
    rows = [row for row in c.execute("SELECT * FROM TEMPERATURE_READINGS")]
    rows = [row for row in rows[1:] if row]
    aux = [(int(row[0]), int(row[1]), row[2]) for row in rows]
    data = []
    time_slot = []

    for row in aux:
        time = int(row[1])

        if time < start or time > end:
            continue

        while time - start > duration:
            if time_slot:
                data.append(time_slot)
                time_slot = []

            start = start + duration

        time_slot.append([row[1], row[2]])

    if time_slot:
        data.append(time_slot)

    connection.close()
    return data


def get_temperature_aggregation(start, end, aggregation, operator):
    duration = hours_ms if aggregation == 'HOURLY' else day_ms
    temperatures = get_temp_by_duration(start, end, duration)
    result = {'start_date': start, 'end_date': end, 'aggregation_type': aggregation, 'operator_type': operator,
              'measurements': []}

    for temperature in temperatures:
        temp_val = [temp[1] for temp in temperature]
        print(temp_val)

        if operator == 'AVERAGE':
            aggregated_val = sum(temp_val) / len(temp_val)
        elif operator == 'MEDIAN':
            aggregated_val = median(temp_val)
        elif operator == 'MAX':
            aggregated_val = max(temp_val)

        measurement = {'timestamp': temperature[0][0], 'value': aggregated_val}
        result['measurements'].append(measurement)

    return result


def get_raw_temperature(start, end):
    connection = db_config.connect_to_db()
    c = connection.cursor()
    result = {'start_date': start, 'end_date': end, 'measurements': []}
    rows = [row for row in c.execute("SELECT * FROM TEMPERATURE_READINGS")]
    rows = [row for row in rows[1:] if row]
    aux = [(int(row[0]), int(row[1]), row[2]) for row in rows]

    for row in aux:
        time_ms = int(row[1])

        if time_ms >= start and time_ms <= end:
            result['measurements'].append({'timestamp': time_ms, 'value': float(row[2])})

    connection.close()
    return result

def get_raw_temperature_for_event(start, end):
    connection = db_config.connect_to_db()
    c = connection.cursor()
    result = {'event_start': start, 'event_stop': end, 'measurements': []}
    rows = [row for row in c.execute("SELECT * FROM TEMPERATURE_READINGS")]
    rows = [row for row in rows[1:] if row]
    aux = [(int(row[0]), int(row[1]), row[2]) for row in rows]

    for row in aux:
        time_ms = int(row[1])

        if time_ms >= start and time_ms <= end:
            result['measurements'].append({'timestamp': time_ms, 'value': float(row[2])})

    connection.close()
    return result


def get_temp(request):
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))

    if 'aggregation' in request.args and 'operator' in request.args:
        return get_temperature_aggregation(start, end, request.args.get('aggregation'), request.args.get('operator'))

    return get_raw_temperature(start, end)


def get_fever(request):
    connection = db_config.connect_to_db()
    c2 = connection.cursor()
    rows2 = [row for row in c2.execute("SELECT * FROM FEVER_EVENTS")]
    rows2 = [row for row in rows2[1:] if row]
    fever = [(int(row[0]), int(row[1]), row[2]) for row in rows2]

    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    result_measurements = []

    for row in fever:
        result_measurements.append(get_raw_temperature_for_event(row[1],row[2]))

    result = {'start_date': start, 'end_date': end, 'events': result_measurements}
    return result


def check_arguments(request):
    if not 'start' in request.args or not 'end' in request.args:
        return False

    try:
        start = int(request.args.get('start'))
        start = int(request.args.get('end'))
    except:
        return False

    if 'aggregation' in request.args:
        if not 'operator' in request.args:
            return False

        aggregation = request.args.get('aggregation')

        if not aggregation == 'HOURLY' and not aggregation == 'DAILY':
            return False

    if 'operator' in request.args:
        if not 'aggregation' in request.args:
            return False

        operator = request.args.get('operator')

        if not operator == 'AVERAGE' and not operator == 'MEDIAN' and not operator == 'MAX':
            return False

    return True


@app.route('/<requestType>', methods=['GET'])
def get_request(requestType):
    if not check_arguments(request):
        result = INVALID_QUERY
    elif requestType == 'fever':
        result = get_fever(request)
    elif requestType == 'temperature':
        result = get_temp(request)
    else:
        result = ['invalid query type', ]
    return jsonify(result)


def main():
    return render_template('index.html')
    # app.run(port=5051)


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5051)
    # main()