# Academic Project Report (CIA-III)

# Brokerage Intelligence: BI-Based Stock Trading & Market Activity Analytics

**Course**: Business Intelligence (CIA-III)  
**Academic Program**: Master of Business Administration / Master of Science in Data Analytics  
**Primary Platform**: Tableau Public (Visual Analytics) with Python 3.12 & SQL (Data Engineering)  
**Submission Date**: October 2026  

---

## 1. Title
**Brokerage Intelligence: BI-Based Stock Trading & Market Activity Analytics**

---

## 2. Executive Summary
This project delivers a comprehensive, end-to-end Business Intelligence (BI) solution for capital market trading and liquidity analytics using authentic historical datasets from the National Stock Exchange of India (NSE). By analyzing 244,637 daily equity trading records across 100 blue-chip companies and 114,419 daily index benchmark records across 30 indices spanning over a decade (2010–2020), this study models market microstructure, trading velocity, and delivery patterns.

Key empirical findings reveal an intense concentration of liquidity (top 10 equities capture 36.5% of total turnover) and a profound secular shift in Indian market behavior from delivery-based investing (53.1% in 2010) to high-velocity intraday trading (35.4% in 2020). Using a Fact-Constellation dimensional architecture, automated data cleaning pipelines, and interactive Tableau Public dashboards, the project equips brokerage executives, institutional sales desks, and risk controllers with actionable decision support.

---

## 3. Introduction
Financial markets generate immense volumes of transactional data daily. In modern capital markets, brokerage institutions, liquidity providers, and investment analysts rely heavily on Business Intelligence architectures to evaluate trading velocity, order execution quality, delivery patterns, and systemic volatility. 

While raw exchange trade summaries (Bhavcopies) contain comprehensive records of prices, volumes, and trade counts, their isolated and unstructured format impedes strategic analysis. This project establishes an enterprise-grade BI pipeline that extracts, normalizes, validates, and models raw market feeds into a dimensional warehouse, culminating in an interactive analytical dashboard deployed on Tableau Public.

---

## 4. Business Problem
Institutional brokerages and financial analysts face severe operational hurdles in translating raw exchange data into strategic decisions:
1. **Liquidity Opacity**: Inability to quickly identify which sectors and individual stocks command true market depth versus temporary speculative bursts.
2. **Delivery vs. Speculation Ambiguity**: Difficulty distinguishing long-term institutional accumulation from high-frequency intraday churning.
3. **Benchmarking Disconnect**: Lack of integrated visual tools to benchmark individual equity liquidity and returns against broad-market (NIFTY 50) and sectoral indices.
4. **Volatility Regime Risks**: Sub-optimal margin calibration due to siloed volatility metrics during systemic market dislocations.

---

## 5. Objectives
### Primary Objectives:
1. Audit and profile real-world trading feeds from the NSE Top 100 equities and NSE 30 Indices.
2. Develop an automated, modular, and reproducible Python ETL pipeline.
3. Design a Fact-Constellation dimensional warehouse schema sharing conformed calendar attributes.
4. Demonstrate multidimensional OLAP operations (Roll-up, Drill-down, Slice, Dice, Pivot).
5. Formulate and engineer 15 robust trading Key Performance Indicators (KPIs).
6. Build and publish an interactive, executive-grade analytical dashboard exclusively on Tableau Public.

---

## 6. Data Sources
The project utilizes two real raw datasets from official National Stock Exchange archives:
1. **Dataset 1: NSE Top 100 Stocks**:
   - Location: `data/raw/nse_top_100/`
   - Format: 100 individual Excel files (`Stock_<SYMBOL>.xlsx`) plus 3 benchmark index files.
   - Volume: 244,901 raw rows across 15 columns.
   - Temporal Range: January 4, 2010 to October 1, 2020 (2,668 trading sessions).
2. **Dataset 2: NSE 30 Indices**:
   - Location: `data/raw/nse_30_indices/NSE_Daily_indices_data.csv`
   - Format: 1 single CSV file (12.2 MB).
   - Volume: 114,419 rows across 15 columns.
   - Temporal Range: February 4, 1997 to May 16, 2025 (28+ years).

---

## 7. Data Description (Real Data vs. Derived Data)

To maintain absolute academic integrity, the project strictly distinguishes between **Real Raw Data Attributes** and **Derived / Calculated Fields**:

### 7.1 Real Raw Data Attributes
* **Stock Attributes**: `Date`, `Symbol`, `Series` (`'EQ'`), `Prev Close`, `Open`, `High`, `Low`, `Last`, `Close`, `VWAP`, `Volume`, `Turnover` (raw scale $10^5$), `Trades`, `Deliverable Volume`, `%Deliverble`.
* **Index Attributes**: `DATETIME`, `SYMBOL`, `OPEN`, `HIGH`, `LOW`, `CLOSE`, `VOLUME`, `PREVIOUS_CLOSE`, `CHANGE`, `CHANGE_PERCENT`, `LOW_CLOSE`, `HIGH_CLOSE`, `TOTAL`, `GAP`, `INTERVAL`.

### 7.2 Derived / Calculated Attributes (Engineered in ETL & BI Layer)
* `Turnover_INR`: True rupee turnover calculated as $\text{Raw\_Turnover} / 100,000$.
* `Date_Key`: Integer surrogate key formatted as `YYYYMMDD`.
* `Stock_Key` & `Index_Key`: Surrogate primary keys for dimensional modeling.
* `Daily_Return_Pct`: Percentage daily close-to-close price return.
* `Price_Spread`: Intraday price volatility spread calculated as $\text{High} - \text{Low}$.
* `Avg_Trade_Size_INR`: Average monetary order size calculated as $\text{Turnover\_INR} / \text{Trades}$.
* `Deliverable_Turnover_INR`: Monetary delivery turnover calculated as $\text{Turnover\_INR} \times \text{Deliverable\_Pct}$.
* `Sector` & `Benchmark_Index`: Dimension enrichment mapping each of the 100 stocks to official NSE sectors.
* `Index_Category`: Classification into Broad Market, Sectoral, or Volatility index.

---

## 8. Data Quality & Audit Governance
A rigorous data quality assessment was executed via `scripts/validate_data.py`, achieving a **100.0% pass rate across 15 validation rules**:
1. **Deduplication**: Identified and purged 264 redundant rows occurring on identical dates across 88 stock files.
2. **Turnover Scale Correction**: Corrected the raw $10^5$ scaling factor to prevent 100,000x monetary inflation.
3. **Symbol Reconciliation**: Reconciled 6 historical ticker changes (`MUNDRAPORT` $\rightarrow$ `ADANIPORTS`, `BAJAUTOFIN` $\rightarrow$ `BAJFINANCE`, `HEROHONDA` $\rightarrow$ `HEROMOTOCO`, `INFOSYSTCH` $\rightarrow$ `INFY`, `PIRHEALTH` $\rightarrow$ `PEL`, `UNIPHOS` $\rightarrow$ `UPL`).
4. **Structural Missing Trades Audit**: Accounted for 30,684 missing values in `Trades` as an exchange-level regulatory introduction that commenced on June 1, 2011.
5. **Referential Integrity**: Ensured 100% of equities map cleanly to verified sectors and benchmark indices.

---

## 9. ETL Process
The end-to-end ETL architecture was engineered in Python 3.12:
- **Extract**: Loaded 100 Excel files and 1 index CSV using `pandas` and `openpyxl`.
- **Transform**: Standardized dates to ISO `YYYY-MM-DD`, converted numeric columns, rescaled turnover, computed derived metrics, and enriched with dimensional metadata.
- **Validate**: Automated assertion suite verified data invariants, ranges, and uniqueness constraints.
- **Load**: Outputted normalized relational tables into `data/warehouse/` and optimized, denormalized extracts into `data/tableau_ready/`.

---

## 10. Data Warehouse Architecture
The dimensional model implements a **Fact Constellation (Galaxy Schema)**:
- **Conformed Dimension**: `DIM_DATE` (7,025 rows, Calendar attributes).
- **Domain Dimensions**: `DIM_STOCK` (100 equities), `DIM_INDEX` (30 indices), `DIM_SECTOR` (26 sectors).
- **Fact Tables**:
  - `FACT_STOCK_DAILY` (244,637 rows; Grain: Stock $\times$ Day).
  - `FACT_INDEX_DAILY` (114,419 rows; Grain: Index $\times$ Day).

---

## 11. Star Schema / Fact Constellation Design
The schema features clear 1:N relationships connecting dimensions to fact tables. Surrogate keys (`Date_Key`, `Stock_Key`, `Index_Key`) guarantee query performance and shield analytics from transactional system renames.

```
       ┌─────────────────┐
       │    DIM_DATE     │
       │ (7,025 Records) │
       └────────┬────────┘
                │
     ┌──────────┴──────────┐
     │ 1:N                 │ 1:N
┌────▼───────────────┐┌────▼───────────────┐
│  FACT_STOCK_DAILY  ││  FACT_INDEX_DAILY  │
│ (244,637 Records)  ││ (114,419 Records)  │
└────▲───────────────┘└────▲───────────────┘
     │ N:1                 │ N:1
┌────┴───────────────┐┌────┴───────────────┐
│     DIM_STOCK      ││     DIM_INDEX      │
│   (100 Records)    ││   (30 Records)     │
└────────────────────┘└────────────────────┘
```

---

## 12. Multidimensional OLAP Analysis
OLAP capabilities were validated using analytical SQL queries in SQLite:
- **Roll-up**: Temporal aggregation showed annual turnover surging from ₹15.82 Lakh Cr (2010) to ₹69.15 Lakh Cr (2020).
- **Drill-down**: Hierarchical navigation from Market Universe $\rightarrow$ Sector $\rightarrow$ Individual Stock.
- **Slice**: Filtering on a single dimension slice (e.g., Information Technology sector across 10 years).
- **Dice**: Multi-dimensional sub-cube slicing (e.g., Banking & IT sectors during Q1 2020).
- **Pivot**: Cross-tabular heatmap evaluating delivery percentages across sectors and years.

---

## 13. Key Performance Indicator (KPI) Design
Fifteen KPIs were designed and formulated:
1. *Total Traded Turnover*: $\sum \text{Turnover\_INR}$
2. *Total Traded Volume*: $\sum \text{Volume}$
3. *Total Executed Trades*: $\sum \text{Trades}$
4. *Average Daily Turnover*: $\sum \text{Turnover\_INR} / \text{Trading Days}$
5. *Average Daily Volume*: $\sum \text{Volume} / \text{Trading Days}$
6. *Deliverable Volume*: $\sum \text{Deliverable\_Volume}$
7. *Delivery Percentage*: $\sum \text{Deliverable\_Volume} / \sum \text{Volume}$
8. *Average Trade Ticket Size*: $\sum \text{Turnover\_INR} / \sum \text{Trades}$
9. *Daily Price Return %*: $((\text{Close} - \text{Prev\_Close}) / \text{Prev\_Close}) \times 100$
10. *Cumulative Return %*: $((\text{Close}_{\text{end}} - \text{Close}_{\text{start}}) / \text{Close}_{\text{start}}) \times 100$
11. *Turnover Market Share %*: $\text{Stock Turnover} / \text{Market Turnover}$
12. *Intraday Price Spread*: $\text{High} - \text{Low}$
13. *VWAP Premium / Discount %*: $((\text{Close} - \text{VWAP}) / \text{VWAP}) \times 100$
14. *Benchmark Index Return %*: Point return of benchmark indices
15. *India Volatility Index (VIX)*: Systemic annualized implied volatility

---

## 14. Tableau Public Dashboard Blueprint & Delivery
The visual analytics layer consists of three targeted, interactive dashboards implemented in Tableau Public:

### 14.1 Dashboard 1: Executive Market Overview
* **Focus**: High-level market liquidity, macro KPI scorecards, long-term turnover trends, and volatility regimes.
* **Key Visuals**:
  - 4 Macro KPI Cards (Volume, Trades, Turnover, Delivery %).
  - Dual-Axis Market Turnover (₹ Cr) and Traded Volume Trend (2010–2020).
  - Horizontal Bar Ranking of Top 10 Liquid Equities color-coded by Delivery Conviction.
  - Benchmark NIFTY 50 vs. INDIA VIX Volatility tracking.
* **Visual Reference**:
  ![Dashboard 1: Executive Market Overview](../tableau/dashboard_images/dashboard_1_executive_market_overview.png)

### 14.2 Dashboard 2: Stock Trading & Liquidity Deep-Dive
* **Focus**: Sector capital allocation, multi-year delivery rate compression, and intraday price spread dynamics.
* **Key Visuals**:
  - Capital Allocation Treemap across 11+ key sectors.
  - Secular delivery compression timeline showing the structural shift to intraday trading.
  - High-Low price spread volatility timeline.
* **Visual Reference**:
  ![Dashboard 2: Stock Trading & Liquidity Deep-Dive](../tableau/dashboard_images/dashboard_2_stock_trading_liquidity_deep_dive.png)

### 14.3 Dashboard 3: Sectoral Dynamics & Market Microstructure
* **Focus**: Multi-dimensional OLAP analysis linking sector participation with investment conviction vs. return profiles.
* **Key Visuals**:
  - Sector Treemap with turnover size and delivery rate color-coding.
  - Investment Conviction vs. Return Quadrant (Scatter plot of Delivery Rate % vs. Daily Return %, sized by Turnover INR).
  - Interactive Click-Filter Action: Clicking any sector in the treemap dynamically filters the scatter plot.
* **Visual Reference**:
  ![Dashboard 3: Sectoral Dynamics & Market Microstructure](../tableau/dashboard_images/dashboard_3_sectoral_dynamics_market_microstructure.png)


---

## 15. Empirical Business Insights
1. **Extreme Liquidity Concentration**: The top 10 stocks capture 36.5% of total market turnover, led by `RELIANCE` (5.66%) and `SBIN` (4.76%).
2. **Secular Decline in Delivery Conviction**: Average market delivery fell from 53.1% in 2010 to 35.4% in 2020 as traded volumes expanded over five-fold, demonstrating a structural rise in algorithmic intraday trading.
3. **Defensive vs. Cyclical Divergence**: FMCG and Technology sustain high delivery rates (55%–68%), whereas Banking and Metals act as speculative trading instruments (delivery $<35\%$).
4. **Volatility Spikes During Market Shocks**: In March 2020, INDIA VIX reached 83.6 as intraday price spreads widened by over 300%.
5. **Ticket Size Disparity**: High nominal price shares exhibit ticket sizes exceeding ₹150,000 (institutional participation), whereas low nominal price shares register ticket sizes under ₹30,000 (retail dominance).

---

## 16. Business Recommendations
1. **Order Routing & Execution**: Implement Smart Order Routers with specialized dark pool / block matching for the Top 10 turnover leaders.
2. **Infrastructure Investment**: Prioritize low-latency, real-time risk surveillance engines to manage high-velocity intraday order churn.
3. **Segmented Product Offerings**: Offer fundamental research and SIP baskets for high-delivery defensive equities, and quantitative intraday margin facilities for high-beta cyclical stocks.
4. **Dynamic Volatility Circuit-Breakers**: Automatically adjust margin haircuts and leverage multipliers when `INDIAVIX > 30`.
5. **Tiered Client Interfaces**: Provide algorithmic execution tools (VWAP/TWAP) for institutional ticket sizes and simplified mobile interfaces for retail order flow.

---

## 17. Limitations
- **Granularity Limitation**: Data represents end-of-day Bhavcopy summaries; intraday tick-level order book dynamics (Level 2/3) are unavailable.
- **Historical Trades Metric**: Trade counts prior to June 1, 2011 were not captured by the exchange, restricting trade-ticket size calculations to post-2011 sessions.
- **Fixed Top 100 Universe**: The dataset tracks the 100 constituent equities established at dataset creation, without historical index reconstitution rebalancing.

---

## 18. Future Scope
- Integration of live API feeds (e.g., NSE WebSocket or AlphaVantage) for real-time intraday streaming analytics.
- Integration of derivative open interest (Futures & Options) to analyze market positioning and put-call ratios.
- Expansion to include small-cap universes and ESG (Environmental, Social, Governance) sustainability metrics.

---

## 19. Conclusion
This project successfully demonstrates the end-to-end lifecycle of Business Intelligence in capital market analytics. By upholding strict academic honesty, resolving genuine data-quality anomalies, engineering a robust Fact-Constellation warehouse, and deploying an interactive Tableau Public dashboard, this study provides actionable operational intelligence into liquidity concentration, participant behavior, and market volatility across India's premier stock exchange.

---

## 20. Dataset Citations & Sources
1. **NSE Top 100 Stocks Historical Dataset (2010–2020)**: Extracted from National Stock Exchange of India (NSE) Bhavcopy archives; available via Kaggle Open Datasets (`rohanrao/nifty-stocks-dataset`).
2. **NSE 30 Indices Daily Dataset (1997–2025)**: Sourced from NSE Indices Limited daily historical index statistics; available via Kaggle Open Datasets (`pratikasar/nse-daily-indices-data`).

