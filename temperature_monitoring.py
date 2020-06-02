import temperature_sensor
import db_config

def read_temperature():
    temperature = temperature_sensor.read_temp()
    command = "INSERT INTO TEMPERATURE_READINGS (TEMPERATURE) VALUES ("+str(temperature)+");"
    connection = db_config.connect_to_db()
    connection.execute(command)
    connection.commit()
    connection.close()

