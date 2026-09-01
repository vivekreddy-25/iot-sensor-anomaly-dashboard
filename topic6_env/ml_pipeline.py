import psycopg2, time
import pandas as pd
import numpy as np
from datetime import datetime

conn = psycopg2.connect(
    dbname="topic6_demo",
    user="postgres",
    password="root",
    host="localhost",
    port=5432
)

print("ML Pipeline running... Press Ctrl+C to stop")
last_id = 0

while True:
    cur = conn.cursor()
    cur.execute("""
        SELECT id, temperature, pressure FROM sensor_data
        WHERE id > %s ORDER BY id LIMIT 50
    """, (last_id,))
    rows = cur.fetchall()

    if rows:
        df = pd.DataFrame(rows, columns=["id", "temperature", "pressure"])
        df = df.dropna()
        for col in ["temperature", "pressure"]:
            mean, std = df[col].mean(), df[col].std()
            std = std if std > 0 else 1
            df[f"{col}_zscore"] = (df[col] - mean) / std

        for _, row in df.iterrows():
            reasons = []
            if abs(row["temperature_zscore"]) > 2.5:
                reasons.append(f"temp z={row['temperature_zscore']:.2f}")
            if row["temperature"] > 50:
                reasons.append(f"temp {row['temperature']}°C > 50°C")
            if row["pressure"] < 20:
                reasons.append(f"pressure {row['pressure']} < 20 hPa")

            is_anomaly = len(reasons) > 0

            cur.execute("""
                INSERT INTO cleaned_data
                (sensor_id, temperature, pressure, temp_zscore, pres_zscore, is_anomaly)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (int(row["id"]), float(row["temperature"]), float(row["pressure"]),
                  float(row["temperature_zscore"]), float(row["pressure_zscore"]), is_anomaly))

            if is_anomaly:
                cur.execute("""
                    INSERT INTO anomaly_log (sensor_id, temperature, pressure, reason)
                    VALUES (%s, %s, %s, %s)
                """, (int(row["id"]), float(row["temperature"]), float(row["pressure"]),
                      "; ".join(reasons)))
                print(f"[{datetime.now():%H:%M:%S}] ⚠️  Anomaly — {'; '.join(reasons)}")

        conn.commit()
        last_id = int(df["id"].max())
        print(f"[{datetime.now():%H:%M:%S}] Processed {len(df)} rows")

    cur.close()
    time.sleep(4)
