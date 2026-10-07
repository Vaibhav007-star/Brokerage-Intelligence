"""
scripts/validate_data.py
Performs automated data quality tests and assertions on cleaned datasets.
Provides Phase 3 automated validation results.
"""

import pandas as pd
import numpy as np

def run_validations():
    print("=" * 60)
    print("DATA QUALITY VALIDATION SUITE (PHASE 3)")
    print("=" * 60)
    
    # 1. Load Cleaned Datasets
    stocks_path = "data/cleaned/cleaned_stocks.csv"
    indices_path = "data/cleaned/cleaned_indices.csv"
    
    print(f"Loading cleaned stocks from: {stocks_path}")
    df_s = pd.read_csv(stocks_path)
    print(f"Loading cleaned indices from: {indices_path}")
    df_i = pd.read_csv(indices_path)
    
    passed_tests = 0
    total_tests = 0
    
    def test_assertion(name, condition, details=""):
        nonlocal passed_tests, total_tests
        total_tests += 1
        status = "PASSED" if condition else "FAILED"
        if condition:
            passed_tests += 1
            print(f"  [PASS] {name} {details}")
        else:
            print(f"  [FAIL] {name} - Details: {details}")
            
    print("\n--- 1. Uniqueness & Primary Key Tests ---")
    stock_dups = df_s.duplicated(subset=['Date', 'Symbol']).sum()
    test_assertion("Stock Natural Key (Date, Symbol) Uniqueness", stock_dups == 0, f"(Duplicates found: {stock_dups})")
    
    idx_dups = df_i.duplicated(subset=['Date', 'Symbol']).sum()
    test_assertion("Index Natural Key (Date, Symbol) Uniqueness", idx_dups == 0, f"(Duplicates found: {idx_dups})")
    
    print("\n--- 2. Date Integrity Tests ---")
    df_s['Date_dt'] = pd.to_datetime(df_s['Date'], errors='coerce')
    stock_bad_dates = df_s['Date_dt'].isnull().sum()
    test_assertion("Stock Date Parsing Valid", stock_bad_dates == 0, f"(Invalid dates: {stock_bad_dates})")
    
    df_i['Date_dt'] = pd.to_datetime(df_i['Date'], errors='coerce')
    idx_bad_dates = df_i['Date_dt'].isnull().sum()
    test_assertion("Index Date Parsing Valid", idx_bad_dates == 0, f"(Invalid dates: {idx_bad_dates})")
    
    stock_min, stock_max = df_s['Date_dt'].min(), df_s['Date_dt'].max()
    test_assertion("Stock Date Range Expected (2010 to 2020)", (stock_min.year == 2010 and stock_max.year == 2020), f"({stock_min.strftime('%Y-%m-%d')} to {stock_max.strftime('%Y-%m-%d')})")
    
    print("\n--- 3. Numerical Validity & Price Logic Tests ---")
    neg_prices = (df_s[['Open', 'High', 'Low', 'Close', 'VWAP']] <= 0).sum().sum()
    test_assertion("Stock Prices Strictly Positive", neg_prices == 0, f"(Negative or zero prices: {neg_prices})")
    
    # High >= Low
    high_low_violations = (df_s['High'] < df_s['Low']).sum()
    test_assertion("Stock High >= Low Invariant", high_low_violations == 0, f"(Violations: {high_low_violations})")
    
    # Non-negative volume and turnover
    neg_volume = (df_s['Volume'] < 0).sum()
    test_assertion("Stock Volume Non-Negative", neg_volume == 0, f"(Negative volumes: {neg_volume})")
    
    neg_turnover = (df_s['Turnover_INR'] < 0).sum()
    test_assertion("Stock Turnover (INR) Non-Negative", neg_turnover == 0, f"(Negative turnovers: {neg_turnover})")
    
    # Delivery percentage between 0 and 1 (with tiny floating point tolerance)
    deliv_pct_violations = ((df_s['%Deliverble'] < 0.0) | (df_s['%Deliverble'] > 1.0001)).sum()
    test_assertion("Deliverable % within Valid Range [0.0, 1.0]", deliv_pct_violations == 0, f"(Violations: {deliv_pct_violations})")
    
    print("\n--- 4. Dimensional Integrity & Mapping Tests ---")
    unmapped_sectors = df_s['Sector'].isnull().sum()
    test_assertion("100% Stocks Mapped to Valid Sector", unmapped_sectors == 0, f"(Unmapped stocks: {unmapped_sectors})")
    
    unmapped_benchmarks = df_s['Benchmark_Index'].isnull().sum()
    test_assertion("100% Stocks Mapped to Benchmark Index", unmapped_benchmarks == 0, f"(Unmapped benchmarks: {unmapped_benchmarks})")
    
    distinct_stocks = df_s['Symbol'].nunique()
    test_assertion("Exactly 100 Reconciled Stock Tickers", distinct_stocks == 100, f"(Distinct symbols: {distinct_stocks})")
    
    distinct_indices = df_i['Symbol'].nunique()
    test_assertion("Exactly 30 Unique Indices", distinct_indices == 30, f"(Distinct indices: {distinct_indices})")
    
    print("\n--- 5. Trades Historical Consistency Test ---")
    # Trades should be present post June 1, 2011
    post_2011 = df_s[df_s['Date_dt'] >= '2011-06-01']
    null_trades_post_2011 = post_2011['Trades'].isnull().sum()
    test_assertion("Trades Non-Null Post-June 2011", null_trades_post_2011 == 0, f"(Post-2011 null trades: {null_trades_post_2011})")
    
    print("\n" + "=" * 60)
    print(f"VALIDATION SUMMARY: {passed_tests} / {total_tests} Tests Passed ({(passed_tests/total_tests)*100:.1f}%)")
    print("=" * 60)
    
    return passed_tests == total_tests

if __name__ == '__main__':
    run_validations()
