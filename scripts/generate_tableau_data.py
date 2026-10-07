"""
scripts/generate_tableau_data.py
Creates pre-joined, optimized, Tableau Public ready datasets in data/tableau_ready/.
Enables seamless visual analytics and high performance in Tableau Public.
"""

import os
import pandas as pd
import numpy as np

def generate_tableau_files():
    print("=" * 60)
    print("GENERATING TABLEAU PUBLIC READY DATASETS (PHASE 4 & 9)")
    print("=" * 60)
    
    os.makedirs("data/tableau_ready", exist_ok=True)
    
    # 1. Load Warehouse Tables
    dim_date = pd.read_csv("data/warehouse/dim_date.csv")
    dim_stock = pd.read_csv("data/warehouse/dim_stock.csv")
    dim_index = pd.read_csv("data/warehouse/dim_index.csv")
    fact_stock = pd.read_csv("data/warehouse/fact_stock_daily.csv")
    fact_index = pd.read_csv("data/warehouse/fact_index_daily.csv")
    
    # 2. Build tableau_stock_analytics.csv
    print("\n[Tableau File 1/3] Assembling tableau_stock_analytics.csv...")
    stock_joined = fact_stock.merge(dim_date, on='Date_Key', how='inner')
    stock_joined = stock_joined.merge(dim_stock, on='Stock_Key', how='inner')
    
    tableau_stock_cols = [
        'Date', 'Year', 'Quarter', 'Month', 'Month_Name', 'Year_Month', 'Day_Name',
        'Symbol', 'Company_Name', 'Sector', 'Benchmark_Index',
        'Open', 'High', 'Low', 'Close', 'VWAP',
        'Volume', 'Turnover_INR', 'Trades',
        'Deliverable_Volume', 'Deliverable_Pct',
        'Daily_Return_Pct', 'Price_Spread',
        'Avg_Trade_Size_INR', 'Deliverable_Turnover_INR'
    ]
    df_tab_stock = stock_joined[tableau_stock_cols].sort_values(['Symbol', 'Date']).reset_index(drop=True)
    tab_stock_path = "data/tableau_ready/tableau_stock_analytics.csv"
    df_tab_stock.to_csv(tab_stock_path, index=False)
    print(f"  Created: {tab_stock_path} | Rows: {len(df_tab_stock):,} | Size: {os.path.getsize(tab_stock_path) / (1024*1024):.2f} MB")
    
    # 3. Build tableau_index_analytics.csv
    print("\n[Tableau File 2/3] Assembling tableau_index_analytics.csv...")
    index_joined = fact_index.merge(dim_date, on='Date_Key', how='inner')
    index_joined = index_joined.merge(dim_index, on='Index_Key', how='inner')
    
    tableau_index_cols = [
        'Date', 'Year', 'Quarter', 'Month', 'Month_Name', 'Year_Month',
        'Symbol', 'Index_Name', 'Index_Category',
        'Open', 'High', 'Low', 'Close', 'Volume', 'Change_Pct', 'Gap'
    ]
    df_tab_index = index_joined[tableau_index_cols].sort_values(['Symbol', 'Date']).reset_index(drop=True)
    tab_index_path = "data/tableau_ready/tableau_index_analytics.csv"
    df_tab_index.to_csv(tab_index_path, index=False)
    print(f"  Created: {tab_index_path} | Rows: {len(df_tab_index):,} | Size: {os.path.getsize(tab_index_path) / (1024*1024):.2f} MB")
    
    # 4. Build tableau_market_summary.csv (Executive Macro KPI Dataset)
    print("\n[Tableau File 3/3] Assembling tableau_market_summary.csv...")
    # Aggregate daily market-wide numbers from stock data
    daily_stock_agg = df_tab_stock.groupby('Date').agg(
        Total_Market_Turnover_INR=('Turnover_INR', 'sum'),
        Total_Market_Volume=('Volume', 'sum'),
        Total_Market_Trades=('Trades', 'sum'),
        Avg_Market_Delivery_Pct=('Deliverable_Pct', 'mean'),
        Active_Stocks_Traded=('Symbol', 'count')
    ).reset_index()
    
    # Extract NIFTY 50 benchmark daily close and return
    nifty_daily = df_tab_index[df_tab_index['Symbol'] == 'NIFTY'][['Date', 'Close', 'Change_Pct']].rename(
        columns={'Close': 'NIFTY_50_Close', 'Change_Pct': 'NIFTY_50_Change_Pct'}
    )
    
    # Extract INDIA VIX daily close
    vix_daily = df_tab_index[df_tab_index['Symbol'] == 'INDIAVIX'][['Date', 'Close']].rename(
        columns={'Close': 'INDIA_VIX_Close'}
    )
    
    # Merge daily summary
    market_summary = daily_stock_agg.merge(nifty_daily, on='Date', how='left')
    market_summary = market_summary.merge(vix_daily, on='Date', how='left')
    
    # Add calendar attributes
    market_summary = market_summary.merge(dim_date[['Date', 'Year', 'Quarter', 'Month', 'Month_Name', 'Year_Month']], on='Date', how='left')
    
    # Sort and reorder
    summary_cols = [
        'Date', 'Year', 'Quarter', 'Month', 'Month_Name', 'Year_Month',
        'Total_Market_Turnover_INR', 'Total_Market_Volume', 'Total_Market_Trades',
        'Avg_Market_Delivery_Pct', 'Active_Stocks_Traded',
        'NIFTY_50_Close', 'NIFTY_50_Change_Pct', 'INDIA_VIX_Close'
    ]
    df_tab_summary = market_summary[summary_cols].sort_values('Date').reset_index(drop=True)
    tab_summary_path = "data/tableau_ready/tableau_market_summary.csv"
    df_tab_summary.to_csv(tab_summary_path, index=False)
    print(f"  Created: {tab_summary_path} | Rows: {len(df_tab_summary):,} | Size: {os.path.getsize(tab_summary_path) / (1024*1024):.2f} MB")
    
    print("\n" + "=" * 60)
    print("ALL TABLEAU PUBLIC DATASETS GENERATED SUCCESSFULLY")
    print("=" * 60)

if __name__ == '__main__':
    generate_tableau_files()
