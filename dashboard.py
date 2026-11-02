import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from db import get_conn

st.set_page_config(page_title="IoT Sensor Anomaly Dashboard", layout="wide")
st.title("IoT Sensor Anomaly Dashboard")

st_autorefresh(interval=3000, key="r")
st.markdown("Auto-refreshing every 3 seconds...")

conn = get_conn()

col1, col2, col3 = st.columns(3)
df = pd.read_sql("SELECT * FROM sensor_data ORDER BY ts DESC LIMIT 100", conn)
df_anom = pd.read_sql("SELECT * FROM anomaly_log ORDER BY detected_at DESC LIMIT 20", conn)
total = pd.read_sql("SELECT COUNT(*) AS n FROM sensor_data", conn)["n"][0]
n_anom = pd.read_sql("SELECT COUNT(*) AS n FROM anomaly_log", conn)["n"][0]

col1.metric("Total Readings", total)
col2.metric("Anomalies Detected", n_anom)
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
