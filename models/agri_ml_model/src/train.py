import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from pathlib import Path

DATA_PATH = Path("../data/datasets.csv")
MODEL_PATH = Path("../model")

MODEL_PATH.mkdir(parents=True, exist_ok=True)

# Load data
data = pd.read_csv(DATA_PATH)

numeric_cols = data.select_dtypes(include=np.number).columns.tolist()
categorical_cols = data.select_dtypes(exclude=np.number).columns.tolist()

# Encode categorical data
encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col].astype(str))
    encoders[col] = le

X = data.drop(columns=numeric_cols)
y = data[numeric_cols]

# Train model
model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)
model.fit(X, y)

# Save artifacts
joblib.dump(model, MODEL_PATH / "agri_model.pkl")
joblib.dump(encoders, MODEL_PATH / "encoders.pkl")
joblib.dump(numeric_cols, MODEL_PATH / "numeric_cols.pkl")

print("✅ Model trained and saved successfully")
