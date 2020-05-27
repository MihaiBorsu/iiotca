import db_config

# try:
connection = db_config.connect_to_db()
db_config.create_table(connection)
connection.close()
# except:
#     print("connection to local database error")
