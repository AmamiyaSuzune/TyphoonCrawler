#根据dict中的数据将台风年份及编号插入typhoon_number中
import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    port = "3306",
    user = "root",
    password = "",
    database = "typhoon"
)

cursor = conn.cursor()

select_query = "SELECT year, count FROM dict"
cursor.execute(select_query)

for year, count in cursor.fetchall():
    for i in range(1, count + 1):
        count_str = str(i).zfill(2)

        number = int(str(year) + count_str)

        insert_query = "INSERT INTO typhoon_data (year, number) VALUES (%s, %s)"
        data = (year, number)
        cursor.execute(insert_query, data)

conn.commit()
conn.close()