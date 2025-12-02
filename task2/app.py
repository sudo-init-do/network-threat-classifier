import streamlit as st
import pandas as pd
import numpy as np
import re
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import io

st.title("🔥 Firewall Log Threat Pattern Finder")
st.write("Upload a CSV log file (columns: timestamp, src_ip, dst_ip, port, action, reason) to detect threats.")

# File uploader
uploaded_file = st.file_uploader("Choose CSV file", type="csv")

if uploaded_file is not None:
    # Load logs
    logs = pd.read_csv(uploaded_file, parse_dates=['timestamp'])
    st.write(f"Loaded {len(logs)} log entries.")
    st.dataframe(logs.head())

    # Regex for IP
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    logs['src_ip_extracted'] = logs['src_ip'].astype(str).str.extract(ip_pattern)[0]
    logs['time_window'] = logs['timestamp'].dt.floor('1min')

    # Detect threats (same logic as script)
    threats = []

    # Port Scan
    scan_logs = logs[(logs['action'] == 'DENY') & (logs['reason'].str.contains('PORT_SCAN|INVALID', na=False))]
    scan_counts = scan_logs.groupby(['src_ip_extracted', 'port', 'time_window']).size().reset_index(name='count')
    scans = scan_counts[scan_counts['count'] > 10]
    for _, row in scans.iterrows():
        threats.append({'type': 'Port Scan', 'ip': row['src_ip_extracted'], 'port': row['port'], 'count': row['count'], 'window': row['time_window']})

    # Brute Force
    brute_logs = logs[(logs['action'] == 'DENY') & (logs['reason'].str.contains('AUTH_FAIL', na=False)) & (logs['port'] == 22)]
    brute_counts = brute_logs.groupby(['src_ip_extracted', 'time_window']).size().reset_index(name='count')
    brutes = brute_counts[brutes['count'] > 5]
    for _, row in brutes.iterrows():
        threats.append({'type': 'Brute Force', 'ip': row['src_ip_extracted'], 'port': 22, 'count': row['count'], 'window': row['time_window']})

    # Traffic Flood
    flood_counts = logs[logs['action'] == 'DENY'].groupby(['src_ip_extracted', 'time_window']).size().reset_index(name='count')
    floods = flood_counts[flood_counts['count'] > 50]
    for _, row in floods.iterrows():
        threats.append({'type': 'Traffic Flood', 'ip': row['src_ip_extracted'], 'port': 'N/A', 'count': row['count'], 'window': row['time_window']})

    threat_df = pd.DataFrame(threats)
    if not threat_df.empty:
        st.subheader("🛑 Detected Threats")
        st.dataframe(threat_df)
    else:
        st.info("No threats detected.")

    # Top Deny IPs Plot
    deny_counts = logs[logs['action'] == 'DENY'].groupby('src_ip_extracted').size().sort_values(ascending=False)
    st.subheader("📊 Top IPs by Deny Count")
    fig, ax = plt.subplots(figsize=(10, 6))
    deny_counts.head(10).plot(kind='bar', ax=ax)
    ax.set_title('Top 10 IPs by Number of Denies')
    ax.set_xlabel('Source IP')
    ax.set_ylabel('Deny Count')
    st.pyplot(fig)

else:
    st.info("👆 Upload a CSV to start analysis. Try the synthetic sample: `task2/data/sample_firewall_logs.csv`.")