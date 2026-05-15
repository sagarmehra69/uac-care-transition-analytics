# 📊 UAC Care Transition Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Interactive_App-FF4B4B.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data_Engineering-150458.svg)
![Plotly](https://img.shields.io/badge/Plotly-Visual_Analytics-3F4F75.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-F7931E.svg)

---

## 🌐 Live Dashboard
🔗 **Application Link:** [![Live App](https://img.shields.io/badge/Live-Dashboard-success?style=for-the-badge&logo=streamlit)](https://uac-care-transition-analytics-gs5voaajtvshx3psqheer7.streamlit.app/)

---

# 📖 Project Overview

The **UAC Care Transition Analytics Dashboard** is an operational intelligence platform developed to analyze, monitor, and forecast care-transition workflows associated with the U.S. Unaccompanied Alien Children (UAC) program.

The system transforms raw operational records into actionable insights through:
- KPI engineering
- bottleneck detection
- anomaly identification
- forecasting pipelines
- executive-level reporting

The dashboard is designed to simulate how modern public-sector analytics systems monitor organizational strain, placement demand, transfer efficiency, and discharge stability in high-uncertainty operational environments.

Instead of functioning as a static reporting tool, the platform acts as a dynamic decision-support system capable of surfacing operational risks and trend anomalies in real time.

---

# ✨ Core Features

## ⚙️ Intelligent Data Processing
- Automated preprocessing pipeline for inconsistent CSV structures
- Dynamic column remapping system
- Date standardization and interpolation handling
- Missing value recovery and numeric sanitation
- Defensive validation against malformed datasets

---

## 📈 Operational KPI Engine
Tracks critical system-wide performance indicators including:
- Transfer Efficiency Ratio
- Discharge Effectiveness Index
- Pipeline Throughput
- Backlog Accumulation Rate
- Operational Stability Score

All KPIs are dynamically recalculated using adjustable policy thresholds.

---

## 📊 Interactive Analytics Dashboard
- Fully interactive Plotly visualizations
- Responsive Streamlit layout
- Dynamic filtering and date slicing
- Comparative operational analysis
- KPI trend monitoring
- Chronological bottleneck visualization

---

## 🚨 Bottleneck Detection System
Advanced bottleneck logic identifies:
- sustained operational congestion
- intake/discharge imbalance
- transfer inefficiencies
- backlog escalation periods
- critical operational alerts

Includes:
- severity scoring
- flagged period ledgers
- bottleneck heatmaps
- operational strain summaries

---

## 🔮 Forecasting & Predictive Analytics
The platform integrates forecasting capabilities using:
- Facebook Prophet
- time-series trend projection
- confidence interval visualization
- surge prediction logic
- operational stress forecasting

---

## 🔍 Anomaly Detection
Machine learning-based anomaly detection powered by:
- Isolation Forest
- statistical outlier identification
- abnormal discharge/apprehension spikes
- operational irregularity detection

---

## 📄 Executive Reporting
Generate:
- Executive Summary Snapshots (.md)
- Processed operational datasets (.csv)
- Downloadable analytical summaries

---

# 📌 Key KPIs Monitored

| KPI | Description |
|---|---|
| **Transfer Efficiency Ratio** | Measures how effectively CBP transitions children out of temporary custody |
| **Discharge Effectiveness Index** | Evaluates HHS placement and discharge performance |
| **Pipeline Throughput** | Tracks overall operational movement through the care pipeline |
| **Backlog Accumulation Rate** | Measures growth of unresolved operational load |
| **Outcome Stability Score** | Evaluates consistency of discharge operations over time |

---

# 🛠️ Technology Stack

## Frontend & UI
- Streamlit

## Data Engineering
- Pandas
- NumPy

## Machine Learning
- Scikit-learn
- Prophet

## Visualization
- Plotly Express
- Plotly Graph Objects
- Matplotlib

## Architecture
- Modular Python backend
- Component-based analytics design
- Cached data pipelines
- Reusable visualization modules

---

# 📂 Project Structure

```text
care-transition-analytics/
│
├── .streamlit/
│   └── config.toml
│
├── app/
│   └── streamlit_app.py
│
├── assets/
│   ├── hero.jpg
│   └── logo.png
│
├── data/
│   └── HHS_Unaccompanied_Alien_Children_Program.csv
│
├── reports/
│   ├── executive_summary.md
│   └── research_paper.md
│
├── src/
│   ├── __init__.py
│   ├── anomaly_detection.py
│   ├── bottleneck.py
│   ├── data_loader.py
│   ├── executive_summary.py
│   ├── forecasting.py
│   ├── metrics.py
│   ├── preprocessing.py
│   ├── style.py
│   ├── ui_components.py
│   ├── utils.py
│   └── visualization.py
│
├── .gitignore
├── README.md
└── requirements.txt
```


# ⚡ Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/uac-care-transition-analytics.git

cd uac-care-transition-analytics
```

## 2️⃣ Create a Virtual Environment

### 🪟 Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### 🍎 Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3️⃣ Install Required Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Launch the Streamlit Dashboard

```bash
streamlit run app/streamlit_app.py
```

---

# 📊 Expected Dataset Structure

The preprocessing engine automatically detects and standardizes operational fields from HHS/CBP datasets.

### Required Core Fields

| Operational Field | Description |
|---|---|
| Date | Chronological operational record |
| CBP Apprehensions | Daily intake into CBP custody |
| In CBP Custody | Current children held in CBP custody |
| Transfers Out of CBP Custody | Children transitioned from CBP to HHS |
| In HHS Care | Current children under HHS care |
| HHS Discharges | Children discharged from HHS shelters |

---

### 🧹 Automatic Data Cleaning

The system automatically handles:
- malformed dates
- commas in numerical values
- missing operational records
- inconsistent column names
- blank values
- numeric sanitation
- interpolation of time-series gaps

---

# 💡 Usage Workflow

## 📂 Upload or Use Default Dataset

Use the sidebar to:
- upload a fresh operational CSV dataset
- or use the bundled historical UAC dataset

---

## 🎛️ Configure KPI Thresholds

Dynamically adjust:
- Transfer Efficiency thresholds
- Discharge Effectiveness thresholds
- Throughput performance thresholds

to simulate operational policy scenarios and monitor system behavior under different performance targets.

---

## 📈 Explore Dashboard Tabs

Navigate through multiple analytical sections:

| Dashboard Section | Purpose |
|---|---|
| Overview | High-level operational snapshot |
| KPI Trends | Historical metric analysis |
| Bottleneck Analysis | Congestion and operational strain detection |
| Forecasting | Predictive trend analysis |
| Anomaly Detection | Statistical outlier detection |
| Executive Summary | Downloadable operational reports |

---

# 🚀 Future Enhancements

Planned future upgrades include:

- ARIMA & XGBoost forecasting comparison
- automated operational alerts
- role-based dashboard access
- live API data ingestion
- staffing optimization models
- explainable AI integrations
- PDF executive report generation
- drift detection systems
- cloud deployment scaling

---

# ⚖️ Disclaimer

This project was developed for:
- academic learning
- research exploration
- portfolio demonstration
- analytics engineering practice

The dashboard utilizes publicly available operational data structures associated with the U.S. Department of Health & Human Services (HHS) and UAC reporting systems.
All generated insights, forecasts, and recommendations are algorithmic interpretations and should not be considered official government policy, operational directives, or legal guidance.

---

# ⭐ Support & Connect

If you found this project valuable:

- ⭐ Star the repository
- 🔁 Share feedback
- 🤝 Connect on LinkedIn
- 💡 Suggest future improvements

## 👨‍💻 Author

**Sagar Mehra**  
🔗 LinkedIn: https://www.linkedin.com/in/sagar-mehra69-data
---
