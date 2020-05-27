import sqlite3

def connect_to_db():
    connection = sqlite3.connect('local.db')
    return connection

def create_table(connection):
    connection.execute('''CREATE TABLE TEMPERATURE_READINGS
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            READING_DATE DATETIME DEFAULT (strftime('%s','now')*1000),
            TEMPERATURE FLOAT(5));
    ''')
    print("Table TEMPERATURE_READINGS has been created with the following fields: ID, READING_DATE, TEMPERATURE ")
    connection.execute('''CREATE TABLE FEVER_EVENTS
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            START_DATE DATETIME,
            END_DATE DATETIME);
    ''')
    print("Table FEVER_EVENTS has been created with the following fields: ID, START_DATE, END_DATE ")

