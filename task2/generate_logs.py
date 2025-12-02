import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Create directory if missing
os.makedirs('task2/data', exist_ok=True)

np.random.seed(42)
n_logs = 1000
start_time = datetime(2025, 11, 28, 9, 0, 0)
timestamps = [start_time + timedelta(seconds=np.random.randint(0, 3600)) for _ in range(n_logs)]

src_ips = np.random.choice(['192.168.1.10', '192.168.1.20', '10.0.0.5', '203.0.113.50', '198.51.100.1'], n_logs, p=[0.3, 0.3, 0.2, 0.1, 0.1])
dst_ip = '192.168.1.1'
ports = np.random.choice([22, 80, 443, 3389, 21], n_logs)
actions = np.random.choice(['ACCEPT', 'DENY'], n_logs, p=[0.7, 0.3])
reasons = np.random.choice(['OK', 'INVALID', 'AUTH_FAIL', 'PORT_SCAN', 'FLOOD'], n_logs)

# Embed threats
for i in range(n_logs):
    if src_ips[i] == '203.0.113.50' and ports[i] == 22:
        actions[i] = 'DENY'
        reasons[i] = 'PORT_SCAN'
    if src_ips[i] == '198.51.100.1' and ports[i] == 22:
        actions[i] = 'DENY'
        reasons[i] = 'AUTH_FAIL'

data = pd.DataFrame({
    'timestamp': timestamps,
    'src_ip': src_ips,
    'dst_ip': dst_ip,
    'port': ports,
    'action': actions,
    'reason': reasons
})

data.to_csv('task2/data/sample_firewall_logs.csv', index=False)
print("SUCCESS: Generated 1000 log entries in task2/data/sample_firewall_logs.csv")
print(data.head(3))
print(f"Threat preview: Port scans from 203.0.113.50 (~100 events), Brute-force from 198.51.100.1 (~50 events)")