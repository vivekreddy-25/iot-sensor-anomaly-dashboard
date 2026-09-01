import streamlit as st
import psycopg2
import pandas as pd

st.set_page_config(page_title="Topic 6 — Live Dashboard", layout="wide")
st.title("🌡️ Real-Time Sensor Dashboard")

def get_conn():
    return psycopg2.connect(
        dbname="topic6_demo", user="postgres",
        password="root", host="localhost", port=5432
    )

# Auto-refresh every 3 seconds
st.markdown("Auto-refreshing every 3 seconds...")

conn = get_conn()

col1, col2, col3 = st.columns(3)
df = pd.read_sql("SELECT * FROM sensor_data ORDER BY ts DESC LIMIT 100", conn)
df_anom = pd.read_sql("SELECT * FROM anomaly_log ORDER BY detected_at DESC LIMIT 20", conn)

col1.metric("Total Readings", len(df))
col2.metric("Anomalies Detected", len(df_anom))
col3.metric("Latest Temp (°C)", f"{df['temperature'].iloc[0]:.2f}" if not df.empty else "—")

st.subheader("📈 Live Temperature Chart")
chart_df = df[["ts", "temperature"]].sort_values("ts")
st.line_chart(chart_df.set_index("ts")["temperature"])

st.subheader("⚠️ Anomaly Log")
if not df_anom.empty:
    st.dataframe(df_anom[["sensor_id", "temperature", "pressure", "reason", "detected_at"]],
                use_container_width=True)
else:
    st.info("No anomalies detected yet...")

conn.close()
st.caption(f"Last refreshed: {pd.Timestamp.now().strftime('%H:%M:%S')}")

st.button("🔄 Refresh")
