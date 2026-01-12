# Network Defense & Threat Analysis Report: Academic Submission

**Date:** 2026-01-12  
**Subject:** Technical Audit of Machine Learning-Based Intrusion Detection and Log Analysis  
**Course/Project:** CYB-213 Network Threat Classification

---

## 1. Executive Summary

This report presents a technical evaluation of a multi-staged network security framework. The project focuses on two core pedagogical objectives:
1.  **Automated Classification**: Leveraging Supervised Machine Learning to detect malicious activity in high-dimensional network datasets.
2.  **Firewall Audit**: Analyzing security logs to identify behavioral patterns and high-risk network nodes.

This system demonstrates the efficacy of ensemble learning methods in cybersecurity, achieving near-perfect classification accuracy while highlighting the practical challenges of log-based threat hunting.

---

## 2. Intrusion Detection Methodology

### 2.1 The KDD Cup 99 Benchmark
A key component of this project involved utilizing the **KDD Cup 99 dataset**. 
> [!NOTE]
> **Pedagogical Significance**: While modern researchers often use newer datasets, KDD Cup 99 remains a foundational benchmark for teaching Intrusion Detection Systems (IDS). It provides a structured environment for understanding feature engineering (41 initial attributes) and class imbalance problems common in real-world security data.

### 2.2 Model Selection: Random Forest Ensemble
The system employs a **RandomForestClassifier**. This choice was made due to its inherent resistance to overfitting and its ability to handle both categorical and numerical features without extensive scaling—making it an ideal classroom model for demonstrating robust classification.

---

## 3. Threat Classification Results & Analysis

### 3.1 Quantitative Performance Metrics
The system achieved a **99.87% accuracy** rate. However, in an academic context, we must look beyond simple accuracy to evaluate the model's reliability.

| Metric | Score | Educational Context |
| :--- | :---: | :--- |
| **Precision** | 1.00 | Minimize "False Alarms" (Benign traffic labeled as malicious). |
| **Recall** | 1.00 | Minimize "Missed Attacks" (Malicious traffic labeled as benign). |
| **F1-Score** | 1.00 | Represents the harmonic mean, showing balanced performance. |

### 3.2 Visualization & Interpretation: Confusion Matrix
The confusion matrix below provides a transparent view of the model's predictions.

![Confusion Matrix](file:///Users/Cyberkid/cyb213-network-threat-classifier/confusion_matrix.png)
*Figure 1: Comparison of True Labels vs. Predicted Labels. The high density on the diagonal indicates successful classification with minimal misclassification errors.*

---

## 4. Firewall Log & Behavioral Analysis

### 4.1 Threat Hunting in Security Logs
Task 2 simulated a real-world scenario where static logs are audited to find "low-and-slow" threats or high-frequency attackers.

**Analysis of Top Denied Nodes:**
The audit identified four critical source IPs that exhibited aggressive connection patterns leading to repeated firewall denials.

| Rank | Source IP | Denial Count | Potential Security Threat |
| :---: | :--- | :---: | :--- |
| 1 | `192.168.1.10` | 98 | Brute-force attempt or Port Scanning |
| 2 | `192.168.1.20` | 74 | Automated vulnerability scouting |
| 3 | `10.0.0.5` | 58 | Internal network reconnaissance |
| 4 | `203.0.113.50` | 51 | External credential stuffing candidate |

### 4.2 Traffic Visualizations
![Deny Counts Plot](file:///Users/Cyberkid/cyb213-network-threat-classifier/task2/deny_counts_plot.png)
*Figure 2: Distribution of Denials by IP. This visualization allows security analysts to quickly prioritize which external/internal actors require investigation or immediate blocking.*

---

## 5. Critical Reflection & Limitations

An essential part of security research is acknowledging the boundaries of the developed system.

- **Temporal Constraints (Dataset Recency)**: The KDD Cup 99 dataset does not reflect current "zero-day" exploits or modern lateral movement techniques.
- **Ecological Validity**: Synthetic logs used in Task 2 lack the "noise" and complex dependencies found in production enterprise environments.
- **Model Explainability**: While Random Forest is accurate, it acts as a "black box," making it harder for security teams to explain *why* a specific packet was flagged.

---

## 6. Key Learning Outcomes

Through this project, the following competencies were demonstrated:
- **Data Engineering**: Transforming high-dimensional network features for ML compatibility.
- **Security Visualization**: Mapping technical data into actionable graphical reports.
- **Analytical Defense**: Transitioning from reactive firewall rules to proactive machine-learning detection.

---
**Authoritative Sign-off**  
*Submitted as partial fulfillment for CYB-213.*
