# Comprehensive Viva Voce Preparation Guide (Phase 14)

**Project**: Brokerage Intelligence: BI-Based Stock Trading & Market Activity Analytics  
**Course**: Business Intelligence (CIA-III)  

---

## Section 1: Data Architecture & Dimensional Modeling

### Q1: Why did you design a Fact-Constellation (Galaxy) Schema instead of a single Star Schema?
**Answer**:
"A single star schema requires all facts to share the exact same grain. In our project, we have two distinct real-world data sources that operate at fundamentally different grains:
1. **`FACT_STOCK_DAILY`**: Grain is **one record per Stock Symbol per Trading Day** (244,637 rows).
2. **`FACT_INDEX_DAILY`**: Grain is **one record per Index Symbol per Trading Day** (114,419 rows).

If we attempted to force both into a single flat fact table, we would either create massive null redundancy (since indices do not have individual stock metrics like Deliverable Volume or Trades) or create invalid Cartesian joins. Therefore, the textbook-correct BI solution is a **Fact Constellation (Galaxy Schema)**, where both facts share a conformed date dimension (`DIM_DATE`)."

---

### Q2: What is a Conformed Dimension, and how is it used in your project?
**Answer**:
"A conformed dimension is a dimension table that has the exact same meaning, primary key, and attributes across multiple fact tables in a data warehouse. In our project, **`DIM_DATE`** is a conformed dimension. Both `FACT_STOCK_DAILY` and `FACT_INDEX_DAILY` connect to `DIM_DATE` via `Date_Key`. This enables **drill-across** operations—for example, comparing the daily turnover of RELIANCE directly against the closing value of the NIFTY 50 index on that same date."

---

### Q3: What are Additive, Semi-Additive, and Non-Additive measures in your Fact Tables?
**Answer**:
"In `FACT_STOCK_DAILY`:
* **Fully Additive Measures**: Can be summed across all dimensions (Time, Stock, Sector). Examples: `Volume`, `Turnover_INR`, and `Trades`.
* **Semi-Additive Measures**: Can be summed across some dimensions (like Stock or Sector), but cannot be summed across Time. Examples: `Close`, `Open`, `High`, `Low`, and `VWAP`. A stock's closing price cannot be added across Monday and Tuesday; it must be evaluated using an Average or Closing snapshot.
* **Non-Additive Measures**: Cannot be meaningfully added across any dimension; they must be computed using ratios. Examples: `Deliverable_Pct` ($\sum \text{Deliverable Volume} / \sum \text{Volume}$) and `Daily_Return_Pct`."

---

## Section 2: Data Quality & Technical ETL

### Q4: What major data-quality issues did you discover, and how did you resolve them?
**Answer**:
"We performed an exhaustive data audit and discovered four critical issues:
1. **Turnover Scale Factor**: In raw exchange files, `Turnover` was scaled by $10^5$ relative to `Volume * VWAP`. We rescaled it in our ETL pipeline: `Turnover_INR = Raw_Turnover / 100000.0`.
2. **Deduplication**: We detected 264 duplicate rows on identical dates across 88 stock files and eliminated them.
3. **Historical Ticker Changes**: 6 companies changed tickers on the NSE during 2010–2020 (e.g., `MUNDRAPORT` $\rightarrow$ `ADANIPORTS`, `INFOSYSTCH` $\rightarrow$ `INFY`, `HEROHONDA` $\rightarrow$ `HEROMOTOCO`). We mapped them to current primary tickers while maintaining original ticker lineage.
4. **Missing Values in `Trades`**: 30,684 records (12.53%) were missing trade counts. We investigated and discovered that the NSE only began publishing trade counts in Bhavcopy files on **June 1, 2011**. We preserved this structural historical reality."

---

### Q5: How did you ensure academic integrity regarding real vs. synthetic data?
**Answer**:
"We adhered strictly to academic honesty:
- We did not generate any synthetic clients, fake account numbers, or fictional brokerage commissions.
- We relied exclusively on real, audited National Stock Exchange historical trade logs.
- We clearly distinguished between **Real Raw Data** (Bhavcopy prices, volumes, deliverable volumes) and **Derived Metrics** (Turnover in Crores, Daily Return %, Average Trade Ticket Size, Delivery Conviction Buckets)."

---

## Section 3: Multidimensional OLAP Operations

### Q6: Demonstrate the 5 core OLAP operations in your project.
**Answer**:
1. **Roll-up**: Aggregating from Day $\rightarrow$ Month $\rightarrow$ Year. Shows annual turnover growing from ₹15.82 Lakh Cr (2010) to ₹69.15 Lakh Cr (2020).
2. **Drill-down**: De-aggregating from Total Market $\rightarrow$ Sector (Banking) $\rightarrow$ Stock (`HDFCBANK`) $\rightarrow$ Daily trading sessions.
3. **Slice**: Selecting a single dimension slice, such as analyzing only the `Information Technology` sector across the 10-year period.
4. **Dice**: Selecting a sub-cube with multiple dimensional constraints, such as `Sectors IN ('Banking', 'IT')` during `Quarter = 'Q1 2020'`.
5. **Pivot**: Rotating axes in a cross-tabular view to display Sectors as rows, Years as columns, and Average Delivery % as values."

---

## Section 4: Tableau Public & Analytical Delivery

### Q7: Why was Tableau Public chosen as the visualization platform?
**Answer**:
"Tableau Public is the industry benchmark for visual analytics and self-service BI. It allows us to:
- Publish an interactive, publicly accessible dashboard for academic evaluation without requiring licensed desktop software for evaluators.
- Utilize intuitive Level of Detail (LOD) and Table Calculations.
- Provide fluid interactive filtering, parameter-based Top N ranking, and dual-axis time-series visualizations."

---

### Q8: What are the primary business insights discovered from the dashboard?
**Answer**:
"Three primary empirical findings stand out:
1. **Liquidity Concentration**: Market turnover is heavily concentrated; the top 10 stocks capture 36.5% of total exchange turnover (led by RELIANCE at 5.66% and SBIN at 4.76%).
2. **The Intraday Shift**: Delivery percentage declined steadily from 53.1% in 2010 to 35.4% in 2020, while total volume expanded five-fold, proving a structural transition toward algorithmic intraday trading.
3. **Sectoral Conviction**: Defensive sectors like FMCG and Pharma maintain high delivery rates (>60%), indicating long-term institutional investment, whereas high-beta Financials and Metals act as speculative trading instruments with delivery rates below 35%."

