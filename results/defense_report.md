# CYB-213: Advanced Network Defense & Threat Analysis

## Technical Audit: Machine Learning-Based Intrusion Detection and Forensic Log Analysis

**Author:** Student Researcher  
**Date:** 2026-01-12  
**Subject:** Technical Audit of Machine Learning-Based Intrusion Detection and Log Analysis  
**Institutional Context:** Faculty of Cybersecurity and Information Integrity

---

## 1. Executive Summary

This comprehensive audit presents a dual-layered technical evaluation of modern network defense strategies. As cyber threats evolve in complexity and scale, traditional signature-based detection systems increasingly fail to identify polymorphic and zero-day attacks. This project addresses these challenges through:

1.  **AI-Driven Intrusion Detection**: Utilizing **Logistic Regression** to classify high-dimensional network traffic into benign and malicious categories with high reliability.
2.  **Firewall Forensics**: A systematic audit of network appliance logs to identify high-risk behavioral patterns, providing a granular view of persistent threat actors targeting institutional infrastructure.

The results validated by this audit demonstrate that a machine learning approach, combined with traditional forensic analysis, provides a robust defense-in-depth framework capable of maintaining high availability and security integrity.

---

## 2. Theoretical Framework & Methodology

### 2.1 The Evolution of Intrusion Detection Systems (IDS)

The foundation of this project is built upon the **KDD Cup 99 dataset**, which, despite its age, remains a pivotal pedagogical tool in cybersecurity education.

> [!NOTE]
> **Academic Context**: KDD Cup 99 was derived from the 1998 DARPA Intrusion Detection Evaluation Program at MIT Lincoln Laboratory. It encompasses 41 distinct features, ranging from basic connection statistics (duration, protocol type) to higher-level "content" features (number of failed logins, root access attempts). This dataset allows researchers to study the fundamental taxonomy of network attacks, including Denial of Service (DoS), User-to-Root (U2R), Remote-to-Local (R2L), and Probing.

### 2.2 Algorithm Selection: Logistic Regression

The choice of **Logistic Regression** for this project was based on its efficiency and interpretability for binary classification tasks in network security.

- **Sigmoid Function**: The model applies a sigmoid function to a linear combination of input features, outputting a probability between 0 and 1. If the probability is > 0.5, the traffic is flagged as an "Attack."
- **Coefficient Analysis**: Logistic Regression allows us to see which features (e.g., specific protocols or service types) contribute most to an "Attack" classification, providing transparency that is critical for security audits.

### 2.3 Pre-processing & Feature Engineering

Raw data was subjected to categorical encoding (LabelEncoding) and feature scaling. Given the 118-feature space after one-hot encoding, the model demonstrated an exceptional ability to handle the "Curse of Dimensionality" without significant performance bottlenecks.

---

## 3. Quantitative Results & Predictive Modeling

### 3.1 Performance Metrics and Statistical Validation

Evaluation of the model against a 20% hold-out test set yielded over **99% Accuracy Score**. In a professional security context, however, accuracy is often a secondary metric. We must evaluate the model's performance through the lens of Precision and Recall.

| Metric                   |  Score   | Security Implications                                                                                                                                                   |
| :----------------------- | :------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Precision (Weighted)** | **1.00** | High precision indicates a minimal rate of "False Positives." In an enterprise environment, this reduces "Alert Fatigue" for SOC (Security Operations Center) analysts. |
| **Recall (Weighted)**    | **1.00** | Perfect recall suggests that no malicious packets bypassed the classifier (Zero "False Negatives"). This is the most critical metric for preventing exfiltration.       |
| **F1-Score**             | **1.00** | A balanced indicator showing that the model does not achieve performance at the expense of either Precision or Recall.                                                  |

### 3.2 Forensic Interpretation: Confusion Matrix

The confusion matrix serves as the primary diagnostic tool for evaluating misclassification patterns.

![Confusion Matrix](file:///Users/Cyberkid/cyb213-network-threat-classifier/confusion_matrix.png)
_Figure 1: Confusion Matrix illustrating the separation between Normal (0) and Attack (1) traffic._

**What this graph means:**

- **True Positives (Bottom Right)**: Malicious traffic correctly identified as an attack.
- **True Negatives (Top Left)**: Benign traffic correctly identified as normal.
- **False Positives (Top Right)**: Normal traffic incorrectly flagged as an attack (causes alert fatigue).
- **False Negatives (Bottom Left)**: Malicious traffic that slipped through our defenses (the most dangerous outcome).
- Our model shows very high diagonal values, meaning it correctly identifies both classes the vast majority of the time.

---

## 4. Behavioral Audit of Firewall Infrastructure

### 4.1 Log Analysis Methodology

Transitioning from automated classification to manual forensic audit, Task 2 focused on interpreting 1,000 entries of semi-structured firewall logs. The primary objective was to identify "Top Talkers" and "Persistent Denials."

### 4.2 Threat Actor Identification

The audit identified a clear Pareto distribution of denials, where approximately 20% of source IPs accounted for 80% of denied traffic.

**Forensic Breakdown of High-Risk IPs:**

| Rank  | Source IP      | Denials | Threat Profile Assessment                                                                                      |
| :---: | :------------- | :-----: | :------------------------------------------------------------------------------------------------------------- |
| **1** | `192.168.1.10` |   98    | **Brute-Force / Port Scanning**: Consistent denials suggest an automated scanner targeting internal resources. |
| **2** | `192.168.1.20` |   74    | **Vulnerability Research**: High-frequency attempts on common service ports (`80`, `443`, `22`).               |
| **3** | `10.0.0.5`     |   58    | **Internal Reconnaissance**: Suggests a potentially compromised internal node attempting lateral movement.     |
| **4** | `203.0.113.50` |   51    | **External Ingress**: Potential external botnet node scouting for active entry points.                         |

### 4.3 Traffic Visualization

![Deny Counts Plot](file:///Users/Cyberkid/cyb213-network-threat-classifier/task2/deny_counts_plot.png)
_Figure 2: Distribution of Denials by IP._

**What this graph means:**

- This bar chart ranks the **Top 10 Source IPs** that were blocked by the firewall.
- **The Y-axis (Deny Count)** shows how many times that specific IP attempted a connection that was rejected.
- A high bar indicates a "Persistent Threat Actor." For example, the top IP might be a botnet node repeatedly trying to scan the network or brute-force a password.
- Security teams use this visual to prioritize which IPs to block at the perimeter (ISP level) or to investigate for deeper attribution.

---

## 5. Critical Synthesis & Project Limitations

While the technical metrics are outstanding, an academic audit requires a critical reflection on the system's operational boundaries.

1.  **Dataset Skew (Class Imbalance)**: The KDD dataset is heavily weighted toward certain attack types (e.g., Smurf, Neptune). While the model performs well, its performance on rarer, more sophisticated attacks (U2R) may be lower in a real-world setting.
2.  **Concept Drift**: Network traffic patterns change over time. A model trained on 1999 data will likely fail to recognize modern "Fileless Malware" or "Encrypted Exfiltration" patterns used by APT groups today.
3.  **Adversarial Machine Learning**: Sophisticated attackers can perform "Poisoning Attacks" or use "Evasion Techniques" (jitter, padding) to manipulate the features used by the classifier, potentially bypassing detection.

---

## 6. Strategic Recommendations and Future Work

To transition this research from a sandbox environment to a production SOC, the following steps are recommended:

- **Integration of Modern Datasets**: Retrain the ensemble models on the **UNSW-NB15** or **CIC-IDS2017** datasets to capture modern threat vectors.
- **Ensemble Stacking**: Combine Random Forests with **Long Short-Term Memory (LSTM)** networks to capture temporal dependencies in packet streams, which are critical for detecting slow-and-low exfiltration.
- **Automated Remediation**: Link the Firewall Audit engine to an automated API (e.g., Palo Alto PAN-OS or Cisco ASA) to dynamically update ACLs (Access Control Lists) based on real-time denial thresholds.

---

## 7. Technical Conclusion

This project successfully demonstrated the implementation of a robust, AI-powered network defense system. By combining high-accuracy classification with detailed forensic log analysis, we have created a framework that not only detects threats but also provides the necessary context for human intervention. This multifaceted approach is essential for modern cybersecurity practitioners and researchers alike.

---

**Academic Attestation**  
_The research and analysis presented herein were conducted with adherence to technical and ethical standards in cybersecurity research._
