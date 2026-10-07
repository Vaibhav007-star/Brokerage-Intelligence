"""
scripts/etl_pipeline.py
Constructs the Dimensional Data Warehouse (Fact-Constellation Star Schema).
Loads dimensions and fact tables into data/warehouse/.
"""

import os
import pandas as pd
import numpy as np

INDEX_NAMES = {
    'NIFTY': 'NIFTY 50 Benchmark',
    'NIFTYJR': 'NIFTY Next 50',
    'CNX100': 'NIFTY 100 Large Cap',
    'CNX200': 'NIFTY 200 Broad Market',
    'CNX500': 'NIFTY 500 Multicap',
    'NIFTY_TOTAL_MKT': 'NIFTY Total Market',
    'NIFTYMIDCAP50': 'NIFTY Midcap 50',
    'CNXMIDCAP': 'NIFTY Midcap 100',
    'NIFTYMIDCAP150': 'NIFTY Midcap 150',
    'NIFTYSMLCAP50': 'NIFTY Smallcap 50',
    'NIFTYSMLCAP250': 'NIFTY Smallcap 250',
    'NIFTY_LARGEMID250': 'NIFTY LargeMidcap 250',
    'NIFTY500_MULTICAP': 'NIFTY 500 Multicap 50:25:25',
    'NIFTY_MICROCAP250': 'NIFTY Microcap 250',
    'NIFTY_MID_SELECT': 'NIFTY Midcap Select',
    'CNXIT': 'NIFTY IT Sector',
    'CNXFINANCE': 'NIFTY Financial Services',
    'CNXPSUBANK': 'NIFTY PSU Bank Sector',
    'NIFTYPVTBANK': 'NIFTY Private Bank Sector',
    'NIFTYFINSRV25_50': 'NIFTY Financial Services 25/50',
    'CNXAUTO': 'NIFTY Auto Sector',
    'CNXFMCG': 'NIFTY FMCG Sector',
    'CNXPHARMA': 'NIFTY Pharma Sector',
    'NIFTY_HEALTHCARE': 'NIFTY Healthcare Index',
    'CNXMETAL': 'NIFTY Metal Sector',
    'CNXREALTY': 'NIFTY Realty Sector',
    'CNXMEDIA': 'NIFTY Media Sector',
    'NIFTY_OIL_AND_GAS': 'NIFTY Oil & Gas Sector',
    'NIFTY_CONSR_DURBL': 'NIFTY Consumer Durables Sector',
    'INDIAVIX': 'India Volatility Index (VIX)'
}

def build_data_warehouse():
    print("=" * 60)
    print("BUILDING DIMENSIONAL DATA WAREHOUSE (PHASE 5 & 6)")
    print("=" * 60)
    
    os.makedirs("data/warehouse", exist_ok=True)
    
    # 1. Load Cleaned Datasets
    print("Loading cleaned datasets...")
    df_stocks = pd.read_csv("data/cleaned/cleaned_stocks.csv")
    df_indices = pd.read_csv("data/cleaned/cleaned_indices.csv")
    
    # 2. Build DIM_DATE (Conformed Dimension)
    print("\n[DW 1/6] Building DIM_DATE...")
    dates_stocks = set(df_stocks['Date'].unique())
    dates_indices = set(df_indices['Date'].unique())
    all_dates = sorted(list(dates_stocks.union(dates_indices)))
    
    dim_date = pd.DataFrame({'Date': all_dates})
    dim_date['Date_dt'] = pd.to_datetime(dim_date['Date'])
    dim_date['Date_Key'] = dim_date['Date_dt'].dt.strftime('%Y%m%d').astype(int)
    dim_date['Year'] = dim_date['Date_dt'].dt.year
    dim_date['Quarter'] = 'Q' + dim_date['Date_dt'].dt.quarter.astype(str)
    dim_date['Month'] = dim_date['Date_dt'].dt.month
    dim_date['Month_Name'] = dim_date['Date_dt'].dt.strftime('%B')
    dim_date['Year_Month'] = dim_date['Date_dt'].dt.strftime('%Y-%m')
    dim_date['Week'] = dim_date['Date_dt'].dt.isocalendar().week.astype(int)
    dim_date['Day'] = dim_date['Date_dt'].dt.day
    dim_date['Day_Of_Week'] = dim_date['Date_dt'].dt.dayofweek + 1
    dim_date['Day_Name'] = dim_date['Date_dt'].dt.strftime('%A')
    dim_date['Is_Weekend'] = dim_date['Day_Of_Week'].isin([6, 7]).astype(int)
    dim_date = dim_date.drop(columns=['Date_dt'])
    
    # Reorder columns
    dim_date = dim_date[['Date_Key', 'Date', 'Year', 'Quarter', 'Month', 'Month_Name', 'Year_Month', 'Week', 'Day', 'Day_Of_Week', 'Day_Name', 'Is_Weekend']]
    dim_date.to_csv("data/warehouse/dim_date.csv", index=False)
    print(f"  DIM_DATE created: {len(dim_date):,} dates from {dim_date['Date'].min()} to {dim_date['Date'].max()}")
    
    # 3. Build DIM_STOCK
    print("\n[DW 2/6] Building DIM_STOCK...")
    stock_meta = df_stocks[['Symbol', 'Company_Name', 'Sector', 'Benchmark_Index']].drop_duplicates().sort_values('Symbol').reset_index(drop=True)
    stock_meta['Stock_Key'] = range(1, len(stock_meta) + 1)
    dim_stock = stock_meta[['Stock_Key', 'Symbol', 'Company_Name', 'Sector', 'Benchmark_Index']]
    dim_stock.to_csv("data/warehouse/dim_stock.csv", index=False)
    print(f"  DIM_STOCK created: {len(dim_stock)} stocks")
    
    # 4. Build DIM_INDEX
    print("\n[DW 3/6] Building DIM_INDEX...")
    idx_meta = df_indices[['Symbol', 'Index_Category']].drop_duplicates().sort_values('Symbol').reset_index(drop=True)
    idx_meta['Index_Key'] = range(1, len(idx_meta) + 1)
    idx_meta['Index_Name'] = idx_meta['Symbol'].map(INDEX_NAMES).fillna(idx_meta['Symbol'])
    dim_index = idx_meta[['Index_Key', 'Symbol', 'Index_Name', 'Index_Category']]
    dim_index.to_csv("data/warehouse/dim_index.csv", index=False)
    print(f"  DIM_INDEX created: {len(dim_index)} indices")
    
    # 5. Build DIM_SECTOR
    print("\n[DW 4/6] Building DIM_SECTOR...")
    sec_meta = df_stocks[['Sector', 'Benchmark_Index']].drop_duplicates().sort_values('Sector').reset_index(drop=True)
    sec_meta['Sector_Key'] = range(1, len(sec_meta) + 1)
    dim_sector = sec_meta[['Sector_Key', 'Sector', 'Benchmark_Index']]
    dim_sector.to_csv("data/warehouse/dim_sector.csv", index=False)
    print(f"  DIM_SECTOR created: {len(dim_sector)} unique sectors")
    
    # Date key lookup map
    date_to_key = dict(zip(dim_date['Date'], dim_date['Date_Key']))
    stock_to_key = dict(zip(dim_stock['Symbol'], dim_stock['Stock_Key']))
    index_to_key = dict(zip(dim_index['Symbol'], dim_index['Index_Key']))
    
    # 6. Build FACT_STOCK_DAILY
    print("\n[DW 5/6] Building FACT_STOCK_DAILY...")
    df_stocks['Date_Key'] = df_stocks['Date'].map(date_to_key)
    df_stocks['Stock_Key'] = df_stocks['Symbol'].map(stock_to_key)
    
    fact_stock_cols = [
        'Date_Key', 'Stock_Key',
        'Open', 'High', 'Low', 'Close', 'VWAP',
        'Volume', 'Turnover_INR', 'Trades',
        'Deliverable Volume', '%Deliverble',
        'Daily_Return_Pct', 'Price_Spread',
        'Avg_Trade_Size_INR', 'Deliverable_Turnover_INR'
    ]
    fact_stock = df_stocks[fact_stock_cols].rename(columns={
        'Deliverable Volume': 'Deliverable_Volume',
        '%Deliverble': 'Deliverable_Pct'
    })
    fact_stock.to_csv("data/warehouse/fact_stock_daily.csv", index=False)
    print(f"  FACT_STOCK_DAILY created: {len(fact_stock):,} rows | Grain: (Date_Key, Stock_Key)")
    
    # 7. Build FACT_INDEX_DAILY
    print("\n[DW 6/6] Building FACT_INDEX_DAILY...")
    df_indices['Date_Key'] = df_indices['Date'].map(date_to_key)
    df_indices['Index_Key'] = df_indices['Symbol'].map(index_to_key)
    
    fact_idx_cols = [
        'Date_Key', 'Index_Key',
        'Open', 'High', 'Low', 'Close',
        'Volume', 'Prev_Close', 'Change',
        'Change_Pct', 'Gap'
    ]
    fact_index = df_indices[fact_idx_cols]
    fact_index.to_csv("data/warehouse/fact_index_daily.csv", index=False)
    print(f"  FACT_INDEX_DAILY created: {len(fact_index):,} rows | Grain: (Date_Key, Index_Key)")
    
    print("\n" + "=" * 60)
    print("DATA WAREHOUSE GENERATION COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    build_data_warehouse()
