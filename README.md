# IoT Sensor Anomaly Dashboard

Real-time data pipeline that simulates IoT sensor readings, stores them in PostgreSQL, detects anomalies with a Python ML pipeline, and visualizes everything live through a Streamlit dashboard and a FastAPI REST API — all running on local infrastructure with no cloud dependency.

## Group Members
- Preetham Siddapura Umesh
- Vivek Macharla
- Ekatha Nagesh Hassan
- Harshitha Appaiah
- Anushka Vaidya

## Course
M.Sc. Artificial Intelligence & Big Data
SRH Berlin University of Applied Sciences
Big Data & Business Intelligence — July 2026

---

## Project Overview

Simulated IoT sensor data flows into a PostgreSQL database, is automatically cleaned and analyzed for anomalies using a Python ML pipeline, served through a FastAPI REST API, and visualized live through a Streamlit dashboard (and optionally Tableau).

---

## Architecture — 5 Layers

| Layer | Tool | Purpose |
|-------|------|---------|
| Layer 1 | `simulate.py` + psycopg2 | Generates fake IoT sensor data every 2 seconds |
| Layer 2 | PostgreSQL 18 + PgAdmin 4 | Stores raw, cleaned, and anomaly data |
| Layer 3 | Python + pandas + scikit-learn | ML pipeline for cleaning and anomaly detection |
| Layer 4 | FastAPI + Uvicorn | REST API exposing data on port 8000 |
| Layer 5 | Streamlit + Tableau Desktop | Live web dashboard and BI visualization |

---

## Files in This Project

| File | Description |
|------|-------------|
| `simulate.py` | Generates random temperature and pressure sensor readings every 2 seconds and inserts into PostgreSQL |
| `ml_pipeline.py` | Reads new rows, cleans data, computes z-scores, flags anomalies |
| `dashboard.py` | Streamlit live web dashboard at `localhost:8501` |
| `api.py` | FastAPI server exposing `/data`, `/anomalies`, `/cleaned` endpoints at port 8000 |
| `1_setup_db.sql` | SQL script to create all 3 tables in PostgreSQL |

---

## Prerequisites

- Python 3.10+
- PostgreSQL 18
- PgAdmin 4
- Tableau Desktop (trial version, optional)

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vivekreddy-25/iot-sensor-anomaly-dashboard.git
cd iot-sensor-anomaly-dashboard
```

2. Create and activate a virtual environment:
```bash
python3 -m venv topic6_env
source topic6_env/bin/activate      # macOS/Linux
topic6_env\Scripts\activate         # Windows
```

3. Install required Python packages:
```bash
pip install psycopg2-binary pandas scikit-learn streamlit fastapi uvicorn
```

4. Set up the PostgreSQL database:
   - Open PgAdmin
   - Create a database named `topic6_demo`
   - Open the Query Tool and run `1_setup_db.sql`

5. Set your database credentials as environment variables instead of hardcoding them (recommended before pushing/sharing code):
```bash
export DB_NAME=topic6_demo
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
```

---

## How to Run

Open 4 separate terminal tabs and run each command:

**Terminal 1 — Data Simulator:**
```bash
python3 simulate.py
```

**Terminal 2 — ML Pipeline:**
```bash
python3 ml_pipeline.py
```

**Terminal 3 — FastAPI Server:**
```bash
uvicorn api:app --reload --port 8000
```

**Terminal 4 — Streamlit Dashboard:**
```bash
streamlit run dashboard.py
```

---

## Access the System

| Tool | URL |
|------|-----|
| Streamlit Dashboard | http://localhost:8501 |
| FastAPI Swagger UI | http://localhost:8000/docs |
| FastAPI Anomalies | http://localhost:8000/anomalies |
| FastAPI Raw Data | http://localhost:8000/data |
| FastAPI Cleaned Data | http://localhost:8000/cleaned |

---

## Tableau Connection (Optional)

1. Open Tableau Desktop
2. Connect → More → PostgreSQL
3. Fill in:
   - Server: `localhost`
   - Port: `5432`
   - Database: `topic6_demo`
   - Username: `postgres`
   - Password: (your password)
4. Select Live connection mode
5. Drag the `cleaned_data` table onto the canvas
6. Set `Processed At` on Columns, `AVG Temperature` on Rows
7. Color by `Is Anomaly` field

---

## Database Tables

| Table | Description |
|-------|-------------|
| `sensor_data` | Raw readings — temperature, pressure, timestamp |
| `cleaned_data` | Processed rows with z-scores and anomaly flags |
| `anomaly_log` | Only flagged records with reason for flagging |

---

## Anomaly Detection Logic

- Z-score formula: `z = (value - mean) / standard deviation`
- Flag if absolute z-score > 2.5
- Flag if temperature > 50°C
- Flag if pressure < 20 hPa
- Normal temperature range: 22°C to 48°C
- Anomaly temperature range: 65°C to 90°C
- ~12% probability of anomaly per reading

---

## Modules Used

| Module | Purpose |
|--------|---------|
| psycopg2 | Connect Python to PostgreSQL |
| pandas | Data cleaning and dataframe operations |
| numpy | Mathematical calculations for z-score |
| scikit-learn | ML library for statistical processing |
| fastapi | Build REST API endpoints |
| uvicorn | Run FastAPI server |
| streamlit | Build live web dashboard |
| random | Generate fake sensor readings |
| time | Control insert interval |
| datetime | Timestamp each reading |

---

## Expected Output

- PostgreSQL database continuously growing with live sensor readings
- ML pipeline automatically detecting and logging anomalous readings
- Streamlit dashboard showing live temperature chart and anomaly count
- FastAPI returning live JSON data from all endpoints
- Tableau chart showing an orange anomaly line and blue normal line connected live to PostgreSQL
