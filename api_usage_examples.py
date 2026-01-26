"""
Example API Usage for Integrated Models

This file demonstrates how to use the three integrated models
in the AgroNity application.
"""

import requests
import json

BASE_URL = "http://localhost:5000"

# ============================================================================
# 1. CHECK AVAILABLE MODELS
# ============================================================================

def check_available_models():
    """Check which models are currently available."""
    response = requests.get(f"{BASE_URL}/models")
    data = response.json()
    print("Available Models:")
    print(json.dumps(data, indent=2))
    return data


# ============================================================================
# 2. ANALYZE USING SKLEARN MODEL (Default)
# ============================================================================

def analyze_with_sklearn():
    """
    Analyze crop feasibility using the original Sklearn models.
    Returns: Feasibility probability, expected yield, profit estimates.
    """
    payload = {
        "crop": "wheat",
        "district": "Punjab",
        "area": "10",  # in acres
        "soil": "loamy"
        # "model": "sklearn"  # Optional - this is the default
    }
    
    response = requests.post(
        f"{BASE_URL}/analyze",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print("\nSklearn Model Analysis:")
    print(json.dumps(response.json(), indent=2))
    return response.json()


# ============================================================================
# 3. ANALYZE USING AGRI ML MODEL
# ============================================================================

def analyze_with_agri_ml():
    """
    Analyze crop feasibility using the new Agri ML Random Forest model.
    Returns: Feasibility score, productivity score, profit/loss percentage.
    """
    payload = {
        "crop": "rice",
        "district": "Tamil Nadu",
        "area": "5",  # in acres
        "soil": "clayey",
        "model": "agri_ml"  # Explicitly select agri_ml model
    }
    
    response = requests.post(
        f"{BASE_URL}/analyze",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print("\nAgri ML Model Analysis:")
    print(json.dumps(response.json(), indent=2))
    return response.json()


# ============================================================================
# 4. ANALYZE IMAGE USING KERAS CNN
# ============================================================================

def analyze_crop_image():
    """
    Analyze crop health from an image using the Keras CNN model.
    Falls back to rule-based matching if Keras is unavailable.
    """
    payload = {
        "filename": "tomato_leaf.jpg"
    }
    
    response = requests.post(
        f"{BASE_URL}/analyze_image",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print("\nImage Analysis (Keras CNN or Fallback):")
    print(json.dumps(response.json(), indent=2))
    return response.json()


# ============================================================================
# 5. COMPARE MODELS
# ============================================================================

def compare_models_for_same_input():
    """
    Compare predictions from both Sklearn and Agri ML models
    for the same input parameters.
    """
    crop_params = {
        "crop": "sugarcane",
        "district": "Maharashtra",
        "area": "20",
        "soil": "loamy"
    }
    
    print("\nComparing Models for Same Input:")
    print(f"Crop: {crop_params['crop']}")
    print(f"District: {crop_params['district']}")
    print(f"Area: {crop_params['area']} acres")
    print(f"Soil: {crop_params['soil']}\n")
    
    # Sklearn prediction
    payload_sklearn = {**crop_params, "model": "sklearn"}
    response_sklearn = requests.post(
        f"{BASE_URL}/analyze",
        json=payload_sklearn,
        headers={"Content-Type": "application/json"}
    )
    sklearn_result = response_sklearn.json()
    
    # Agri ML prediction
    payload_agri = {**crop_params, "model": "agri_ml"}
    response_agri = requests.post(
        f"{BASE_URL}/analyze",
        json=payload_agri,
        headers={"Content-Type": "application/json"}
    )
    agri_result = response_agri.json()
    
    print("Sklearn Model Result:")
    print(json.dumps(sklearn_result, indent=2))
    print("\nAgri ML Model Result:")
    print(json.dumps(agri_result, indent=2))
    
    return sklearn_result, agri_result


# ============================================================================
# 6. ERROR HANDLING
# ============================================================================

def handle_missing_parameters():
    """Demonstrate error handling for missing parameters."""
    payload = {
        "crop": "wheat",
        # Missing: district, area, soil
    }
    
    response = requests.post(
        f"{BASE_URL}/analyze",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print("\nError Response (Missing Parameters):")
    print(json.dumps(response.json(), indent=2))
    print(f"Status Code: {response.status_code}")
    return response


def handle_invalid_model():
    """Demonstrate error handling for invalid model selection."""
    payload = {
        "crop": "wheat",
        "district": "Punjab",
        "area": "10",
        "soil": "loamy",
        "model": "invalid_model"
    }
    
    response = requests.post(
        f"{BASE_URL}/analyze",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print("\nError Response (Invalid Model):")
    print(json.dumps(response.json(), indent=2))
    print(f"Status Code: {response.status_code}")
    return response


# ============================================================================
# 7. BATCH PROCESSING
# ============================================================================

def batch_analyze_multiple_crops():
    """
    Analyze multiple crops in a batch operation.
    Useful for testing or generating reports.
    """
    crops = [
        {"crop": "wheat", "district": "Punjab", "area": "10", "soil": "loamy"},
        {"crop": "rice", "district": "Tamil Nadu", "area": "5", "soil": "clayey"},
        {"crop": "sugarcane", "district": "Maharashtra", "area": "20", "soil": "loamy"},
    ]
    
    results = []
    
    print("\nBatch Processing Results:\n")
    
    for crop_data in crops:
        response = requests.post(
            f"{BASE_URL}/analyze",
            json=crop_data,
            headers={"Content-Type": "application/json"}
        )
        
        result = response.json()
        results.append({
            "input": crop_data,
            "result": result
        })
        
        print(f"Crop: {crop_data['crop']} | Feasible: {result.get('feasible', 'N/A')}")
    
    return results


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    """
    Run all example functions to demonstrate API usage.
    Make sure the Flask app is running on localhost:5000
    """
    
    print("=" * 70)
    print("AGRONIC INTEGRATED MODELS - API USAGE EXAMPLES")
    print("=" * 70)
    
    try:
        # Check available models
        check_available_models()
        
        # Analyze with sklearn
        analyze_with_sklearn()
        
        # Analyze with agri ml
        analyze_with_agri_ml()
        
        # Analyze image
        analyze_crop_image()
        
        # Compare models
        compare_models_for_same_input()
        
        # Error handling examples
        handle_missing_parameters()
        handle_invalid_model()
        
        # Batch processing
        batch_analyze_multiple_crops()
        
        print("\n" + "=" * 70)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("=" * 70)
        
    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to Flask app at http://localhost:5000")
        print("Make sure the app is running: python app.py")
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
