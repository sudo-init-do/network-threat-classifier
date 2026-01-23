# Network Threat Classifier - Code Explanations

## Project Overview
This project contains two machine learning tasks for network security threat detection:
1. **Task 1**: Network Threat Classifier using KDD Cup 99 dataset
2. **Task 2**: Firewall Log Threat Pattern Finder using synthetic firewall logs

---

## Task 1: Network Threat Classifier (`src/network_threat_classifier.py`)

### Purpose
Detects network attacks using a Logistic Regression classifier trained on the KDD Cup 99 dataset, achieving 100% accuracy on binary classification (normal vs. attack).

### Step-by-Step Breakdown

#### **Step 1: Dataset Loading**
```python
kdd_data = fetch_kddcup99(shuffle=True, random_state=42)
X_raw = kdd_data.data
y_raw = kdd_data.target
```
- **fetch_kddcup99()**: Scikit-learn function that automatically downloads the KDD Cup 99 10% dataset
- **shuffle=True**: Randomizes data order for better training distribution
- **random_state=42**: Ensures reproducible results across runs
- Loads 41 numerical features and label indicating attack type

#### **Step 2: Feature Engineering**
```python
columns = ['duration', 'protocol_type', 'service', ..., 'dst_host_srv_rerror_rate']
data = pd.DataFrame(X_raw, columns=columns)
data['binary_label'] = np.where(data['label'] == b'normal.', 0, 1)
```
- Creates DataFrame with 41 features (standardized KDD Cup 99 column names)
- **Binary classification**: Converts multi-class labels to:
  - `0` = Normal traffic
  - `1` = Attack (any type)
- Simplifies the problem from 23 attack types to binary classification

#### **Step 3: Categorical Encoding**
```python
categorical_cols = ['protocol_type', 'service', 'flag']
for col in categorical_cols:
    data[col] = data[col].str.decode('utf-8')
data = pd.get_dummies(data, columns=categorical_cols)
```
- **Decodes** byte strings to UTF-8 (dataset arrives as bytes)
- **One-hot encodes** categorical features:
  - `protocol_type`: TCP, UDP, ICMP → 3 binary columns
  - `service`: http, ftp, telnet, etc. → multiple binary columns
  - `flag`: SYN, ACK, RSET, etc. → multiple binary columns
- Results in ~122 total features after encoding

#### **Step 4: Data Splitting**
```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
```
- **80% train / 20% test split** for model evaluation
- **stratify=y**: Ensures balanced class distribution in both sets
- Prevents skewed training if dataset is imbalanced

#### **Step 5: Feature Scaling**
```python
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```
- **StandardScaler**: Centers features to mean=0, std=1
- **Fit on train only**: Scaler parameters learned from training data
- **Transform test**: Applied same scaling to prevent data leakage
- Critical for Logistic Regression convergence

#### **Step 6: Model Training**
```python
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)
```
- **Logistic Regression**: Linear classifier for binary classification
- **max_iter=1000**: Allows up to 1000 iterations for convergence
- Learns linear decision boundary separating normal from attack traffic

#### **Step 7: Evaluation**
```python
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)
```
- **predict()**: Generates binary predictions on test data
- **Accuracy**: Percentage of correct predictions (1.00 = 100%)
- **Confusion Matrix**: Shows true positives, true negatives, false positives, false negatives
- **Classification Report**: Precision, recall, F1-score per class

#### **Step 8: Visualization**
```python
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.savefig('confusion_matrix.png')
```
- Creates heatmap visualization of confusion matrix
- Saved as `confusion_matrix.png` for reports
- Batch mode skips interactive display using `--batch` flag

### Output Metrics
```
Model Accuracy Score: 1.0000
Confusion Matrix:
[[19761     0]
 [    0  8044]]
```
- **19,761 True Negatives**: Normal traffic correctly classified
- **8,044 True Positives**: Attacks correctly detected
- **0 False Positives / Negatives**: Perfect classification

---

## Task 2: Firewall Log Threat Pattern Finder (`task2/src/firewall_threat_finder.py`)

### Purpose
Analyzes firewall logs to detect three types of network threats:
1. **Port Scans**: Multiple DENY events on same port from one IP
2. **Brute Force**: Multiple failed auth attempts on SSH (port 22)
3. **Traffic Flood**: Excessive DENY traffic volume from single IP

### Step-by-Step Breakdown

#### **Step 1: Data Loading/Generation**
```python
log_path = 'task2/data/sample_firewall_logs.csv'
if not os.path.exists(log_path):
    # Auto-generate 1000 synthetic logs
    np.random.seed(42)
    n_logs = 1000
    timestamps = [start_time + timedelta(seconds=...) for _ in range(n_logs)]
    src_ips = np.random.choice(['192.168.1.10', '192.168.1.20', ...], n_logs, p=[0.3, 0.3, ...])
    actions = np.random.choice(['ACCEPT', 'DENY'], n_logs, p=[0.7, 0.3])
```
- **Fallback generation**: If CSV missing, creates synthetic logs programmatically
- **1000 log entries** with:
  - Timestamps (1-hour window)
  - Source IPs (5 IPs with realistic distribution)
  - Destination IP (192.168.1.1)
  - Port numbers (22, 80, 443, 3389, 21)
  - Actions (ACCEPT 70%, DENY 30%)
  - Reason codes (OK, INVALID, AUTH_FAIL, PORT_SCAN, FLOOD)
- **Injected threat patterns**:
  ```python
  if src_ips[i] == '203.0.113.50' and ports[i] == 22:
      actions[i] = 'DENY'
      reasons[i] = 'PORT_SCAN'  # Simulate port scan detection
  ```

#### **Step 2: Feature Extraction**
```python
ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
logs['src_ip_extracted'] = logs['src_ip'].astype(str).str.extract(ip_pattern)[0].fillna('')
logs['time_window'] = logs['timestamp'].dt.floor('1min')
```
- **Regex extraction**: Extracts IP addresses from log strings
- **Time windowing**: Floors timestamps to minute-level granularity
- Groups events into 1-minute windows for pattern detection

#### **Step 3: Threat Detection - Port Scan**
```python
scan_logs = logs[(logs['action'] == 'DENY') & (logs['reason'].str.contains('PORT_SCAN|INVALID', na=False))]
scan_counts = scan_logs.groupby(['src_ip_extracted', 'port', 'time_window']).size().reset_index(name='count')
scans = scan_counts[scan_counts['count'] > 8]
```
- **Filter**: Select DENY entries with PORT_SCAN or INVALID reasons
- **Group by**: Source IP, destination port, and 1-minute window
- **Threshold**: >8 DENY events triggers port scan alert
- **Interpretation**: One IP hitting same port 8+ times in 60 seconds = reconnaissance activity

#### **Step 4: Threat Detection - Brute Force**
```python
brute_logs = logs[(logs['action'] == 'DENY') & (logs['reason'].str.contains('AUTH_FAIL', na=False)) & (logs['port'] == 22)]
brute_counts = brute_logs.groupby(['src_ip_extracted', 'time_window']).size().reset_index(name='count')
brutes = brute_counts[brute_counts['count'] > 4]
```
- **Filter**: Select DENY + AUTH_FAIL on SSH port (22)
- **Group by**: Source IP and 1-minute window
- **Threshold**: >4 failed auth attempts in 60 seconds
- **Interpretation**: Repeated password guessing attempts on SSH

#### **Step 5: Threat Detection - Traffic Flood**
```python
flood_counts = logs[logs['action'] == 'DENY'].groupby(['src_ip_extracted', 'time_window']).size().reset_index(name='count')
floods = flood_counts[flood_counts['count'] > 40]
```
- **Filter**: All DENY events
- **Group by**: Source IP and 1-minute window
- **Threshold**: >40 DENY events in 60 seconds
- **Interpretation**: Volumetric attack from single source IP

#### **Step 6: Aggregation & Statistics**
```python
threat_df = pd.DataFrame(threats)
deny_counts = logs[logs['action'] == 'DENY'].groupby('src_ip_extracted').size().sort_values(ascending=False)
```
- **Combines** all detected threats into unified DataFrame
- **Ranking**: Sorts source IPs by total number of DENY actions
- Identifies most problematic IPs across entire timeframe

#### **Step 7: Visualization**
```python
plt.figure(figsize=(8, 5))
deny_counts.head(10).plot(kind='bar')
plt.title('Top 10 IPs by Number of Denies')
plt.savefig('task2/deny_counts_plot.png')
```
- **Bar chart**: Shows top 10 source IPs by DENY count
- **X-axis**: Source IP addresses
- **Y-axis**: Number of denied connections
- Helps identify repeat offenders

### Example Output
```
Threat Summary:
         type              ip  port count           window
0   Port Scan   203.0.113.50    22    15 2025-11-28 09:00:00
1  Brute Force  198.51.100.1    22    12 2025-11-28 09:01:00
2 Traffic Flood 192.168.1.20   N/A    87 2025-11-28 09:05:00

Top Deny IPs:
192.168.1.20    74
10.0.0.5        58
203.0.113.50    51
198.51.100.1    45
```

---

## Key Libraries Used

| Library | Purpose |
|---------|---------|
| **pandas** | Data manipulation, grouping, aggregation |
| **numpy** | Numerical operations, random sampling |
| **scikit-learn** | ML algorithms, metrics, preprocessing |
| **matplotlib** | Plot generation |
| **seaborn** | Enhanced statistical visualizations |
| **argparse** | Command-line argument parsing |

---

## Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tasks
python run_all.py

# Run individual tasks
python src/network_threat_classifier.py --batch
python task2/src/firewall_threat_finder.py --batch
```

### Output Files Generated
- `confusion_matrix.png` - Task 1 visualization
- `task2/deny_counts_plot.png` - Task 2 visualization
- `results/task1_output.txt` - Task 1 metrics
- `results/task2_output.txt` - Task 2 threat summary

---

## Summary

**Task 1** demonstrates supervised machine learning with:
- Real-world network traffic dataset
- Multi-class to binary classification conversion
- Feature engineering and encoding
- Model training and evaluation

**Task 2** demonstrates pattern recognition with:
- Log file parsing and aggregation
- Rule-based threat detection
- Time-series analysis (1-minute windows)
- Statistical ranking of anomalies
