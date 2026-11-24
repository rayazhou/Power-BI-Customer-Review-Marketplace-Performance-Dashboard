import os
import re
import datetime
import pandas as pd
import numpy as np

base_dir = os.path.dirname(os.path.abspath(__file__))

print("Verifying data sources and building test model...")

# 1. Overview Calling Data
xl_overview = pd.ExcelFile(os.path.join(base_dir, 'Overview Calling Data (3).xlsx'))
print("Overview sheets:", xl_overview.sheet_names)

# Rating Overview
df_ro = xl_overview.parse('Rating Overview')
print("Rating Overview raw count:", len(df_ro))

# Clean Date function
def fix_date(d):
    if pd.isna(d):
        return pd.NaT
    s = str(d).strip()
    if s == '01-0-26':
        return pd.to_datetime('2026-07-01')
    return pd.to_datetime(d, format='mixed', dayfirst=True)

df_ro['Clean_Date'] = df_ro['Calling Date'].apply(fix_date)
df_ro['Effective_Agent'] = df_ro['Person Concerned'].apply(lambda x: 'Chandni (User)' if str(x).strip().title() in ['Chandni', 'Vipin'] else str(x).strip().title())

print("Reviews by Effective Agent:")
print(df_ro['Effective_Agent'].value_counts())

# Customer Issues CSV
df_issues = pd.read_csv(os.path.join(base_dir, 'Customer Issues(Flipkart-Philips) (1).csv'), encoding='latin1').iloc[:268].copy()
print("Valid base customer issues:", len(df_issues))

print("Verification complete.")
