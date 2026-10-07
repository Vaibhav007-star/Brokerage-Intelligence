# Brokerage Intelligence: BI-Based Stock Trading & Market Activity Analytics

**Academic Course**: Business Intelligence (CIA-III)  
**Primary Analytical Platform**: Tableau Public (Visual Analytics)  
**Data Engineering Stack**: Python 3.12 (.venv), Pandas, NumPy, OpenPyXL, SQLite / SQL  

---

## 1. Project Directory Structure

```
c:\Projects\Brokerage Intelligence\
│
├── archive (1).zip                    # Original raw backup archive (NSE Top 100 Stocks)
├── archive (2).zip                    # Original raw backup archive (NSE 30 Indices)
│
├── data/
│   ├── raw/
│   │   ├── nse_top_100/               # 100 raw Stock_*.xlsx files + 3 Index_*.xlsx files
│   │   └── nse_30_indices/            # NSE_Daily_indices_data.csv (114,419 rows)
│   ├── cleaned/
│   │   ├── cleaned_stocks.csv         # Cleaned stocks (244,637 rows, deduped, rescaled)
│   │   └── cleaned_indices.csv        # Cleaned indices (114,419 rows, categorized)
│   ├── warehouse/
│   │   ├── dim_date.csv               # Conformed date dimension (7,025 calendar days)
│   │   ├── dim_stock.csv              # 100 equity entities with sector & benchmark mapping
│   │   ├── dim_index.csv              # 30 NSE indices categorized
│   │   ├── dim_sector.csv             # 26 unique sectors
│   │   ├── fact_stock_daily.csv       # 244,637 rows | Grain: Stock x Day
│   │   └── fact_index_daily.csv       # 114,419 rows | Grain: Index x Day
│   └── tableau_ready/
│       ├── tableau_stock_analytics.csv    # 49.4 MB | Primary stock visual analytics source
│       ├── tableau_index_analytics.csv    # 14.5 MB | Index benchmark source
│       └── tableau_market_summary.csv     # 0.28 MB | Daily executive macro summary
│
├── scripts/
│   ├── profile_data.py                # Phase 1: Comprehensive data profiling script
│   ├── clean_data.py                  # Phase 3: Raw data extraction, cleaning & scaling
│   ├── validate_data.py               # Phase 3: Automated assertion test suite (15/15 Passed)
│   ├── etl_pipeline.py                # Phase 4/5: Star schema / constellation builder
│   └── generate_tableau_data.py       # Phase 4/9: Tableau Public extract generator
│
├── sql/
│   └── analytical_queries.sql         # Phase 7: OLAP operations (Roll-up, Drill-down, Slice, Dice)
│
├── documentation/
│   ├── business_case.md               # Phase 0: Complete business case & BI objectives
│   ├── data_profiling_report.md       # Phase 1: Deep technical profiling report
│   ├── data_quality.md                # Phase 3: Data quality report & cleaning rules
│   ├── etl.md                         # Phase 4: ETL pipeline architecture documentation
│   ├── data_warehouse.md              # Phase 5: Dimensional warehouse architecture
│   ├── star_schema.md                 # Phase 6: Star schema / constellation ER diagram
│   ├── olap.md                        # Phase 7: OLAP operations & dimensional hierarchies
│   ├── kpis.md                        # Phase 8: Complete 15-KPI dictionary & formulas
│   ├── tableau_calculated_fields.md   # Phase 10: Exact calculated fields for Tableau Public
│   ├── business_insights.md           # Phase 12: Empirical data-backed insights & recommendations
│   ├── cia_iii_final_report.md        # Phase 13: Full 20-section academic CIA-III report
│   └── viva_preparation_guide.md      # Phase 14: Comprehensive viva voce questions & model answers
│
├── tableau/
│   └── tableau_build_guide.md         # Phase 9/11: Step-by-step Tableau Public assembly guide
│
└── README.md
```

---

## 2. Quickstart & Pipeline Execution

To reproduce the entire data engineering and warehouse pipeline from scratch:

```powershell
# 1. Activate the Python virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Run Data Profiling (Phase 1)
python scripts/profile_data.py

# 3. Clean and Transform Data (Phase 3)
python scripts/clean_data.py

# 4. Run Automated Data Quality Tests (Phase 3)
python scripts/validate_data.py

# 5. Build Dimensional Data Warehouse (Phase 5 & 6)
python scripts/etl_pipeline.py

# 6. Generate Tableau Public Ready Datasets (Phase 4 & 9)
python scripts/generate_tableau_data.py
```

---

## 3. Academic Integrity & Dataset Sources

1. **NSE Top 100 Stocks Dataset (2010–2020)**: Real historical Bhavcopy files from the National Stock Exchange of India. Sourced via Kaggle Open Datasets (`rohanrao/nifty-stocks-dataset`).
2. **NSE 30 Indices Daily Dataset (1997–2025)**: Real historical daily index statistics from NSE Indices Limited. Sourced via Kaggle Open Datasets (`pratikasar/nse-daily-indices-data`).
3. **No Synthetic Data**: No synthetic records, client accounts, or fictional brokerage trades were created. All metrics are derived from real market data.

