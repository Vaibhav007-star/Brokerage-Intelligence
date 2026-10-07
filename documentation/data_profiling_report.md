# Comprehensive Data Profiling Report (Phase 1)

**Project**: Brokerage Intelligence: BI-Based Stock Trading & Market Activity Analytics  
**Date**: October 2026  
**Environment**: Python 3.12 (.venv) / Pandas / OpenPyXL  

---

## 1. Executive Summary & Raw File Inventory

The project utilizes two real raw datasets downloaded directly from National Stock Exchange (NSE) historical archives:

| Dataset | Raw File Location | Format | Raw Files Count | Total Records | Date Range | Primary Entities |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Dataset 1: NSE Top 100 Stocks** | `data/raw/nse_top_100/` | Excel (`.xlsx`) | 100 stock files (+ 3 index files) | **244,901 rows** | 2010-01-04 to 2020-10-01 | 100 Blue-chip equities |
| **Dataset 2: NSE 30 Indices** | `data/raw/nse_30_indices/` | CSV (`.csv`) | 1 file (`NSE_Daily_indices_data.csv`) | **114,419 rows** | 1997-02-04 to 2025-05-16 | 30 Broad & Sectoral Indices |

---

## 2. Dataset 1 Detailed Inspection: NSE Top 100 Stocks

### 2.1 File Characteristics & Schema
- **Path**: `data/raw/nse_top_100/Stock_<SYMBOL>.xlsx`
- **Total Stock Files**: 100 files
- **Total Records**: 244,901 rows
- **Schema Homogeneity**: 100% of the 100 files follow the exact identical 15-column schema:

| Column Name | Raw Data Type | Inferred Type | Null Count | Null % | Description & Business Meaning |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Date` | datetime64[us] | Date | 0 | 0.00% | Trading date |
| `Symbol` | object / string | Text | 0 | 0.00% | Stock ticker symbol |
| `Series` | object / string | Text | 0 | 0.00% | Equity trading segment (all `'EQ'`) |
| `Prev Close`| float64 | Decimal Currency | 0 | 0.00% | Previous trading day closing price (₹) |
| `Open` | float64 | Decimal Currency | 0 | 0.00% | Opening traded price of the session (₹) |
| `High` | float64 | Decimal Currency | 0 | 0.00% | Highest traded price during session (₹) |
| `Low` | float64 | Decimal Currency | 0 | 0.00% | Lowest traded price during session (₹) |
| `Last` | float64 | Decimal Currency | 0 | 0.00% | Last traded price prior to closing bell (₹) |
| `Close` | float64 | Decimal Currency | 0 | 0.00% | Official daily closing price (₹) |
| `VWAP` | float64 | Decimal Currency | 0 | 0.00% | Volume Weighted Average Price (₹) |
| `Volume` | int64 | Integer | 0 | 0.00% | Total number of equity shares traded |
| `Turnover` | float64 | Scaled Currency | 0 | 0.00% | Traded value (Raw scale factor: ₹ * 10^5) |
| `Trades` | float64 | Integer | 30,684 | 12.53% | Total number of trade orders executed |
| `Deliverable Volume`| int64 | Integer | 0 | 0.00% | Shares transferred to demat accounts |
| `%Deliverble` | float64 | Decimal Ratio | 0 | 0.00% | Ratio of Deliverable Volume to Volume |

### 2.2 Key Findings in Dataset 1
1. **Symbol Inconsistency via Historical Name Changes**:
   Across the 100 stock files, **106 unique symbols** appear. Investigation revealed that 6 companies underwent official NSE ticker renaming during the 2010–2020 observation period:
   - `MUNDRAPORT` → `ADANIPORTS`
   - `BAJAUTOFIN` → `BAJFINANCE`
   - `HEROHONDA` → `HEROMOTOCO`
   - `INFOSYSTCH` → `INFY`
   - `PIRHEALTH` → `PEL`
   - `UNIPHOS` → `UPL`
   *ETL Action*: Reconcile historical symbols to the standardized primary ticker while preserving original ticker mapping in `Dim_Stock`.

2. **Exact Duplicate Records**:
   - There are **264 duplicate records** across 88 stock files.
   - Example dates: 2011-05-06, 2011-08-09, 2011-10-24. In each occurrence, identical rows were recorded twice.
   *ETL Action*: Deduplicate on `(Date, Symbol)` during extraction/cleaning.

3. **Missing Values in `Trades` Column**:
   - Exactly **30,684 records (12.53%)** have `Trades = NaN`.
   - Inspection shows these nulls are strictly clustered between `2010-01-04` and `2011-05-31`.
   - *Domain Context*: The National Stock Exchange officially began capturing and publishing the "Number of Trades" field in its Bhavcopy on **June 1, 2011**. Records prior to this date legitimately lacked trade counts.

4. **Turnover Scale Factor Discovery**:
   - Verification across multiple blue-chips (`TCS`, `INFY`, `HDFCBANK`, `ABBOTINDIA`) shows that `Turnover / (Volume * VWAP) ≈ 100,000`.
   - In raw NSE exchange files, turnover is represented in paise or scaled by 10^5.
   *ETL Action*: Rescale turnover in the ETL pipeline to true INR (`Turnover_INR = Turnover / 100000` or use `Volume * VWAP`).

---

## 3. Dataset 2 Detailed Inspection: NSE 30 Indices

### 3.1 File Characteristics & Schema
- **Path**: `data/raw/nse_30_indices/NSE_Daily_indices_data.csv`
- **Total Records**: 114,419 rows
- **Total Columns**: 15 columns
- **Date Range**: 1997-02-04 to 2025-05-16 (Over 28 years)
- **Unique Indices**: Exactly 30 indices

| Column Name | Raw Data Type | Inferred Type | Null Count | Null % | Description & Business Meaning |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `DATETIME` | object / string | Date (`%d-%m-%Y`) | 0 | 0.00% | Trading session date |
| `SYMBOL` | object / string | Text | 0 | 0.00% | Index identifier (e.g. `NIFTY`, `CNXIT`) |
| `OPEN` | float64 | Index Points | 0 | 0.00% | Index opening value |
| `HIGH` | float64 | Index Points | 0 | 0.00% | Session high value |
| `LOW` | float64 | Index Points | 0 | 0.00% | Session low value |
| `CLOSE` | float64 | Index Points | 0 | 0.00% | Official closing value |
| `VOLUME` | float64 | Integer | 0 | 0.00% | Total volume of constituent stocks |
| `PREVIOUS_CLOSE` | float64 | Index Points | 1 | 0.00% | Prior day's close (1 null on inception date) |
| `CHANGE` | float64 | Index Points | 1 | 0.00% | Day change in index points |
| `CHANGE_PERCENT` | float64 | Decimal Percentage | 1 | 0.00% | Day percentage change |
| `LOW_CLOSE` | float64 | Index Points | 0 | 0.00% | Close minus Low spread |
| `HIGH_CLOSE` | float64 | Index Points | 0 | 0.00% | Close minus High spread |
| `TOTAL` | float64 | Index Points | 0 | 0.00% | Intraday trading range (High - Low) |
| `GAP` | object / string | Categorical | 0 | 0.00% | Market opening direction (`gap up`, `gap down`)|
| `INTERVAL` | object / string | Categorical | 0 | 0.00% | Aggregation timeframe (all `'DAILY'`) |

### 3.2 30 Indices Inventory & Categorization
The 30 indices represent three distinct categories:
1. **Benchmark & Broad Market (15 Indices)**:
   - `NIFTY` (NIFTY 50), `NIFTYJR` (NIFTY Next 50), `CNX100`, `CNX200`, `CNX500`, `NIFTY_TOTAL_MKT`, `NIFTYMIDCAP50`, `CNXMIDCAP`, `NIFTYMIDCAP150`, `NIFTYSMLCAP50`, `NIFTYSMLCAP250`, `NIFTY_LARGEMID250`, `NIFTY500_MULTICAP`, `NIFTY_MICROCAP250`, `NIFTY_MID_SELECT`
2. **Sectoral Indices (14 Indices)**:
   - `CNXIT` (Information Technology)
   - `CNXFINANCE` (Financial Services)
   - `CNXPSUBANK` (Public Sector Banking)
   - `NIFTYPVTBANK` (Private Banking)
   - `NIFTYFINSRV25_50` (Financial Services 25/50)
   - `CNXAUTO` (Automotive)
   - `CNXFMCG` (Fast Moving Consumer Goods)
   - `CNXPHARMA` (Pharmaceuticals)
   - `NIFTY_HEALTHCARE` (Healthcare)
   - `CNXMETAL` (Metals & Mining)
   - `CNXREALTY` (Real Estate)
   - `CNXMEDIA` (Media & Entertainment)
   - `NIFTY_OIL_AND_GAS` (Energy, Oil & Gas)
   - `NIFTY_CONSR_DURBL` (Consumer Durables)
3. **Volatility Index (1 Index)**:
   - `INDIAVIX` (NSE Volatility Index)

---

## 4. Grain Analysis & Dataset Relationships

| Dataset | Granularity (Grain) | Natural Primary Key | Temporal Alignment |
| :--- | :--- | :--- | :--- |
| **NSE Top 100 Stocks** | One record per **Stock Symbol per Trading Day** | `(Symbol, Date)` | 2010-01-04 to 2020-10-01 (2,668 trading days) |
| **NSE 30 Indices** | One record per **Index Symbol per Trading Day** | `(SYMBOL, DATETIME)` | 1997-02-04 to 2025-05-16 (Overlapping: 2010–2020) |

### Integration Feasibility:
- **Shared Temporal Dimension**: Both datasets share the exact daily trading calendar (`Date` = `DATETIME`).
- **Different Analytical Grain**: Stocks are at the equity level, whereas indices are aggregate market/sector benchmarks.
- **Architectural Solution**: A **Fact-Constellation (Galaxy) Schema** where both `Fact_Stock_Daily` and `Fact_Index_Daily` share a conformed `Dim_Date` dimension. Additionally, stocks link to sectors which map to the corresponding sectoral indices for alpha and benchmark comparison.
