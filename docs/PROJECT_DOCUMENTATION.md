# SkyCity Auckland — Order Channel Performance & Market Share Analytics
## Complete Project Documentation | MCA Internship Submission

---

## 1. INTRODUCTION

### 1.1 Background and Context

The Auckland hospitality market is one of New Zealand's most competitive, with over
3,000 registered food-service outlets across the city. SkyCity Auckland—the country's
largest integrated resort and entertainment complex—operates multiple restaurants and
bars across segments including QSR (Quick Service), Cafes, Full-Service dining, and
Ghost Kitchens.

The rapid growth of food-delivery platforms such as UberEats and DoorDash has
fundamentally disrupted the traditional dine-in model. Multi-channel ordering is now
the norm: a single restaurant may simultaneously receive orders via its dine-in floor,
a third-party delivery app, its own website, or a self-operated delivery fleet.

### 1.2 Business Problem Statement

SkyCity currently lacks a unified analytics view of how each order channel contributes
to revenue, profitability, and market share. Business leaders cannot easily answer:

> *"Which order channel delivers the highest net profit per order? Where are margins
> being eroded by commission fees? Which cuisine types thrive on delivery vs dine-in?
> How should channel strategy differ by subregion?"*

This project builds a data-driven answer to these questions using a dataset of
1,696 restaurant records across 8 cuisine types, 4 segments, and 4 Auckland subregions.

---

## 2. OBJECTIVES

### 2.1 Primary Objectives
1. Analyze revenue contribution and market share of each order channel
   (In-Store, UberEats, DoorDash, Self-Delivery)
2. Identify the most profitable channels and cuisine types
3. Forecast future revenue using ARIMA, Moving Average, and Exponential Smoothing
4. Build an interactive Streamlit dashboard for business decision-making

### 2.2 Secondary Objectives
1. Compare performance across segments: QSR, Cafe, Full-Service, Ghost Kitchen
2. Understand subregional variation (CBD, North Shore, South Auckland, West Auckland)
3. Assess impact of delivery radius and delivery cost on Self-Delivery profitability
4. Provide actionable recommendations for channel mix optimization

### 2.3 Business Goals
- Reduce commission costs by identifying where Self-Delivery is viable
- Shift mix toward higher-margin channels where feasible
- Target high-growth subregions for expansion
- Improve Ghost Kitchen utilization for delivery-only revenue

---

## 3. DATASET DESCRIPTION

**File:** `SkyCity_Auckland_Restaurants_Bars.csv`
**Records:** 1,696 restaurants | **Columns:** 30 raw + 13 engineered

### Column Reference

| Column | Type | Description |
|---|---|---|
| RestaurantID | int | Unique identifier |
| RestaurantName | str | Restaurant/bar name |
| CuisineType | str | Burgers, Indian, Pizza, Chinese, Chicken, Kebabs, Japanese, Thai |
| Segment | str | QSR / Cafe / Full-service / Ghost Kitchen |
| Subregion | str | CBD / North Shore / South Auckland / West Auckland |
| GrowthFactor | float | Monthly growth multiplier (e.g., 1.04 = 4% growth) |
| AOV | float | Average Order Value (NZD) |
| MonthlyOrders | int | Total monthly orders across all channels |
| InStoreOrders | int | Dine-in orders |
| InStoreRevenue | float | In-store revenue (NZD) |
| UberEatsOrders | int | UberEats orders |
| UberEatsRevenue | float | UberEats revenue (NZD) |
| DoorDashOrders | int | DoorDash orders |
| DoorDashRevenue | float | DoorDash revenue (NZD) |
| SelfDeliveryOrders | int | Self-delivery orders |
| SelfDeliveryRevenue | float | Self-delivery revenue (NZD) |
| COGSRate | float | Cost of Goods Sold as % of revenue |
| OPEXRate | float | Operating Expenses as % of revenue |
| CommissionRate | float | Platform commission rate (e.g., 0.28 = 28%) |
| DeliveryRadiusKM | int | Self-delivery radius |
| DeliveryCostPerOrder | float | Cost per self-delivery order (NZD) |
| SD_DeliveryTotalCost | float | Total monthly self-delivery cost (NZD) |
| InStoreNetProfit | float | In-store channel net profit |
| UberEatsNetProfit | float | UberEats channel net profit (after commission) |
| DoorDashNetProfit | float | DoorDash channel net profit (after commission) |
| SelfDeliveryNetProfit | float | Self-delivery channel net profit |
| InStoreShare | float | In-store revenue share (0–1) |
| UE_share | float | UberEats revenue share |
| DD_share | float | DoorDash revenue share |
| SD_share | float | Self-delivery revenue share |

### Engineered Features (added in cleaning step)
| Feature | Formula |
|---|---|
| TotalRevenue | InStore + UberEats + DoorDash + SelfDelivery |
| TotalOrders | Sum of all channel orders |
| TotalNetProfit | Sum of all channel profits |
| InStore_Share% | InStoreRevenue / TotalRevenue × 100 |
| [Channel]_RPO | Channel Revenue / Channel Orders |
| Profitable | TotalNetProfit > 0 |
| RevenueTier | Low / Medium / High / Premium |

---

## 4. DATA ANALYSIS RESULTS

### 4.1 Key Performance Indicators

| KPI | Value |
|---|---|
| **Total Revenue (NZD)** | **$77,739,307** |
| In-Store Revenue | $14,284,378 (18.4%) |
| UberEats Revenue | $30,816,371 (39.6%) |
| DoorDash Revenue | $16,789,381 (21.6%) |
| Self-Delivery Revenue | $15,849,176 (20.4%) |
| Average Order Value (AOV) | $38.52 |
| Total Restaurants | 1,696 |
| % Profitable Restaurants | ~72% |

### 4.2 Channel Market Share Finding
**UberEats dominates** with 39.6% of total revenue, nearly double In-Store (18.4%).
This reflects Auckland's strong delivery culture and UberEats's market penetration.
However, **UberEats also has the lowest net profit per restaurant** due to 28–33%
commission rates — a key strategic tension.

### 4.3 Segment Finding
- **Ghost Kitchens** have the highest average net profit ($9,051) — lowest OPEX
- **Full-Service** restaurants average a **loss** (-$2,880) — high overheads
- **QSR and Cafes** perform similarly with $6,600–$7,500 average profit

### 4.4 Cuisine Finding
Burgers lead in total revenue ($18.7M) and order volume (484,875 orders).
All cuisine types have nearly identical AOV (~$38.50), suggesting AOV is driven
by SkyCity pricing strategy rather than cuisine type.

---

## 5. FORECASTING METHODOLOGY

### Model 1: Moving Average (MA)
```
MA(n) = (x_t + x_(t-1) + ... + x_(t-n+1)) / n
```
- **MA3**: 3-month window — more responsive to recent changes
- **MA6**: 6-month window — smoother, less noise
- Best for: stable series with no strong trend

### Model 2: ARIMA(2,1,2)
```
Parameters: p=2 (AR terms), d=1 (differencing), q=2 (MA terms)
AIC Score: 706.40
```
- **AR(2)**: Revenue depends on previous 2 months
- **I(1)**: First-difference removes trend non-stationarity
- **MA(2)**: Smooths 2 lagged forecast errors
- Best for: trended short time-series

### Model 3: Exponential Smoothing (ES) with Seasonal Index
```
ES_t = α × x_t + (1-α) × ES_(t-1)   where α = 0.3
Forecast = ES_last × Seasonal_Index(month)
```
- Gives 30% weight to latest observation, decaying weights to history
- Monthly seasonal index captures NZ summer/winter effects
- Best for: seasonal data with recent trend shifts

### Ensemble Forecast (Recommended)
Average of MA6 + ARIMA + ES for robustness. 6-month projection:

| Month | Ensemble Forecast (NZD) |
|---|---|
| Jan 2025 | ~$37,737 |
| Feb 2025 | ~$35,343 |
| Mar 2025 | ~$32,794 |
| Apr 2025 | ~$33,294 |
| May 2025 | ~$33,376 |
| Jun 2025 | ~$31,070 |

---

## 6. DASHBOARD FEATURES

The Streamlit dashboard (`dashboard/app.py`) includes:

| Section | Charts/Components |
|---|---|
| KPI Cards | Total Revenue, Orders, AOV, Net Profit, Profitable % |
| Channel Revenue | Horizontal bar chart (NZD) |
| Market Share | Donut pie chart |
| Cuisine Analysis | Grouped bar chart |
| Segment Scatter | Bubble chart (Revenue vs Profit vs Size) |
| Subregion Pie | Regional distribution |
| Channel Profit | Color-coded bar chart (profit/loss) |
| Forecast | Multi-line chart (all 3 models + ensemble) |
| Top 20 Table | Sortable dataframe |
| Heatmap | Cuisine × Channel revenue matrix |
| Sidebar Filters | Cuisine, Segment, Subregion, Revenue range |

---

## 7. RESULTS & CONCLUSIONS

### 7.1 Key Findings
1. **UberEats is the revenue king but profit liability** — 39.6% revenue but thin
   margins due to high commissions. Restaurants should evaluate if UberEats volume
   compensates for the 28-33% commission drain.

2. **Self-Delivery is the growth opportunity** — 20.4% market share, lower
   commissions, and controllable costs. Restaurants within 10–15 km of dense
   residential areas should expand Self-Delivery.

3. **Ghost Kitchens outperform on profit** — $9,051 average net profit vs
   Full-Service restaurants averaging a loss. SkyCity should consider expanding
   Ghost Kitchen operations.

4. **Full-Service is under pressure** — High OPEX rates make full-service the
   least profitable segment. Menu optimization and upselling are critical.

5. **Burgers dominate** — 375 restaurants and $18.7M revenue make Burgers
   the highest-performing cuisine category.

### 7.2 Recommendations
1. Negotiate lower commission rates with UberEats/DoorDash or introduce
   incentives for customers to order via Direct/Self-Delivery channels
2. Launch Self-Delivery pilots in West Auckland and South Auckland
   (highest restaurant density)
3. Reposition underperforming Full-Service restaurants as Cafe or Ghost Kitchen
4. Use the forecast model to pre-staff and pre-stock for summer peaks (Dec-Feb)
5. Offer Loyalty Discounts on Direct Website / In-Store orders to shift
   mix away from commission-heavy platforms

### 7.3 Future Scope
1. Integrate real-time order data via POS system API
2. Add customer sentiment analysis from review platforms
3. Build customer segmentation model (RFM analysis)
4. Time-series analysis with actual monthly timestamps
5. Geospatial heatmap of order density by Auckland suburb
6. A/B test channel promotions and measure lift

---

## 8. VIVA QUESTIONS & ANSWERS

**Q1: What is the business problem this project solves?**
A: SkyCity lacks a unified view of which order channels (In-Store, UberEats,
DoorDash, Self-Delivery) drive revenue vs profit. This project provides that view
using data analysis, forecasting, and an interactive dashboard.

**Q2: Why is UberEats the top channel by revenue but potentially not the best?**
A: UberEats holds 39.6% revenue share but charges 28-33% commission. This
significantly erodes net profit. In-Store and Self-Delivery often yield higher
net profit per order despite lower volumes.

**Q3: Explain ARIMA and why you chose order (2,1,2).**
A: ARIMA stands for AutoRegressive Integrated Moving Average.
- p=2: uses 2 lagged observations
- d=1: one differencing makes the series stationary
- q=2: considers 2 lagged forecast errors
I chose (2,1,2) after checking AIC scores; it gave AIC=706.40, the lowest among
tested configurations for this 36-month series.

**Q4: What is the difference between Moving Average and Exponential Smoothing?**
A: Moving Average gives equal weight to the last n observations. Exponential
Smoothing gives exponentially decreasing weights — the most recent observation
gets the highest weight (α=0.3 = 30%), older ones get progressively less.
ES is better when recent data matters more than historical data.

**Q5: What are KPIs and which ones did you calculate?**
A: KPIs (Key Performance Indicators) measure business performance.
I calculated: Total Revenue, Avg Order Value, Net Profit, Market Share %,
% Profitable Restaurants, Revenue per Order per Channel.

**Q6: Why did you use an Ensemble forecast?**
A: Each model has limitations — MA is stable but lags trends, ARIMA captures
trends but can overfit, ES responds quickly but can be noisy. Averaging them
(Ensemble) balances these weaknesses and gives a more robust forecast.

**Q7: What is Ghost Kitchen and why does it outperform Full-Service?**
A: Ghost Kitchens are delivery-only kitchens with no dine-in space. They have
near-zero front-of-house costs (no waitstaff, no dining furniture, smaller space)
resulting in lower OPEX rates, making them more profitable per order.

**Q8: How did you handle missing values in the dataset?**
A: The dataset had 0 missing values in numeric columns. The Delivery_Time_Min
column was only applicable to delivery channels — NULL values for In-Store are
expected and treated as not-applicable, not as missing data.

**Q9: What is market share and how did you calculate it?**
A: Market share is the percentage of total revenue captured by a channel.
Formula: Channel_Revenue / Total_Revenue × 100.
UberEats = $30.8M / $77.7M × 100 = 39.6% market share.

**Q10: What deployment steps are needed for the Streamlit dashboard?**
A: Install requirements: `pip install -r requirements.txt`
Run locally: `streamlit run dashboard/app.py`
Deploy to cloud: Push to GitHub → deploy on Streamlit Community Cloud
(free) or containerize with Docker and deploy on AWS/GCP/Azure.

---

## 9. FOLDER STRUCTURE

```
skycity_project/
├── data/
│   ├── SkyCity_Auckland_Restaurants_Bars.csv   ← Raw dataset
│   └── skycity_cleaned.csv                     ← After cleaning
├── src/
│   ├── 01_data_cleaning.py                     ← Cleaning + feature engineering
│   ├── 02_eda_analysis.py                      ← EDA + KPI calculation
│   └── 03_forecasting.py                       ← ARIMA + MA + ES forecasting
├── dashboard/
│   └── app.py                                  ← Streamlit dashboard
├── outputs/
│   ├── kpi_summary.csv
│   ├── cuisine_analysis.csv
│   ├── segment_analysis.csv
│   ├── region_analysis.csv
│   ├── top10_restaurants.csv
│   └── forecast_results.csv
├── docs/
│   └── PROJECT_DOCUMENTATION.md               ← This file
├── requirements.txt
└── README.md
```

---

## 10. DEPLOYMENT STEPS

```bash
# 1. Clone / set up project
cd skycity_project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run data pipeline
cd data && python ../src/01_data_cleaning.py
cd .. && python src/02_eda_analysis.py
python src/03_forecasting.py

# 4. Launch dashboard
streamlit run dashboard/app.py

# 5. Deploy to Streamlit Cloud
# - Push project to GitHub
# - Go to share.streamlit.io → New App
# - Select repo, set main file = dashboard/app.py
# - Click Deploy
```
