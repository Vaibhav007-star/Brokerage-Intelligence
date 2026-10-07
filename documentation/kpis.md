# Key Performance Indicator (KPI) Design & Formulas (Phase 8)

**Project**: Brokerage Intelligence: BI-Based Stock Trading & Market Activity Analytics  
**Course**: Business Intelligence (CIA-III)  

---

## Complete KPI Dictionary

| # | KPI Name | Business Meaning | Mathematical Formula | Source Fields | Tableau Public Implementation | Business Usefulness |
| :- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Total Traded Turnover** | Gross monetary value of equities traded across the market | $\sum \text{Turnover\_INR}$ | `Turnover_INR` | `SUM([Turnover_INR])` | Measures market size and liquidity depth |
| **2** | **Total Traded Volume** | Aggregate quantity of equity shares traded | $\sum \text{Volume}$ | `Volume` | `SUM([Volume])` | Measures market participation volume |
| **3** | **Total Trade Executions** | Total number of individual trade orders matched | $\sum \text{Trades}$ | `Trades` | `SUM([Trades])` | Indicates market transaction frequency |
| **4** | **Average Daily Turnover** | Typical daily monetary transaction value | $\frac{\sum \text{Turnover\_INR}}{\text{Distinct Trading Days}}$ | `Turnover_INR`, `Date` | `SUM([Turnover_INR]) / COUNTD([Date])` | Establishes daily liquidity baseline |
| **5** | **Average Daily Volume** | Typical daily quantity of shares exchanged | $\frac{\sum \text{Volume}}{\text{Distinct Trading Days}}$ | `Volume`, `Date` | `SUM([Volume]) / COUNTD([Date])` | Benchmarks normal vs abnormal volume |
| **6** | **Deliverable Volume** | Total shares transferred to demat accounts | $\sum \text{Deliverable\_Volume}$ | `Deliverable_Volume` | `SUM([Deliverable_Volume])` | Separates genuine investment from intraday trades |
| **7** | **Delivery Percentage** | Proportion of trading resulting in actual delivery | $\frac{\sum \text{Deliverable\_Volume}}{\sum \text{Volume}} \times 100$ | `Deliverable_Volume`, `Volume` | `SUM([Deliverable_Volume]) / SUM([Volume])` | Distinguishes institutional conviction from speculation |
| **8** | **Average Trade Ticket Size** | Average monetary value per trade order | $\frac{\sum \text{Turnover\_INR}}{\sum \text{Trades}}$ | `Turnover_INR`, `Trades` | `SUM([Turnover_INR]) / SUM([Trades])` | Differentiates retail (<₹50k) vs institutional (>₹200k) participation |
| **9** | **Daily Price Return %** | Single-session percentage price movement | $\frac{\text{Close} - \text{Prev\_Close}}{\text{Prev\_Close}} \times 100$ | `Close`, `Prev Close` | `([Close] - [Prev Close]) / [Prev Close]` | Evaluates single-day capital gain/loss |
| **10**| **Cumulative Stock Return** | Multi-year capital appreciation over holding period | $\frac{\text{Close}_{\text{end}} - \text{Close}_{\text{start}}}{\text{Close}_{\text{start}}} \times 100$ | `Close` | `(ZN(SUM([Close])) - LOOKUP(ZN(SUM([Close])), FIRST())) / ABS(LOOKUP(ZN(SUM([Close])), FIRST()))` | Evaluates long-term wealth creation |
| **11**| **Turnover Market Share %** | Proportion of total exchange turnover captured by a stock | $\frac{\text{Stock Turnover}}{\text{Total Market Turnover}} \times 100$ | `Turnover_INR` | `SUM([Turnover_INR]) / TOTAL(SUM([Turnover_INR]))` | Highlights liquidity concentration risk |
| **12**| **Intraday Price Spread** | High minus Low session volatility spread | $\text{High} - \text{Low}$ | `High`, `Low` | `AVG([High] - [Low])` | Measures intraday trading range |
| **13**| **VWAP Premium / Discount** | Closing price relative to volume-weighted average | $\frac{\text{Close} - \text{VWAP}}{\text{VWAP}} \times 100$ | `Close`, `VWAP` | `(AVG([Close]) - AVG([VWAP])) / AVG([VWAP])` | Assesses execution quality and price pressure |
| **14**| **Benchmark Index Return %** | Percentage movement in benchmark index points | $\frac{\text{Close}_{\text{index}} - \text{Prev\_Close}_{\text{index}}}{\text{Prev\_Close}_{\text{index}}} \times 100$ | `Close`, `Prev_Close` | `SUM([Change]) / SUM([Prev_Close])` | Benchmarks broad market performance |
| **15**| **Market Volatility Index (VIX)** | Annualized implied volatility level from option prices | $\text{Close}_{\text{INDIAVIX}}$ | `Close` (for INDIAVIX) | `AVG(IF [Symbol] = 'INDIAVIX' THEN [Close] END)` | Measures systemic market risk and fear |
