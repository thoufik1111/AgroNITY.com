# 🌾 AgroNity - Quick Start Guide

## System Requirements
- Python 3.7+
- Flask
- TensorFlow/Keras
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Microphone (for voice input)

## Installation

### 1. Install Dependencies
```bash
cd "c:\Users\Darunima DH\OneDrive\Desktop\SIH"
pip install -r requirements.txt
```

### 2. Verify Models Are Loaded
```bash
python -c "import agronity_test as ag; ag.load_models(); print('✓ All models loaded successfully')"
```

### 3. Start the Server
```bash
python app.py
```

Output should show:
```
 * Running on http://127.0.0.1:5000
```

### 4. Open in Browser
Open: **http://localhost:5000**

---

## 🚀 Quick Test

### Test 1: Voice Input + Chatbot (30 seconds)
```
1. Login with OTP: 2622
2. Click the 🎤 (microphone) button
3. Say: "How much water does paddy need?"
4. Check bot responds with watering advice
5. Say: "How to prevent rice blast?"
6. Check disease management response
```

### Test 2: Dynamic Graphs (30 seconds)
```
1. Stay logged in
2. Select: Crop=Paddy, District=Sangrur, Area=2, Soil=Alluvial
3. Click "Submit"
4. Watch graph update with 12-month profit projection
5. Change crop to Wheat, area to 5
6. Click "Submit" again
7. Notice graph changed completely
```

### Test 3: Image Classification (30 seconds)
```
1. Click "Upload Image"
2. Upload any image with crop name: rice.jpg, tomato.jpg, maize.jpg, etc.
3. System analyzes and shows:
   - Crop identification
   - Health status
   - Disease risk
   - Farming recommendations
   - Production statistics
```

---

## 🎯 Feature Summary

### ✅ Voice Input (NEW)
- Speak agricultural questions in English
- Chatbot responds with farming advice
- 11+ query categories supported
- Auto-sends transcribed text

### ✅ Dynamic Graphs (ENHANCED)
- Real-time 12-month profit projections
- Updates based on analysis results
- Different inputs = different graphs
- Shows realistic variations and growth

### ✅ Image Classification (EXPANDED)
- Now supports 12+ crop types (was 6)
- Includes health assessment
- Provides crop-specific recommendations
- Shows disease risk and statistics

---

## 📊 Supported Crops (12+)

| Crop | Filename | Alternative Names |
|------|----------|------------------|
| Rice | rice.jpg | paddy.jpg |
| Wheat | wheat.jpg | - |
| Tomato | tomato.jpg | - |
| Cotton | cotton.jpg | - |
| Groundnut | groundnut.jpg | mungfali.jpg |
| Sugarcane | sugarcane.jpg | - |
| Maize | maize.jpg | corn.jpg |
| Chilli | chilli.jpg | pepper.jpg |
| Soybean | soybean.jpg | - |
| Mustard | mustard.jpg | - |
| Potato | potato.jpg | - |
| Onion | onion.jpg | - |

---

## 🔧 Troubleshooting

### Voice Not Working?
- ✓ Reload browser
- ✓ Check microphone permission
- ✓ Try Chrome/Firefox
- ✓ Speak slowly and clearly

### Graph Not Updating?
- ✓ Ensure feasibility is "FEASIBLE" ✅
- ✓ Try different crop selection
- ✓ Check browser console (F12)
- ✓ Refresh page

### Image Not Recognized?
- ✓ Include crop name in filename
- ✓ Use supported crop names
- ✓ Try alternatives (corn for maize)
- ✓ Check file format (JPG/PNG/GIF)

---

## 📝 Important Notes

1. **OTP for Login**: `2622`
2. **Server Address**: `http://localhost:5000`
3. **Voice Language**: English only (for now)
4. **Available Models**: 
   - Sklearn (default)
   - Agri ML (regional data)
   - Keras CNN (image analysis)

---

## 📚 Documentation

For detailed information, see:
- `FEATURES_DOCUMENTATION.md` - Complete feature guide
- `requirements.txt` - All dependencies
- `app.py` - Backend API
- `sih.html` - Frontend interface
- `agronity_test.py` - ML models and analysis

---

## 🧪 Run Tests

### Test Image Classification
```bash
python test_image_classification.py
```

### Test API Endpoints
```bash
python test_api.py
```

---

## 💡 Tips for Best Results

1. **Voice Input**:
   - Speak naturally and clearly
   - Use agricultural keywords (water, fertilizer, pest, etc.)
   - Ask one question at a time
   - System works best with English accent

2. **Graphs**:
   - Submit multiple analyses to see different patterns
   - Higher profit values show clearer graph patterns
   - Monthly variations are realistic (±30%)

3. **Image Upload**:
   - Use clear, well-lit crop images
   - Include crop name in filename
   - JPG format recommended
   - File size < 5MB

---

## 🎓 Learning Resources

### Agricultural Queries That Work Well:
- "How to increase rice yield?"
- "What's the best fertilizer for wheat?"
- "When should I water my tomato plants?"
- "How to prevent cotton diseases?"
- "What are current mandi prices?"
- "Tell me about government farming schemes"
- "How to practice organic farming?"
- "What soil pH is best for groundnut?"

---

## 📞 Support

For questions or issues:
1. Check the documentation
2. Review test output
3. Check browser console (F12)
4. Try the troubleshooting section above

---

**Happy Farming! 🌾🚜**
