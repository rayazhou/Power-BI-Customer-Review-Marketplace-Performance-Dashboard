import os
import sys
import subprocess
import time

def refresh():
    print("="*70)
    print(" SKYWORTH & PHILIPS TV DASHBOARD - AUTOMATED PIPELINE REFRESH")
    print("="*70)
    start_time = time.time()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    print("\n[1/3] Building relational data model from Overview & Call data...")
    res1 = subprocess.run([sys.executable, "build_powerbi_model.py"], capture_output=True, text=True)
    if res1.returncode != 0:
        print("ERROR in build_powerbi_model.py:")
        print(res1.stderr)
        return False
    print(res1.stdout.strip())

    print("\n[2/4] Updating Power BI Template (Skyworth_Review_Operations.pbit)...")
    res2 = subprocess.run([sys.executable, "create_pbit.py"], capture_output=True, text=True)
    if res2.returncode != 0:
        print("ERROR in create_pbit.py:")
        print(res2.stderr)
        return False
    print(res2.stdout.strip())

    print("\n[3/4] Updating Power BI Project (Skyworth_Review_Operations.pbip)...")
    res_pbip = subprocess.run([sys.executable, "create_pbip.py"], capture_output=True, text=True)
    if res_pbip.returncode != 0:
        print("ERROR in create_pbip.py:")
        print(res_pbip.stderr)
        return False
    print(res_pbip.stdout.strip())

    print("\n[4/4] Updating Interactive Executive Web Dashboard (HTML)...")
    res3 = subprocess.run([sys.executable, "generate_dashboard_html.py"], capture_output=True, text=True)
    if res3.returncode != 0:
        print("ERROR in generate_dashboard_html.py:")
        print(res3.stderr)
        return False
    print(res3.stdout.strip())

    elapsed = time.time() - start_time
    print("\n" + "="*70)
    print(f" SUCCESS: Full Solution Refreshed in {elapsed:.1f} seconds!")
    print(" Files updated:")
    print("  [OK] Skyworth_Analytics_Model.xlsx (Integrated multi-sheet Excel model)")
    print("  [OK] Fact_DailyCallingOverview.csv, Fact_Reviews.csv, Fact_CustomerIssues.csv")
    print("  [OK] Fact_EmailSupport.csv, Fact_CallActivity.csv, Fact_Coupons.csv")
    print("  [OK] Dim_Product.csv, Dim_Calendar.csv")
    print("  [OK] Skyworth_Review_Operations.pbit (Power BI Template)")
    print("  [OK] Skyworth_Executive_Dashboard.html (Web Dashboard)")
    print("\n In Power BI Desktop: Click 'Refresh' on the Home tab ribbon!")
    print("="*70)
    return True

if __name__ == '__main__':
    refresh()
