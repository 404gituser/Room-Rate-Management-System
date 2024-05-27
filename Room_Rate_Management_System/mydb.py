import mysql.connector

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'admin123'
)


cursor_obj = db.cursor()

# cursor_obj.execute('CREATE DATABASE hotel')

print("DB created Sucessfully")

