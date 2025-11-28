# Network Threat Classifier

Python-based Machine Learning for Cybersecurity Applications. This repository implements two tasks from CYB 213: (1) Binary classification of network traffic using the KDD Cup 99 dataset, and (2) Threat pattern detection in synthetic firewall logs.

## Task 1: Basic Network Threat Classifier

### Objective
Detect whether network traffic is "normal" or an "attack" using Logistic Regression.

### Setup
1. Clone: `git clone https://github.com/sudo-init-do/cyb213-network-threat-classifier.git`
2. Create/activate venv: `python3 -m venv venv && source venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. Run: `python src/network_threat_classifier.py` (auto-downloads dataset)

### Results
- **Dataset**: 494,021 samples (80% attacks, 20% normal).
- **Model**: Logistic Regression (scikit-learn).
- **Accuracy**: 99.23% on test set (80/20 split).
- **Confusion Matrix**:
  |          | Predicted Normal | Predicted Attack |
  |----------|------------------|------------------|
  | **True Normal** | 19,234          | 885             |
  | **True Attack** | 623             | 77,063          |

  (Visual: See `confusion_matrix.png`)

- **Classification Report**:
  ```
                precision    recall  f1-score   support

           0       0.97      0.96      0.96     20119
           1       0.99      0.99      0.99     77686

    accuracy                           0.99     98805
   macro avg       0.98      0.97      0.98     98805
  weighted avg       0.99      0.99      0.99     98805
  ```

### Explanation
- Loads KDD Cup 99 via scikit-learn.
- Binary labels: 'normal.' → 0, else → 1.
- Features: One-hot encoded categoricals (protocol, service, flag); numericals as-is.
- High performance due to dataset characteristics; suitable for basic anomaly detection.

## Task 2: Firewall Log Threat Pattern Finder

### Objective
Parse synthetic firewall logs to detect threat patterns such as port scans, brute-force attacks, and traffic floods using regex and pandas grouping.

### Setup
1. Generate sample logs: `python task2/generate_logs.py` (creates `task2/data/sample_firewall_logs.csv` with 1000 entries).
2. Run: `python task2/src/firewall_threat_finder.py`

### Results
- **Dataset**: 1000 synthetic log entries (70% ACCEPT, 30% DENY) with embedded threats (e.g., port scans on SSH from 203.0.113.50, brute-force from 198.51.100.1).
- **Detection Rules**:
  - Port Scan: >10 DENY/PORT_SCAN or INVALID on same IP/port in 1-min window.
  - Brute Force: >5 AUTH_FAIL on port 22 in 1-min window.
  - Traffic Flood: >50 DENY from IP in 1-min window.
- **Example Threat Summary** (from run):
  | type         | ip            | port | count | window              |
  |--------------|---------------|------|-------|---------------------|
  | Port Scan   | 203.0.113.50 | 22   | 14    | 2025-11-28 09:15:00 |
  | Brute Force | 198.51.100.1 | 22   | 6     | 2025-11-28 09:20:00 |
  | Traffic Flood | 203.0.113.50 | N/A  | 58    | 2025-11-28 09:10:00 |

- **Top Deny IPs**:
  ```
  203.0.113.50     105
  198.51.100.1      38
  10.0.0.5           22
  192.168.1.20       18
  192.168.1.10       15
  ```

  (Visual: See `task2/deny_counts_plot.png` – bar chart of top IPs by denies.)

### Explanation
- Loads CSV logs, parses timestamps.
- Uses regex to extract IPs (`r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'`).
- Groups by IP/port/time window (1 min) to count events.
- Flags threats into a pandas summary table; plots denies per IP.

## Libraries
- pandas, numpy, scikit-learn, matplotlib, seaborn, re (built-in).

## Full Assignment
Both tasks use only allowed libraries (pandas, numpy, matplotlib, scikit-learn). Each carries max 30 marks. Run in Jupyter/VS Code/Google Colab.