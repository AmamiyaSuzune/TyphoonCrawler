#获取某年某号台风时刻数据

from datetime import datetime
from bs4 import BeautifulSoup
import requests
import mysql.connector
import re

db_connection = mysql.connector.connect(
    host = "localhost",
    port = "3306",
    user = "root",
    password = "",
    database = "typhoon"
)

cursor = db_connection.cursor()
cursor.execute("SELECT id, number FROM typhoon_data")

url_base = "http://agora.ex.nii.ac.jp/digital-typhoon/summary/wnp/i/"
url_tail = ".html.en"

for row in cursor.fetchall():
    typhoon_id, typhoon_number = row
    url = url_base + str(typhoon_number) + url_tail

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    area_elements = soup.find_all('area', shape='rect')
    href_contents = [area['href'] for area in area_elements]

    for href_content in href_contents:
        match = re.search(r'prefix=(\w+)', href_content)
        prefix = match.group(1)
        date_str = prefix[4:]
        year_prefix = "19" if int(date_str[:2]) > 24 else "20"
        date_str = year_prefix + date_str
        date_format = "%Y%m%d%H"
        date = datetime.strptime(date_str, date_format)
        insert_query = "INSERT INTO timetable (tid, time) VALUES (%s, %s)"
        cursor.execute(insert_query, (typhoon_id, date))


db_connection.commit()
db_connection.close()