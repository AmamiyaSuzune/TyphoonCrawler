import mysql.connector
import sqlite3

db_connection = mysql.connector.connect(
    host = "localhost",
    port = "3306",
    user = "root",
    password = "",
    database = "typhoon"
)

conn = sqlite3.connect('typhoon.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM dict")
result = cursor.fetchall()
for row in result:
    print(row)
cursor.execute("SELECT year, count FROM dict")
year_data = cursor.fetchall()

cursor.execute("CREATE TABLE IF NOT EXISTS typhoon_years (id INTEGER PRIMARY KEY AUTOINCREMENT, year INTEGER NOT NULL, year_and_count INTEGER NOT NULL)")

for year, occurrences in year_data:
    year_and_count = year + count
    cursor.execute("INSERT INTO typhoon_years (year, year_and_count) VALUES (?, ?)", (year, year_and_count))

conn.commit()
conn.close()
