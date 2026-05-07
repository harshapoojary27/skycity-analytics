"""
SkyCity Auckland - Order Channel Analytics Dashboard
THEME: CYBERPUNK DARK (Black + Neon Cyan)
Run: streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SkyCity Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Share+Tech+Mono&display=swap');

/* ---------- background ---------- */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main, .main > div {
    background-color: #050d1a !important;
}

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] {
    background-color: #0a1628 !important;
    border-right: 1px solid rgba(0,255,224,0.15) !important;
}
[data-testid="stSidebar"] * {
    color: #00ffe0 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* ---------- block container ---------- */
.block-container {
    padding-top: 1rem !important;
    background: #050d1a !important;
}

/* ---------- ALL text default ---------- */
body, p, div, span, label {
    color: #00ffe0 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* ---------- metric card ---------- */
[data-testid="metric-container"] {
    background: #0a1628 !important;
    border: 1px solid rgba(0,255,224,0.25) !important;
    border-radius: 8px !important;
    padding: 16px 12px !important;
    width: 100% !important;
    box-sizing: border-box !important;
    overflow: visible !important;
}

/* metric label */
[data-testid="metric-container"] label,
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p,
[data-testid="stMetricLabel"] div {
    color: rgba(0,255,224,0.6) !important;
    font-size: 0.6rem !important;
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    text-align: center !important;
    width: 100% !important;
    display: block !important;
    white-space: normal !important;
    word-break: break-word !important;
}

/* metric value */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #00ffe0 !important;
    font-size: 1.25rem !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    text-align: center !important;
    width: 100% !important;
    display: block !important;
    white-space: nowrap !important;
    overflow: visible !important;
}

/* metric delta */
[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] div {
    color: rgba(0,255,224,0.5) !important;
    font-size: 0.6rem !important;
    text-align: center !important;
    width: 100% !important;
    display: block !important;
}

/* center the inner flex containers */
[data-testid="stMetricLabel"] > div,
[data-testid="stMetricValue"] > div,
[data-testid="stMetricDelta"] > div {
    justify-content: center !important;
}

/* ---------- section header ---------- */
.sh {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.62rem;
    color: rgba(0,255,224,0.65);
    letter-spacing: 3px;
    text-transform: uppercase;
    border-left: 3px solid #00ffe0;
    padding: 4px 0 4px 12px;
    margin: 20px 0 12px 0;
    background: rgba(0,255,224,0.03);
}

/* ---------- divider ---------- */
hr { border-color: rgba(0,255,224,0.1) !important; }

/* ---------- dataframe ---------- */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,255,224,0.15) !important;
    border-radius: 6px !important;
}

/* ---------- hide material icon font (fixes keyboard_double_arrow_right) ---------- */
[data-testid="stMetricDelta"] svg { display: none !important; }
[data-testid="stMetricDelta"] { display: none !important; }

/* ---------- scrollbar ---------- */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #050d1a; }
::-webkit-scrollbar-thumb { background: rgba(0,255,224,0.3); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ── Plotly constants ──────────────────────────────────────────────────────────
BG    = '#050d1a'
PAPER = '#0a1628'
GRID  = 'rgba(0,255,224,0.07)'
TICK  = 'rgba(0,255,224,0.45)'
CYAN  = '#00ffe0'
CYAN2 = '#00b4cc'
CYAN3 = '#007a8a'
RED   = '#ff4444'

def cyber(fig, h=340, leg=False):
    fig.update_layout(
        height=h,
        paper_bgcolor=PAPER,
        plot_bgcolor=BG,
        font=dict(family='Share Tech Mono, monospace', color=CYAN),
        margin=dict(l=14, r=14, t=14, b=14),
        showlegend=leg,
        legend=dict(bgcolor=PAPER, bordercolor='rgba(0,255,224,0.15)',
                    borderwidth=1, font=dict(color=TICK, size=10),
                    orientation='h', yanchor='bottom', y=1.02),
        xaxis=dict(gridcolor=GRID, zerolinecolor=GRID,
                   tickfont=dict(color=TICK, size=10),
                   title_font=dict(color=TICK)),
        yaxis=dict(gridcolor=GRID, zerolinecolor=GRID,
                   tickfont=dict(color=TICK, size=10),
                   title_font=dict(color=TICK)),
    )
    return fig

def sh(title):
    st.markdown(f'<div class="sh">// &nbsp; {title}</div>', unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    df = pd.read_csv("data/SkyCity_Auckland_Restaurants_Bars.csv")
    df['TotalRevenue']   = (df['InStoreRevenue']   + df['UberEatsRevenue']
                          + df['DoorDashRevenue']   + df['SelfDeliveryRevenue'])
    df['TotalOrders']    = (df['InStoreOrders']    + df['UberEatsOrders']
                          + df['DoorDashOrders']    + df['SelfDeliveryOrders'])
    df['TotalNetProfit'] = (df['InStoreNetProfit'] + df['UberEatsNetProfit']
                          + df['DoorDashNetProfit'] + df['SelfDeliveryNetProfit'])
    df['Profitable']     = df['TotalNetProfit'] > 0
    return df

df = load()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<p style='font-family:Orbitron,monospace;font-size:1rem;font-weight:700;"
        "color:#00ffe0;letter-spacing:3px;margin-bottom:4px;'>⚡ SKYCITY</p>"
        "<p style='font-size:0.55rem;letter-spacing:2px;color:rgba(0,255,224,0.4);"
        "margin-bottom:20px;'>ANALYTICS.SYS</p>",
        unsafe_allow_html=True
    )
    cuisine_opts = ["All"] + sorted(df['CuisineType'].unique().tolist())
    sel_cuisine  = st.selectbox("CUISINE TYPE", cuisine_opts)

    segment_opts = ["All"] + sorted(df['Segment'].unique().tolist())
    sel_segment  = st.selectbox("SEGMENT", segment_opts)

    region_opts  = ["All"] + sorted(df['Subregion'].unique().tolist())
    sel_region   = st.selectbox("SUBREGION", region_opts)

    sel_rev = st.slider("REVENUE RANGE (NZD)",
                        int(df['TotalRevenue'].min()),
                        int(df['TotalRevenue'].max()),
                        (int(df['TotalRevenue'].min()), int(df['TotalRevenue'].max())),
                        step=1000)
    st.markdown("---")
    st.markdown(
        "<p style='font-size:0.55rem;letter-spacing:1px;color:rgba(0,255,224,0.3);"
        "line-height:2;'>SKYCITY AUCKLAND<br>MCA INTERNSHIP PROJECT<br>"
        "PYTHON · STREAMLIT · PLOTLY</p>",
        unsafe_allow_html=True
    )

# ── Filter ────────────────────────────────────────────────────────────────────
fdf = df.copy()
if sel_cuisine != "All": fdf = fdf[fdf['CuisineType'] == sel_cuisine]
if sel_segment != "All": fdf = fdf[fdf['Segment']     == sel_segment]
if sel_region  != "All": fdf = fdf[fdf['Subregion']   == sel_region]
fdf = fdf[(fdf['TotalRevenue'] >= sel_rev[0]) & (fdf['TotalRevenue'] <= sel_rev[1])]

# ── KPI calc ──────────────────────────────────────────────────────────────────
total_rev  = fdf['TotalRevenue'].sum()
ue_rev     = fdf['UberEatsRevenue'].sum()
ins_rev    = fdf['InStoreRevenue'].sum()
dd_rev     = fdf['DoorDashRevenue'].sum()
sd_rev     = fdf['SelfDeliveryRevenue'].sum()
tot_orders = fdf['TotalOrders'].sum()
aov        = fdf['AOV'].mean()
net_profit = fdf['TotalNetProfit'].sum()
prof_pct   = fdf['Profitable'].mean() * 100

# ── Header banner ─────────────────────────────────────────────────────────────
st.markdown(
    "<div style='background:#0a1628;border-bottom:1px solid rgba(0,255,224,0.18);"
    "padding:16px 20px;margin:-1rem -1rem 1.2rem -1rem;'>"
    "<span style='font-family:Orbitron,monospace;font-size:1.05rem;font-weight:700;"
    "color:#00ffe0;letter-spacing:2px;'>⚡ SKYCITY AUCKLAND — ORDER CHANNEL ANALYTICS</span>"
    f"<br><span style='font-size:0.58rem;color:rgba(0,255,224,0.4);letter-spacing:1px;'>"
    f"Showing {len(fdf):,} of {len(df):,} restaurants &nbsp;·&nbsp; "
    f"Cuisine: {sel_cuisine} &nbsp;·&nbsp; Segment: {sel_segment} &nbsp;·&nbsp; Region: {sel_region}"
    f"</span></div>",
    unsafe_allow_html=True
)

# ════════════════════════════════════════════════════════════════
# KPI ROW 1
# ════════════════════════════════════════════════════════════════
sh("Key Performance Indicators")
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Total Revenue",   f"${total_rev/1e6:.2f}M")
c2.metric("Total Orders",    f"{tot_orders:,}")
c3.metric("Avg Order Value", f"${aov:.2f}")
c4.metric("Net Profit",      f"${net_profit/1e6:.2f}M")
c5.metric("Profitable",      f"{prof_pct:.1f}%")

# ── KPI ROW 2 ─────────────────────────────────────────────────────────────────
c6,c7,c8,c9,c10 = st.columns(5)
c6.metric("In-Store Rev",    f"${ins_rev/1e6:.2f}M")
c7.metric("UberEats Rev",    f"${ue_rev/1e6:.2f}M")
c8.metric("DoorDash Rev",    f"${dd_rev/1e6:.2f}M")
c9.metric("Self-Delivery",   f"${sd_rev/1e6:.2f}M")
c10.metric("Restaurants",    f"{len(fdf):,}")

st.markdown("---")

# ════════════════════════════════════════════════════════════════
# ROW 1 — Revenue by Channel | Market Share
# ════════════════════════════════════════════════════════════════
sh("Revenue & Market Share")
col1, col2 = st.columns([1.1, 0.9])

with col1:
    ch = pd.DataFrame({
        'Channel': ['In-Store','UberEats','DoorDash','Self-Delivery'],
        'Revenue': [ins_rev, ue_rev, dd_rev, sd_rev],
    }).sort_values('Revenue', ascending=True)

    fig = go.Figure(go.Bar(
        x=ch['Revenue'], y=ch['Channel'], orientation='h',
        marker=dict(
            color=['rgba(0,255,224,0.3)','rgba(0,255,224,0.5)',
                   'rgba(0,255,224,0.75)','rgba(0,255,224,1.0)'],
            line=dict(color=CYAN, width=0.5)),
        text=[f"${v/1e6:.2f}M" for v in ch['Revenue']],
        textposition='outside',
        textfont=dict(color=CYAN, size=11),
    ))
    cyber(fig, h=300)
    fig.update_layout(xaxis_title="Revenue (NZD)",
                      yaxis=dict(tickfont=dict(color=CYAN,size=12),
                                 gridcolor='rgba(0,0,0,0)'))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = go.Figure(go.Pie(
        labels=['In-Store','UberEats','DoorDash','Self-Delivery'],
        values=[ins_rev, ue_rev, dd_rev, sd_rev],
        hole=0.55,
        marker=dict(
            colors=['rgba(0,255,224,0.25)','rgba(0,255,224,1.0)',
                    'rgba(0,255,224,0.65)','rgba(0,255,224,0.42)'],
            line=dict(color=BG, width=2)),
        textinfo='percent+label',
        textfont=dict(color=CYAN, size=10),
    ))
    cyber(fig2, h=300)
    fig2.add_annotation(text=f"{ue_rev/total_rev*100:.1f}%",
                        x=0.5, y=0.55,
                        font=dict(size=22,color=CYAN,family='Orbitron,monospace'),
                        showarrow=False)
    fig2.add_annotation(text="UBEREATS TOP",
                        x=0.5, y=0.4,
                        font=dict(size=8,color=TICK,family='Share Tech Mono,monospace'),
                        showarrow=False)
    st.plotly_chart(fig2, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# ROW 2 — Cuisine | Segment Scatter
# ════════════════════════════════════════════════════════════════
sh("Cuisine & Segment Analysis")
col3, col4 = st.columns(2)

with col3:
    cg = (fdf.groupby('CuisineType')['TotalRevenue']
            .sum().reset_index()
            .sort_values('TotalRevenue', ascending=False))
    n = len(cg)
    fig3 = go.Figure(go.Bar(
        x=cg['CuisineType'], y=cg['TotalRevenue'],
        marker=dict(
            color=[f'rgba(0,255,224,{round(1.0-(i/n)*0.55,2)})' for i in range(n)],
            line=dict(color='rgba(0,255,224,0.3)', width=0.8)),
        text=[f"${v/1e6:.1f}M" for v in cg['TotalRevenue']],
        textposition='outside',
        textfont=dict(color=CYAN, size=10),
    ))
    cyber(fig3, h=330)
    fig3.update_layout(yaxis_title="Revenue (NZD)",
                       xaxis=dict(tickfont=dict(color=CYAN,size=10),gridcolor=GRID))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    sg = fdf.groupby('Segment').agg(
        TotalRevenue=('TotalRevenue','sum'),
        AvgProfit=('TotalNetProfit','mean'),
        Count=('RestaurantID','count')
    ).reset_index()
    seg_cols = [CYAN, CYAN2, CYAN3, RED]
    fig4 = go.Figure()
    for i, row in sg.iterrows():
        c = seg_cols[i % 4]
        fig4.add_trace(go.Scatter(
            x=[row['TotalRevenue']], y=[row['AvgProfit']],
            mode='markers+text',
            marker=dict(size=max(row['Count']/8,12), color=c,
                        line=dict(color=c,width=1.5), opacity=0.85),
            text=[row['Segment']], textposition='top center',
            textfont=dict(color=c, size=10), name=row['Segment'],
        ))
    cyber(fig4, h=330)
    fig4.update_layout(xaxis_title="Total Revenue (NZD)",
                       yaxis_title="Avg Net Profit (NZD)")
    st.plotly_chart(fig4, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# ROW 3 — Subregion Pie | Net Profit Bars
# ════════════════════════════════════════════════════════════════
sh("Region & Profitability")
col5, col6 = st.columns(2)

with col5:
    rg = fdf.groupby('Subregion')['TotalRevenue'].sum().reset_index()
    n  = len(rg)
    fig5 = go.Figure(go.Pie(
        labels=rg['Subregion'], values=rg['TotalRevenue'],
        hole=0.4,
        marker=dict(
            colors=[f'rgba(0,255,224,{round(1.0-i*0.2,1)})' for i in range(n)],
            line=dict(color=BG, width=2)),
        textinfo='percent+label',
        textfont=dict(color=CYAN, size=10),
    ))
    cyber(fig5, h=320)
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    pvals = [fdf['InStoreNetProfit'].sum(), fdf['UberEatsNetProfit'].sum(),
             fdf['DoorDashNetProfit'].sum(), fdf['SelfDeliveryNetProfit'].sum()]
    pcols = [CYAN if v >= 0 else RED for v in pvals]
    fig6 = go.Figure(go.Bar(
        x=['In-Store','UberEats','DoorDash','Self-Delivery'],
        y=pvals,
        marker=dict(color=pcols, line=dict(color=pcols, width=0.5)),
        text=[f"${v/1e3:.0f}K" for v in pvals],
        textposition='outside',
        textfont=dict(color=CYAN, size=11),
    ))
    cyber(fig6, h=320)
    fig6.update_layout(
        yaxis_title="Net Profit (NZD)",
        xaxis=dict(tickfont=dict(color=CYAN,size=11), gridcolor=GRID),
        yaxis=dict(gridcolor=GRID, tickfont=dict(color=TICK,size=10),
                   zerolinecolor='rgba(0,255,224,0.2)', zerolinewidth=1),
    )
    st.plotly_chart(fig6, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# FORECAST
# ════════════════════════════════════════════════════════════════
sh("6-Month Revenue Forecast — ARIMA + MA + Exponential Smoothing")
try:
    fc = pd.read_csv("outputs/forecast_results.csv")
    fig7 = go.Figure()
    traces = [
        ('MA6',          'MA-6',           'rgba(0,255,224,0.3)', 'dot',   2),
        ('ARIMA',        'ARIMA',           CYAN2,                 'solid', 2),
        ('ES_Seasonal',  'Exp. Smoothing',  CYAN3,                 'dash',  2),
        ('Ensemble_Avg', 'Ensemble (Best)', CYAN,                  'solid', 3),
    ]
    for col, name, color, dash, width in traces:
        fig7.add_trace(go.Scatter(
            x=fc['Month'], y=fc[col], mode='lines+markers', name=name,
            line=dict(color=color, dash=dash, width=width),
            marker=dict(color=color, size=6),
        ))
    cyber(fig7, h=360, leg=True)
    fig7.update_layout(xaxis_title="Month", yaxis_title="Revenue Forecast (NZD)")
    st.plotly_chart(fig7, use_container_width=True)
except FileNotFoundError:
    st.info("Run `python src/03_forecasting.py` first to generate forecast data.")

# ════════════════════════════════════════════════════════════════
# TOP 20 TABLE
# ════════════════════════════════════════════════════════════════
sh("Top 20 Restaurants — By Total Revenue")
top20 = fdf.nlargest(20, 'TotalRevenue')[
    ['RestaurantName','CuisineType','Segment','Subregion',
     'TotalRevenue','TotalOrders','AOV','TotalNetProfit','Profitable']
].reset_index(drop=True)
top20.index += 1
top20['TotalRevenue']   = top20['TotalRevenue'].apply(lambda x: f"${x:,.0f}")
top20['TotalNetProfit'] = top20['TotalNetProfit'].apply(lambda x: f"${x:,.0f}")
top20['AOV']            = top20['AOV'].apply(lambda x: f"${x:.2f}")
top20['Profitable']     = top20['Profitable'].map({True:"✅ YES", False:"❌ NO"})
st.dataframe(top20, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# HEATMAP
# ════════════════════════════════════════════════════════════════
sh("Cuisine × Channel Revenue Heatmap")
heat = fdf.groupby('CuisineType').agg(
    InStore=('InStoreRevenue','sum'),
    UberEats=('UberEatsRevenue','sum'),
    DoorDash=('DoorDashRevenue','sum'),
    SelfDelivery=('SelfDeliveryRevenue','sum'),
).reset_index()

zvals = heat[['InStore','UberEats','DoorDash','SelfDelivery']].values
ztxt  = [[f"${v/1e6:.1f}M" for v in row] for row in zvals]

fig8 = go.Figure(go.Heatmap(
    z=zvals,
    x=['In-Store','UberEats','DoorDash','Self-Delivery'],
    y=heat['CuisineType'].tolist(),
    colorscale=[
        [0.0,  'rgba(0,13,26,1)'],
        [0.33, 'rgba(0,100,115,0.7)'],
        [0.66, 'rgba(0,180,204,0.85)'],
        [1.0,  'rgba(0,255,224,1)'],
    ],
    text=ztxt,
    texttemplate="%{text}",
    textfont=dict(color='#050d1a', size=10),
    showscale=False,
))
cyber(fig8, h=340)
fig8.update_layout(
    xaxis=dict(tickfont=dict(color=CYAN,size=11), gridcolor='rgba(0,0,0,0)'),
    yaxis=dict(tickfont=dict(color=CYAN,size=11), gridcolor='rgba(0,0,0,0)'),
    xaxis_title="Order Channel",
    yaxis_title="Cuisine Type",
)
st.plotly_chart(fig8, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;font-size:0.55rem;letter-spacing:2px;"
    "color:rgba(0,255,224,0.25);font-family:Orbitron,monospace;'>"
    "SKYCITY AUCKLAND // MCA INTERNSHIP PROJECT // PYTHON · STREAMLIT · PLOTLY"
    "</p>",
    unsafe_allow_html=True
)
