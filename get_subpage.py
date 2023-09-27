import mysql.connector
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

db_connection = mysql.connector.connect(
    host = "localhost",
    port = "3306",
    user = "root",
    password = "",
    database = "typhoon"
)

url_base = "http://agora.ex.nii.ac.jp/digital-typhoon/summary/wnp/i/"
url_tail = ".html.en"

cursor = db_connection.cursor()
cursor.execute("SELECT id, number FROM typhoon_data")

for row in cursor.fetchall():
    typhoon_id, typhoon_number = row
    url = url_base + str(typhoon_number) + url_tail
    res = requests.get(url)
    html_content = res.text
    soup = BeautifulSoup(html_content, 'html.parser')
    area_tag = soup.find('area', {'shape': 'rect'})
    if area_tag:
        href = area_tag.get('href')
        href_head = "http://agora.ex.nii.ac.jp" + href[:34]
        href_tail = href[-28:]

        cursor.execute("SELECT time FROM timetable WHERE tid = %s", (typhoon_id,))
        time_rows = cursor.fetchall()
        time_str_list = []
        for time_row in time_rows:
            time_datetime = time_row[0]
            time_str = time_datetime.strftime("%y%m%d%H")
            time_str_list.append(time_str)

        for time_now in time_str_list:
            datetime_now = datetime.strptime(time_now, "%y%m%d%H")
            sub_url = href_head + time_now + href_tail
            sub_res = requests.get(sub_url)
            html_text = sub_res.text
            soup = BeautifulSoup(html_text, 'html.parser')

            data = {}
            table_rows = soup.find_all('tr')
            for i in range(len(table_rows)):
                row = table_rows[i]
                th = row.find('th', class_='META')
                if th:
                    key = th.text.strip()
                    td = table_rows[i + 1].find('td', class_='META')
                    if td:
                        value = td.text.strip()
                        data[key] = value

            latitude = data.get('Latitude')
            longitude = data.get('Longitude')
            central_pressure = data.get('Central Pressure')
            if central_pressure is not None:
                central_pressure = central_pressure.replace('hPa', '').strip()
            maximum_wind = data.get('Maximum Wind')
            if maximum_wind is not None:
                maximum_wind = maximum_wind.replace('kt', '').strip()

            update_query = """
                UPDATE timetable
                SET 
                    url = %s,
                    Latitude = %s,
                    Longitude = %s,
                    `Central Pressure` = %s,
                    `Maximum Wind` = %s
                WHERE tid = %s AND time = %s
                """
            cursor.execute(update_query,
                           (sub_url, latitude, longitude, central_pressure, maximum_wind, typhoon_id, datetime_now))
            print(time_now)
        db_connection.commit()
        continue
db_connection.close()