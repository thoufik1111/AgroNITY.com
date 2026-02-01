import os
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

# Try to import Keras for the image model
try:
    import keras
    KERAS_AVAILABLE = True
except ImportError:
    KERAS_AVAILABLE = False

# Try to import TensorFlow for the image model
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

# Try to import OpenCV for image processing
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

# Try to import PIL for image processing
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Get the directory where this script is located
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(MODEL_DIR, "models")
DATA_FILE = "sihdatasets.csv"

# --------------------
# Data & Model Loading
# --------------------
def load_data():
    """Loads and combines datasets from the CSV files."""
    try:
        # Get the directory where this script is located
        MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
        file1_path = os.path.join(MODEL_DIR, "sihdatasets.csv")
        file2_path = os.path.join(MODEL_DIR, "corrected_soil_dataset.csv")
        
        # Load both dataframes
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)
        
        # Concatenate them into a single dataframe
        combined_df = pd.concat([df1, df2], ignore_index=True)
        
        # Rename a column to match the expected format for your model
        combined_df = combined_df.rename(columns={'Major_Crops': 'crop'})
        
        return combined_df
    except FileNotFoundError as e:
        print(f"Error: Dataset file not found: {e}.")
        print("Make sure both 'sihdatasets.csv' and 'updateddatasets.csv' are in the same folder.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the dataset: {e}")
        return None


def load_agri_ml_regional_data():
    """Loads and combines regional datasets (Punjab and Tamil Nadu) for agri_ml model."""
    try:
        agri_ml_data_path = os.path.join(MODELS_DIR, "agri_ml_model", "data")
        
        punjab_path = os.path.join(agri_ml_data_path, "expanded_punjab_dataset.csv")
        tn_path = os.path.join(agri_ml_data_path, "expanded_tn_dataset.csv")
        
        # Load regional datasets
        df_punjab = pd.read_csv(punjab_path)
        df_tn = pd.read_csv(tn_path)
        
        # Combine both regional datasets
        combined_regional_df = pd.concat([df_punjab, df_tn], ignore_index=True)
        
        print(f"✓ Agri ML regional data loaded: {len(combined_regional_df)} rows (Punjab + TN)")
        return combined_regional_df
    except FileNotFoundError as e:
        print(f"⚠ Agri ML regional datasets not found: {e}")
        return None
    except Exception as e:
        print(f"⚠ Error loading agri_ml regional data: {e}")
        return None


def load_models():
    """Loads all available pre-trained models from the local directory."""
    models = {
        "sklearn": {"preprocessor": None, "clf": None, "reg": None},
        "agri_ml": None,
        "keras_cnn": None
    }
    
    # Load existing joblib models (sklearn)
    try:
        models["sklearn"]["preprocessor"] = joblib.load(os.path.join(MODEL_DIR, "preprocessor.joblib"))
        models["sklearn"]["clf"] = joblib.load(os.path.join(MODEL_DIR, "feasibility_clf.joblib"))
        models["sklearn"]["reg"] = joblib.load(os.path.join(MODEL_DIR, "yield_reg.joblib"))
        print("✓ Sklearn models loaded successfully")
    except FileNotFoundError:
        print("⚠ Sklearn model files not found")
    except Exception as e:
        print(f"⚠ Error loading sklearn models: {e}")
    
    # ---- DISABLE AGRI MODEL ON RENDER ----
    print("⚠ agri_model disabled on Render to prevent backend crash")
    models["agri_ml"] = None
    
    # Load Keras CNN model for image classification
    if KERAS_AVAILABLE and TF_AVAILABLE:
        try:
            keras_path = os.path.join(MODELS_DIR, "modelskeras_model")
            model_file = os.path.join(keras_path, "model.weights.h5")
            config_file = os.path.join(keras_path, "config.json")
            
            if os.path.exists(config_file) and os.path.exists(model_file):
                # Load model architecture from config
                with open(config_file, 'r') as f:
                    import json
                    config = json.load(f)
                
                keras_model = keras.Sequential.from_config(config['config'])
                keras_model.load_weights(model_file)
                models["keras_cnn"] = keras_model
                print("✓ Keras CNN model loaded successfully")
        except Exception as e:
            print(f"⚠ Error loading keras model: {e}")
    
    return models

# --------------------
# Analysis Functions
# --------------------
def analyze_feasibility(models, data_df, crop_type, district, area_size, soil_type, use_model="sklearn"):
    """
    Analyzes the feasibility and potential profit using loaded data.
    
    Parameters:
    - models: Dict containing all loaded models
    - data_df: DataFrame with agricultural data
    - crop_type: Crop name
    - district: District name
    - area_size: Area in acres
    - soil_type: Soil type
    - use_model: Which model to use ("sklearn", "agri_ml")
    """
    
    if use_model == "sklearn":
        return _analyze_feasibility_sklearn(models, data_df, crop_type, district, area_size, soil_type)
    elif use_model == "agri_ml":
        return _analyze_feasibility_agri_ml(models, data_df, crop_type, district, area_size, soil_type)
    else:
        return {"feasible": False, "error": f"Unknown model type: {use_model}"}


def _analyze_feasibility_sklearn(models, data_df, crop_type, district, area_size, soil_type):
    """Analyze feasibility using sklearn models (original implementation)."""
    preprocessor = models["sklearn"]["preprocessor"]
    clf = models["sklearn"]["clf"]
    reg = models["sklearn"]["reg"]
    
    if preprocessor is None or clf is None or reg is None:
        return {
            "feasible": False,
            "error": "Sklearn models not loaded"
        }
    
    # Find the row that matches the user's inputs for district and soil type
    match = data_df[(data_df['District'].str.lower() == district.lower()) & 
                    (data_df['Soil_Type'].str.lower() == soil_type.lower())]

    if match.empty:
        return {
            "feasible": False,
            "reasons": [f"No data found for the combination of '{district}' and '{soil_type}'. Please check your spelling or try a different combination."]
        }
    
    # Extract all the required feature values from the found row
    matched_row = match.iloc[0].to_dict()
    
    # 2. Create the input DataFrame for the model
    input_data = {
        "crop": crop_type.lower(),
        "district": matched_row["District"],
        "soil_type": matched_row["Soil_Type"],
        "area_ha": float(area_size) * 0.4047,  # Convert acres to hectares
        "avg_rain": matched_row["Avg_Rainfall_mm"],
        "temp": matched_row["Avg_Temperature_C"],
        "Fertilizer_Usage_kg_per_ha": matched_row["Fertilizer_Usage_kg_per_ha"],
        "pH_Level": matched_row["pH_Level"],
        "Phosphorus_kg_per_ha": matched_row["Phosphorus_kg_per_ha"],
        "Potassium_kg_per_ha": matched_row["Potassium_kg_per_ha"],
        "Nitrogen_kg_per_ha": matched_row["Nitrogen_kg_per_ha"],
        "Organic_Matter_Percentage": matched_row["Organic_Matter_Percentage"],
        "Electrical_Conductivity_dS_per_m": matched_row["Electrical_Conductivity_dS_per_m"],
        "Cation_Exchange_Capacity_meq_per_100g": matched_row["Cation_Exchange_Capacity_meq_per_100g"],
        "Zinc_ppm": matched_row["Zinc_ppm"],
        "Iron_ppm": matched_row["Iron_ppm"],
        "Manganese_ppm": matched_row["Manganese_ppm"],
        "Copper_ppm": matched_row["Copper_ppm"],
    }
    
    input_df = pd.DataFrame([input_data])
    
    # 3. Transform input and get predictions
    try:
        X_input = preprocessor.transform(input_df)
    except ValueError as e:
        return {
            "feasible": False,
            "reasons": [f"Error during data transformation: {e}. This likely means a new crop, district, or soil type was entered that the model has not seen before."]
        }

    feasibility_prob = clf.predict_proba(X_input)[0, 1]
    is_feasible = bool(clf.predict(X_input)[0])

    if is_feasible:
        # Predict yield and calculate profit
        modal_price_per_quintal = matched_row["Mandi_Price_Rupees_per_kg"]
        expected_yield_tpha = reg.predict(X_input)[0]
        
        # To avoid negative yields from the regressor
        expected_yield_tpha = max(0, expected_yield_tpha)
        
       # More realistic profit calculation

        # Adjustment factors
        MARKETING_LOSSES_FACTOR = 0.90     # ~10% reduction due to transport, commission, wastage
        YIELD_REALIZATION_FACTOR = 0.80    # ~20% reduction due to field losses, pests, etc.
        DEFAULT_COST_PER_HA = 30000        # average cost of cultivation per hectare in INR
        
        # Price per ton after accounting for marketing losses
        price_per_ton = modal_price_per_quintal * 10 * MARKETING_LOSSES_FACTOR
        
        # Effective yield (tons/ha) after accounting for field realities
        effective_yield_tpha = expected_yield_tpha * YIELD_REALIZATION_FACTOR
        
        # Total revenue = effective yield × price × area
        total_revenue = effective_yield_tpha * price_per_ton * input_data["area_ha"]
        
        # Total cost (use provided cost_per_ha if available, else fallback to default)
        cost_per_ha = input_data.get("cost_per_ha", DEFAULT_COST_PER_HA)
        total_cost = cost_per_ha * input_data["area_ha"]
        
        # Final profit
        profit = total_revenue - total_cost
           
        # We use a known high-end yield for percentage calculation.
        max_yield_ref = data_df["Crop_Production_Rate_Yearly"].max() 
        yield_percentage = (expected_yield_tpha / max_yield_ref) * 100
        
        # Future revenue projections (assuming 5% annual growth)
        revenue_1yr = total_revenue * 1.05
        revenue_2yr = total_revenue * (1.05)**2
        
        return {
            "feasible": True,
            "probability": feasibility_prob,
            "expected_yield_tpha": expected_yield_tpha,
            "yield_percentage": yield_percentage,
            "profit_rs": profit,
            "total_revenue_rs": total_revenue,
            "revenue_1yr_rs": revenue_1yr,
            "revenue_2yr_rs": revenue_2yr,
            "mandi_price_rs_per_quintal": modal_price_per_quintal,
            "model_used": "sklearn"
        }
    else:
        # State reasons for unsuitability (a general message as the model's logic is complex)
        reasons = ["Based on the trained model, the combination of factors is not optimal for this crop in this area."]
        return {
            "feasible": False,
            "reasons": reasons
        }


def _analyze_feasibility_agri_ml(models, data_df, crop_type, district, area_size, soil_type):
    """Analyze feasibility using agri_ml Random Forest model with regional data."""
    if models["agri_ml"] is None:
        return {"feasible": False, "error": "Agri ML model not loaded"}
    
    agri_ml = models["agri_ml"]
    model = agri_ml["model"]
    encoders = agri_ml["encoders"]
    numeric_cols = agri_ml["numeric_cols"]
    
    # First, try to find exact match for district + crop
    match = data_df[(data_df['District'].str.lower() == district.lower()) &
                    (data_df['Major_Crops'].str.lower() == crop_type.lower())]
    
    # If no exact match, try just district
    if match.empty:
        match = data_df[(data_df['District'].str.lower() == district.lower())]
    
    if match.empty:
        return {
            "feasible": False,
            "reasons": [f"No data found for district '{district}' in regional database"]
        }
    
    # Get mean numeric values for the matched data
    mean_numeric = match[numeric_cols].mean()
    
    # Calculate feasibility and productivity scores
    soil_cols = [c for c in ["pH_Level", "Organic_Matter_Percentage", "Clay_Percentage"] if c in mean_numeric.index]
    rain_col = "Avg_Rainfall_mm"
    
    soil_score = mean_numeric[soil_cols].mean() if soil_cols else 0
    rain_score = mean_numeric[rain_col] if rain_col in mean_numeric.index else 0
    
    soil_max = data_df[soil_cols].mean(axis=1).max() if soil_cols else 1
    rain_max = data_df[rain_col].max() if rain_col in data_df.columns else 1
    
    feasibility_score = ((soil_score / soil_max) + (rain_score / rain_max)) / 2 * 100 if soil_max > 0 and rain_max > 0 else 0
    
    # Productivity score
    nutrient_cols = [c for c in [
        "Nitrogen_kg_per_ha",
        "Phosphorus_kg_per_ha",
        "Potassium_kg_per_ha",
        "Organic_Matter_Percentage"
    ] if c in mean_numeric.index]
    
    nutrient_score = mean_numeric[nutrient_cols].sum() if nutrient_cols else 0
    dataset_avg = data_df[nutrient_cols].sum(axis=1).mean() if nutrient_cols else 1
    
    productivity_score = (nutrient_score / dataset_avg) * 100 if dataset_avg > 0 else 0
    
    profit_loss = (feasibility_score * productivity_score) / 100 - 100
    is_feasible = feasibility_score > 50 and productivity_score > 50
    
    return {
        "feasible": is_feasible,
        "feasibility_score": float(feasibility_score),
        "productivity_score": float(productivity_score),
        "profit_loss_percent": float(profit_loss),
        "model_used": "agri_ml"
    }

def analyze_image(models, data_df, filename):
    """
    Analyzes the image based on filename and Keras model if available.
    Falls back to rule-based matching if model is unavailable or image not found.
    """
    # Try to use Keras model first (only if model is loaded)
    if models["keras_cnn"] is not None:
        try:
            return _analyze_image_keras(models, filename)
        except Exception as e:
            # Log the error but continue to fallback
            print(f"⚠ Keras CNN analysis failed: {str(e)}. Using rule-based detection instead.")
    
    # Fallback to rule-based matching (analyzes based on filename)
    result = _analyze_image_ruleset(data_df, filename)
    if result["status"] == "success":
        result["fallback"] = True  # Indicate we're using fallback method
    return result


def _analyze_image_keras(models, filename):
    """Analyze image using Keras CNN model."""
    keras_model = models["keras_cnn"]
    
    # Load the image
    img_path = os.path.join(MODEL_DIR, "uploads", filename)
    
    if not os.path.exists(img_path):
        # If file doesn't exist, raise exception to trigger fallback
        raise FileNotFoundError(f"Image file not found: {filename}")
    
    # Load and preprocess image
    if PIL_AVAILABLE:
        img = Image.open(img_path)
        img = img.convert('RGB')
        img = img.resize((128, 128))
        img_array = np.array(img) / 255.0
    else:
        img_array = cv2.imread(img_path)
        img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        img_array = cv2.resize(img_array, (128, 128))
        img_array = img_array / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    # Make prediction
    prediction = keras_model.predict(img_array, verbose=0)
    confidence = float(prediction[0][0])
    
    # Determine if crop is healthy
    is_healthy = confidence > 0.5
    
    return {
        "status": "success",
        "model_used": "keras_cnn",
        "confidence": confidence,
        "is_healthy": is_healthy,
        "diagnosis": "Plant appears healthy" if is_healthy else "Plant shows signs of disease"
    }


def _analyze_image_ruleset(data_df, filename):
    """Analyze image using comprehensive crop detection with health assessment."""
    filename_lower = filename.lower()
    
    # Comprehensive crop detection mapping
    crop_mappings = {
        "rice": ["rice", "paddy", "धान", "நெல்"],
        "wheat": ["wheat", "गेहूं", "கோதுமை"],
        "tomato": ["tomato", "टमाटर", "தக்காளி"],
        "cotton": ["cotton", "कपास", "棉"],
        "groundnut": ["groundnut", "mungfali", "गंडु", "கடலை"],
        "sugarcane": ["sugarcane", "गन्ना", "கரும்பு"],
        "maize": ["maize", "corn", "मक्का", "玉米"],
        "chilli": ["chilli", "pepper", "मिर्च", "மிளகாய்"],
        "soybean": ["soybean", "सोयाबीन", "சோயாபீன்"],
        "mustard": ["mustard", "सरसों", "芥末"],
        "potato": ["potato", "आलू", "உருளை"],
        "onion": ["onion", "प्याज", "வெங்காயம்"]
    }
    
    # Find matching crop
    detected_crop = None
    for crop, keywords in crop_mappings.items():
        if any(keyword in filename_lower for keyword in keywords):
            detected_crop = crop.capitalize()
            break
    
    if not detected_crop:
        return {
            "status": "error",
            "message": "Could not identify crop type from filename. Please use format like 'tomato.jpg', 'wheat.jpg', etc.",
            "suggested_crops": list(crop_mappings.keys())
        }
    
    # Get crop data from dataset
    crop_data = data_df[data_df['crop'].str.lower() == detected_crop.lower()]
    
    if crop_data.empty:
        # Return basic info even if no dataset match
        return {
            "status": "success",
            "model_used": "ruleset",
            "crop": detected_crop,
            "message": f"Crop identified as {detected_crop}",
            "avg_production": "Data not available",
            "mandi_price": "Check local mandi rates"
        }
    
    # Get statistics from dataset
    avg_production = crop_data['Crop_Production_Rate_Yearly'].mean() if 'Crop_Production_Rate_Yearly' in crop_data.columns else 0
    avg_mandi_price = crop_data['Mandi_Price_Rupees_per_kg'].mean() if 'Mandi_Price_Rupees_per_kg' in crop_data.columns else 0
    
    # Health assessment based on image characteristics (heuristic)
    # In real scenario, Keras model would do this
    health_status = "Healthy"  # Default
    confidence = 0.65
    disease_risk = "Low"
    
    # Filename patterns might indicate disease state
    if any(word in filename_lower for word in ["disease", "sick", "brown", "rust", "blight", "rot"]):
        health_status = "Diseased"
        disease_risk = "High"
        confidence = 0.75
    
    return {
        "status": "success",
        "model_used": "ruleset_enhanced",
        "crop": detected_crop,
        "health_status": health_status,
        "confidence": confidence,
        "disease_risk": disease_risk,
        "avg_production": f"{avg_production:.2f} tons/year" if avg_production > 0 else "Not available",
        "mandi_price": f"₹{avg_mandi_price:.2f}/kg" if avg_mandi_price > 0 else "Check local market",
        "recommendations": get_crop_recommendations(detected_crop)
    }


def get_crop_recommendations(crop):
    """Get farming recommendations for different crops."""
    recommendations = {
        "rice": "Water management is critical. Maintain 2-3 inches standing water. Watch for rice blast in humid conditions.",
        "wheat": "Sow in November-December. Needs 3-4 irrigations. Susceptible to rust - monitor weather.",
        "tomato": "Use trellising system. Daily monitoring for late blight. Requires consistent water supply.",
        "cotton": "Monitor for bollworms weekly. Use integrated pest management. Avoid waterlogging.",
        "groundnut": "Requires well-drained soil. Watch for leaf spot diseases. Harvest when leaves turn yellow.",
        "sugarcane": "Heavy feeder crop. Needs 18-24 months. Monitor for red rot disease.",
        "maize": "Susceptible to stem borers - use neem oil spray. Needs timely water at silking stage.",
        "chilli": "Sensitive to water stress. Spider mites and thrips are major pests. Regular scouting needed.",
        "soybean": "Crop rotation recommended. Monitor for rust. Harvest at pod maturity stage.",
        "mustard": "Needs cool weather. Susceptible to alternaria blight in humid conditions.",
        "potato": "Store in cool, dark place. Watch for late blight in monsoon season.",
        "onion": "Thrips and purple blotch are major issues. Avoid overwatering."
    }
    return recommendations.get(crop.lower(), "Monitor crop regularly for pest and disease outbreaks.")


# --------------------
# Main execution block - DO NOT RUN as a standalone script anymore
# This file is now a module for app.py
# --------------------
# if __name__ == "__main__":
#     preprocessor, clf, reg = load_models()
#     data_df = load_data()
#     # The rest of the script is now in app.py
