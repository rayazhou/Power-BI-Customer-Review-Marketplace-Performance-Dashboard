import pandas as pd
import numpy as np

xl = pd.ExcelFile('Overview Calling Data (3).xlsx')

def parse_overview_daily(sheet_name):
    df_raw = xl.parse(sheet_name, header=None)
    records = []
    
    # 1. Standard top blocks (row 0 month header, row 1 column headers)
    for col_start in range(0, df_raw.shape[1], 5):
        if col_start + 4 >= df_raw.shape[1]:
            continue
        m_head = df_raw.iloc[0, col_start]
        
        for r_idx in range(2, len(df_raw)):
            row_vals = df_raw.iloc[r_idx, col_start:col_start+5]
            plat = row_vals.iloc[0]
            ser = row_vals.iloc[1]
            d = row_vals.iloc[2]
            calls = row_vals.iloc[3]
            rate = row_vals.iloc[4]
            
            if str(d).strip().upper() == 'DATE' or str(calls).strip().upper() == 'CALLS':
                continue
            if str(plat).strip().upper().startswith('TOTAL') or str(ser).strip().upper().startswith('TOTAL') or str(d).strip().upper().startswith('TOTAL'):
                continue
            if pd.isna(d) and pd.isna(calls) and pd.isna(rate):
                continue
            
            dt = pd.to_datetime(d, errors='coerce', dayfirst=True)
            if pd.notna(dt) and dt.year >= 2024:
                c_num = pd.to_numeric(calls, errors='coerce')
                r_num = pd.to_numeric(rate, errors='coerce')
                records.append({
                    'Agent': sheet_name,
                    'Date': dt,
                    'Platform': str(plat).strip() if pd.notna(plat) else 'Unknown',
                    'Series': str(ser).strip() if pd.notna(ser) else 'Unknown',
                    'Calls': c_num if pd.notna(c_num) else 0,
                    'Ratings': r_num if pd.notna(r_num) else 0
                })
                
    # 2. Check for lower sub-tables (e.g. Row 35 Col 57 in Chandni sheet)
    for r in range(2, len(df_raw)):
        for c in range(2, df_raw.shape[1] - 2):
            val = str(df_raw.iloc[r, c]).strip().upper()
            if val == 'DATE':
                plat_col = c - 2
                ser_col = c - 1
                date_col = c
                calls_col = c + 1
                rate_col = c + 2
                for sub_r in range(r + 1, len(df_raw)):
                    d = df_raw.iloc[sub_r, date_col]
                    calls = df_raw.iloc[sub_r, calls_col] if calls_col < df_raw.shape[1] else None
                    rate = df_raw.iloc[sub_r, rate_col] if rate_col < df_raw.shape[1] else None
                    plat = df_raw.iloc[sub_r, plat_col]
                    ser = df_raw.iloc[sub_r, ser_col]
                    if str(d).strip().upper().startswith('TOTAL') or str(plat).strip().upper().startswith('TOTAL'):
                        break
                    dt = pd.to_datetime(d, errors='coerce', dayfirst=True)
                    if pd.notna(dt) and dt.year >= 2024:
                        c_num = pd.to_numeric(calls, errors='coerce')
                        r_num = pd.to_numeric(rate, errors='coerce')
                        records.append({
                            'Agent': sheet_name,
                            'Date': dt,
                            'Platform': str(plat).strip() if pd.notna(plat) else 'Unknown',
                            'Series': str(ser).strip() if pd.notna(ser) else 'Unknown',
                            'Calls': c_num if pd.notna(c_num) else 0,
                            'Ratings': r_num if pd.notna(r_num) else 0
                        })
                        
    df_res = pd.DataFrame(records).drop_duplicates(subset=['Agent', 'Date', 'Platform', 'Series', 'Calls', 'Ratings'])
    return df_res

df_c = parse_overview_daily('Chandni')
df_v = parse_overview_daily('Vipin')
df_s = parse_overview_daily('Sorav')

for name, df in [('Chandni', df_c), ('Vipin', df_v), ('Sorav', df_s)]:
    d_min = df['Date'].min().strftime('%Y-%m-%d') if len(df) else 'N/A'
    d_max = df['Date'].max().strftime('%Y-%m-%d') if len(df) else 'N/A'
    c_tot = df['Calls'].sum()
    r_tot = df['Ratings'].sum()
    n_days = df['Date'].nunique()
    print(f"{name}: {len(df)} rows, {n_days} unique days ({d_min} to {d_max}). Total Calls: {c_tot:.0f}, Total Ratings: {r_tot:.0f}")
