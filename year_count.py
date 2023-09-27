#获取年份及当年发生台风次数

import requests
from bs4 import BeautifulSoup
import mysql.connector

db_connection = mysql.connector.connect(
    host = "localhost",
    port = "3306",
    user = "root",
    password = "",
    database = "typhoon"
)

cursor = db_connection.cursor()

base_url = "http://agora.ex.nii.ac.jp/digital-typhoon/year/wnp/"
for year in range(1979, 2024):
    url = base_url + str(year) + ".html.en"
    html = requests.get(url)
    soup = BeautifulSoup(html.text,'html.parser')
    target_input = soup.find('input', {'name': 'ids'})
    value = target_input['value']
    value_list = value.split(':')
    last_number = value_list[-1]
    year = int(last_number[:4])
    count = int(last_number[-2:])

    insert_query = "INSERT INTO dict (year, count) VALUES (%s, %s)"
    values = (year, count)
    cursor.execute(insert_query ,values)
    db_connection.commit()

cursor.close()
db_connection.close()
