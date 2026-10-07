# Star Schema & Dimensional Model Documentation (Phase 6)

**Project**: Brokerage Intelligence: BI-Based Stock Trading & Market Activity Analytics  
**Course**: Business Intelligence (CIA-III)  

---

## 1. Dimensional Architecture Diagram (Mermaid)

```mermaid
erDiagram
    DIM_DATE ||--o{ FACT_STOCK_DAILY : "contains (1:N)"
    DIM_DATE ||--o{ FACT_INDEX_DAILY : "contains (1:N)"
    DIM_STOCK ||--o{ FACT_STOCK_DAILY : "tracks (1:N)"
    DIM_INDEX ||--o{ FACT_INDEX_DAILY : "measures (1:N)"
    DIM_SECTOR ||--o{ DIM_STOCK : "classifies (1:N)"
    DIM_SECTOR ||--o{ DIM_INDEX : "maps_to (1:1)"

    DIM_DATE {
        int Date_Key PK
        date Date
        int Year
        string Quarter
        int Month
        string Month_Name
        string Year_Month
        int Week
        string Day_Name
    }

    DIM_STOCK {
        int Stock_Key PK
        string Symbol
        string Company_Name
        string Sector
        string Benchmark_Index
    }

    DIM_INDEX {
        int Index_Key PK
        string Symbol
        string Index_Name
        string Index_Category
    }

    DIM_SECTOR {
        int Sector_Key PK
        string Sector
        string Benchmark_Index
    }

    FACT_STOCK_DAILY {
        int Date_Key FK
        int Stock_Key FK
        decimal Open
        decimal High
        decimal Low
        decimal Close
        decimal VWAP
        bigint Volume
        decimal Turnover_INR
        bigint Trades
        bigint Deliverable_Volume
        decimal Deliverable_Pct
        decimal Daily_Return_Pct
        decimal Price_Spread
        decimal Avg_Trade_Size_INR
        decimal Deliverable_Turnover_INR
    }

    FACT_INDEX_DAILY {
        int Date_Key FK
        int Index_Key FK
        decimal Open
        decimal High
        decimal Low
        decimal Close
        bigint Volume
        decimal Prev_Close
        decimal Change
        decimal Change_Pct
        string Gap
    }
```

---

## 2. Relationships & Cardinality

1. **`DIM_DATE` $\rightarrow$ `FACT_STOCK_DAILY` (1 : N)**:
   - One date in `DIM_DATE` is associated with up to 100 stock records in `FACT_STOCK_DAILY` per trading day.
   - Enforced via foreign key `FACT_STOCK_DAILY.Date_Key = DIM_DATE.Date_Key`.

2. **`DIM_DATE` $\rightarrow$ `FACT_INDEX_DAILY` (1 : N)**:
   - One date in `DIM_DATE` is associated with up to 30 index records in `FACT_INDEX_DAILY`.
   - Enforced via foreign key `FACT_INDEX_DAILY.Date_Key = DIM_DATE.Date_Key`.

3. **`DIM_STOCK` $\rightarrow$ `FACT_STOCK_DAILY` (1 : N)**:
   - One stock entity in `DIM_STOCK` has ~2,668 historical trading session rows in `FACT_STOCK_DAILY`.
   - Enforced via foreign key `FACT_STOCK_DAILY.Stock_Key = DIM_STOCK.Stock_Key`.

4. **`DIM_INDEX` $\rightarrow$ `FACT_INDEX_DAILY` (1 : N)**:
   - One index entity in `DIM_INDEX` has between 2,668 and 7,000+ daily session rows in `FACT_INDEX_DAILY`.
   - Enforced via foreign key `FACT_INDEX_DAILY.Index_Key = DIM_INDEX.Index_Key`.

5. **`DIM_STOCK` $\rightarrow$ `DIM_INDEX` (Conceptual Sector Mapping)**:
   - Stocks belong to sectors that map to specific benchmark sectoral indices (e.g., `TCS` $\rightarrow$ `Information Technology` $\rightarrow$ `CNXIT`). This enables comparative alpha calculations in Tableau.

---

## 3. Grain & Measure Classification

| Table | Grain | Additive Measures | Semi-Additive Measures | Non-Additive Measures |
| :--- | :--- | :--- | :--- | :--- |
| **`FACT_STOCK_DAILY`** | Stock × Day | `Volume`, `Turnover_INR`, `Trades`, `Deliverable_Volume`, `Deliverable_Turnover_INR`, `Price_Spread` | `Close`, `Open`, `High`, `Low`, `VWAP` (meaningful via Average/Last) | `Deliverable_Pct`, `Daily_Return_Pct`, `Avg_Trade_Size_INR` |
| **`FACT_INDEX_DAILY`** | Index × Day | `Volume`, `Change` | `Close`, `Open`, `High`, `Low`, `Prev_Close` | `Change_Pct` |
