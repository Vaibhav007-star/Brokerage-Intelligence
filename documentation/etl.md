# ETL Pipeline Architecture & Technical Documentation (Phase 4)

**Project**: Brokerage Intelligence: BI-Based Stock Trading & Market Activity Analytics  
**Course**: Business Intelligence (CIA-III)  

---

## 1. ETL Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────────┐
│                          EXTRACT PHASE (E)                             │
├──────────────────────────────────┬─────────────────────────────────────┤
│  Dataset 1: NSE Top 100 Stocks   │  Dataset 2: NSE 30 Indices          │
│  - 100 Excel (.xlsx) files       │  - 1 CSV file                       │
│  - 244,901 rows                  │  - 114,419 rows                     │
└─────────────────┬────────────────┴──────────────────┬──────────────────┘
                  │                                   │
                  ▼                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        TRANSFORM PHASE (T)                             │
├──────────────────────────────────┬─────────────────────────────────────┤
│  Stock Transformations:          │  Index Transformations:             │
│  1. ISO Date Standardization     │  1. Format Parsing (%d-%m-%Y)       │
│  2. Deduplication (Date, Symbol) │  2. Inception Null Imputation       │
│  3. Ticker Reconciliation        │  3. Category Classification         │
│  4. Turnover Rescaling (÷ 10^5)  │     (Broad, Sectoral, Volatility)   │
│  5. Derived KPI Formulations     │  4. Standardized Column Naming      │
│  6. Master Dimension Enrichment  │                                     │
└─────────────────┬────────────────┴──────────────────┬──────────────────┘
                  │                                   │
                  ▼                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         VALIDATE PHASE (V)                             │
│  Automated Assertion Engine (scripts/validate_data.py)                 │
│  - 15 Validation Rules (Keys, Logic, Integrity, Bounds)                │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                          LOAD PHASE (L)                                │
├──────────────────────────────────┬─────────────────────────────────────┤
│  Dimensional Data Warehouse:     │  Tableau Public Optimized Extracts: │
│  - dim_date.csv (7,025 rows)     │  - tableau_stock_analytics.csv      │
│  - dim_stock.csv (100 rows)      │  - tableau_index_analytics.csv      │
│  - dim_index.csv (30 rows)       │  - tableau_market_summary.csv       │
│  - dim_sector.csv (26 rows)      │                                     │
│  - fact_stock_daily.csv (244K)   │                                     │
│  - fact_index_daily.csv (114K)   │                                     │
└──────────────────────────────────┴─────────────────────────────────────┘
```

---

## 2. Reusable ETL Scripts Directory

| Script Name | Purpose | Execution Command | Output Artifacts |
| :--- | :--- | :--- | :--- |
| `scripts/clean_data.py` | Raw data extraction, schema normalization, scale correction, deduplication | `python scripts/clean_data.py` | `data/cleaned/cleaned_stocks.csv`<br>`data/cleaned/cleaned_indices.csv` |
| `scripts/validate_data.py` | Automated data-quality audit with 15 assertion tests | `python scripts/validate_data.py` | Console Test Report (100% Pass) |
| `scripts/etl_pipeline.py` | Surrogate key generation and dimensional table loading | `python scripts/etl_pipeline.py` | `data/warehouse/*.csv` (6 tables) |
| `scripts/generate_tableau_data.py` | Generates flat, denormalized extracts optimized for Tableau Public | `python scripts/generate_tableau_data.py` | `data/tableau_ready/*.csv` (3 files) |

---

## 3. Transformation Rules & Derivation Logic

### 3.1 Date Standardization
$$\text{Date\_Key} = \text{CAST}(\text{FORMAT}(\text{Date}, \text{'YYYYMMDD'}) \text{ AS INT})$$
Example: `2020-03-23` becomes `20200323`.

### 3.2 Turnover Rescaling
$$\text{Turnover\_INR} = \frac{\text{Raw\_Turnover}}{100,000}$$

### 3.3 Daily Return Percentage
$$\text{Daily\_Return\_Pct} = \left( \frac{\text{Close} - \text{Prev\_Close}}{\text{Prev\_Close}} \right) \times 100$$

### 3.4 Deliverable Turnover
$$\text{Deliverable\_Turnover\_INR} = \text{Turnover\_INR} \times \text{Deliverable\_Pct}$$

### 3.5 Average Trade Ticket Size
$$\text{Avg\_Trade\_Size\_INR} = \begin{cases} \frac{\text{Turnover\_INR}}{\text{Trades}}, & \text{if } \text{Trades} > 0 \\ \text{NULL}, & \text{otherwise} \end{cases}$$
