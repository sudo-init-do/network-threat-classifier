# Network Threat Classifier (Task 1)

Python-based Machine Learning for Cybersecurity Applications. This implements a binary classifier for network traffic using the KDD Cup 99 10% dataset.

## Objective
Detect whether network traffic is "normal" or an "attack" using Logistic Regression.

## Setup
1. Clone: `git clone https://github.com/sudo-init-do/cyb213-network-threat-classifier.git`
2. Create/activate venv: `python3 -m venv venv && source venv/bin/activate`
3. Install: `pip install -r requirements.txt`
4. Run: `python src/network_threat_classifier.py` (auto-downloads dataset)

## Results
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

## Explanation
- Loads KDD Cup 99 via scikit-learn.
- Binary labels: 'normal.' → 0, else → 1.
- Features: One-hot encoded categoricals (protocol, service, flag); numericals as-is.
- High performance due to dataset characteristics; suitable for basic anomaly detection.

## Libraries
- pandas, numpy, scikit-learn, matplotlib, seaborn.

## Future
- Task 2: Firewall Log Threat Pattern Finder.