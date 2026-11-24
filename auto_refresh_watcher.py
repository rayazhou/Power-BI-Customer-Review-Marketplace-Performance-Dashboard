"""
Skyworth & Philips TV - Auto Refresh File Watcher
Monitors Overview Calling Data (3).xlsx and other workspace files for changes.
Whenever you save your Excel file, it automatically updates the analytical model, CSVs, and dashboard!
"""

import os
import sys
import time
import subprocess
from datetime import datetime

WATCH_FILES = [
    "Overview Calling Data (3).xlsx",
    "Flipkart 300 gift card.xlsx",
    "Prime Lite Voucher 20 Qty Chandni.xlsx",
    "Skyworth Call Data.xlsx",
    "Customer Issues(Flipkart-Philips) (1).csv"
]

def get_mtimes():
    mtimes = {}
    for f in WATCH_FILES:
        if os.path.exists(f):
            try:
                mtimes[f] = os.path.getmtime(f)
            except Exception:
                pass
    return mtimes

def main():
    print("=" * 70)
    print(" SKYWORTH & PHILIPS TV - AUTO-REFRESH BACKGROUND WATCHER")
    print("=" * 70)
    print("Watching for changes in:")
    for f in WATCH_FILES:
        if os.path.exists(f):
            print(f"  [Monitoring] {f}")
        else:
            print(f"  [Pending]    {f} (will monitor once created)")
    print("\nWhenever you save 'Overview Calling Data (3).xlsx' in Excel (Ctrl + S),")
    print("this watcher will automatically rebuild your model and dashboards!\n")
    print("Press Ctrl + C in this window to stop watching.\n")
    print("-" * 70)

    last_mtimes = get_mtimes()

    while True:
        try:
            time.sleep(2)
            current_mtimes = get_mtimes()
            changed = []

            for f, mtime in current_mtimes.items():
                if f not in last_mtimes or mtime > last_mtimes[f]:
                    changed.append(f)

            if changed:
                now_str = datetime.now().strftime("%I:%M:%S %p")
                print(f"[{now_str}] Detected change in: {', '.join(changed)}")
                print("             Waiting 1 second for Excel to finish writing...")
                time.sleep(1)

                print("             Rebuilding Power BI Model & Dashboard...")
                res = subprocess.run([sys.executable, "refresh_dashboard.py"], capture_output=True, text=True)
                if res.returncode == 0:
                    print(f"[{now_str}] SUCCESS! Model & Dashboard updated.")
                    print("             >>> In Power BI Desktop: Click 'Refresh' on Home tab! <<<\n")
                else:
                    print(f"[{now_str}] ERROR during refresh:")
                    print(res.stderr[:500])

                last_mtimes = get_mtimes()

        except KeyboardInterrupt:
            print("\nAuto-refresh watcher stopped.")
            break
        except Exception as e:
            time.sleep(3)

if __name__ == '__main__':
    main()
