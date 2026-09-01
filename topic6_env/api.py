from fastapi import FastAPI
import psycopg2
import psycopg2.extras

app = FastAPI()

def get_conn():
    return psycopg2.connect(
        dbname="topic6_demo", user="postgres",
        password="root", host="localhost", port=5432
    )

@app.get("/")
def root():
    return {"message": "Topic 6 - Real-Time Sensor API is running!"}

@app.get("/data")
def get_data():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM sensor_data ORDER BY ts DESC LIMIT 50")
    rows = cur.fetchall()
    conn.close()
    return {"total": len(rows), "data": [dict(r) for r in rows]}

@app.get("/anomalies")
def get_anomalies():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM anomaly_log ORDER BY detected_at DESC LIMIT 20")
    rows = cur.fetchall()
    conn.close()
    return {"total_anomalies": len(rows), "anomalies": [dict(r) for r in rows]}

@app.get("/cleaned")
def get_cleaned():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM cleaned_data ORDER BY processed_at DESC LIMIT 50")
    rows = cur.fetchall()
    conn.close()
    return {"total": len(rows), "data": [dict(r) for r in rows]}
