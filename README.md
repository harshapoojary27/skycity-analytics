# 🏙️ SkyCity Auckland — Order Channel Performance & Market Share Analytics

Python · Streamlit · Plotly · Statsmodels 

---

## Quick Start

```bash
pip install -r requirements.txt
python src/01_data_cleaning.py
python src/02_eda_analysis.py
python src/03_forecasting.py
streamlit run dashboard/app.py
```

## Dataset
1,696 restaurants across 8 cuisine types, 4 segments, 4 Auckland subregions.
Channels: In-Store · UberEats · DoorDash · Self-Delivery

## Key Findings
- **$77.7M** total revenue across all channels
- **UberEats** holds 39.6% market share but erodes profits via commissions
- **Ghost Kitchens** are the most profitable segment ($9,051 avg net profit)
- **Self-Delivery** is the growth opportunity for margin recovery

## Tech Stack
| Layer | Tools |
|---|---|
| Data | pandas, numpy |
| Analysis | statsmodels, scikit-learn |
| Visualization | plotly, matplotlib |
| Dashboard | Streamlit |
| Forecasting | ARIMA, Moving Average, Exponential Smoothing |

## Folder Structure
```
skycity_project/
├── data/          ← Raw + cleaned datasets
├── src/           ← Analysis scripts (run in order: 01 → 02 → 03)
├── dashboard/     ← Streamlit app
├── outputs/       ← Generated CSV reports
├── docs/          ← Full project documentation
└── requirements.txt
```
