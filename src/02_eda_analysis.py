"""
╔═══════════════════════════════════════════════════════════════╗
║  SkyCity Auckland — Step 2: Exploratory Data Analysis (EDA)  ║
╚═══════════════════════════════════════════════════════════════╝
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("../data/skycity_cleaned.csv")

print("=" * 65)
print("  SKYCITY AUCKLAND — EXPLORATORY DATA ANALYSIS")
print("=" * 65)

# ─── KPI SUMMARY ──────────────────────────────────────────────────────────────
grand_revenue    = df['TotalRevenue'].sum()
instore_rev      = df['InStoreRevenue'].sum()
ubereats_rev     = df['UberEatsRevenue'].sum()
doordash_rev     = df['DoorDashRevenue'].sum()
selfdel_rev      = df['SelfDeliveryRevenue'].sum()
total_orders     = df['TotalOrders'].sum()
avg_aov          = df['AOV'].mean()
avg_profit       = df['TotalNetProfit'].mean()
total_profit     = df['TotalNetProfit'].sum()
profitable_pct   = df['Profitable'].mean() * 100

print(f"""
┌─────────────────────────────────────────────────────────┐
│                  KEY PERFORMANCE INDICATORS              │
├──────────────────────────────────┬──────────────────────┤
│ Total Revenue (NZD)              │ ${grand_revenue:>18,.0f} │
│ In-Store Revenue                 │ ${instore_rev:>18,.0f} │
│ UberEats Revenue                 │ ${ubereats_rev:>18,.0f} │
│ DoorDash Revenue                 │ ${doordash_rev:>18,.0f} │
│ Self-Delivery Revenue            │ ${selfdel_rev:>18,.0f} │
│ Total Monthly Orders             │ {total_orders:>19,} │
│ Average Order Value (AOV)        │ ${avg_aov:>18.2f} │
│ Avg Net Profit per Restaurant    │ ${avg_profit:>18,.2f} │
│ Total Net Profit                 │ ${total_profit:>18,.0f} │
│ Profitable Restaurants           │ {profitable_pct:>17.1f}% │
│ Total Restaurants                │ {len(df):>19,} │
└──────────────────────────────────┴──────────────────────┘
""")

# ─── CHANNEL MARKET SHARE ─────────────────────────────────────────────────────
print("─" * 65)
print("CHANNEL MARKET SHARE ANALYSIS")
print("─" * 65)
channels = {
    'In-Store':      instore_rev,
    'UberEats':      ubereats_rev,
    'DoorDash':      doordash_rev,
    'Self-Delivery': selfdel_rev,
}
for ch, rev in sorted(channels.items(), key=lambda x: -x[1]):
    pct  = rev / grand_revenue * 100
    bar  = "█" * int(pct / 2)
    print(f"  {ch:<16} {bar:<22} {pct:.1f}%   NZD ${rev:,.0f}")

# ─── CUISINE TYPE ANALYSIS ────────────────────────────────────────────────────
print(f"\n{'─'*65}")
print("CUISINE TYPE ANALYSIS")
print("─" * 65)
cuisine = df.groupby('CuisineType').agg(
    Restaurants  = ('RestaurantID', 'count'),
    Avg_AOV      = ('AOV', 'mean'),
    Total_Revenue= ('TotalRevenue', 'sum'),
    Total_Orders = ('TotalOrders', 'sum'),
    Avg_Profit   = ('TotalNetProfit', 'mean')
).round(2).sort_values('Total_Revenue', ascending=False)
print(cuisine.to_string())

# ─── SEGMENT ANALYSIS ─────────────────────────────────────────────────────────
print(f"\n{'─'*65}")
print("SEGMENT ANALYSIS (QSR / Cafe / Full-Service / Ghost Kitchen)")
print("─" * 65)
segment = df.groupby('Segment').agg(
    Count         = ('RestaurantID', 'count'),
    Total_Revenue = ('TotalRevenue', 'sum'),
    Avg_AOV       = ('AOV', 'mean'),
    Avg_Profit    = ('TotalNetProfit', 'mean'),
    Profitable_Pct= ('Profitable', lambda x: x.mean() * 100)
).round(2).sort_values('Total_Revenue', ascending=False)
print(segment.to_string())

# ─── SUBREGION ANALYSIS ───────────────────────────────────────────────────────
print(f"\n{'─'*65}")
print("SUBREGION ANALYSIS")
print("─" * 65)
region = df.groupby('Subregion').agg(
    Restaurants   = ('RestaurantID', 'count'),
    Total_Revenue = ('TotalRevenue', 'sum'),
    Avg_Revenue   = ('TotalRevenue', 'mean'),
    Avg_Orders    = ('TotalOrders', 'mean'),
    Top_Channel   = ('UberEatsRevenue', 'mean')
).round(2).sort_values('Total_Revenue', ascending=False)
print(region.to_string())

# ─── CHANNEL PROFITABILITY ────────────────────────────────────────────────────
print(f"\n{'─'*65}")
print("CHANNEL NET PROFIT ANALYSIS")
print("─" * 65)
profit_data = {
    'In-Store':       df['InStoreNetProfit'].sum(),
    'UberEats':       df['UberEatsNetProfit'].sum(),
    'DoorDash':       df['DoorDashNetProfit'].sum(),
    'Self-Delivery':  df['SelfDeliveryNetProfit'].sum(),
}
for ch, profit in sorted(profit_data.items(), key=lambda x: -x[1]):
    print(f"  {ch:<16}  NZD ${profit:>12,.0f}")

# ─── TOP 10 RESTAURANTS ───────────────────────────────────────────────────────
print(f"\n{'─'*65}")
print("TOP 10 RESTAURANTS BY TOTAL REVENUE")
print("─" * 65)
top10 = df.nlargest(10, 'TotalRevenue')[
    ['RestaurantName', 'CuisineType', 'Subregion', 'Segment',
     'TotalRevenue', 'TotalOrders', 'TotalNetProfit']
]
print(top10.to_string(index=False))

# ─── SAVE SUMMARY ─────────────────────────────────────────────────────────────
cuisine.to_csv("../outputs/cuisine_analysis.csv")
segment.to_csv("../outputs/segment_analysis.csv")
region.to_csv("../outputs/region_analysis.csv")
top10.to_csv("../outputs/top10_restaurants.csv", index=False)

kpi = pd.DataFrame({
    'KPI':   ['Total Revenue (NZD)', 'In-Store Revenue', 'UberEats Revenue',
               'DoorDash Revenue', 'Self-Delivery Revenue', 'Total Orders',
               'Avg Order Value', 'Total Net Profit', '% Profitable Restaurants'],
    'Value': [f"${grand_revenue:,.0f}", f"${instore_rev:,.0f}", f"${ubereats_rev:,.0f}",
              f"${doordash_rev:,.0f}", f"${selfdel_rev:,.0f}", f"{total_orders:,}",
              f"${avg_aov:.2f}", f"${total_profit:,.0f}", f"{profitable_pct:.1f}%"]
})
kpi.to_csv("../outputs/kpi_summary.csv", index=False)
print("\n✓ Analysis files saved to outputs/")
