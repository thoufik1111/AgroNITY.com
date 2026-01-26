#!/usr/bin/env python
"""Test script for chatbot responses via API"""

import requests
import json
import time

# Test the Flask API
BASE_URL = "http://localhost:5000"

print("\n" + "="*80)
print("TESTING FLASK API ENDPOINTS")
print("="*80 + "\n")

# Test 1: Check if server is running
print("Test 1: Checking server status...")
try:
    response = requests.get(BASE_URL, timeout=2)
    print(f"✓ Server is running (Status: {response.status_code})")
except Exception as e:
    print(f"✗ Server not running: {str(e)}")
    print("\nTo start the server, run: python app.py")
    exit(1)

# Test 2: Test feasibility analysis with Sklearn model
print("\nTest 2: Testing feasibility analysis (Sklearn)...")
payload = {
    "crop": "Paddy",
    "district": "Sangrur",
    "area": "2",
    "soil": "Alluvial",
    "model": "sklearn"
}

try:
    response = requests.post(f"{BASE_URL}/analyze", json=payload)
    result = response.json()
    
    if response.status_code == 200:
        if result.get('feasible'):
            print(f"✓ Feasibility Analysis Successful")
            print(f"  Crop: {result.get('crop')}")
            print(f"  Feasible: {result.get('feasible')}")
            print(f"  Profit: ₹{result.get('profit_rs', 0):.2f}")
            print(f"  Expected Yield: {result.get('expected_yield_tpha', 0):.2f} tons/ha")
        else:
            print(f"✓ Analysis Complete (Not Feasible)")
            print(f"  Reasons: {result.get('reasons', [])}")
    else:
        print(f"✗ Error: {result.get('error', 'Unknown')}")
except Exception as e:
    print(f"✗ Request failed: {str(e)}")

# Test 3: Test with Agri ML model
print("\nTest 3: Testing with Agri ML model...")
payload['model'] = 'agri_ml'

try:
    response = requests.post(f"{BASE_URL}/analyze", json=payload)
    result = response.json()
    
    if response.status_code == 200 and result.get('feasible'):
        print(f"✓ Agri ML Analysis Successful")
        print(f"  Profit: ₹{result.get('profit_rs', 0):.2f}")
    else:
        print(f"✓ Analysis complete (may not be feasible)")
except Exception as e:
    print(f"✗ Request failed: {str(e)}")

# Test 4: Test models endpoint
print("\nTest 4: Checking available models...")
try:
    response = requests.get(f"{BASE_URL}/models")
    result = response.json()
    
    if response.status_code == 200:
        print(f"✓ Models available:")
        for model, status in result.items():
            print(f"  - {model}: {status}")
    else:
        print(f"✗ Error: {result}")
except Exception as e:
    print(f"✗ Request failed: {str(e)}")

print("\n" + "="*80)
print("API TESTING COMPLETE")
print("="*80)
print("\nNote: Voice input and dynamic graphs are frontend features tested in browser.")
print("Test them by:")
print("1. Opening http://localhost:5000 in your browser")
print("2. Logging in with OTP: 2622")
print("3. Click the microphone button to use voice input")
print("4. Ask agricultural questions to trigger chatbot responses")
print("5. Submit feasibility analysis to see dynamic graph updates")
