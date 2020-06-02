import db_config


connection = db_config.connect_to_db()
db_config.create_table(connection)
connection.close()

