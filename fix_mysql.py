import mysql.connector

db_connection = mysql.connector.connect(
    host = "localhost",
    port = "3306",
    user = "root",
    password = "",
    database = "typhoon"
)

missing_data = [
    {"id": 22737, "tid": 332, "time": "1991-07-24 19:00:00", "url": "http://agora.ex.nii.ac.jp/cgi-bin/dt/single2.pl?prefix=GMS491072419&id=199109&basin=wnp&lang=en", "Latitude": 17.1, "Longitude": 130.4, "Central Pressure": 985, "Maximum Wind": 50},
    {"id": 63127, "tid": 660, "time": "2004-05-18 05:00:00", "url": "http://agora.ex.nii.ac.jp/cgi-bin/dt/single2.pl?prefix=GOE904051805&id=200402&basin=wnp&lang=en", "Latitude": 17.4, "Longitude": 123.7, "Central Pressure": 940, "Maximum Wind": 90},
    {"id": 100072, "tid": 951, "time": "2016-08-21 01:00:00", "url": "http://agora.ex.nii.ac.jp/cgi-bin/dt/single2.pl?prefix=HMW816082101&id=201609&basin=wnp&lang=en", "Latitude": 28.3, "Longitude": 140.5, "Central Pressure": 985, "Maximum Wind": 50},
    {"id": 100084, "tid": 951, "time": "2016-08-21 13:00:00", "url": "http://agora.ex.nii.ac.jp/cgi-bin/dt/single2.pl?prefix=HMW816082113&id=201609&basin=wnp&lang=en", "Latitude": 31.8, "Longitude": 139.4, "Central Pressure": 980, "Maximum Wind": 55},
    {"id": 100552, "tid": 956, "time": "2016-09-12 14:00:00", "url": "http://agora.ex.nii.ac.jp/cgi-bin/dt/single2.pl?prefix=HMW816091214&id=201614&basin=wnp&lang=en", "Latitude": 19.1, "Longitude": 127.7, "Central Pressure": 910, "Maximum Wind": 105},
    {"id": 100588, "tid": 956, "time": "2016-09-14 02:00:00", "url": "http://agora.ex.nii.ac.jp/cgi-bin/dt/single2.pl?prefix=HMW816091402&id=201614&basin=wnp&lang=en", "Latitude": 21.9, "Longitude": 120.5, "Central Pressure": 910, "Maximum Wind": 105},
    {"id": 100591, "tid": 956, "time": "2016-09-14 05:00:00", "url": "http://agora.ex.nii.ac.jp/cgi-bin/dt/single2.pl?prefix=HMW816091405&id=201614&basin=wnp&lang=en", "Latitude": 22.3, "Longitude": 120.0, "Central Pressure": 910, "Maximum Wind": 105},
    {"id": 100593, "tid": 956, "time": "2016-09-14 07:00:00", "url": "http://agora.ex.nii.ac.jp/cgi-bin/dt/single2.pl?prefix=HMW816091407&id=201614&basin=wnp&lang=en", "Latitude": 22.7, "Longitude": 119.6, "Central Pressure": 930, "Maximum Wind": 90},
    {"id": 100596, "tid": 956, "time": "2016-09-14 10:00:00", "url": "http://agora.ex.nii.ac.jp/cgi-bin/dt/single2.pl?prefix=HMW816091410&id=201614&basin=wnp&lang=en", "Latitude": 23.2, "Longitude": 119.2, "Central Pressure": 930, "Maximum Wind": 90},
    {"id": 100606, "tid": 956, "time": "2016-09-14 20:00:00", "url": "http://agora.ex.nii.ac.jp/cgi-bin/dt/single2.pl?prefix=HMW816091420&id=201614&basin=wnp&lang=en", "Latitude": 24.7, "Longitude": 118.1, "Central Pressure": 965, "Maximum Wind": 70},
    {"id": 100608, "tid": 956, "time": "2016-09-14 22:00:00", "url": "http://agora.ex.nii.ac.jp/cgi-bin/dt/single2.pl?prefix=HMW816091422&id=201614&basin=wnp&lang=en", "Latitude": 24.9, "Longitude": 117.9, "Central Pressure": 965, "Maximum Wind": 70},
    {"id": 100610, "tid": 956, "time": "2016-09-15 00:00:00", "url": "http://agora.ex.nii.ac.jp/cgi-bin/dt/single2.pl?prefix=HMW816091500&id=201614&basin=wnp&lang=en", "Latitude": 25.2, "Longitude": 117.7, "Central Pressure": 980, "Maximum Wind": 55},
    {"id": 100731, "tid": 958, "time": "2016-09-16 17:00:00", "url": "http://agora.ex.nii.ac.jp/cgi-bin/dt/single2.pl?prefix=HMW816091617&id=201616&basin=wnp&lang=en", "Latitude": 22.8, "Longitude": 123.1, "Central Pressure": 940, "Maximum Wind": 85},
]

cursor = db_connection.cursor()

for data in missing_data:
    cursor.execute("""
        UPDATE timetable
        SET 
            url = %s,
            Latitude = %s,
            Longitude = %s,
            `Central Pressure` = %s,
            `Maximum Wind` = %s
        WHERE id = %s AND tid = %s AND time = %s
        """,
        (data["url"], data["Latitude"], data["Longitude"], data["Central Pressure"], data["Maximum Wind"], data["id"], data["tid"], data["time"]))

    print(f"Updated data for id={data['id']}, tid={data['tid']}, time={data['time']}")

db_connection.commit()
db_connection.close()
