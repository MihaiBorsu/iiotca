import fever_monitoring
import temperature_monitoring
import time
import db_config


connection = db_config.connect_to_db()
fever_status = False
prv_fever_status = False
print("Initial status not fever, waiting for 10 readings")

while(True):
    temperature_monitoring.read_temperature()
    time.sleep(0.5)
    fever_status = fever_monitoring.check_fever(fever_status)

    if fever_status is True and prv_fever_status is False:
        print("FEVER SEQUENCE BEGINNING DETECTED!")
        cursor = connection.execute("SELECT READING_DATE FROM TEMPERATURE_READINGS ORDER BY ID DESC LIMIT 1")
        for row in cursor:
            start_time = row[0]
        fever_monitoring.post_to_firebase(start_time)
        fever_monitoring.post_to_plotly(start_time, start=True)

    elif fever_status is False and prv_fever_status is True:
        print("FEVER ENDED, 10 READINGS < 37.3")
        cursor = connection.execute("SELECT READING_DATE FROM TEMPERATURE_READINGS ORDER BY ID DESC LIMIT 1")
        for row in cursor:
            end_time = row[0]
        if(start_time is not None):
            fever_monitoring.save_fever_event(start_time,end_time)
        fever_monitoring.post_to_plotly(start_time, end=True)

    elif fever_status is True:
        cursor = connection.execute("SELECT READING_DATE FROM TEMPERATURE_READINGS ORDER BY ID DESC LIMIT 1")
        for row in cursor:
            start_time = row[0]
        fever_monitoring.post_to_plotly(start_time)

    prv_fever_status = fever_status
    time.sleep(0.5)
