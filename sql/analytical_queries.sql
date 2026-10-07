-- ============================================================
-- BROKERAGE INTELLIGENCE: ANALYTICAL SQL & OLAP QUERIES
-- Academic Course: Business Intelligence (CIA-III)
-- ============================================================

-- ------------------------------------------------------------
-- 1. ROLL-UP (Temporal Aggregation: Day -> Month -> Quarter -> Year)
-- Aggregates daily trading activity up to Annual level
-- ------------------------------------------------------------
SELECT 
    d.Year,
    COUNT(DISTINCT s.Stock_Key) AS Active_Stocks,
    COUNT(DISTINCT f.Date_Key) AS Trading_Days,
    ROUND(SUM(f.Volume), 0) AS Total_Traded_Volume,
    ROUND(SUM(f.Turnover_INR) / 10000000.0, 2) AS Total_Turnover_Crores_INR,
    ROUND(SUM(f.Trades), 0) AS Total_Trade_Executions,
    ROUND(AVG(f.Deliverable_Pct) * 100, 2) AS Avg_Delivery_Percentage
FROM fact_stock_daily f
JOIN dim_date d ON f.Date_Key = d.Date_Key
JOIN dim_stock s ON f.Stock_Key = s.Stock_Key
GROUP BY d.Year
ORDER BY d.Year;

-- ------------------------------------------------------------
-- 2. DRILL-DOWN (Hierarchical: Market -> Sector -> Individual Stock)
-- Drills from high-level sector down into stock-level liquidity
-- ------------------------------------------------------------
SELECT 
    s.Sector,
    s.Symbol,
    s.Company_Name,
    ROUND(SUM(f.Turnover_INR) / 10000000.0, 2) AS Total_Turnover_Crores_INR,
    ROUND(AVG(f.Volume), 0) AS Avg_Daily_Volume,
    ROUND(AVG(f.Deliverable_Pct) * 100, 2) AS Avg_Delivery_Percentage,
    ROUND(AVG(f.Avg_Trade_Size_INR), 2) AS Avg_Trade_Ticket_Size_INR
FROM fact_stock_daily f
JOIN dim_stock s ON f.Stock_Key = s.Stock_Key
JOIN dim_date d ON f.Date_Key = d.Date_Key
WHERE d.Year = 2020
GROUP BY s.Sector, s.Symbol, s.Company_Name
ORDER BY s.Sector ASC, Total_Turnover_Crores_INR DESC;

-- ------------------------------------------------------------
-- 3. SLICE (Filtering on a Single Dimension: Sector = 'Information Technology')
-- Focuses exclusively on IT equities across the 10-year horizon
-- ------------------------------------------------------------
SELECT 
    d.Year,
    s.Symbol,
    ROUND(AVG(f.Close), 2) AS Avg_Annual_Close_INR,
    ROUND(SUM(f.Turnover_INR) / 10000000.0, 2) AS Annual_Turnover_Crores_INR,
    ROUND(AVG(f.Deliverable_Pct) * 100, 2) AS Avg_Delivery_Pct
FROM fact_stock_daily f
JOIN dim_stock s ON f.Stock_Key = s.Stock_Key
JOIN dim_date d ON f.Date_Key = d.Date_Key
WHERE s.Sector = 'Information Technology'
GROUP BY d.Year, s.Symbol
ORDER BY d.Year DESC, Annual_Turnover_Crores_INR DESC;

-- ------------------------------------------------------------
-- 4. DICE (Multi-dimensional Sub-cube: Sectors IN ('Banking', 'IT') AND Period = 'Q1 2020')
-- Evaluates trading dynamics during the Q1 2020 market crash
-- ------------------------------------------------------------
SELECT 
    d.Year_Month,
    s.Sector,
    s.Symbol,
    ROUND(SUM(f.Turnover_INR) / 10000000.0, 2) AS Monthly_Turnover_Crores_INR,
    ROUND(AVG(f.Daily_Return_Pct), 2) AS Avg_Daily_Return_Pct,
    ROUND(AVG(f.Deliverable_Pct) * 100, 2) AS Avg_Delivery_Pct
FROM fact_stock_daily f
JOIN dim_stock s ON f.Stock_Key = s.Stock_Key
JOIN dim_date d ON f.Date_Key = d.Date_Key
WHERE s.Sector IN ('Banking', 'Information Technology')
  AND d.Year = 2020 AND d.Quarter = 'Q1'
GROUP BY d.Year_Month, s.Sector, s.Symbol
ORDER BY d.Year_Month, s.Sector, Monthly_Turnover_Crores_INR DESC;

-- ------------------------------------------------------------
-- 5. TOP 10 LIQUID STOCKS BY TOTAL TURNOVER (Market Concentration KPI)
-- Identifies the primary turnover drivers in the Indian stock exchange
-- ------------------------------------------------------------
SELECT 
    s.Symbol,
    s.Company_Name,
    s.Sector,
    ROUND(SUM(f.Turnover_INR) / 10000000.0, 2) AS Cumulative_Turnover_Crores_INR,
    ROUND(SUM(f.Volume), 0) AS Cumulative_Volume,
    ROUND(AVG(f.Deliverable_Pct) * 100, 2) AS Avg_Delivery_Pct,
    ROUND(
        (SUM(f.Turnover_INR) * 100.0) / 
        (SELECT SUM(Turnover_INR) FROM fact_stock_daily), 
    2) AS Turnover_Share_Pct
FROM fact_stock_daily f
JOIN dim_stock s ON f.Stock_Key = s.Stock_Key
GROUP BY s.Symbol, s.Company_Name, s.Sector
ORDER BY Cumulative_Turnover_Crores_INR DESC
LIMIT 10;

-- ------------------------------------------------------------
-- 6. INVESTMENT CONVICTION VS SPECULATION (Delivery % Ranking)
-- Categorizes stocks by investor holding vs intraday speculation
-- ------------------------------------------------------------
SELECT 
    s.Symbol,
    s.Sector,
    ROUND(AVG(f.Deliverable_Pct) * 100, 2) AS Delivery_Percentage,
    ROUND(SUM(f.Turnover_INR) / 10000000.0, 2) AS Total_Turnover_Crores_INR,
    CASE 
        WHEN AVG(f.Deliverable_Pct) >= 0.60 THEN 'High Investment Accumulation (>60%)'
        WHEN AVG(f.Deliverable_Pct) BETWEEN 0.35 AND 0.5999 THEN 'Moderate Delivery (35%-60%)'
        ELSE 'High Speculative Intraday Churn (<35%)'
    END AS Trading_Behavior_Classification
FROM fact_stock_daily f
JOIN dim_stock s ON f.Stock_Key = s.Stock_Key
GROUP BY s.Symbol, s.Sector
ORDER BY Delivery_Percentage DESC;

-- ------------------------------------------------------------
-- 7. BENCHMARK PERFORMANCE & VOLATILITY (NIFTY 50 vs INDIA VIX)
-- Cross-fact analysis linking broad market trend with volatility
-- ------------------------------------------------------------
SELECT 
    d.Year,
    d.Quarter,
    ROUND(AVG(CASE WHEN i.Symbol = 'NIFTY' THEN fi.Close END), 2) AS Avg_NIFTY_Close,
    ROUND(AVG(CASE WHEN i.Symbol = 'INDIAVIX' THEN fi.Close END), 2) AS Avg_VIX_Volatility_Level,
    ROUND(MAX(CASE WHEN i.Symbol = 'INDIAVIX' THEN fi.High END), 2) AS Peak_VIX_Level
FROM fact_index_daily fi
JOIN dim_index i ON fi.Index_Key = i.Index_Key
JOIN dim_date d ON fi.Date_Key = d.Date_Key
WHERE i.Symbol IN ('NIFTY', 'INDIAVIX')
  AND d.Year BETWEEN 2010 AND 2020
GROUP BY d.Year, d.Quarter
ORDER BY d.Year, d.Quarter;
