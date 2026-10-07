# Tableau Public Calculated Fields Reference Manual (Phase 10)

**Project**: Brokerage Intelligence: BI-Based Stock Trading & Market Activity Analytics  
**Course**: Business Intelligence (CIA-III)  
**Target Platform**: Tableau Public  

---

## 1. Overview & Data Sources

These calculated fields are engineered for direct implementation in Tableau Public. All calculations are optimized for high performance without unnecessary nested Level of Detail (LOD) calculations.

The primary Tableau Public data sources are:
1. `tableau_stock_analytics.csv` (`Primary Stock Analytics Source`)
2. `tableau_market_summary.csv` (`Executive Macro Overview Source`)
3. `tableau_index_analytics.csv` (`Benchmark & Sectoral Index Source`)

---

## 2. Calculated Fields Dictionary

### Calculation 1: Turnover in ₹ Crores (Monetary Scaling)
* **Field Name**: `Turnover (Cr ₹)`
* **Data Source**: `tableau_stock_analytics.csv` / `tableau_market_summary.csv`
* **Exact Tableau Formula**:
  ```tableau
  [Turnover_INR] / 10000000
  ```
* **Purpose**: Converts raw rupee turnover into standard Indian financial unit (1 Crore = 10,000,000 INR).
* **Where Used**: All Turnover KPI cards, bar charts, and trend lines.
* **Number Format**: Currency (Custom) $\rightarrow$ Prefix: `₹`, Suffix: ` Cr`, Decimals: `1`.

---

### Calculation 2: Deliverable Turnover in ₹ Crores
* **Field Name**: `Deliverable Turnover (Cr ₹)`
* **Data Source**: `tableau_stock_analytics.csv`
* **Exact Tableau Formula**:
  ```tableau
  [Deliverable_Turnover_INR] / 10000000
  ```
* **Purpose**: Measures the absolute monetary value of equity shares transferred to demat accounts.
* **Where Used**: Delivery vs. Intraday turnover breakdown charts.
* **Number Format**: Currency (Custom) $\rightarrow$ Prefix: `₹`, Suffix: ` Cr`, Decimals: `1`.

---

### Calculation 3: Aggregate Delivery Percentage
* **Field Name**: `Delivery Rate %`
* **Data Source**: `tableau_stock_analytics.csv`
* **Exact Tableau Formula**:
  ```tableau
  SUM([Deliverable_Volume]) / SUM([Volume])
  ```
* **Purpose**: Computes the true weighted delivery ratio across any aggregated level (Sector, Year, Market).
* **Where Used**: Sector delivery comparisons, annual trends, scatter plots.
* **Number Format**: Percentage $\rightarrow$ Decimals: `1`.

---

### Calculation 4: Average Trade Ticket Size (₹)
* **Field Name**: `Avg Trade Ticket Size`
* **Data Source**: `tableau_stock_analytics.csv`
* **Exact Tableau Formula**:
  ```tableau
  SUM([Turnover_INR]) / SUM([Trades])
  ```
* **Purpose**: Determines the monetary average order value to identify institutional vs. retail market participation.
* **Where Used**: Stock liquidity deep-dive worksheets, tooltip metrics.
* **Number Format**: Currency (Custom) $\rightarrow$ Prefix: `₹`, Decimals: `0`.

---

### Calculation 5: Trading Behavior / Conviction Segment
* **Field Name**: `Delivery Conviction Category`
* **Data Source**: `tableau_stock_analytics.csv`
* **Exact Tableau Formula**:
  ```tableau
  IF [Delivery Rate %] >= 0.60 THEN "High Conviction (>60%)"
  ELSEIF [Delivery Rate %] >= 0.35 THEN "Moderate Delivery (35%-60%)"
  ELSE "Speculative Churn (<35%)"
  END
  ```
* **Purpose**: Classifies stocks or sectors into behavioral buckets based on investor holding conviction.
* **Where Used**: Color dimension on scatter plots and treemaps.

---

### Calculation 6: Traded Volume in Millions
* **Field Name**: `Volume (M Shares)`
* **Data Source**: `tableau_stock_analytics.csv`
* **Exact Tableau Formula**:
  ```tableau
  [Volume] / 1000000
  ```
* **Purpose**: Formats share volumes for clean chart labels.
* **Where Used**: Volume bar charts and dual-axis trends.
* **Number Format**: Number (Custom) $\rightarrow$ Suffix: ` M`, Decimals: `1`.

---

### Calculation 7: Stock Turnover Rank
* **Field Name**: `Rank by Turnover`
* **Data Source**: `tableau_stock_analytics.csv`
* **Exact Tableau Formula**:
  ```tableau
  RANK(SUM([Turnover_INR]), 'desc')
  ```
* **Purpose**: Dynamically ranks equities by traded monetary turnover based on active filters.
* **Where Used**: Top N filtering and leaderboard tables.

---

### Calculation 8: Top 10 Stock Selector
* **Field Name**: `Is Top 10 Stock`
* **Data Source**: `tableau_stock_analytics.csv`
* **Exact Tableau Formula**:
  ```tableau
  [Rank by Turnover] <= 10
  ```
* **Purpose**: Boolean filter to restrict visualizations to the Top 10 most liquid stocks.
* **Where Used**: Filter shelf (Filter = `True`).

---

### Calculation 9: Year-over-Year (YoY) Turnover Growth %
* **Field Name**: `YoY Turnover Growth %`
* **Data Source**: `tableau_market_summary.csv`
* **Exact Tableau Formula**:
  ```tableau
  (ZN(SUM([Total_Market_Turnover_INR])) - LOOKUP(ZN(SUM([Total_Market_Turnover_INR])), -1)) 
  / ABS(LOOKUP(ZN(SUM([Total_Market_Turnover_INR])), -1))
  ```
* **Purpose**: Table calculation measuring annual expansion rate of exchange trading turnover.
* **Where Used**: Executive summary annual growth waterfall or delta indicators.
* **Number Format**: Percentage $\rightarrow$ Decimals: `1`.

---

### Calculation 10: 20-Day Moving Average Turnover
* **Field Name**: `Turnover 20D Moving Avg (Cr ₹)`
* **Data Source**: `tableau_stock_analytics.csv`
* **Exact Tableau Formula**:
  ```tableau
  WINDOW_AVG(SUM([Turnover (Cr ₹)]), -19, 0)
  ```
* **Purpose**: Smooths daily turnover volatility to reveal underlying liquidity trends.
* **Where Used**: Stock-level trading trend lines.
* **Number Format**: Currency (Custom) $\rightarrow$ Prefix: `₹`, Suffix: ` Cr`, Decimals: `1`.

---

### Calculation 11: Cumulative Capital Return %
* **Field Name**: `Cumulative Return %`
* **Data Source**: `tableau_stock_analytics.csv`
* **Exact Tableau Formula**:
  ```tableau
  (ZN(SUM([Close])) - LOOKUP(ZN(SUM([Close])), FIRST())) 
  / ABS(LOOKUP(ZN(SUM([Close])), FIRST()))
  ```
* **Purpose**: Tracks long-term capital appreciation from the baseline session of the selected date range.
* **Where Used**: Stock multi-year performance benchmarking worksheet.
* **Number Format**: Percentage $\rightarrow$ Decimals: `1`.

---

### Calculation 12: Intraday Volatility Spread %
* **Field Name**: `Intraday Spread %`
* **Data Source**: `tableau_stock_analytics.csv`
* **Exact Tableau Formula**:
  ```tableau
  (AVG([High]) - AVG([Low])) / AVG([Low])
  ```
* **Purpose**: Measures the average daily high-to-low percentage trading range.
* **Where Used**: Risk and volatility comparison charts.
* **Number Format**: Percentage $\rightarrow$ Decimals: `2`.

