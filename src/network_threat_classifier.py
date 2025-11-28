import pandas as pd
import numpy as np
from sklearn.datasets import fetch_kddcup99
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns  # Optional for better confusion matrix plot; can remove if not allowed

# Step 1: Load the dataset using scikit-learn (auto-downloads 10% subset if needed)
print("Loading KDD Cup 99 10% dataset...")
try:
    kdd_data = fetch_kddcup99(shuffle=True, random_state=42)  # Shuffle for reproducibility
    X_raw = kdd_data.data  # Features as numpy array
    y_raw = kdd_data.target  # Labels as numpy array of strings (bytes)
    print("Dataset loaded successfully via scikit-learn!")
except Exception as e:
    print(f"Auto-load failed: {e}. Falling back to manual file (ensure data/kddcup.data_10_percent exists).")
    # Fallback: Uncomment and fill if needed
    # columns = [ ... ]  # Full columns list
    # data = pd.read_csv('data/kddcup.data_10_percent', names=columns + ['label'], header=None)
    raise e

# Define column names for features (standard for KDD Cup 99)
columns = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent',
    'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root',
    'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login', 'is_guest_login',
    'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
    'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
    'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
    'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
]

# Convert to DataFrame
data = pd.DataFrame(X_raw, columns=columns)
data['label'] = y_raw  # Add labels (bytes)

# Clean labels for printing (strip b'' and .)
data['label_clean'] = data['label'].str.decode('utf-8').str.rstrip('.')

print(f"Dataset shape: {data.shape}")
print(f"Label distribution:\n{data['label_clean'].value_counts().head()}")

# Step 2: Create binary label - 'normal' vs 'attack'
data['binary_label'] = np.where(data['label'] == b'normal.', 0, 1)
data['binary_label'] = data['binary_label'].astype(int)
print(f"Binary label distribution:\n{data['binary_label'].value_counts()}")

# Step 3: Feature extraction and preprocessing
# Clean categorical features from bytes to strings (no int conversion needed)
categorical_cols = ['protocol_type', 'service', 'flag']
for col in categorical_cols:
    data[col] = data[col].str.decode('utf-8')

# One-hot encode categorical columns (works directly on strings)
data = pd.get_dummies(data, columns=categorical_cols)

# Drop original labels (keep binary)
data = data.drop(['label', 'label_clean'], axis=1)

# Features (X) and target (y)
X = data.drop('binary_label', axis=1)
y = data['binary_label']

print(f"Processed features shape: {X.shape}")  # ~122 columns after one-hot

# Step 4: Split the data into train and test sets (80/20 split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")

# Step 5: Train Logistic Regression model
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)

# Step 6: Predict on test set
y_pred = model.predict(X_test)

# Step 7: Evaluate the model
acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"\nModel Accuracy Score: {acc:.4f}")
print("\nConfusion Matrix:")
print(cm)
print("\nPrediction Report:")
print(report)

# Optional: Plot confusion matrix
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Normal', 'Attack'], yticklabels=['Normal', 'Attack'])
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.savefig('confusion_matrix.png')  # Save for GitHub
plt.show()