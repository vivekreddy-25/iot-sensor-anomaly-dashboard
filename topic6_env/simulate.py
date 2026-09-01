import psycopg2, random, time
from datetime import datetime

conn = psycopg2.connect(
    dbname="topic6_demo",
    user="postgres",
    password="root",
    host="localhost",
    port=5432
)
cur = conn.cursor()
print("Simulator running... Press Ctrl+C to stop")

count = 0
while True:
    anomaly = random.random() < 0.12
    temp = round(random.uniform(65, 90), 2) if anomaly else round(random.uniform(22, 48), 2)
    pres = round(random.uniform(10, 15), 2) if anomaly else round(random.uniform(25, 55), 2)
    cur.execute("INSERT INTO sensor_data (temperature, pressure) VALUES (%s, %s)", (temp, pres))
    conn.commit()
    count += 1
    flag = " ⚠️ ANOMALY" if anomaly else ""
    print(f"[{datetime.now():%H:%M:%S}] #{count} temp={temp}°C  pressure={pres} hPa{flag}")
    time.sleep(2)
