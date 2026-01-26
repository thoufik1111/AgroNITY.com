import pandas as pd
import numpy as np
import joblib
from utils import feasibility_score, productivity_score
from pathlib import Path

MODEL_PATH = Path("../model")
DATA_PATH = Path("../data/datasets.csv")

# Load assets
model = joblib.load(MODEL_PATH / "agri_model.pkl")
encoders = joblib.load(MODEL_PATH / "encoders.pkl")
numeric_cols = joblib.load(MODEL_PATH / "numeric_cols.pkl")

data = pd.read_csv(DATA_PATH)

district = input("Enter District: ").strip()
crop = input("Enter Major Crop: ").strip()

subset = data[
    (data["District"] == district) &
    (data["Major_Crops"] == crop)
]

if subset.empty:
    raise ValueError("❌ No data found")

mean_numeric = subset[numeric_cols].mean()

# Encode input row
encoded_data = data.copy()
for col, le in encoders.items():
    encoded_data[col] = le.transform(encoded_data[col].astype(str))

X = encoded_data.drop(columns=numeric_cols)
test_row = X[
    (data["District"] == district) &
    (data["Major_Crops"] == crop)
].iloc[[0]]

predicted_mean = model.predict(test_row)[0].mean()
current_mean = mean_numeric.mean()
future_growth = ((predicted_mean - current_mean) / current_mean) * 100

feasibility = feasibility_score(mean_numeric, data)
productivity = productivity_score(mean_numeric, data)
profit_loss = (feasibility * productivity) / 100 - 100

# OUTPUT
print("\n📈 FINAL REPORT\n")
print(f"District      : {district}")
print(f"Major Crop    : {crop}\n")

for col in numeric_cols:
    print(f"{col:<25}: {mean_numeric[col]:.2f}")

print("\nFEASIBILITY     :", round(feasibility, 2))
print("PRODUCTIVITY   :", round(productivity, 2))
print("FUTURE GROWTH  :", round(future_growth, 2))
print("PROFIT / LOSS  :", round(profit_loss, 2), "%")
