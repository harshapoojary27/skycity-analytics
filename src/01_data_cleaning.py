"""
╔═══════════════════════════════════════════════════════════════╗
║  SkyCity Auckland — Step 1: Data Cleaning & Preprocessing     ║
║  Dataset: SkyCity_Auckland_Restaurants_Bars.csv               ║
╚═══════════════════════════════════════════════════════════════╝
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

DATA_PATH = "../data/SkyCity_Auckland_Restaurants_Bars.csv"

# ─── 1. Load Raw Data ─────────────────────────────────────────────────────────
print("=" * 65)
print("  STEP 1: DATA LOADING")
print("=" * 65)

df_raw = pd.read_csv(DATA_PATH)
print(f"Raw shape        : {df_raw.shape[0]:,} rows × {df_raw.shape[1]} columns")
print(f"Missing values   : {df_raw.isnull().sum().sum()}")
print(f"Duplicate rows   : {df_raw.duplicated().sum()}")
print(f"\nColumns:\n{list(df_raw.columns)}")

# ─── 2. Feature Engineering ───────────────────────────────────────────────────
print("\n" + "=" * 65)
print("  STEP 2: FEATURE ENGINEERING")
print("=" * 65)

df = df_raw.copy()

# Derived revenue columns
df['TotalRevenue']    = (df['InStoreRevenue'] + df['UberEatsRevenue']
                         + df['DoorDashRevenue'] + df['SelfDeliveryRevenue'])
df['TotalOrders']     = (df['InStoreOrders'] + df['UberEatsOrders']
                         + df['DoorDashOrders'] + df['SelfDeliveryOrders'])
df['TotalNetProfit']  = (df['InStoreNetProfit'] + df['UberEatsNetProfit']
                         + df['DoorDashNetProfit'] + df['SelfDeliveryNetProfit'])

# Channel market shares (per restaurant)
df['InStore_Share%']   = (df['InStoreRevenue']    / df['TotalRevenue'] * 100).round(2)
df['UberEats_Share%']  = (df['UberEatsRevenue']   / df['TotalRevenue'] * 100).round(2)
df['DoorDash_Share%']  = (df['DoorDashRevenue']   / df['TotalRevenue'] * 100).round(2)
df['SelfDel_Share%']   = (df['SelfDeliveryRevenue']/ df['TotalRevenue'] * 100).round(2)

# Revenue per order per channel
df['InStore_RPO']   = (df['InStoreRevenue']     / df['InStoreOrders']).round(2)
df['UberEats_RPO']  = (df['UberEatsRevenue']    / df['UberEatsOrders']).round(2)
df['DoorDash_RPO']  = (df['DoorDashRevenue']    / df['DoorDashOrders']).round(2)
df['SelfDel_RPO']   = (df['SelfDeliveryRevenue']/ df['SelfDeliveryOrders']).round(2)

# Profitability flag
df['Profitable'] = df['TotalNetProfit'] > 0

# Revenue tier
df['RevenueTier'] = pd.cut(
    df['TotalRevenue'],
    bins=[0, 40000, 60000, 80000, float('inf')],
    labels=['Low', 'Medium', 'High', 'Premium']
)

print("New columns added:")
new_cols = ['TotalRevenue','TotalOrders','TotalNetProfit',
            'InStore_Share%','UberEats_Share%','DoorDash_Share%','SelfDel_Share%',
            'InStore_RPO','UberEats_RPO','DoorDash_RPO','SelfDel_RPO',
            'Profitable','RevenueTier']
for c in new_cols:
    print(f"  + {c}")

# ─── 3. Data Quality Checks ───────────────────────────────────────────────────
print("\n" + "=" * 65)
print("  STEP 3: DATA QUALITY REPORT")
print("=" * 65)
print(f"Records with negative Net Profit : {(df['TotalNetProfit'] < 0).sum()}")
print(f"Records with zero Total Revenue  : {(df['TotalRevenue'] == 0).sum()}")
print(f"Profitable restaurants           : {df['Profitable'].sum()} / {len(df)}")
print(f"Avg Total Revenue (NZD)          : ${df['TotalRevenue'].mean():,.2f}")
print(f"Avg Order Value (AOV)            : ${df['AOV'].mean():.2f}")

# ─── 4. Save Cleaned Data ─────────────────────────────────────────────────────
df.to_csv("../data/skycity_cleaned.csv", index=False)
print(f"\n✓ Cleaned dataset saved → data/skycity_cleaned.csv")
print(f"  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
