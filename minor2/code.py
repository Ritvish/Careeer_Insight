import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load the dataset
file_path = "dataset.csv"  # Ensure the file is in the same directory
df = pd.read_csv(file_path)

# Encode the target variable (Career) using LabelEncoder
label_encoder = LabelEncoder()
df["Career"] = label_encoder.fit_transform(df["Career"])  # Ensures labels are consecutive

# Separate features (X) and target variable (y)
X = df.drop(columns=["Career"])
y = df["Career"]

# Check for rare classes (labels appearing only once)
value_counts = y.value_counts()
rare_classes = value_counts[value_counts < 2].index.tolist()

# Remove rare classes to avoid stratification issues
df_filtered = df[~df["Career"].isin(rare_classes)]
X = df_filtered.drop(columns=["Career"])
y = df_filtered["Career"]

# Split into training (80%) and testing (20%) sets (without stratify)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train an XGBoost classifier
xgb_model = XGBClassifier(eval_metric="mlogloss")  # Removed `use_label_encoder=False`
xgb_model.fit(X_train, y_train)

# Predictions
y_pred = xgb_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)

# Use only unique y_test values as labels
classification_rep = classification_report(y_test, y_pred, labels=np.unique(y_test))

print(f"Accuracy: {accuracy}")
print(classification_rep)
