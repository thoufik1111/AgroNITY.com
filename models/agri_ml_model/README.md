# Agricultural ML Model

A machine learning model for agricultural prediction and analysis, including crop yield estimation, feasibility checks, and crop suitability scoring.

## Project Structure

```
agri_ml_model/
│
├── data/
│   └── datasets.csv            # Your uploaded CSVs merged
│
├── model/
│   ├── agri_model.pkl          # Trained ML model
│   ├── encoders.pkl            # Label encoders for categorical features
│   ├── numeric_cols.pkl        # Numeric column list
│
├── src/
│   ├── train.py                # Trains & saves model
│   ├── predict.py              # Loads model & predicts
│   └── utils.py                # Feasibility & math logic
│
├── requirements.txt            # Project dependencies
└── README.md                   # This file
```

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Training the Model

Place your dataset in `data/datasets.csv` and run:

```bash
python src/train.py
```

This will:
- Load and preprocess the data
- Encode categorical variables
- Train a Random Forest model
- Save model artifacts to `model/` directory

### Making Predictions

```python
from src.predict import predict

# Single prediction
sample_input = {
    'temperature': 25.5,
    'humidity': 70,
    'feature3': 'category_value',
}

prediction = predict(sample_input)
print(f"Prediction: {prediction[0]}")
```

### Using Utility Functions

```python
from src.utils import (
    check_feasibility,
    calculate_yield_estimate,
    calculate_crop_suitability
)

features = {
    'temperature': 25,
    'humidity': 70,
    'soil_quality': 75,
    'rainfall': 900
}

# Check if features are in feasible range
is_feasible = check_feasibility(features)

# Estimate yield
yield_estimate = calculate_yield_estimate(75, 25, 70, 900)

# Get suitability score
suitability = calculate_crop_suitability(features)

print(f"Feasible: {is_feasible}")
print(f"Yield: {yield_estimate:.2f} kg/hectare")
print(f"Suitability: {suitability:.2f}/100")
```

## Features

### Model Training (`train.py`)
- Loads agricultural data from CSV
- Handles both numeric and categorical features
- Encodes categorical variables using LabelEncoder
- Trains a Random Forest classifier
- Saves model, encoders, and column information

### Prediction (`predict.py`)
- Loads pre-trained model and encoders
- Makes predictions on new input data
- Handles both dict and DataFrame inputs
- Properly encodes categorical features

### Utilities (`utils.py`)
- **check_feasibility()**: Validates input features against feasible ranges
- **calculate_yield_estimate()**: Estimates crop yield based on environmental factors
- **normalize_features()**: Performs z-score normalization
- **calculate_crop_suitability()**: Generates a suitability score (0-100) for crop growth

## Data Format

Your `data/datasets.csv` should contain:
- Numeric columns (temperature, humidity, nitrogen, phosphorus, potassium, etc.)
- Categorical columns (crop type, soil type, region, etc.)
- A target column for supervised learning

Example:
```
temperature,humidity,ph,soil_type,crop_type,yield_category
25.5,70,6.5,loamy,wheat,high
23.0,65,7.0,clayey,rice,medium
...
```

## Requirements

- Python 3.7+
- pandas
- scikit-learn
- numpy
- matplotlib
- seaborn

## License

This project is open for agricultural research and development purposes.

## Contact

For questions or improvements, please submit an issue or pull request.
