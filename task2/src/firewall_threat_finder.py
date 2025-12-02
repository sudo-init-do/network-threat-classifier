import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os

# Batch mode flag
parser = argparse.ArgumentParser()
parser.add_argument('--batch', action='store_true', help='Run in batch mode (no interactive plot)')
args = parser.parse_args()

# Step 1: Load sample firewall logs (with auto-generate if missing)
log_path = 'task2/data/sample_firewall_logs.csv'
if not os.path.exists(log_path):
    print("CSV missing—auto-generating synthetic logs...")
    # Auto-generate here
    np.random.seed(42)
    n_logs = 1000
    start_time = datetime(2025, 11, 28, 9, 0, 0)
    timestamps = [start_time + timedelta(seconds=np.random.randint(0, 3600)) for _ in range(n_logs)]
    src_ips = np.random.choice(['192.168.1.10', '192.168.1.20', '10.0.0.5', '203.0.113.50', '198.51.100.1'], n_logs, p=[0.3, 0.3, 0.2, 0.1, 0.1])
    dst_ip = '192.168.1.1'
    ports = np.random.choice([22, 80, 443, 3389, 21], n_logs)
    actions = np.random.choice(['ACCEPT', 'DENY'], n_logs, p=[0.7, 0.3])
    reasons = np.random.choice(['OK', 'INVALID', 'AUTH_FAIL', 'PORT_SCAN', 'FLOOD'], n_logs)
    for i in range(n_logs):
        if src_ips[i] == '203.0.113.50' and ports[i] == 22:
            actions[i] = 'DENY'
            reasons[i] = 'PORT_SCAN'
        if src_ips[i] == '198.51.100.1' and ports[i] == 22:
            actions[i] = 'DENY'
            reasons[i] = 'AUTH_FAIL'
    logs = pd.DataFrame({
        'timestamp': timestamps,
        'src_ip': src_ips,
        'dst_ip': dst_ip,
        'port': ports,
        'action': actions,
        'reason': reasons
    })
    os.makedirs('task2/data', exist_ok=True)
    logs.to_csv(log_path, index=False)
    print(f"Generated and saved {len(logs)} logs to {log_path}")
else:
    logs = pd.read_csv(log_path, parse_dates=['timestamp'])

print(f"Loaded {len(logs)} log entries.")
print(logs.head())

# Step 2: Extract patterns with regex
ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
logs['src_ip_extracted'] = logs['src_ip'].astype(str).str.extract(ip_pattern)[0].fillna('')
logs['time_window'] = logs['timestamp'].dt.floor('1min')

# Step 3: Detect threats
threats = []

# Pattern 1: Port Scan - >8 DENY from same IP on same port in 1 min
scan_logs = logs[(logs['action'] == 'DENY') & (logs['reason'].str.contains('PORT_SCAN|INVALID', na=False))]
scan_counts = scan_logs.groupby(['src_ip_extracted', 'port', 'time_window']).size().reset_index(name='count')
scans = scan_counts[scan_counts['count'] > 8]
for _, row in scans.iterrows():
    threats.append({
        'type': 'Port Scan',
        'ip': row['src_ip_extracted'],
        'port': row['port'],
        'count': row['count'],
        'window': row['time_window']
    })

# Pattern 2: Brute Force - >4 AUTH_FAIL from same IP on port 22 in 1 min
brute_logs = logs[(logs['action'] == 'DENY') & (logs['reason'].str.contains('AUTH_FAIL', na=False)) & (logs['port'] == 22)]
brute_counts = brute_logs.groupby(['src_ip_extracted', 'time_window']).size().reset_index(name='count')
brutes = brute_counts[brute_counts['count'] > 4]
for _, row in brutes.iterrows():
    threats.append({
        'type': 'Brute Force',
        'ip': row['src_ip_extracted'],
        'port': 22,
        'count': row['count'],
        'window': row['time_window']
    })

# Pattern 3: Flood/High Volume - >40 total DENY from IP in 1 min
flood_counts = logs[logs['action'] == 'DENY'].groupby(['src_ip_extracted', 'time_window']).size().reset_index(name='count')
floods = flood_counts[flood_counts['count'] > 40]
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
    print("\nNo threats detected in sample. (Try lowering thresholds or rerunning with different seed.)")

# Overall stats
deny_counts = logs[logs['action'] == 'DENY'].groupby('src_ip_extracted').size().sort_values(ascending=False)
print(f"\nTop Deny IPs:\n{deny_counts.head()}")

# Step 5: Plot denies per IP (batch mode skips show)
plt.figure(figsize=(8, 5))
deny_counts.head(10).plot(kind='bar')
plt.title('Top 10 IPs by Number of Denies')
plt.xlabel('Source IP')
plt.ylabel('Deny Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('task2/deny_counts_plot.png')
if not args.batch:
    plt.show()
else:
    plt.close()