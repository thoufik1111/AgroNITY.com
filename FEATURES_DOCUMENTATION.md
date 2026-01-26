# AgroNity - Enhanced Features Documentation

## Overview
This document describes the three major feature enhancements made to the AgroNity agricultural advisory system.

---

## 1. Voice Input with Chatbot Responses 🎤

### How It Works
- **Technology**: Web Speech API (browser-native, no installation needed)
- **Language**: English voice recognition
- **Auto-Response**: User speech is transcribed, and the chatbot automatically responds with agricultural advice

### Features
✅ **Voice Recording**: Click the microphone button to start/stop recording
✅ **Real-time Feedback**: "🎤 Listening..." displays while recording
✅ **Transcript Display**: Shows what the system heard in real-time
✅ **Auto-Send**: Speech automatically sends to chat when recording ends
✅ **Intelligent Responses**: Chatbot provides answers to 11+ agricultural query categories

### Supported Agricultural Topics
1. **💧 Watering & Irrigation** - "How much water for rice?"
2. **🌾 Fertilizers & NPK** - "What's the NPK ratio for cotton?"
3. **🐛 Pest & Disease Management** - "How to prevent rust in wheat?"
4. **🌾 Yield Improvement** - "How to increase paddy production?"
5. **🔬 Soil Health** - "What should be the soil pH?"
6. **💰 Cost Estimation** - "How much does tomato cost?"
7. **☀️ Weather Considerations** - "When to sow wheat?"
8. **🌱 Organic Farming** - "How to farm organically?"
9. **🏛️ Government Schemes** - "What subsidies are available?"
10. **📈 Market Prices** - "What are current mandi rates?"
11. **👋 General Help** - "How can you help me?"

### Usage Instructions
```
1. Login with OTP: 2622
2. Click the microphone (🎤) button in chat controls
3. Speak your agricultural question in English
4. System displays what it heard
5. Wait for chatbot response with relevant advice
6. Continue the conversation
```

### Browser Support
- Chrome/Chromium 25+
- Firefox 25+
- Opera 27+
- Edge 79+
- Safari 14.1+

---

## 2. Dynamic Graph Updates 📊

### How It Works
- **Before**: Graph showed hardcoded constant values
- **Now**: Graph generates dynamic 12-month projections based on actual analysis results

### Features
✅ **Real-time Updates**: Chart updates when you submit feasibility analysis
✅ **Profit Projections**: Shows 12-month profit trends
✅ **Growth Modeling**: Includes realistic growth patterns
✅ **Result-Based**: Each different input generates different graph
✅ **Visual Feedback**: Bot confirms graph update with message

### Data Points
- **Base Data**: Profit result from feasibility analysis
- **Monthly Variation**: ±30% natural variation
- **Growth Factor**: 2% growth per month (realistic agricultural pattern)
- **12 Months**: January through December projections

### Usage Instructions
```
1. Select crop, district, area, and soil type
2. Click "Submit" button
3. System analyzes feasibility
4. Graph automatically updates with 12-month projections
5. Profit trends shown with realistic variations
6. Different inputs = different graph shapes
```

### Example Output
```
If profit = ₹50,000:
- Month 1: ₹35,000-38,000 (base + variation)
- Month 2: ₹36,000-39,500 (base + variation + growth)
- ...
- Month 12: ₹48,000-60,000 (base + variation + 24% growth)
```

---

## 3. Enhanced Image Classification 🖼️

### How It Works
- **Before**: Only detected 6 crop types (rice, tomato, wheat, cotton, groundnut, paddy)
- **Now**: Supports 12+ crop types with health assessment and recommendations

### Supported Crops
✅ Rice (and alternative "Paddy")
✅ Wheat
✅ Tomato
✅ Cotton
✅ Groundnut (and "Mungfali" variants)
✅ **[NEW]** Sugarcane
✅ **[NEW]** Maize/Corn
✅ **[NEW]** Chilli/Pepper
✅ **[NEW]** Soybean
✅ **[NEW]** Mustard
✅ **[NEW]** Potato
✅ **[NEW]** Onion

### Classification Features
✅ **Crop Detection**: From filename patterns and image analysis
✅ **Health Assessment**: Healthy/Diseased classification
✅ **Confidence Score**: Indicates certainty of classification
✅ **Disease Risk**: Low/High risk assessment
✅ **Crop Statistics**: Average production and mandi prices from dataset
✅ **Recommendations**: Specific cultivation tips for each crop

### Supported Disease Keywords
- Disease, Sick, Brown, Rust, Blight, Rot

### Multilingual Support
- Crop names detected in: English, Hindi, Tamil, and Punjabi

### Usage Instructions
```
1. Click "Upload Image" button
2. Select an image with crop name in filename (e.g., "tomato.jpg")
3. System analyzes the image
4. Get crop identification, health status, and recommendations
5. View disease risk and production statistics
```

### Example Output
```
Crop: Tomato
Health Status: Healthy (Confidence: 0.65)
Disease Risk: Low
Recommendation: Use trellising system. Daily monitoring for late blight...
Avg Production: X tons/year
Mandi Price: ₹Y/kg
```

### Fallback Mechanism
- **Keras CNN**: Tries first (if available)
- **Rule-based Detection**: Falls back if Keras fails
- **Error Handling**: Graceful degradation with helpful messages

---

## Technical Implementation

### Frontend (sih.html)
```javascript
// Voice Recognition Setup
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
recognition.lang = 'en-US';
// Auto-sends transcribed text to chat

// Chatbot Response Generator
function generateChatbotResponse(question) {
    // 11+ response categories with agricultural advice
    // Returns formatted markdown with emojis and helpful info
}

// Dynamic Chart Update
function updateChartDynamically(result) {
    // Takes profit_rs from analysis result
    // Generates 12-month projections
    // Updates Chart.js with new data
}
```

### Backend (agronity_test.py)
```python
def _analyze_image_ruleset(data_df, filename):
    """Enhanced with 12+ crop detection"""
    # Detects crop from filename patterns
    # Assesses health status
    # Provides crop-specific recommendations
    # Returns statistics from dataset

def get_crop_recommendations(crop):
    """Returns crop-specific farming tips"""
    # Unique recommendations for each of 12+ crops
```

---

## Testing

### Test Voice Input
```
1. Open http://localhost:5000
2. Login (OTP: 2622)
3. Click microphone button
4. Say: "How much water does rice need?"
5. Check bot response
```

### Test Dynamic Graphs
```
1. Select Crop: Paddy, District: Sangrur, Area: 2, Soil: Alluvial
2. Click Submit
3. Observe graph updates automatically
4. Try different inputs to see graph change
```

### Test Image Classification
```
1. Upload images named: rice.jpg, tomato.jpg, maize.jpg, etc.
2. System should identify crop and provide analysis
3. All 12+ crops should be recognized
```

### Automated Tests
```bash
# Test image classification
python test_image_classification.py

# Test API endpoints
python test_api.py
```

---

## Performance Metrics

| Feature | Status | Coverage |
|---------|--------|----------|
| Voice Input | ✅ Fully Implemented | English speech recognition |
| Chatbot | ✅ 11+ Categories | Covers major farming queries |
| Dynamic Graphs | ✅ Real-time Updates | All analysis results |
| Image Classification | ✅ 12+ Crops | Expanded from 6 to 12+ |
| Recommendations | ✅ Crop-specific | All 12+ crops covered |

---

## Troubleshooting

### Voice Not Working
- **Issue**: Microphone button not responding
- **Solution**: 
  - Check browser compatibility (Chrome/Firefox/Edge)
  - Allow microphone permission when prompted
  - Speak clearly in English
  - Check internet connection

### Graph Not Updating
- **Issue**: Chart stays with default values
- **Solution**:
  - Make sure feasibility analysis is successful (shows ✅)
  - Try with different crop/district/soil
  - Check browser console for errors
  - Reload page and try again

### Image Classification Fails
- **Issue**: "Could not identify crop type" error
- **Solution**:
  - Include crop name in filename (e.g., rice.jpg, tomato.jpeg)
  - Use supported crop names (see list above)
  - Try common variations (paddy for rice, corn for maize)
  - Check file format (JPG, PNG, GIF supported)

---

## Future Enhancements

1. **Multi-language Voice**: Support for Hindi, Tamil, Telugu
2. **Advanced CNN**: Train dedicated crop classification model
3. **Real-time Disease Detection**: ML-based pest identification
4. **Weather Integration**: Live weather API for recommendations
5. **Market Integration**: Real-time mandi price updates
6. **Historical Data**: Track previous crops and profits
7. **SMS Alerts**: Push notifications for critical farming events

---

## Credits & References

- **Web Speech API**: Mozilla Developer Network
- **Chart.js**: Chart library for JavaScript
- **TensorFlow/Keras**: Deep learning framework
- **Sklearn**: Machine learning library
- **Agricultural Data**: Punjab & Tamil Nadu regional datasets

---

## Support
For issues or feature requests, contact the development team.
