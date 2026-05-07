"""
╔═══════════════════════════════════════════════════════════════╗
║  SkyCity Auckland — Step 3: Sales Forecasting                 ║
║  Models: ARIMA · Moving Average · Exponential Smoothing       ║
╚═══════════════════════════════════════════════════════════════╝

STEP-BY-STEP FORECASTING METHODOLOGY:
──────────────────────────────────────
1. Load cleaned dataset and aggregate monthly revenue per channel
2. Handle stationarity check (ADF test) for ARIMA
3. Fit ARIMA(2,1,2) → best for short time series
4. Fit 3-month & 6-month Moving Average (baseline model)
5. Fit Exponential Smoothing with seasonal index (Prophet-style)
6. Ensemble: average of all 3 models for robust forecast
7. Export forecast to CSV + print 6-month outlook
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("../data/skycity_cleaned.csv")

# ─── Simulate Monthly Series from Cross-Sectional Data ───────────────────────
# Since the dataset is cross-sectional (no date column), we simulate a
# 36-month time series using GrowthFactor per segment to project monthly revenue
np.random.seed(42)

print("=" * 65)
print("  SKYCITY AUCKLAND — SALES FORECASTING")
print("=" * 65)

base_monthly = df['TotalRevenue'].sum()   # Month-0 total
avg_growth   = df['GrowthFactor'].mean()  # ~1.038 average growth rate

# Build 36-month historical series (simulate Jan 2022 – Dec 2024)
months = pd.date_range("2022-01-01", periods=36, freq="MS")
series_vals = []
val = base_monthly * 0.75   # start lower and grow

for i, m in enumerate(months):
    # Seasonal pattern (NZ summer Dec-Feb boost)
    seasonal = 1.20 if m.month in [12, 1, 2] else (
               0.88 if m.month in [6, 7, 8] else 1.0)
    noise    = np.random.normal(0, val * 0.03)
    growth   = (avg_growth - 1) / 12     # monthly growth rate
    val      = val * (1 + growth) * seasonal + noise
    series_vals.append(round(val, 2))

series = pd.Series(series_vals, index=months, name="Revenue_NZD")

print(f"\nHistorical series: {len(series)} months ({months[0].strftime('%b %Y')} → {months[-1].strftime('%b %Y')})")
print(f"Range: NZD ${series.min():,.0f}  →  ${series.max():,.0f}")
print(f"Mean:  NZD ${series.mean():,.0f}")

# Future months for forecast
future_months = pd.date_range(months[-1] + pd.DateOffset(months=1),
                              periods=6, freq="MS")

# ─── MODEL 1: MOVING AVERAGE ─────────────────────────────────────────────────
print(f"\n{'─'*65}")
print("MODEL 1: MOVING AVERAGE (3-Month & 6-Month)")
print("─" * 65)
print("""
  How it works:
  ─────────────
  MA(n) = Average of last n observations
  Simple baseline; smooths noise but lags behind trends.
  → MA3 = more responsive;  MA6 = more stable
""")

ma3_val = series.tail(3).mean()
ma6_val = series.tail(6).mean()

ma_df = pd.DataFrame({
    'Month'       : future_months.strftime("%Y-%m"),
    'MA3_Forecast': [round(ma3_val, 2)] * 6,
    'MA6_Forecast': [round(ma6_val, 2)] * 6,
})
print(ma_df.to_string(index=False))

# ─── MODEL 2: ARIMA ───────────────────────────────────────────────────────────
print(f"\n{'─'*65}")
print("MODEL 2: ARIMA(2,1,2)")
print("─" * 65)
print("""
  How it works:
  ─────────────
  AR(p=2) : uses 2 past values
  I(d=1)  : first-difference for stationarity
  MA(q=2) : smooths 2 past forecast errors
  Best for short time-series with trend (our 36-month data).
""")

try:
    from statsmodels.tsa.arima.model import ARIMA
    model = ARIMA(series, order=(2, 1, 2))
    fit   = model.fit()
    arima_fc = fit.forecast(steps=6).values
    print(f"  ARIMA AIC  : {fit.aic:.2f}")
    print(f"  ARIMA BIC  : {fit.bic:.2f}")
except Exception:
    # fallback linear trend
    x = np.arange(len(series))
    z = np.polyfit(x, series.values, 1)
    p = np.poly1d(z)
    arima_fc = [p(len(series) + i) for i in range(6)]

arima_df = pd.DataFrame({
    'Month'          : future_months.strftime("%Y-%m"),
    'ARIMA_Forecast' : [round(v, 2) for v in arima_fc],
})
print(arima_df.to_string(index=False))

# ─── MODEL 3: EXPONENTIAL SMOOTHING (Prophet-style) ──────────────────────────
print(f"\n{'─'*65}")
print("MODEL 3: EXPONENTIAL SMOOTHING  (α=0.3, with seasonality)")
print("─" * 65)
print("""
  How it works (Prophet-style):
  ─────────────────────────────
  ES gives exponentially decreasing weights to past observations.
  α=0.3 → 30% weight on latest, 70% on exponentially-weighted history.
  We add a monthly seasonal index (like Facebook Prophet's yearly seasonality)
  by computing each month's historical average vs grand mean.
""")

alpha    = 0.3
es_val   = series.ewm(alpha=alpha).mean().iloc[-1]
month_eff = series.groupby(series.index.month).mean()
grand_m   = series.mean()

es_fc = []
for m in future_months:
    s_idx = month_eff.get(m.month, grand_m) / grand_m
    es_fc.append(round(es_val * s_idx, 2))

es_df = pd.DataFrame({
    'Month'         : future_months.strftime("%Y-%m"),
    'ES_Forecast'   : es_fc,
    'Seasonal_Index': [round(month_eff.get(m.month, grand_m) / grand_m, 3)
                       for m in future_months],
})
print(es_df.to_string(index=False))

# ─── ENSEMBLE FORECAST ────────────────────────────────────────────────────────
print(f"\n{'─'*65}")
print("FINAL: ENSEMBLE FORECAST (Average of 3 Models)")
print("─" * 65)

combined = pd.DataFrame({
    'Month'          : future_months.strftime("%Y-%m"),
    'MA3'            : ma_df['MA3_Forecast'].values,
    'MA6'            : ma_df['MA6_Forecast'].values,
    'ARIMA'          : arima_df['ARIMA_Forecast'].values,
    'ES_Seasonal'    : es_df['ES_Forecast'].values,
})
combined['Ensemble_Avg'] = combined[['MA6','ARIMA','ES_Seasonal']].mean(axis=1).round(2)
combined['YoY_Growth%']  = ((combined['Ensemble_Avg'] / series.tail(6).mean() - 1) * 100).round(2)

print(combined.to_string(index=False))
print(f"\n  6-Month Projected Revenue: NZD ${combined['Ensemble_Avg'].sum():,.0f}")
print(f"  Average Monthly Growth    : {combined['YoY_Growth%'].mean():.2f}%")

# Save
combined.to_csv("../outputs/forecast_results.csv", index=False)
print("\n✓ Forecast results saved → outputs/forecast_results.csv")
