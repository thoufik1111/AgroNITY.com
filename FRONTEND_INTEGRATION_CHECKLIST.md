# 🎨 Frontend Integration Checklist

Complete this checklist to integrate model selection into your UI.

## Phase 1: Model Detection

- [ ] Fetch available models on page load
  ```javascript
  fetch('/models').then(r => r.json()).then(data => console.log(data))
  ```

- [ ] Display which models are available in the UI

- [ ] Store available models in a variable for reference

## Phase 2: Model Selection UI

- [ ] Add radio buttons or dropdown for model selection
  ```html
  <select id="model-select">
    <option value="sklearn">Sklearn Model (Default)</option>
    <option value="agri_ml">Agri ML Model</option>
  </select>
  ```

- [ ] Label models clearly:
  - "Sklearn Model - Detailed Analysis (Default)"
  - "Agri ML Model - Quick Scoring"

- [ ] Show model availability:
  - Disable unavailable models
  - Show reason why model is unavailable (e.g., "Keras not installed")

## Phase 3: API Integration

- [ ] Update `/analyze` request to include model parameter:
  ```javascript
  const payload = {
    crop: cropInput.value,
    district: districtInput.value,
    area: areaInput.value,
    soil: soilInput.value,
    model: modelSelect.value  // Add this
  };
  ```

- [ ] Update `/analyze_image` endpoint (no changes needed - auto-detects)

- [ ] Test both models with various inputs

## Phase 4: Response Handling

### Sklearn Model Response
```javascript
// Handle these fields:
result.feasible           // boolean
result.probability        // 0-1
result.expected_yield_tpha  // number
result.profit_rs          // number
result.total_revenue_rs   // number
result.revenue_1yr_rs     // number
result.revenue_2yr_rs     // number
result.mandi_price_rs_per_quintal  // number
result.model_used         // "sklearn"
```

### Agri ML Model Response
```javascript
// Handle these fields:
result.feasible           // boolean
result.feasibility_score  // 0-100
result.productivity_score // 0-100
result.profit_loss_percent // number
result.model_used         // "agri_ml"
```

### Display Differences
- [ ] Sklearn: Show profit estimate, revenue projections
- [ ] Agri ML: Show score percentages, profit/loss percentage

## Phase 5: Image Analysis

- [ ] Add support for image upload (if not already present)

- [ ] Send image filename to `/analyze_image`

- [ ] Handle both response types:
  ```javascript
  if (result.model_used === "keras_cnn") {
    // Display: confidence, is_healthy, diagnosis
  } else if (result.model_used === "ruleset") {
    // Display: crop name, avg_production, mandi_price
  }
  ```

## Phase 6: Comparison Feature (Optional)

- [ ] Add "Compare Models" button

- [ ] Run both models with same input

- [ ] Display predictions side-by-side:
  ```
  INPUT: Wheat in Punjab, 10 acres, loamy soil
  
  SKLEARN MODEL:
  - Feasible: Yes
  - Profit: ₹50,000
  - Yield: 4.5 tons/ha
  
  AGRI ML MODEL:
  - Feasible: Yes
  - Feasibility Score: 78%
  - Productivity Score: 82%
  ```

## Phase 7: Error Handling

- [ ] Handle missing/unavailable models gracefully
  ```javascript
  if (!availableModels.sklearn) {
    // Disable sklearn option
  }
  ```

- [ ] Show user-friendly error messages:
  ```javascript
  "No data found for this combination"
  "Selected model is currently unavailable"
  "Invalid parameters"
  ```

## Phase 8: UX Enhancements

- [ ] Add tooltip explaining each model:
  - Sklearn: "Provides detailed yield & profit predictions"
  - Agri ML: "Quick feasibility scoring with productivity metrics"

- [ ] Show which model is currently selected

- [ ] Add loading spinner while analyzing

- [ ] Display execution time:
  ```javascript
  "Analysis completed in {time}ms"
  ```

- [ ] Show model information:
  ```javascript
  "Using Sklearn model (Detailed Analysis)"
  ```

## Phase 9: Testing

- [ ] Test with Sklearn model
  ```
  Input: Wheat, Punjab, 10 acres, loamy
  Expected: Feasibility probability + Profit estimates
  ```

- [ ] Test with Agri ML model
  ```
  Input: Wheat, Punjab, 10 acres, loamy
  Expected: Feasibility + Productivity scores
  ```

- [ ] Test with unavailable model
  ```
  Expected: Graceful error or fallback
  ```

- [ ] Test model switching
  ```
  Expected: Quick response with different results
  ```

- [ ] Test image analysis
  ```
  Input: Upload crop image
  Expected: Health diagnosis or crop info
  ```

## Phase 10: Documentation

- [ ] Update frontend README with model selection docs

- [ ] Add comments in code explaining model responses

- [ ] Document which fields come from which model

- [ ] Create user guide for model selection

## Code Examples

### Fetching Available Models
```javascript
async function initializeModels() {
  try {
    const response = await fetch('/models');
    const data = await response.json();
    console.log('Available models:', data.available_models);
    
    // Update UI based on available models
    document.getElementById('model-select').disabled = !data.available_models.sklearn;
  } catch (error) {
    console.error('Failed to fetch models:', error);
  }
}

// Call on page load
window.addEventListener('load', initializeModels);
```

### Updated Analyze Function
```javascript
async function analyzeWithModelSelection() {
  const selectedModel = document.getElementById('model-select').value;
  
  const payload = {
    crop: document.getElementById('crop').value,
    district: document.getElementById('district').value,
    area: document.getElementById('area').value,
    soil: document.getElementById('soil').value,
    model: selectedModel  // Pass selected model
  };
  
  try {
    const response = await fetch('/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    const result = await response.json();
    displayResult(result, selectedModel);
  } catch (error) {
    console.error('Analysis failed:', error);
    showError('Analysis failed. Please try again.');
  }
}
```

### Display Result Handler
```javascript
function displayResult(result, modelUsed) {
  if (result.feasible) {
    if (modelUsed === 'sklearn') {
      // Display sklearn-specific fields
      document.getElementById('result').innerHTML = `
        <h3>Analysis Results (Sklearn Model)</h3>
        <p>Feasible: Yes</p>
        <p>Probability: ${(result.probability * 100).toFixed(1)}%</p>
        <p>Expected Yield: ${result.expected_yield_tpha.toFixed(2)} tons/ha</p>
        <p>Estimated Profit: ₹${Math.round(result.profit_rs).toLocaleString('en-IN')}</p>
      `;
    } else if (modelUsed === 'agri_ml') {
      // Display agri_ml-specific fields
      document.getElementById('result').innerHTML = `
        <h3>Analysis Results (Agri ML Model)</h3>
        <p>Feasible: Yes</p>
        <p>Feasibility Score: ${result.feasibility_score.toFixed(1)}/100</p>
        <p>Productivity Score: ${result.productivity_score.toFixed(1)}/100</p>
        <p>Profit/Loss: ${result.profit_loss_percent.toFixed(1)}%</p>
      `;
    }
  } else {
    document.getElementById('result').innerHTML = `
      <h3>Analysis Results</h3>
      <p>Not feasible for this crop-location-soil combination</p>
    `;
  }
}
```

---

## Progress Tracking

| Phase | Status | Notes |
|-------|--------|-------|
| 1. Detection | ⭕ TODO | |
| 2. UI Selection | ⭕ TODO | |
| 3. API Integration | ⭕ TODO | |
| 4. Response Handling | ⭕ TODO | |
| 5. Image Analysis | ⭕ TODO | |
| 6. Comparison | ⭕ TODO | Optional |
| 7. Error Handling | ⭕ TODO | |
| 8. UX Enhancements | ⭕ TODO | |
| 9. Testing | ⭕ TODO | |
| 10. Documentation | ⭕ TODO | |

---

## Support

For API details, see:
- `MODEL_INTEGRATION_GUIDE.md` - Full API documentation
- `api_usage_examples.py` - Code examples

For backend issues, check:
- `INTEGRATION_SUMMARY.md` - Quick reference
- App server logs for model loading status

---

**Last Updated**: January 22, 2026  
**Priority**: High - Enables full model functionality  
**Estimated Effort**: 2-4 hours
