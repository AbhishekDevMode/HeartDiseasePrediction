# ❤️ CardioCheck: Heart Disease Risk Assessment Tool

An educational, interactive web application that estimates heart disease risk based on clinical measurements and diagnostic test results using standard UCI Heart Disease parameters.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## 🌟 Key Features

- **Clinical Input Suite**: Collects 13 standard UCI cardiac parameters (Demographics, Exercise Testing, Resting ECG, Fluoroscopy, Thalassemia).
- **Instant Risk Assessment**: Evaluates log-odds probability and categorizes risk into **Low**, **Moderate**, and **High**.
- **Diagnostic Factor Breakdown**: Identifies specific contributing metrics (e.g., elevated resting blood pressure, cholesterol limit exceedance, ST depression, exercise-induced angina).
- **Preset Demonstration Profiles**: Easily load representative patient profiles (UCI Baseline Sample, Low Risk, Moderate Risk, High Risk) with a single click.
- **Downloadable Clinical Report**: Generates and exports a structured assessment summary in text format for academic presentation.
- **Safety First**: Prominent emergency warning banner and medical disclaimers emphasizing educational use.

---

## 🚀 How to Run Locally

### 1. Prerequisites
Ensure you have Python 3.9+ installed.

### 2. Clone the Repository
```bash
git clone https://github.com/AbhishekDevMode/HeartDiseasePrediction.git
cd HeartDiseasePrediction
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run streamlit_app.py
```
Or:
```bash
streamlit run app.py
```
The application will open in your default browser at `http://localhost:8501`.

---

## ☁️ How to Deploy on Streamlit Community Cloud (Step-by-Step)

Streamlit Community Cloud is 100% free and deploys directly from your GitHub repository:

### Step 1: Push the Latest Code to GitHub
Open your terminal in this repository and run:
```bash
git add .
git commit -m "Add Streamlit deployment configuration and app"
git push origin main
```

### Step 2: Go to Streamlit Community Cloud
1. Navigate to **[share.streamlit.io](https://share.streamlit.io/)**.
2. Sign in with your **GitHub account**.

### Step 3: Deploy the App
1. Click the **"New app"** (or **"Create app"**) button.
2. Configure the deployment settings:
   - **Repository:** `AbhishekDevMode/HeartDiseasePrediction`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py` *(or `app.py`)*
3. Click **"Deploy!"**.

Streamlit will automatically detect `requirements.txt`, install dependencies, apply the theme from `.streamlit/config.toml`, and make your website live at a public URL (e.g., `https://heartdiseaseprediction-xxxx.streamlit.app`).

---

## 📊 Clinical Parameters (UCI Standard)

| Parameter | Description | Reference / Normal Range |
| :--- | :--- | :--- |
| `age` | Patient age in years | 18 – 120 |
| `sex` | Biological sex | Male (1), Female (0) |
| `cp` | Chest pain classification | 0: Typical angina, 1: Atypical angina, 2: Non-anginal, 3: Asymptomatic |
| `trestbps` | Resting blood pressure | Normal: < 120 mm Hg |
| `chol` | Total serum cholesterol | Desirable: < 200 mg/dL |
| `fbs` | Fasting blood sugar > 120 mg/dL | Normal: No (0), Elevated: Yes (1) |
| `restecg` | Resting electrocardiogram | 0: Normal, 1: ST-T wave abnormality, 2: LV hypertrophy |
| `thalach` | Maximum heart rate achieved | Peak exercise heart rate (bpm) |
| `exang` | Exercise-induced angina | No (0), Yes (1) |
| `oldpeak` | ST depression induced by exercise | 0.0 – 10.0 mm |
| `slope` | Peak exercise ST slope | 0: Upsloping, 1: Flat, 2: Downsloping |
| `ca` | Major vessels colored by fluoroscopy | 0 – 4 vessels |
| `thal` | Thalassemia / perfusion scintigraphy | 1: Normal, 2: Fixed defect, 3: Reversible defect |

---

## 📂 Project Structure

```
HeartDiseasePrediction/
├── .streamlit/
│   └── config.toml          # Custom theme and server settings
├── app.py                   # Streamlit Cloud root entrypoint
├── streamlit_app.py         # Full featured Streamlit application
├── requirements.txt         # Python dependencies for deployment
├── .gitignore               # Git ignore rules
├── README.md                # Project documentation and deployment guide
├── backend/                 # Optional FastAPI backend service
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
└── frontend/                # Optional React/Vite web interface
    ├── src/
    ├── package.json
    └── vite.config.js
```

---

## ⚠️ Medical Disclaimer

*CardioCheck is developed strictly for educational and academic demonstration purposes. It does not provide medical diagnoses, clinical guidance, or emergency advice. Individuals experiencing chest pain, acute pressure, shortness of breath, or other cardiac symptoms should seek immediate emergency medical care.*
