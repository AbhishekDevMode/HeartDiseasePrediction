"""CardioCheck - Heart Disease Risk Assessment Tool
Educational Web Application ready for Streamlit Community Cloud deployment.
"""

from __future__ import annotations

import math
from typing import Dict, Any, Tuple
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CardioCheck | Heart Disease Risk Assessment",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# CUSTOM CSS STYLING (matching the modern medical aesthetic)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,700;1,6..72,400&display=swap');

    :root {
        --brand-teal: #087e8b;
        --brand-teal-dark: #056b76;
        --brand-navy: #0b2942;
        --text-slate: #334e68;
        --text-muted: #627d98;
        --card-bg: #ffffff;
        --card-border: #dce8ef;
        --badge-low-bg: #d8f3dc;
        --badge-low-txt: #116149;
        --badge-mod-bg: #fff3cd;
        --badge-mod-txt: #895a00;
        --badge-high-bg: #ffe3e3;
        --badge-high-txt: #9b2c2c;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3.5rem;
        max-width: 1200px;
    }

    /* Headings */
    .hero-eyebrow {
        font-size: 0.75rem;
        letter-spacing: 0.14em;
        font-weight: 800;
        color: #13759a;
        margin-bottom: 0.4rem;
        text-transform: uppercase;
    }

    .hero-title {
        font-family: 'Newsreader', Georgia, serif;
        font-size: clamp(2.2rem, 3.8vw, 3.2rem);
        color: #0b2942;
        font-weight: 700;
        line-height: 1.12;
        margin-bottom: 0.8rem;
    }

    .hero-lede {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #486581;
        margin-bottom: 1.5rem;
    }

    /* Emergency Alert Banner */
    .emergency-box {
        background: #073b5c;
        color: #ffffff;
        padding: 18px 22px;
        border-radius: 14px;
        box-shadow: 0 10px 25px rgba(11, 41, 66, 0.12);
        margin-bottom: 1.8rem;
        display: flex;
        align-items: flex-start;
        gap: 16px;
    }

    .emergency-icon {
        color: #ff8b7b;
        font-size: 1.8rem;
        line-height: 1;
        margin-top: 2px;
    }

    .emergency-content h4 {
        margin: 0 0 4px 0;
        color: #ffffff;
        font-weight: 700;
        font-size: 1rem;
    }

    .emergency-content p {
        margin: 0;
        color: #d9edf6;
        font-size: 0.88rem;
        line-height: 1.45;
    }

    /* Custom Cards */
    .custom-card {
        background: #ffffff;
        border: 1px solid #dce8ef;
        border-radius: 14px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(16, 42, 67, 0.05);
        margin-bottom: 1.5rem;
    }

    .card-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #0b2942;
        margin-bottom: 0.3rem;
    }

    .card-subtitle {
        font-size: 0.85rem;
        color: #627d98;
        margin-bottom: 1.2rem;
    }

    /* Result Panel */
    .result-card {
        background: #eef9f8;
        border: 1px solid #c9e5e2;
        border-radius: 16px;
        padding: 28px 24px;
        box-shadow: 0 10px 30px rgba(16, 42, 67, 0.06);
        text-align: center;
    }

    .badge-pill {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.9rem;
        letter-spacing: 0.02em;
        margin-bottom: 14px;
    }

    .badge-pill.low {
        background: #d8f3dc;
        color: #116149;
        border: 1px solid #b7e4c7;
    }

    .badge-pill.moderate {
        background: #fff3cd;
        color: #895a00;
        border: 1px solid #ffe69c;
    }

    .badge-pill.high {
        background: #ffe3e3;
        color: #9b2c2c;
        border: 1px solid #f8b4b4;
    }

    .probability-number {
        font-family: 'Newsreader', Georgia, serif;
        font-size: 4.2rem;
        font-weight: 700;
        color: #0b2942;
        line-height: 1;
        margin: 12px 0;
    }

    .result-copy {
        font-size: 1.02rem;
        font-weight: 600;
        color: #102a43;
        line-height: 1.55;
        margin-bottom: 14px;
    }

    .disclaimer-text {
        font-size: 0.82rem;
        color: #627d98;
        line-height: 1.5;
        border-top: 1px solid #c9e5e2;
        padding-top: 14px;
        margin-top: 14px;
    }

    /* Breakdown list */
    .factor-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 6px;
        font-size: 0.86rem;
    }
    .factor-item.elevated {
        background: #fff5f5;
        border-left: 3px solid #e53e3e;
        color: #742a2a;
    }
    .factor-item.normal {
        background: #f0fff4;
        border-left: 3px solid #38a169;
        color: #22543d;
    }

    /* Buttons */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.15s ease-in-out;
    }

    div.stButton > button[kind="primary"] {
        background-color: #087e8b !important;
        border-color: #087e8b !important;
        color: #ffffff !important;
        padding: 0.65rem 1.4rem;
        font-size: 1rem;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #056b76 !important;
        border-color: #056b76 !important;
    }

    /* Footer */
    .app-footer {
        text-align: center;
        font-size: 0.82rem;
        color: #829ab1;
        margin-top: 3.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e2e8f0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# CORE RISK ALGORITHM (100% equivalent to backend/app/main.py)
# -----------------------------------------------------------------------------
def sigmoid(value: float) -> float:
    """Logistic sigmoid function with clamped input bounds."""
    return 1.0 / (1.0 + math.exp(-max(min(value, 30.0), -30.0)))


def calculate_risk(patient: Dict[str, Any]) -> Tuple[float, float, Dict[str, Any]]:
    """Calculates heart disease probability based on UCI Heart Disease parameters.

    Returns:
        probability: float [0, 1]
        raw_score: float linear logit
        factors: dict breakdown of positive contributors
    """
    age = int(patient["age"])
    sex = int(patient["sex"])
    cp = int(patient["cp"])
    trestbps = int(patient["trestbps"])
    chol = int(patient["chol"])
    fbs = int(patient["fbs"])
    restecg = int(patient["restecg"])
    thalach = int(patient["thalach"])
    exang = int(patient["exang"])
    oldpeak = float(patient["oldpeak"])
    slope = int(patient["slope"])
    ca = int(patient["ca"])
    thal = int(patient["thal"])

    # Base intercept
    score = -5.25

    # Linear terms
    score += 0.055 * (age - 45)
    score += 0.42 * sex
    score += [0.0, 0.28, 0.7, 1.18][cp]
    score += 0.016 * max(trestbps - 120, 0)
    score += 0.006 * max(chol - 200, 0)
    score += 0.32 * fbs
    score += 0.20 * restecg
    score += 0.028 * max(150 - thalach, 0)
    score += 0.88 * exang
    score += 0.42 * oldpeak
    score += [0.0, 0.30, 0.62][slope]
    score += 0.48 * ca
    score += [0.0, 0.20, 0.56, 0.78][thal]

    prob = sigmoid(score)

    # Detailed contributing factor analysis for clinical explanation
    factor_notes = []
    if trestbps > 120:
        factor_notes.append({
            "name": "Resting Blood Pressure",
            "val": f"{trestbps} mm Hg",
            "status": "elevated",
            "impact": f"+{round(0.016 * (trestbps - 120), 2)} log-odds (> 120 mm Hg baseline)"
        })
    else:
        factor_notes.append({
            "name": "Resting Blood Pressure",
            "val": f"{trestbps} mm Hg",
            "status": "normal",
            "impact": "Within optimal baseline (≤ 120 mm Hg)"
        })

    if chol > 200:
        factor_notes.append({
            "name": "Serum Cholesterol",
            "val": f"{chol} mg/dL",
            "status": "elevated",
            "impact": f"+{round(0.006 * (chol - 200), 2)} log-odds (> 200 mg/dL desirable limit)"
        })
    else:
        factor_notes.append({
            "name": "Serum Cholesterol",
            "val": f"{chol} mg/dL",
            "status": "normal",
            "impact": "Within desirable limit (≤ 200 mg/dL)"
        })

    if exang == 1:
        factor_notes.append({
            "name": "Exercise-Induced Angina",
            "val": "Present (Yes)",
            "status": "elevated",
            "impact": "+0.88 log-odds (significant cardiac stress indicator)"
        })

    if oldpeak > 0.0:
        factor_notes.append({
            "name": "ST Depression (Oldpeak)",
            "val": f"{oldpeak} mm",
            "status": "elevated",
            "impact": f"+{round(0.42 * oldpeak, 2)} log-odds (ECG myocardial stress marker)"
        })

    if cp > 0:
        cp_names = {1: "Atypical angina", 2: "Non-anginal pain", 3: "Asymptomatic"}
        cp_weights = {1: 0.28, 2: 0.70, 3: 1.18}
        factor_notes.append({
            "name": "Chest Pain Classification",
            "val": cp_names.get(cp, "Unspecified"),
            "status": "elevated",
            "impact": f"+{cp_weights.get(cp, 0.0)} log-odds"
        })

    if ca > 0:
        factor_notes.append({
            "name": "Major Vessels (Fluoroscopy)",
            "val": f"{ca} vessel(s)",
            "status": "elevated",
            "impact": f"+{round(0.48 * ca, 2)} log-odds"
        })

    if thalach < 150:
        factor_notes.append({
            "name": "Max Heart Rate Achieved",
            "val": f"{thalach} bpm",
            "status": "elevated",
            "impact": f"+{round(0.028 * (150 - thalach), 2)} log-odds (below 150 bpm baseline)"
        })

    return prob, score, {"factors": factor_notes}


# -----------------------------------------------------------------------------
# PRESET PATIENT PROFILES
# -----------------------------------------------------------------------------
PRESETS = {
    "Default Sample (UCI Baseline)": {
        "age": 54, "sex": 1, "cp": 2, "trestbps": 130, "chol": 246,
        "fbs": 0, "restecg": 1, "thalach": 150, "exang": 0, "oldpeak": 1.4,
        "slope": 1, "ca": 0, "thal": 2
    },
    "Low-Risk Profile (Healthy Baseline)": {
        "age": 32, "sex": 0, "cp": 0, "trestbps": 112, "chol": 178,
        "fbs": 0, "restecg": 0, "thalach": 172, "exang": 0, "oldpeak": 0.0,
        "slope": 0, "ca": 0, "thal": 1
    },
    "Moderate-Risk Profile": {
        "age": 56, "sex": 1, "cp": 1, "trestbps": 138, "chol": 245,
        "fbs": 0, "restecg": 1, "thalach": 140, "exang": 1, "oldpeak": 1.6,
        "slope": 1, "ca": 1, "thal": 2
    },
    "High-Risk Profile": {
        "age": 67, "sex": 1, "cp": 3, "trestbps": 164, "chol": 298,
        "fbs": 1, "restecg": 2, "thalach": 115, "exang": 1, "oldpeak": 3.2,
        "slope": 2, "ca": 2, "thal": 3
    }
}

# -----------------------------------------------------------------------------
# INITIALIZE SESSION STATE
# -----------------------------------------------------------------------------
if "patient_data" not in st.session_state:
    st.session_state.patient_data = PRESETS["Default Sample (UCI Baseline)"].copy()

def load_preset(preset_name: str):
    """Loads a preset into session state."""
    st.session_state.patient_data = PRESETS[preset_name].copy()


# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🩺 Quick Presets")
    st.caption("Load demonstration patient profiles or reset fields:")

    selected_preset = st.selectbox(
        "Select Profile Template:",
        list(PRESETS.keys()),
        index=0,
        help="Quickly populate clinical inputs with typical test scenarios."
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("📥 Apply Profile", use_container_width=True):
            load_preset(selected_preset)
            st.rerun()
    with col_btn2:
        if st.button("↺ Reset Defaults", use_container_width=True):
            load_preset("Default Sample (UCI Baseline)")
            st.rerun()

    st.markdown("---")
    st.markdown("### 📘 Clinical Parameter Glossary")
    with st.expander("View measurement details"):
        st.markdown(
            """
            - **trestbps**: Resting blood pressure (mm Hg) measured on hospital admission. Normal is < 120 mm Hg.
            - **chol**: Serum cholesterol (mg/dL). Normal desirable level is < 200 mg/dL.
            - **cp (Chest Pain)**:
              - *0: Typical Angina* (chest discomfort with physical exertion)
              - *1: Atypical Angina* (non-classical presentation)
              - *2: Non-anginal pain* (musculoskeletal or other non-cardiac)
              - *3: Asymptomatic* (silent ischemia)
            - **fbs**: Fasting blood sugar > 120 mg/dL (1 = true, 0 = false; marker for diabetes/insulin resistance).
            - **restecg**: Resting electrocardiographic results.
            - **thalach**: Maximum heart rate achieved during exercise stress testing.
            - **exang**: Exercise-induced angina (1 = yes, 0 = no).
            - **oldpeak**: ST depression induced by exercise relative to rest (marker of myocardial ischemia).
            - **slope**: Slope of peak exercise ST segment (0 = upsloping, 1 = flat, 2 = downsloping).
            - **ca**: Number of major vessels (0–4) colored by fluoroscopy.
            - **thal**: Thalassemia blood condition (1 = normal, 2 = fixed defect, 3 = reversible defect).
            """
        )

    st.markdown("---")
    st.caption("CardioCheck v1.0 • Educational AI Project")


# -----------------------------------------------------------------------------
# MAIN CONTENT / HERO
# -----------------------------------------------------------------------------
st.markdown('<p class="hero-eyebrow">EDUCATIONAL SCREENING TOOL</p>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Understand heart-health risk factors.</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-lede">Enter clinical measurements to get an educational risk estimate. '
    'It is designed to support—not replace—a conversation with a healthcare professional.</p>',
    unsafe_allow_html=True,
)

# Emergency Warning Banner
st.markdown(
    """
    <div class="emergency-box">
        <div class="emergency-icon">♥</div>
        <div class="emergency-content">
            <h4>Not for emergencies</h4>
            <p>If you have chest pain, shortness of breath, acute pressure radiating to your arm or jaw, '
            'or another emergency symptom, contact local emergency services immediately.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# INPUT SECTION (Organized into structured tabs)
# -----------------------------------------------------------------------------
p = st.session_state.patient_data

st.markdown("### 📋 Patient Clinical Measurements")
st.caption("Provide patient vitals and diagnostic test results below:")

tab1, tab2, tab3 = st.tabs([
    "👤 1. Demographics & Vitals",
    "🏃 2. Symptoms & Exercise Response",
    "🔬 3. Diagnostics & Imaging"
])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        age_val = st.number_input(
            "Age (years)",
            min_value=18,
            max_value=120,
            value=int(p.get("age", 54)),
            step=1,
            help="Patient age in years (18–120)."
        )

        sex_val = st.selectbox(
            "Biological Sex",
            options=[1, 0],
            format_func=lambda x: "Male" if x == 1 else "Female",
            index=0 if p.get("sex", 1) == 1 else 1,
            help="Biological sex as encoded in standard cardiac datasets (0 = Female, 1 = Male)."
        )

        fbs_val = st.selectbox(
            "Fasting Blood Sugar > 120 mg/dL",
            options=[0, 1],
            format_func=lambda x: "No (≤ 120 mg/dL)" if x == 0 else "Yes (> 120 mg/dL)",
            index=int(p.get("fbs", 0)),
            help="Elevated fasting blood sugar is an indicator of prediabetes or diabetes."
        )

    with col2:
        trestbps_val = st.number_input(
            "Resting Blood Pressure (mm Hg)",
            min_value=70,
            max_value=260,
            value=int(p.get("trestbps", 130)),
            step=1,
            help="Resting blood pressure measured in mm Hg upon clinical intake."
        )

        chol_val = st.number_input(
            "Serum Cholesterol (mg/dL)",
            min_value=80,
            max_value=700,
            value=int(p.get("chol", 246)),
            step=1,
            help="Total serum cholesterol level in mg/dL. Desirable target is under 200 mg/dL."
        )

with tab2:
    col3, col4 = st.columns(2)
    with col3:
        cp_options = {
            0: "Typical angina (chest pain on exertion)",
            1: "Atypical angina (unusual chest discomfort)",
            2: "Non-anginal pain (non-cardiac origin)",
            3: "Asymptomatic (no overt chest discomfort)"
        }
        cp_val = st.selectbox(
            "Chest Pain Type",
            options=list(cp_options.keys()),
            format_func=lambda x: cp_options[x],
            index=int(p.get("cp", 2)),
            help="Nature and character of reported chest discomfort."
        )

        thalach_val = st.number_input(
            "Maximum Heart Rate Achieved (thalach - bpm)",
            min_value=40,
            max_value=240,
            value=int(p.get("thalach", 150)),
            step=1,
            help="Peak heart rate achieved during cardiac exercise stress test."
        )

        exang_val = st.selectbox(
            "Exercise-Induced Angina",
            options=[0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes",
            index=int(p.get("exang", 0)),
            help="Whether physical exertion triggers angina or chest tightness."
        )

    with col4:
        oldpeak_val = st.number_input(
            "ST Depression Induced by Exercise (Oldpeak - mm)",
            min_value=0.0,
            max_value=10.0,
            value=float(p.get("oldpeak", 1.4)),
            step=0.1,
            format="%.1f",
            help="ST segment depression observed on ECG during exercise compared to baseline."
        )

        slope_options = {
            0: "Upsloping (favorable response)",
            1: "Flat (potential ischemic response)",
            2: "Downsloping (strongly abnormal/ischemic)"
        }
        slope_val = st.selectbox(
            "Slope of Peak Exercise ST Segment",
            options=list(slope_options.keys()),
            format_func=lambda x: slope_options[x],
            index=int(p.get("slope", 1)),
            help="Geometric slope of the ST segment at peak exercise."
        )

with tab3:
    col5, col6 = st.columns(2)
    with col5:
        restecg_options = {
            0: "Normal",
            1: "ST-T Wave Abnormality (T wave inversions / ST changes)",
            2: "Left Ventricular Hypertrophy (Estes' criteria)"
        }
        restecg_val = st.selectbox(
            "Resting ECG Result",
            options=list(restecg_options.keys()),
            format_func=lambda x: restecg_options[x],
            index=int(p.get("restecg", 1)),
            help="Resting 12-lead electrocardiographic evaluation."
        )

        ca_val = st.selectbox(
            "Major Vessels Colored by Fluoroscopy (0–4)",
            options=[0, 1, 2, 3, 4],
            index=int(p.get("ca", 0)),
            help="Number of major coronary blood vessels visualized with contrast dye fluoroscopy."
        )

    with col6:
        thal_options = {
            0: "Unknown / Baseline",
            1: "Normal Blood Flow",
            2: "Fixed Defect (e.g. prior myocardial infarction)",
            3: "Reversible Defect (transient exercise ischemia)"
        }
        thal_val = st.selectbox(
            "Thalassemia / Perfusion Defect Result",
            options=list(thal_options.keys()),
            format_func=lambda x: thal_options[x],
            index=int(p.get("thal", 2)),
            help="Nuclear myocardial perfusion scintigraphy scan result."
        )

# Update session state with current inputs
current_inputs = {
    "age": age_val,
    "sex": sex_val,
    "cp": cp_val,
    "trestbps": trestbps_val,
    "chol": chol_val,
    "fbs": fbs_val,
    "restecg": restecg_val,
    "thalach": thalach_val,
    "exang": exang_val,
    "oldpeak": oldpeak_val,
    "slope": slope_val,
    "ca": ca_val,
    "thal": thal_val,
}
st.session_state.patient_data = current_inputs


# -----------------------------------------------------------------------------
# CALCULATION & RESULTS SECTION
# -----------------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
calc_col1, calc_col2 = st.columns([1, 2])

with calc_col1:
    calculate_clicked = st.button("🫀 Calculate Risk Estimate", type="primary", use_container_width=True)

# Compute prediction
prob, logit_score, factor_meta = calculate_risk(current_inputs)
prob_percent = round(prob * 100, 1)

if prob < 0.30:
    risk_level = "Low"
    level_class = "low"
    badge_label = "Low estimated risk"
    message = "The educational estimate is in the lower-risk range. Continue routine preventive care, active lifestyle, and balanced nutrition."
    color_hex = "#116149"
elif prob < 0.60:
    risk_level = "Moderate"
    level_class = "moderate"
    badge_label = "Moderate estimated risk"
    message = "The educational estimate is in the moderate-risk range. Discuss your risk factors and preventive cardiology measures with a clinician."
    color_hex = "#895a00"
else:
    risk_level = "High"
    level_class = "high"
    badge_label = "High estimated risk"
    message = "The educational estimate is in the higher-risk range. Please seek advice from a qualified clinician for structured cardiac evaluation."
    color_hex = "#9b2c2c"

st.markdown("---")
st.markdown("### 📊 Assessment Findings")

res_col1, res_col2 = st.columns([1, 1.3])

with res_col1:
    st.markdown(
        f"""
        <div class="result-card">
            <span class="hero-eyebrow">ESTIMATED RISK LEVEL</span><br>
            <div class="badge-pill {level_class}">● {badge_label.upper()}</div>
            <div class="probability-number">{prob_percent}%</div>
            <div class="result-copy">{message}</div>
            <div class="disclaimer-text">
                <strong>Medical Disclaimer:</strong> For education only. This tool is not a medical diagnosis and must not guide emergency or treatment decisions. Always consult a licensed physician.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with res_col2:
    st.markdown("#### 🎯 Risk Distribution Scale")
    st.progress(min(prob, 1.0))
    st.caption(
        f"**Estimated Risk Score:** {round(logit_score, 2)} log-odds • "
        f"**Model Classification:** {'Positive' if prob >= 0.5 else 'Negative'} (≥ 50% threshold)"
    )

    st.markdown("#### 🔍 Key Contributing Observations")
    factors = factor_meta.get("factors", [])
    if factors:
        for f in factors:
            f_class = f["status"]
            st.markdown(
                f"""
                <div class="factor-item {f_class}">
                    <span><strong>{f['name']}</strong>: {f['val']}</span>
                    <span><em>{f['impact']}</em></span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("All parameters are within baseline reference ranges.")

    # Export / Report generation
    st.markdown("#### 📄 Export Assessment Report")
    summary_report = f"""# CardioCheck Heart Disease Assessment Summary
Date: Current Session
Educational Tool (Not for clinical diagnosis)

Patient Demographics & Vitals:
- Age: {age_val}
- Biological Sex: {"Male" if sex_val == 1 else "Female"}
- Resting Blood Pressure: {trestbps_val} mm Hg
- Serum Cholesterol: {chol_val} mg/dL
- Fasting Blood Sugar > 120: {"Yes" if fbs_val == 1 else "No"}

Symptoms & Exercise Testing:
- Chest Pain Type: {cp_options[cp_val]}
- Max Heart Rate: {thalach_val} bpm
- Exercise-Induced Angina: {"Yes" if exang_val == 1 else "No"}
- ST Depression (Oldpeak): {oldpeak_val} mm
- ST Slope: {slope_options[slope_val]}

Imaging & Specialized Tests:
- Resting ECG: {restecg_options[restecg_val]}
- Major Vessels (Fluoroscopy): {ca_val}
- Thalassemia Result: {thal_options[thal_val]}

Results:
- Estimated Risk Probability: {prob_percent}%
- Risk Classification: {risk_level} Risk
- Clinical Recommendation: {message}

Disclaimer: For educational use only. Do not use for clinical emergencies or medical diagnoses.
"""
    st.download_button(
        label="📥 Download Clinical Summary (.txt)",
        data=summary_report,
        file_name=f"cardiocheck_assessment_{prob_percent}pct.txt",
        mime="text/plain",
        use_container_width=True,
    )

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-footer">
        <p><strong>CardioCheck Academic Demonstration</strong> • Built with Streamlit & Python • UCI Heart Disease Standard Features</p>
        <p>Disclaimer: This application is an educational resource. It does not provide medical diagnosis, treatment recommendations, or emergency advice.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
