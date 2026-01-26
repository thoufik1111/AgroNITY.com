#!/usr/bin/env python
"""Test script for enhanced image classification"""

import agronity_test as ag
import pandas as pd

# Load data
print("Loading data...")
data = ag.load_data()

# Test crop detection for all supported crops
test_files = [
    "rice.jpg",
    "wheat.jpg", 
    "tomato.jpg",
    "cotton.jpg",
    "groundnut.jpg",
    "sugarcane.jpg",
    "maize.jpg",
    "chilli.jpg",
    "soybean.jpg",
    "mustard.jpg",
    "potato.jpg",
    "onion.jpg",
    "paddy.jpg",
    "diseased_tomato.jpg",
    "unknown_crop.jpg"
]

print("\n" + "="*80)
print("ENHANCED IMAGE CLASSIFICATION TEST")
print("="*80 + "\n")

success_count = 0
fail_count = 0

for filename in test_files:
    result = ag._analyze_image_ruleset(data, filename)
    
    if result['status'] == 'success':
        crop = result.get('crop', 'Unknown')
        health = result.get('health_status', 'N/A')
        confidence = result.get('confidence', 0)
        disease_risk = result.get('disease_risk', 'N/A')
        recommendations = result.get('recommendations', 'N/A')
        
        print(f"✓ {filename:<25}")
        print(f"  Crop: {crop}")
        print(f"  Health Status: {health} (Confidence: {confidence})")
        print(f"  Disease Risk: {disease_risk}")
        if recommendations:
            print(f"  Recommendation: {recommendations[:80]}...")
        print()
        success_count += 1
    else:
        error_msg = result.get('message', 'Unknown error')
        print(f"✗ {filename:<25}")
        print(f"  Error: {error_msg[:60]}...")
        print()
        fail_count += 1

print("="*80)
print(f"Results: {success_count} successful, {fail_count} failed")
print("="*80)
