import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, VotingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle

# Load dataset
data = pd.read_csv("dataset.csv")
print(f"Dataset: {len(data)} rows, Label distribution:\n{data['Label'].value_counts()}")

# Feature Engineering
data["PowerPerCurrent"] = data["Power"] / (data["Current"] + 0.001)
data["MeterEfficiency"] = data["MeterDiff"] / ((data["Power"] * data["Time"] / 1000) + 0.001)
data["CurrentVoltageRatio"] = data["Current"] / (data["Voltage"] + 0.001)

# Drop non-numeric
X = data.drop(["State", "District", "Village", "Label"], axis=1)
y = data["Label"]

feature_columns = X.columns.tolist()
print(f"\nFeatures: {feature_columns}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Ensemble model
rf = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
gb = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42)

ensemble = VotingClassifier(estimators=[("rf", rf), ("gb", gb)], voting="soft")
ensemble.fit(X_train_scaled, y_train)

y_pred = ensemble.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n✅ Model Accuracy: {accuracy * 100:.2f}%")
print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")

# Cross-validation
cv_scores = cross_val_score(ensemble, scaler.transform(X), y, cv=5)
print(f"\n5-Fold CV Accuracy: {cv_scores.mean()*100:.2f}% ± {cv_scores.std()*100:.2f}%")

# Save
pickle.dump({
    "model": ensemble,
    "scaler": scaler,
    "features": feature_columns,
    "accuracy": round(accuracy * 100, 2)
}, open("model.pkl", "wb"))

print("\n✅ Enhanced model saved to model.pkl")
