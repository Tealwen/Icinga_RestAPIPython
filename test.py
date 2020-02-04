import mysql.connector

db = mysql.connector.connect(host="localhost",
                            user="felix",password="felix22",
                            database="srtest2")

cursor =db.cursor()

cursor.execute("SELECT * FROM switches")

result = cursor.fetchall()

for x in result:
    print(x)

