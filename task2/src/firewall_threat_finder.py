import pandas as pd
import numpy as np
import re
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load sample firewall logs
log_path = 'task2/data/sample_firewall_logs.csv'
logs = pd.read_csv(log_path, parse_dates=['timestamp'])

print(f"Loaded {len(logs)} log entries.")
print(logs.head())

# Step 2: Extract patterns with regex
# Regex for IP validation (simple check)
ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
logs['src_ip_extracted'] = logs['src_ip'].astype(str).str.extract(ip_pattern)[0]

# Group by time window (1 min) for rate analysis
logs['time_window'] = logs['timestamp'].dt.floor('1min')

# Step 3: Detect threats
threats = []

# Pattern 1: Port Scan - >10 DENY from same IP on same port in 1 min
scan_logs = logs[(logs['action'] == 'DENY') & (logs['reason'].str.contains('PORT_SCAN|INVALID', na=False))]
scan_counts = scan_logs.groupby(['src_ip_extracted', 'port', 'time_window']).size().reset_index(name='count')
scans = scan_counts[scan_counts['count'] > 10]
for _, row in scans.iterrows():
    threats.append({
        'type': 'Port Scan',
        'ip': row['src_ip_extracted'],
        'port': row['port'],
        'count': row['count'],
        'window': row['time_window']
    })

# Pattern 2: Brute Force - >5 AUTH_FAIL from same IP on port 22 in 1 min
brute_logs = logs[(logs['action'] == 'DENY') & (logs['reason'].str.contains('AUTH_FAIL', na=False)) & (logs['port'] == 22)]
brute_counts = brute_logs.groupby(['src_ip_extracted', 'time_window']).size().reset_index(name='count')
brutes = brute_counts[brute_counts['count'] > 5]
for _, row in brutes.iterrows():
    threats.append({
        'type': 'Brute Force',
        'ip': row['src_ip_extracted'],
        'port': 22,
        'count': row['count'],
        'window': row['time_window']
    })

# Pattern 3: Flood/High Volume - >50 total DENY from IP in 1 min
flood_counts = logs[logs['action'] == 'DENY'].groupby(['src_ip_extracted', 'time_window']).size().reset_index(name='count')
floods = flood_counts[flood_counts['count'] > 50]
for _, row in floods.iterrows():
    threats.append({
        'type': 'Traffic Flood',
        'ip': row['src_ip_extracted'],
        'port': 'N/A',
        'count': row['count'],
        'window': row['time_window']
    })

# Step 4: Summary table
threat_df = pd.DataFrame(threats)
if not threat_df.empty:
    print("\nThreat Summary:")
    print(threat_df)
else:
    print("\nNo threats detected in sample.")

# Overall stats
deny_counts = logs[logs['action'] == 'DENY'].groupby('src_ip_extracted').size().sort_values(ascending=False)
print(f"\nTop Deny IPs:\n{deny_counts.head()}")

# Step 5: Plot denies per IP
plt.figure(figsize=(8, 5))
deny_counts.head(10).plot(kind='bar')
plt.title('Top 10 IPs by Number of Denies')
plt.xlabel('Source IP')
plt.ylabel('Deny Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('task2/deny_counts_plot.png')
plt.show()