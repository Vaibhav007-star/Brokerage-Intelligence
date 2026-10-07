# Data Quality Report & Cleaning Governance (Phase 3)

**Project**: Brokerage Intelligence: BI-Based Stock Trading & Market Activity Analytics  
**Course**: Business Intelligence (CIA-III)  

---

## 1. Data Quality Assessment Dimensions

| Dimension | Assessment Scope | Raw Data Status | Resolution / Cleaning Rule | Post-ETL Status |
| :--- | :--- | :--- | :--- | :--- |
| **Completeness** | Null values across 15 stock attributes and 15 index attributes | 30,684 missing values in `Trades` (12.53%); 1 null in index `Prev_Close` | Retain pre-2011 `Trades` as NaN (historical exchange limitation); fill index inception null with `Open` | **100% compliant** |
| **Uniqueness** | Duplicate records on natural keys `(Symbol, Date)` | 264 duplicate rows across 88 stock files | Deduped on `(Date, Symbol)` keeping first valid instance | **Zero duplicates** |
| **Accuracy / Scale** | Unit scale of `Turnover` vs `Volume * VWAP` | Raw turnover scaled by $10^5$ (paise/units) | `Turnover_INR = Raw_Turnover / 100000.0` | **Exact INR values** |
| **Consistency** | Ticker symbol integrity over 10-year horizon | 106 unique symbols across 100 stock files | Reconciled 6 historical ticker changes to primary tickers | **100 unified tickers** |
| **Validity** | Price range invariants (`High >= Low`, `Close > 0`) | All prices strictly positive; zero high-low violations | Automated assertion script (`validate_data.py`) | **15/15 Tests Passed** |
| **Integrity** | Stock sector mapping to benchmark indices | Raw files lacked sector/index metadata | Comprehensive mapping of 100 stocks to authentic NSE sectors | **100% mapped** |

---

## 2. Detailed Data Cleaning Operations (WHAT, WHY, HOW)

### Operation 1: Deduplication of Identical Trading Days
- **WHAT**: Removed 264 duplicate records across 88 stock files.
- **WHY**: In raw Bhavcopy feeds, certain dates (e.g., 2011-05-06, 2011-08-09, 2011-10-24) contained identical duplicate rows. Retaining them would inflate volume and turnover aggregations by 100% on those days.
- **HOW**: Applied `df.drop_duplicates(subset=['Date', 'Symbol'], keep='first')` in `clean_data.py`.

### Operation 2: Scale Factor Correction on Turnover
- **WHAT**: Converted raw `Turnover` into true Indian Rupees (`Turnover_INR`).
- **WHY**: Raw exchange files represented turnover scaled by $10^5$. Raw `Turnover / (Volume * VWAP)` was exactly 100,000 across blue-chips. Failing to correct this would overstate turnover by a factor of 100,000.
- **HOW**: Created `Turnover_INR = df['Turnover'] / 100000.0`, while keeping `Raw_Turnover` for audit lineage.

### Operation 3: Reconciling Historical Ticker Changes
- **WHAT**: Reconciled 6 corporate ticker name changes:
  - `MUNDRAPORT` $\rightarrow$ `ADANIPORTS`
  - `BAJAUTOFIN` $\rightarrow$ `BAJFINANCE`
  - `HEROHONDA` $\rightarrow$ `HEROMOTOCO`
  - `INFOSYSTCH` $\rightarrow$ `INFY`
  - `PIRHEALTH` $\rightarrow$ `PEL`
  - `UNIPHOS` $\rightarrow$ `UPL`
- **WHY**: Without reconciliation, a single corporation's 10-year history is split into two disjoint entities, disrupting continuous time-series analytics and stock comparisons.
- **HOW**: Preserved `Raw_Symbol` and replaced `Symbol` with the current primary ticker.

### Operation 4: Standardizing Temporal Data
- **WHAT**: Converted `Date` in stocks and `DATETIME` (`%d-%m-%Y`) in indices to standard ISO-8601 `YYYY-MM-DD`.
- **WHY**: Consistent string formatting is mandatory to construct a conformed dimensional key (`Date_Key = YYYYMMDD`).
- **HOW**: `pd.to_datetime(col).dt.strftime('%Y-%m-%d')`.

---

## 3. Before vs. After Summary Statistics

| Metric | Raw Stock Data | Cleaned Stock Data | Raw Index Data | Cleaned Index Data |
| :--- | :--- | :--- | :--- | :--- |
| **Total Rows** | 244,901 | 244,637 | 114,419 | 114,419 |
| **Duplicate Keys** | 264 | 0 | 0 | 0 |
| **Distinct Tickers**| 106 | 100 | 30 | 30 |
| **Missing Prices** | 0 | 0 | 1 (Inception) | 0 (Imputed) |
| **Turnover Scale** | Scaled ($10^5$) | True INR (₹) | N/A | N/A |
| **Trades Tracked** | Null pre-June 2011 | Documented & Preserved | N/A | N/A |
| **Sector Metadata**| Absent | 100% Present | Absent | 100% Categorized |

---

## 4. Automated Validation Results

Executed via [validate_data.py](file:///c:/Projects/Brokerage%20Intelligence/scripts/validate_data.py):
- **15 / 15 Tests Passed (100.0% Pass Rate)**
- Confirmed zero duplicate keys, zero negative prices, zero high-low violations, valid delivery ratios $[0.0, 1.0]$, and 100% dimensional referential integrity.
