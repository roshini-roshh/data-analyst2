# 🍽️ Order Channel Performance & Market Share Analytics

An end-to-end Data Analytics project focused on analyzing multi-channel restaurant ordering behavior across the SkyCity Auckland hospitality portfolio. This project evaluates customer ordering trends, delivery platform dependency, geographic preferences, and channel performance using analytical models and interactive dashboards.

---

## 📌 Project Overview

The rapid growth of food delivery platforms such as Uber Eats and DoorDash has transformed the hospitality industry. This project analyzes restaurant operational data to identify:

- Channel-wise order performance
- Market share distribution
- Aggregator dependency risks
- Geographic ordering behavior
- Cuisine-specific channel preferences
- Strategic business insights

The analysis is designed to support data-driven decision-making for restaurant operations and channel optimization.

---

## 🎯 Objectives

- Analyze order volume across multiple channels
- Measure channel market share distribution
- Identify dominant ordering channels by region
- Detect aggregator dependency risks
- Compare cuisine-wise ordering behavior
- Build KPI-driven business insights
- Develop an interactive Streamlit dashboard

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- Statistical Analysis
- Data Visualization

---

## 📂 Dataset Description

The dataset contains 30 structured variables related to:

### Key Features

| Category | Variables |
|---|---|
| Restaurant Details | RestaurantID, Name, CuisineType |
| Geographic Data | Subregion |
| Orders | In-Store, Uber Eats, DoorDash, Self-Delivery |
| Revenue Metrics | Channel Revenue |
| Cost Metrics | COGS, OPEX, Delivery Cost |
| Profit Metrics | Net Profit |
| Channel Shares | UE_share, DD_share, SD_share |

---

## 📊 Channels Analyzed

- 🏪 In-Store
- 🚗 Uber Eats
- 🛵 DoorDash
- 📦 Self-Delivery

---

## 📈 Analytical Methods

### ✅ Channel Volume Aggregation
Analyzed total order volume across:
- Channels
- Cuisine types
- Restaurant segments
- Geographic regions

### ✅ Market Share Analysis
Computed:
- Channel-wise market share
- Delivery Ratio Index (DRI)

### ✅ Channel Diversification Score (CDS)
Measured channel concentration risk and diversification balance.

### ✅ Aggregator Dependency Index (ADI)
Classified restaurants into:
- High Risk
- Moderate Risk
- Balanced

### ✅ Geographic Analysis
Compared ordering behavior across:
- North Shore
- West Auckland
- Central Auckland

---

## 🔍 Key Insights

### 📌 Portfolio-Level Findings

| Channel | Approximate Share |
|---|---|
| In-Store | 42% |
| Uber Eats | 28% |
| DoorDash | 18% |
| Self-Delivery | 12% |

---

### 📌 Geographic Findings

#### North Shore
- Stronger in-store dining preference
- Lower aggregator dependency

#### West Auckland
- Highest dependency on Uber Eats & DoorDash
- Strong QSR delivery dominance

#### Central Auckland
- Balanced channel distribution
- Higher self-delivery efficiency

---

### 📌 Cuisine-Level Findings

| Cuisine | Dominant Channel | Risk Level |
|---|---|---|
| Burgers | Uber Eats | High |
| Pizza | Uber Eats | High |
| Sushi | In-Store / Uber Eats | Moderate |
| Cafe | In-Store | Low |
| Fine Dining | In-Store | Low |

---

## ⚠️ Business Problems Identified

- High dependency on third-party aggregators
- Reduced profit margins due to commissions
- Limited customer ownership
- Uneven channel distribution across regions

---

## 💡 Recommendations

- Strengthen direct ordering platforms
- Expand self-delivery capabilities
- Improve in-store customer engagement
- Reduce excessive aggregator dependency
- Develop channel diversification strategies

---

## 📉 Limitations

- Single-period dataset
- No longitudinal customer tracking
- Limited consumer behavior data

Future improvements may include:
- Time-series analysis
- Customer preference modeling
- Competitor benchmarking

---

## 🖥️ Streamlit Dashboard Features

✔ Interactive Filters  
✔ Cuisine Selection  
✔ Subregion Analysis  
✔ Channel Comparison  
✔ KPI Monitoring  
✔ Real-Time Insights  

---

## 🚀 Conclusion

This project demonstrates how data analytics can help hospitality businesses optimize ordering channels, reduce operational risk, and improve profitability. The framework converts raw operational restaurant data into actionable business intelligence.

---


---

## ⭐ If you like this project

Give this repository a ⭐ on :contentReference[oaicite:1]{index=1}
