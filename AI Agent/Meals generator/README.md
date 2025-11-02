Visheshta from IIT Roorkee, Civil Engineering 
# 🥗 Smart Meal Planner (RAG + LoRA) v3.1.0

A multi-user AI meal planner that uses RAG and LoRA to create personalized meal plans (1–6 meals/day) with a beautiful Streamlit dashboard and Excel/CSV batch mode.

## ✨ Features

- ✅ **Multi-agent orchestration** (Planner, Nutritionist, RAG Retriever, Optimizer, Evaluator, Coach)
- ✅ **RAG integration** (ChromaDB / FAISS) for nutrition data retrieval
- ✅ **LoRA fine-tuning** support for meal generation
- ✅ **Batch processing** for multiple users via CSV/Excel upload
- ✅ **Flexible meal counts** (1-6 meals per day)
- ✅ **12+ goal types** (Weight loss, Keto, Diabetic-friendly, etc.)
- ✅ **Meal timing** with customizable schedules
- ✅ **Excel & CSV support** for batch inputs and outputs
- ✅ **Animated meal cards** and interactive charts
- ✅ **Beautiful dashboard** with glass-style cards and gradients

## 🚀 Quick Start

### Installation
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run Single-User Mode
```bash
streamlit run app.py
```

### Run Batch Excel/CSV Mode
```bash
streamlit run app.py
# Then use the "📂 Multi-User Excel Mode" tab
```

## 📋 CSV/Excel Format for Batch Processing

See `CSV_FORMAT_GUIDE.md` for detailed format requirements.

**Required columns:** UserID, Name, Age, Gender, Goal, Target_Calories, Diet_Preference, Meals_Per_Day, Meal_Times, Allergies, Health_Conditions  
**Optional columns:** Activity_Level, Cuisine_Preference

**Accepted formats:** CSV or Excel (.xlsx)

Download example template: `examples/batch_input_template.csv`

## 🎯 Supported Goals

- Weight loss
- Weight maintenance  
- Muscle gain
- Fat loss
- Balanced diet
- Keto
- Low-carb
- High-protein
- Diabetic-friendly
- Heart-healthy
- Pescatarian
- Gluten-free

## 📊 Output Formats

- **Single user:** Animated meal cards + pie chart + CSV/JSON download
- **Batch mode:** Combined Excel/CSV export with all users' meal plans
- **API:** JSON responses (via FastAPI)
- **CLI:** JSON/CSV file output

## 🎨 Assets & Theming

Place images in the `assets/` directory:
- `assets/banner_mealplanner.png` - Top banner image
- `assets/logo_forkleaf.png` - Logo image
- `assets/bg_gradient.png` - Background gradient
- `assets/icons/` - Icon files (user.png, meal.png, chart.png, download.png)

## 📝 Notes

- Fill API keys in `secrets.py` if using external nutrition APIs
- Place LoRA checkpoints in `models/lora_meal_generator/`
- Build RAG index with `scripts/build_rag_index.py`
- Meal count automatically clipped to 1-6 range
- Excel support requires `openpyxl` package

## 🗂️ Project Structure

```
├── app.py                 # Main Streamlit dashboard
├── agents/                # Agent implementations
├── data/                  # Input data (user_profiles.xlsx)
├── models/                # LoRA models
├── assets/                # Images and icons
├── outputs/               # Generated meal plans
├── logs/                  # Evaluation logs
└── examples/              # Example CSV templates
```

