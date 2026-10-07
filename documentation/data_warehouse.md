# Dimensional Data Warehouse Architecture (Phase 5)

**Project**: Brokerage Intelligence: BI-Based Stock Trading & Market Activity Analytics  
**Course**: Business Intelligence (CIA-III)  

---

## 1. Data Warehouse Architectural Pattern: Fact Constellation (Galaxy Schema)

The analytical data warehouse employs a **Fact Constellation** (Galaxy) design pattern. This architecture is necessary because the two fact sources operate at distinct levels of granularity:
1. **Fact Table 1 (`FACT_STOCK_DAILY`)**: Equity grain — One row per **Individual Stock** per **Trading Day**.
2. **Fact Table 2 (`FACT_INDEX_DAILY`)**: Benchmark grain — One row per **Market/Sector Index** per **Trading Day**.

Both facts share the conformed dimension **`DIM_DATE`**, enabling cross-fact drill-across analytics (e.g., comparing stock volume against index movement on any given day).

---

## 2. Fact Table Specifications

### 2.1 `FACT_STOCK_DAILY`
* **Business Purpose**: Captures daily trading executions, price spreads, liquidity turnover, and delivery ratios for India's top 100 corporate equities.
* **Granularity**: One record per **Stock Symbol** per **Trading Day**.
* **Total Rows**: 244,637 records.
* **Primary Key**: Composite `(Date_Key, Stock_Key)`.

| Column | Role | Data Type | Formula / Description |
| :--- | :--- | :--- | :--- |
| `Date_Key` | Foreign Key | Integer | References `DIM_DATE.Date_Key` |
| `Stock_Key` | Foreign Key | Integer | References `DIM_STOCK.Stock_Key` |
| `Open` | Measure (Additive) | Decimal | Opening session price (₹) |
| `High` | Measure (Additive) | Decimal | Session high (₹) |
| `Low` | Measure (Additive) | Decimal | Session low (₹) |
| `Close` | Measure (Semi-Additive)| Decimal | Official closing price (₹) |
| `VWAP` | Measure (Semi-Additive)| Decimal | Volume-weighted average price (₹) |
| `Volume` | Measure (Fully Additive)| BigInt | Total shares traded |
| `Turnover_INR`| Measure (Fully Additive)| Decimal | Traded turnover in true INR (₹) |
| `Trades` | Measure (Fully Additive)| BigInt | Total trade executions (post-June 2011) |
| `Deliverable_Volume`| Measure (Additive)| BigInt | Shares moved to demat accounts |
| `Deliverable_Pct` | Measure (Non-Additive) | Decimal | Ratio: `Deliverable_Volume / Volume` |
| `Daily_Return_Pct` | Measure (Non-Additive) | Decimal | Session percentage price return |
| `Price_Spread` | Measure (Additive) | Decimal | Intraday spread: `High - Low` (₹) |
| `Avg_Trade_Size_INR`| Measure (Non-Additive) | Decimal | Ticket size: `Turnover_INR / Trades` (₹) |
| `Deliverable_Turnover_INR`| Measure (Additive)| Decimal | Delivery turnover: `Turnover_INR * Deliverable_Pct` (₹) |

---

### 2.2 `FACT_INDEX_DAILY`
* **Business Purpose**: Tracks daily index point benchmarks, returns, and aggregate trading activity across 30 broad-market, sectoral, and volatility indices.
* **Granularity**: One record per **Index Symbol** per **Trading Day**.
* **Total Rows**: 114,419 records.
* **Primary Key**: Composite `(Date_Key, Index_Key)`.

| Column | Role | Data Type | Description |
| :--- | :--- | :--- | :--- |
| `Date_Key` | Foreign Key | Integer | References `DIM_DATE.Date_Key` |
| `Index_Key` | Foreign Key | Integer | References `DIM_INDEX.Index_Key` |
| `Open` | Measure (Additive) | Decimal | Index opening points |
| `High` | Measure (Additive) | Decimal | Session high points |
| `Low` | Measure (Additive) | Decimal | Session low points |
| `Close` | Measure (Semi-Additive)| Decimal | Session closing benchmark level |
| `Volume` | Measure (Additive) | BigInt | Cumulative volume of constituent stocks |
| `Prev_Close` | Measure (Semi-Additive)| Decimal | Prior session close |
| `Change` | Measure (Additive) | Decimal | Point change: `Close - Prev_Close` |
| `Change_Pct` | Measure (Non-Additive) | Decimal | Daily return percentage |
| `Gap` | Attribute | String | Session opening gap (`gap up`, `gap down`) |

---

## 3. Dimension Table Specifications

### 3.1 `DIM_DATE` (Conformed Dimension)
* **Surrogate Key**: `Date_Key` (`YYYYMMDD` integer).
* **Total Rows**: 7,025 trading sessions spanning 1997 to 2025.
* **Attributes**: `Date`, `Year`, `Quarter` (`Q1-Q4`), `Month` (`1-12`), `Month_Name`, `Year_Month`, `Week` (`1-53`), `Day`, `Day_Of_Week` (`1-7`), `Day_Name`, `Is_Weekend` (`0/1`).

### 3.2 `DIM_STOCK`
* **Surrogate Key**: `Stock_Key` (Integer 1 to 100).
* **Total Rows**: 100 blue-chip companies.
* **Attributes**: `Symbol` (Ticker), `Company_Name` (Full corporate title), `Sector` (Industry classification), `Benchmark_Index` (Primary index tracking this equity).

### 3.3 `DIM_INDEX`
* **Surrogate Key**: `Index_Key` (Integer 1 to 30).
* **Total Rows**: 30 NSE indices.
* **Attributes**: `Symbol` (Index ticker), `Index_Name` (Full official title), `Index_Category` (`Broad Market Index`, `Sectoral Index`, `Volatility Index`).

### 3.4 `DIM_SECTOR`
* **Surrogate Key**: `Sector_Key` (Integer 1 to 26).
* **Total Rows**: 26 unique sectors.
* **Attributes**: `Sector` (Sector name), `Benchmark_Index` (Corresponding NSE sectoral index).
