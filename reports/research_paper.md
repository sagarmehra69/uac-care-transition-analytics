# UAC Care Transition Efficiency & Placement Outcome Analytics
## Predictive Forecasting of Care Load & Placement Demand


# Abstract

The Unaccompanied Alien Children (UAC) Program under the U.S. Department of Health & Human Services (HHS) operates in a high-uncertainty environment where sudden changes in border activity and humanitarian situations can rapidly increase the number of children entering federal care. Traditional reporting systems mainly provide historical information and lack predictive operational intelligence required for proactive planning.

This project presents an interactive analytical dashboard developed using Python and Streamlit to monitor operational efficiency, forecast future care demand, detect bottlenecks, and identify anomalies in the UAC system. The dashboard integrates data preprocessing, KPI engineering, forecasting models, anomaly detection, and interactive visualizations to transform raw operational data into actionable intelligence.

The system provides forecasting of care load and discharge demand, identifies sustained operational bottlenecks, and generates analytical insights and recommendations for healthcare planners and government stakeholders. Machine learning models such as Prophet and Isolation Forest were implemented to enhance predictive capabilities and anomaly detection.

**Keywords:** UAC Analytics, Predictive Forecasting, Operational Intelligence, Streamlit Dashboard, Machine Learning, Bottleneck Detection, Healthcare Analytics

---

# 1. Introduction

The Unaccompanied Alien Children (UAC) Program managed by the U.S. Department of Health & Human Services (HHS) is responsible for the care, placement, and discharge of children entering federal custody. The program experiences continuous fluctuations in intake volume, transfer rates, and discharge demand due to changing border conditions, policy enforcement, and humanitarian crises.

Traditional operational reports are limited because they mainly focus on descriptive analytics and historical trends. They do not provide predictive intelligence required for proactive operational planning. As a result, sudden increases in care load may lead to:
- Overcrowding risk
- Delayed discharges
- Increased operational backlog
- Staff pressure
- Reduced operational efficiency

This project introduces a predictive analytics and operational intelligence dashboard capable of forecasting future care demand, monitoring operational performance, detecting bottlenecks, and identifying anomalies in the UAC system.

The research follows a standard analytical research paper structure including introduction, methodology, analysis, results, discussion, and conclusion based on commonly accepted research paper formats. :contentReference[oaicite:0]{index=0}

Official Reference:  
https://www.hhs.gov/

---

# 2. Problem Statement

Despite the availability of daily operational data, the UAC Program currently lacks:
- Short-term forecasting of children in care
- Predictive discharge demand estimation
- Early warning indicators for operational stress
- Automated bottleneck detection systems
- Real-time operational intelligence dashboards

Because of these limitations:
- Resource allocation becomes reactive
- Operational responses are delayed
- Capacity stress increases
- Backlog accumulation becomes difficult to monitor

This project aims to solve these issues through predictive analytics, machine learning, and interactive visualization techniques.

---

# 3. Research Objectives

## Primary Objectives

- Forecast future care load in HHS facilities
- Predict discharge and placement demand
- Monitor operational efficiency using KPIs
- Detect bottlenecks automatically
- Build an interactive analytical dashboard

## Secondary Objectives

- Provide early warning indicators
- Detect operational anomalies
- Generate automated insights and recommendations
- Support data-driven decision-making

---

# 4. Literature Review

Research papers in analytical and operational domains generally follow a structured methodology consisting of introduction, methodology, results, discussion, and conclusion sections. Analytical research focuses on identifying patterns, relationships, and operational insights using evidence-based analysis. :contentReference[oaicite:1]{index=1}

Modern healthcare and operational intelligence systems increasingly use:
- Predictive analytics
- Time-series forecasting
- Machine learning
- Anomaly detection
- Interactive dashboards

Forecasting models such as Prophet are commonly used for time-series prediction, while Isolation Forest is widely used for anomaly detection in operational datasets.

This project combines these analytical approaches into a unified dashboard system for monitoring UAC operational performance.

---

# 5. Dataset Description

The dataset used in this project is:

**HHS_Unaccompanied_Alien_Children_Program.csv**

The dataset contains operational information related to:
- Daily intake volume
- Children in care
- Transfers
- Discharges
- Operational flow

## Main Dataset Attributes

| Column Name | Description |
|---|---|
| Date | Reporting date |
| Children apprehended and placed in CBP custody | Daily intake volume |
| Children transferred out of CBP custody | Transfers into HHS |
| Children in HHS Care | Active HHS care load |
| Children discharged from HHS Care | Successful placements/discharges |

The dataset supports:
- Time-series analysis
- KPI engineering
- Forecasting
- Bottleneck detection
- Anomaly analysis

---

# 6. Methodology

The project follows a structured analytical methodology.

---

## 6.1 Data Preprocessing

Several preprocessing operations were implemented to improve data quality and consistency.

### Preprocessing Steps
- Date conversion to datetime format
- Numeric data cleaning
- Missing value handling
- Data interpolation
- Column standardization
- Chronological sorting

### Dynamic Column Mapping

The system dynamically detects inconsistent column names and standardizes them automatically to ensure compatibility with the dashboard.

---

## 6.2 Feature Engineering

Several analytical and predictive features were generated.

### Derived Features
- Rolling averages
- Rolling variance
- Lag-based operational indicators
- Throughput metrics
- Backlog indicators
- Stability measures

---

## 6.3 KPI Engineering

Important operational KPIs were calculated.

### Transfer Efficiency
- Measures transfer performance relative to apprehensions.

### Discharge Effectiveness
- Measures discharge performance relative to active care load.

### Pipeline Throughput
- Represents operational flow efficiency.

### Backlog Rate
- Easures operational accumulation pressure.

### Stability Score
- Measures operational consistency using rolling standard deviation.

---

## 6.4 Bottleneck Detection

A custom bottleneck detection engine was implemented to identify:
- Sustained operational stress
- Reduced throughput
- Backlog accumulation
- Critical operational periods

### Bottleneck Indicators
- Low transfer efficiency
- High backlog growth
- Reduced discharge performance
- Continuous operational imbalance

---

## 6.5 Forecasting

The Prophet forecasting model was implemented to predict:
- Future care load
- Discharge effectiveness
- Transfer efficiency
- Backlog trends

Forecasting enables proactive planning and resource allocation.

---

## 6.6 Anomaly Detection

The Isolation Forest algorithm was used to detect:
- Unusual spikes
- Irregular operational behavior
- Abnormal trends

This helps identify operational instability and unexpected activity.

---

# 7. Dashboard Development

The dashboard was developed using Streamlit and Plotly.

## Dashboard Modules

### 1. Overview Dashboard
Displays:
- Intake vs discharge trends
- Pipeline load
- Backlog accumulation
- Stability analysis

### 2. KPI Dashboard
Provides:
- KPI tracking
- Rolling trend analysis
- Monthly summaries

### 3. Bottleneck Dashboard
Includes:
- Severity heatmaps
- Critical alerts
- Bottleneck statistics

### 4. Insights & Recommendations
Generates:
- Automated insights
- Operational recommendations
- Priority-based interventions

### 5. Advanced Analytics
Provides:
- Forecasting
- Anomaly detection
- Comparative analysis

---

# 8. Analysis and Numerical Findings

The project analyzed operational data from the **HHS Unaccompanied Alien Children Program dataset** covering multiple years of UAC care operations from **2023 to 2025**.

---

## Key Numerical Analysis Performed

### 1. Children in HHS Care Analysis

The analysis showed major fluctuations in the number of children under HHS care.

### Highest Recorded HHS Care Load
- Approximately **8,390 children** were under HHS care during peak operational periods in March 2024.

### Lowest Recorded HHS Care Load
- Around **2,023 children** were in HHS care during lower operational periods in September 2025.

This indicates a major reduction in care load over time.

---

## 2. CBP Apprehension Analysis

The dataset revealed large differences in daily apprehension counts.

### Highest Apprehension Count
- More than **227 children** were apprehended in a single reporting period during 2024.

### Lowest Apprehension Count
- Some reporting periods in 2025 recorded only **1 to 2 apprehensions** daily.

This demonstrated a sharp decline in border intake activity over time.

---

## 3. Transfer Analysis

The project analyzed transfer flow between CBP and HHS systems.

### Highest Transfer Count
- Transfer counts exceeded **343 transfers** during high operational demand periods in April 2024.

### Lowest Transfer Count
- Several periods in 2025 showed transfer counts below **5 transfers per day**.

This highlighted changing operational pressure and reduced intake volume.

---

## 4. Discharge Performance Analysis

Discharge activity was analyzed to understand placement efficiency.

### Highest Discharge Count
- More than **436 discharges** were recorded during high-capacity operational periods in January 2023.

### Lowest Discharge Count
- Some periods recorded **0 to 5 discharges**, especially during low operational activity in 2025.

The analysis showed that discharge activity directly affected backlog accumulation and operational stability.

---

## 5. Bottleneck and Backlog Findings

The bottleneck analysis identified several operational stress periods where:
- Transfer efficiency decreased
- Discharges slowed down
- Backlog accumulation increased

The most critical bottleneck periods were observed when:
- HHS care load exceeded **7,000–8,000 children**
- Daily discharge rates failed to offset incoming transfers

---

## 6. Forecasting Insights

Forecasting analysis using Prophet models showed:
- Future care demand may remain stable if current discharge efficiency is maintained
- Sudden increases in intake volume could quickly increase operational backlog
- Continuous monitoring is required for proactive planning

---

## 7. Anomaly Detection Results

The Isolation Forest anomaly detection model identified:
- Sudden spikes in transfer activity
- Abnormal discharge fluctuations
- Irregular operational patterns during high-volume periods

These anomalies may indicate:
- Policy changes
- Humanitarian surges
- Operational disruptions

---

## Overall Analytical Summary

The project successfully analyzed:
- Thousands of operational records
- Multi-year care load trends
- Transfer efficiency patterns
- Discharge effectiveness
- Bottleneck severity
- Forecasted operational demand

The numerical analysis helped transform raw operational data into actionable insights for strategic decision-making and operational planning.

# 9. Discussion

The project demonstrates how predictive analytics and operational intelligence can improve decision-making in healthcare and child welfare systems.

The integration of:
- Forecasting
- KPI monitoring
- Bottleneck detection
- Anomaly analysis
- Interactive dashboards

helps stakeholders monitor operational performance more effectively.

The forecasting models provide advance operational visibility, while anomaly detection improves monitoring of unusual events.

The dashboard transforms raw operational data into meaningful analytical insights for government stakeholders.

---

# 10. Challenges Faced

Several challenges were encountered during development.

## Major Challenges
- Missing values in the dataset
- Inconsistent column naming
- Forecast model integration
- Visualization scaling issues
- Limited historical range

## Solutions Implemented
- Data interpolation
- Dynamic column mapping
- Safe preprocessing pipelines
- Automated error handling
- Modular dashboard architecture

---

# 11. Results

The project successfully:
- Built a complete Streamlit analytics dashboard
- Forecasted future operational demand
- Detected bottlenecks automatically
- Identified anomalies using machine learning
- Generated operational insights
- Improved analytical visibility

The dashboard supports:
- Proactive planning
- Resource allocation
- Operational monitoring
- Strategic decision-making

---

# 12. Conclusion

This project demonstrates the importance of predictive analytics and machine learning in operational intelligence systems.

By integrating:
- Data preprocessing
- KPI engineering
- Forecasting
- Bottleneck detection
- Anomaly detection
- Interactive visualization

the project provides a complete analytical solution for monitoring UAC operational performance.

The system enables proactive planning, operational transparency, and data-driven decision-making for healthcare planners and government stakeholders.

---

# 13. Future Scope

Future improvements may include:
- Real-time API integration
- Deep learning forecasting models
- Automated alert systems
- Real-time operational monitoring
- Natural language querying

---

