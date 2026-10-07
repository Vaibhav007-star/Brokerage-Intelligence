# Multidimensional OLAP Analysis & Operations (Phase 7)

**Project**: Brokerage Intelligence: BI-Based Stock Trading & Market Activity Analytics  
**Course**: Business Intelligence (CIA-III)  

---

## 1. Multidimensional OLAP Dimensions & Hierarchies

The dimensional warehouse supports two core hierarchies:

### Hierarchy 1: Temporal Dimension (`DIM_DATE`)
$$\text{Calendar Year} \longrightarrow \text{Calendar Quarter} \longrightarrow \text{Month} \longrightarrow \text{Trading Day}$$

### Hierarchy 2: Equity & Market Structure Dimension (`DIM_STOCK`)
$$\text{Market Universe (Top 100)} \longrightarrow \text{Sector / Industry} \longrightarrow \text{Stock Ticker (Company)}$$

### Hierarchy 3: Benchmark Index Dimension (`DIM_INDEX`)
$$\text{Index Category (Broad / Sectoral / Volatility)} \longrightarrow \text{Specific Benchmark Index}$$

---

## 2. Core OLAP Operations Demonstrated

### 2.1 ROLL-UP (Aggregation to Higher Level)
* **Concept**: Summarizing fine-grained daily trading metrics up to broader temporal or sector levels.
* **SQL Realization**:
  ```sql
  SELECT d.Year, SUM(f.Turnover_INR) / 1e7 AS Turnover_Crores
  FROM fact_stock_daily f
  JOIN dim_date d ON f.Date_Key = d.Date_Key
  GROUP BY d.Year;
  ```
* **Tableau Public Demonstration**: Collapsing the `Date` field hierarchy from `Day` to `Year` or `Quarter` on the Columns shelf, aggregating total exchange volume automatically.

---

### 2.2 DRILL-DOWN (De-aggregation to Finer Detail)
* **Concept**: Navigating from high-level sector totals down to individual stock liquidity and specific trading days.
* **SQL Realization**:
  ```sql
  SELECT s.Sector, s.Symbol, SUM(f.Turnover_INR) / 1e7 AS Turnover_Crores
  FROM fact_stock_daily f
  JOIN dim_stock s ON f.Stock_Key = s.Stock_Key
  GROUP BY s.Sector, s.Symbol;
  ```
* **Tableau Public Demonstration**: Clicking the `+` icon on `Sector` in the Rows shelf to expand the view to `Symbol`, or clicking an interactive Sector bar chart to filter a child stock-level scatter plot.

---

### 2.3 SLICE (Selecting a Single Dimension Value)
* **Concept**: Filtering a multi-dimensional data cube along a single dimension slice (e.g., examining only the `Banking` sector or only the year `2020`).
* **SQL Realization**:
  ```sql
  SELECT d.Date, f.Close, f.Volume
  FROM fact_stock_daily f
  JOIN dim_stock s ON f.Stock_Key = s.Stock_Key
  WHERE s.Symbol = 'RELIANCE';
  ```
* **Tableau Public Demonstration**: Utilizing a Tableau dropdown filter on `Sector` or `Symbol` to isolate a single slice of market data.

---

### 2.4 DICE (Sub-cube Extraction Across Multiple Dimensions)
* **Concept**: Selecting a sub-cube by applying multiple dimensional constraints simultaneously (e.g., `Sector IN ('Banking', 'IT')` AND `Year = 2020` AND `Delivery % >= 0.50`).
* **SQL Realization**:
  ```sql
  SELECT d.Year_Month, s.Sector, SUM(f.Turnover_INR) / 1e7 AS Turnover_Crores
  FROM fact_stock_daily f
  JOIN dim_stock s ON f.Stock_Key = s.Stock_Key
  JOIN dim_date d ON f.Date_Key = d.Date_Key
  WHERE s.Sector IN ('Banking', 'Information Technology')
    AND d.Year = 2020
  GROUP BY d.Year_Month, s.Sector;
  ```
* **Tableau Public Demonstration**: Applying coordinated filters in Tableau Public (e.g., Year slider + Sector checkbox + Delivery % range filter) to observe targeted market behavior.

---

### 2.5 PIVOT (Cross-Tabular Rotation)
* **Concept**: Rotating axes to present Sectors as Rows and Years as Columns with Average Delivery % or Turnover as values.
* **Tableau Public Demonstration**: Matrix heatmap with `Sector` on Rows, `Year` on Columns, and `AVG(Deliverable_Pct)` encoded via color gradient.
