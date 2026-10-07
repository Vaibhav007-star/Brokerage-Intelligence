# Tableau Public Dashboard Screenshots

This folder contains the visual captures of the final interactive dashboards built in Tableau Public for the CIA-III Business Intelligence project: **"Brokerage Intelligence: BI-Based Stock Trading & Market Activity Analytics"**.

---

## Dashboard Inventory

### 1. Dashboard 1: Executive Market Overview
* **File**: `dashboard_1_executive_market_overview.png`
* **Components**:
  - **Macro KPI Cards**: KPI Volume, KPI Trades, KPI Turnover, KPI Delivery Rate.
  - **Market Activity Trend**: Dual-axis monthly time series of Market Turnover (₹ Cr) and Traded Volume (Crore Shares).
  - **Liquidity Leaders**: Horizontal ranking of Top 10 Equities by Turnover (RELIANCE, SBIN, ICICIBANK, INFY, AXISBANK, HDFC...) color-coded by Deliverable Ratio.
  - **Market Benchmark & Volatility**: Dual-axis comparison of NIFTY 50 Index vs. INDIA VIX Volatility levels.

---

### 2. Dashboard 2: Stock Trading & Liquidity Deep-Dive
* **File**: `dashboard_2_stock_trading_liquidity_deep_dive.png`
* **Components**:
  - **Sector Liquidity Treemap**: Capital distribution across sectors (Banking, IT, Oil & Gas, Financial Services, Auto, Pharma, FMCG...).
  - **Delivery Rate Trend**: Historical secular compression line chart showing delivery dropping from ~54% to ~35%.
  - **Intraday Price Spread**: Historical daily price spread volatility (`High - Low`) over time.
  - **Interactive Filters**: Sector checklist and Delivery Rate % range sliders.

---

### 3. Dashboard 3: Sectoral Dynamics & Market Microstructure
* **File**: `dashboard_3_sectoral_dynamics_market_microstructure.png`
* **Components**:
  - **Sector Treemap**: High-level sector participation sized by total monetary turnover and colored by delivery rate.
  - **Investment Conviction vs. Return Quadrant (Scatter Plot)**: 
    - **X-Axis**: Delivery Rate % (with Average reference line at 45%).
    - **Y-Axis**: Average Daily Return %.
    - **Bubble Size**: Turnover INR.
    - **Color**: Industry Sector.
  - **Interactive Filter Action**: Selecting any sector in the treemap dynamically filters the constituent stocks in the scatter plot below.

