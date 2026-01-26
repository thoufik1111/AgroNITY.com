import numpy as np

def feasibility_score(mean_numeric, data):
    soil_cols = [c for c in ["pH_Level", "Organic_Matter_Percentage", "Clay_Percentage"] if c in mean_numeric]
    rain_col = "Avg_Rainfall_mm"

    soil_score = mean_numeric[soil_cols].mean()
    rain_score = mean_numeric[rain_col]

    soil_max = data[soil_cols].mean(axis=1).max()
    rain_max = data[rain_col].max()

    return ((soil_score / soil_max) + (rain_score / rain_max)) / 2 * 100


def productivity_score(mean_numeric, data):
    nutrient_cols = [c for c in [
        "Nitrogen_kg_per_ha",
        "Phosphorus_kg_per_ha",
        "Potassium_kg_per_ha",
        "Organic_Matter_Percentage"
    ] if c in mean_numeric]

    nutrient_score = mean_numeric[nutrient_cols].sum()
    dataset_avg = data[nutrient_cols].sum(axis=1).mean()

    return (nutrient_score / dataset_avg) * 100
