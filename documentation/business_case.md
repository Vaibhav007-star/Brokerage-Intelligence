# Business Case: Brokerage Intelligence — Stock Trading & Market Activity Analytics

**Academic Course**: Business Intelligence (CIA-III)  
**Project Title**: Brokerage Intelligence: BI-Based Stock Trading & Market Activity Analytics  
**Primary Platform**: Tableau Public (Visual Analytics & Dashboards) with Python/SQL (Data Engineering & ETL)  

---

## 1. Business Problem
Institutional brokerages, trading desks, and retail market analysts face immense challenges in evaluating market liquidity, participant engagement, and trading velocity across Indian capital markets. While raw market trade feeds (Bhavcopy) provide millions of daily transactions, financial decision-makers lack unified visual intelligence to:
- Quickly identify which market segments and individual stocks command the highest liquidity (trading volume, turnover, and trade counts).
- Monitor shifts in deliverable volume (genuine investment accumulation vs. speculative intraday churn).
- Benchmark individual stock performance and trading activity against broad market and sectoral indices (e.g., NIFTY 50, NIFTY IT, NIFTY Bank).
- Detect market-wide liquidity anomalies and structural volatility regimes across multi-year cycles.

Without a structured Business Intelligence (BI) layer, brokerage management and market researchers are overwhelmed by isolated, disparate tabular data feeds.

---

## 2. Business Background
The National Stock Exchange of India (NSE) is one of the world's largest derivative and equity exchanges by volume. Market participants generate vast quantities of daily summary data across two distinct levels:
1. **Stock-Level Trading Activity**: Daily performance of blue-chip and high-conviction equities (the NIFTY Top 100 universe), capturing metrics such as Open, High, Low, Close, Volume, Turnover, Number of Trades, Deliverable Volume, and % Deliverable.
2. **Index-Level Market Benchmarks**: Daily aggregate performance across broad-market indices (NIFTY 50, NIFTY Next 50, NIFTY 500) and specialized sectoral indices (Banking, IT, FMCG, Auto, Metals, Pharma, Energy).

A modern brokerage requires a dimensional data warehouse and interactive analytical dashboards to transform these historical trade logs into actionable decision support.

---

## 3. Project Objectives
1. Profile and audit real historical market data from the NSE Top 100 stocks and NSE 30 Indices.
2. Build an automated, reproducible Python ETL pipeline to standardize schemas, handle duplicates, correct scale factors, and prepare warehouse-grade datasets.
3. Design an enterprise-grade dimensional data warehouse (Star Schema / Fact-Constellation) optimized for trading analytics.
4. Support multidimensional OLAP operations (Roll-up, Drill-down, Slice, Dice) across Temporal, Equity, Sectoral, and Benchmark hierarchies.
5. Engineer essential trading KPIs including Liquidity Ratios, Delivery Percentages, Daily Returns, and Turnover Concentration.
6. Build and publish an interactive, executive-grade Tableau Public dashboard for decision support.

---

## 4. BI Objectives
- **Centralized Data Repository**: Unify 100 stock daily records (~244,000+ rows) and 30 market indices into clean, relational analytical tables.
- **Multidimensional Analysis**: Enable slicing by Sector, Market Capitalization tier, Liquidity buckets, and Calendar hierarchies (Year, Quarter, Month, Day).
- **Benchmarking & Alpha Visualization**: Compare stock-specific trading velocity and price movements directly against benchmark indices.
- **Self-Service Interactivity**: Empower brokerage managers to filter, highlight, and drill down from exchange-wide turnover into specific stock and date details within Tableau Public.

---

## 5. Stakeholders
- **Head of Institutional / Retail Brokerage**: Monitors trading volume trends and market liquidity to optimize execution algorithms and liquidity provisioning.
- **Equity Research Analysts**: Evaluates delivery volume patterns to distinguish institutional accumulation from speculative retail churn.
- **Risk & Compliance Officers**: Analyzes market volatility regimes (e.g., INDIAVIX trends, gap openings, price swings) to calibrate margin requirements.
- **Academic Evaluators (Faculty)**: Assesses the rigor of data modeling, dimensional design, KPI formulations, and Tableau Public visual delivery for CIA-III.

---

## 6. Business Questions
1. **Liquidity Concentration**: Which top 10 stocks account for the majority of total exchange turnover and trading volume?
2. **Trading Velocity vs. Investment Conviction**: Which equities demonstrate high delivery percentages (>60%) indicating long-term investment, versus low delivery percentages (<20%) indicating intraday speculation?
3. **Sectoral Divergence**: How do trading volumes and turnover distribute across sectors (IT, Banking, Energy, FMCG, Pharma) during market bull and bear cycles?
4. **Market Shocks & Volatility Regimes**: How did market-wide trading turnover and transaction counts behave during structural market events (e.g., March 2020 COVID shock, 2016 demonetization)?
5. **Benchmark Comparison**: Did top-volume stocks outperform or underperform the benchmark NIFTY 50 index over multi-year holding periods?
6. **Average Trade Size Dynamics**: What is the average value per trade across different stocks, and how does institutional participation correlate with stock market cap?

---

## 7. Scope
- Real historical daily trading data for NSE Top 100 stocks spanning over 10 years (2010 to 2020).
- Real daily data for 30 NSE indices spanning broad-market, sectoral, and volatility benchmarks.
- Rigorous data profiling, quality audit, ETL pipeline implementation, and Star Schema modeling.
- Comprehensive OLAP design and KPI definitions.
- Visual dashboard design, calculation engineering, and deployment exclusively on Tableau Public.
- Comprehensive CIA-III academic documentation.

---

## 8. Out-of-Scope
- **Predictive Machine Learning**: No algorithmic forecasting, ARIMA/LSTM price predictions, or buy/sell recommendations (this is strictly a Business Intelligence project).
- **Intraday Tick-Level High-Frequency Trading (HFT)**: Analysis is conducted at daily Bhavcopy grain, not millisecond tick level.
- **Synthetic Data Generation**: No fictional clients, fake account balances, or fabricated trades.
- **Web App / Alternative BI Tools**: No Power BI, Streamlit, or custom web dashboards. Tableau Public is the mandated visual analytics platform.

---

## 9. Expected Benefits
- **Operational Clarity**: High-level visibility into liquidity distribution across India's largest corporate equities.
- **Analytical Speed**: Elimination of ad-hoc spreadsheet manipulation through a unified, optimized star schema data model.
- **Academic Rigor**: Complete demonstration of end-to-end BI lifecycle adhering strictly to academic honesty and real data characteristics.

---

## 10. Proposed BI Architecture

```
[ RAW DATA SOURCES ]
  - NSE Top 100 Stocks (100 .xlsx files, 244,901 rows)
  - NSE 30 Indices (1 .csv file, 114,419 rows)
          │
          ▼
[ DATA PROFILING & QUALITY LAYER (Python) ]
  - Audit schemas, handle duplicates, reconcile ticker changes
  - Correct turnover unit scale (10^5 adjustment)
  - Validate date formats & verify historical trade tracking
          │
          ▼
[ ETL & WAREHOUSE TRANSFORMATION LAYER (Python / Pandas / SQL) ]
  - Conformed Date Dimension (Dim_Date)
  - Conformed Stock Dimension (Dim_Stock)
  - Conformed Index Dimension (Dim_Index)
  - Fact_Stock_Daily (Grain: Stock Symbol + Date)
  - Fact_Index_Daily (Grain: Index Symbol + Date)
          │
          ▼
[ MULTIDIMENSIONAL OLAP & KPI LAYER ]
  - Hierarchies: Time (Year-Quarter-Month-Day), Sector-Stock
  - Operations: Roll-up, Drill-down, Slice, Dice
  - Core KPIs: Turnover, Volume, Delivery %, Daily Return, VWAP Gap
          │
          ▼
[ TABLEAU PUBLIC PRESENTATION LAYER ]
  - Executive Market Overview Dashboard
  - Stock Trading & Liquidity Deep-Dive Dashboard
  - Sectoral & Benchmark Comparison Dashboard
```
