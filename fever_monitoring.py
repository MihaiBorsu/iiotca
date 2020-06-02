import db_config
import time
import json
import logging

from firebase import firebase as fb
import plotly.express as px

def check_fever(fever_status):
    connection = db_config.connect_to_db()
    cursor = connection.execute("SELECT TEMPERATURE FROM TEMPERATURE_READINGS ORDER BY ID DESC LIMIT 3")

    if(len(list(cursor)) == 3):
        cursor = connection.execute("SELECT TEMPERATURE, READING_DATE FROM TEMPERATURE_READINGS ORDER BY ID DESC LIMIT 3")
        fever_encourencies = 0
        for row in cursor:
            if(row[0] > 37.3):
                fever_encourencies+=1
        if (fever_encourencies == 3):
            fever_status = True

        cursor = connection.execute("SELECT TEMPERATURE FROM TEMPERATURE_READINGS ORDER BY ID DESC LIMIT 3")
        fever_stop_encourencies = 0
        for row in cursor:
            if(row[0] < 37.3):
                fever_stop_encourencies+=1
        if (fever_stop_encourencies == 3):
            fever_status = False

        return fever_status

    else:
        print("not enough reading yet, please wait...")
    connection.commit()
    connection.close()

def save_fever_event(start_time,end_time):
    command = "INSERT INTO FEVER_EVENTS (START_DATE, END_DATE) VALUES ("+str(start_time)+", "+str(end_time)+");"
    connection = db_config.connect_to_db()
    connection.execute(command)
    connection.commit()
    print("event added in local database")
    connection.close()

def post_to_firebase(start_time):
    firebase = fb.FirebaseApplication('https://fevermonitoring.firebaseio.com/', None)
    data = json.dumps({'timestamp': start_time, 'event': 'FEVER SEQUENCE BEGINNING DETECTED!'})
    result = firebase.post("/events", data)
    print(result)

def post_to_plotly(timestamp, start=False, end=False):
    connection = db_config.connect_to_db()
    cursor = connection.execute("SELECT TEMPERATURE FROM TEMPERATURE_READINGS ORDER BY ID DESC LIMIT 1")

    for row in cursor:
        temperature = row[0]
    if start:
        post_to_plotly.temperatures = []
    post_to_plotly.temperatures.append((timestamp, temperature))
    if end:
        plot = px.scatter(x=[temperature[0] for temperature in post_to_plotly.temperatures], y=[temperature[1] for temperature in post_to_plotly.temperatures])
        plot.write_html('plot_{}.html'.format(post_to_plotly.temperatures[0][0]))

    logging.info('Plotly: timestamp {} temperature {}'.format(timestamp, temperature))
    connection.close()