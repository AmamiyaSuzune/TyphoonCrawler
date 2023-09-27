import re
import time

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

query = "SELECT id, url FROM timetable"
insert_query = "INSERT INTO images (tid, url, category) VALUES (%s, %s, %s)"
cursor.execute(query)
timetable_rows = cursor.fetchall()

max_retries = 10

for row in timetable_rows:
    tid = row[0]
    url = row[1]

    retries = 0
    success = False

    while retries < max_retries and not success:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            headings = soup.find_all('th', string=re.compile(r'^(Infrared|Visible)'))

            for heading in headings:
                table = heading.find_parent('table')
                img_links = table.find_all('a', class_='IMGLINK')
                for img_link in img_links:
                    img_src = img_link.find('img')['src']
                    img_src = "http://agora.ex.nii.ac.jp" + img_src
                    category = heading.text
                    cursor.execute(insert_query, (tid, img_src, category))
                    print(tid)
                    db_connection.commit()
            success = True
        except requests.exceptions.RequestException as e:
            print(f"Request Exception: {e}")
            retries +=1
            if retries < max_retries:
                print(f"Retrying ({retries}/{max_retries})...")
                time.sleep(1)
cursor.close()
db_connection.close()