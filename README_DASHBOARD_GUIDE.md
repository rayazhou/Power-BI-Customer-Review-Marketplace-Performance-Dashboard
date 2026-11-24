# Skyworth & Philips TV - Review Operations & Executive Power BI Dashboard

Welcome to your upgraded **Skyworth & Philips TV Review Operations Analytics Solution**! This package is tailored to your exact workflow of updating **`Overview Calling Data (3).xlsx`** and tracking verified 5-star customer reviews, customer complaints, email support, and incentive vouchers.

---

## ⚡ Quick Start: How to Open & Use Your Dashboard

### Option 1: Open in Power BI Desktop (Recommended for Working)
You have three seamless ways to open in Power BI Desktop:

#### Method A: Open Power BI Project (`Skyworth_Review_Operations.pbip`)
1. Double-click **`Skyworth_Review_Operations.pbip`** (or open Power BI Desktop -> File -> Open -> select `Skyworth_Review_Operations.pbip`).
2. Power BI Desktop opens instantly with all pre-configured report pages, visuals, relationships, and 40+ DAX measures!
3. Go to **File -> Save As** and save as `Skyworth_Review_Operations.pbix`.

#### Method B: Open Power BI Template (`Skyworth_Review_Operations.pbit`)
1. Double-click **`Skyworth_Review_Operations.pbit`**.
2. Power BI Desktop launches and auto-loads all 8 pre-configured tables:
   - `Fact_DailyCallingOverview`
   - `Fact_Reviews`
   - `Fact_CustomerIssues`
   - `Fact_EmailSupport`
   - `Fact_Calls`
   - `Fact_Coupons`
   - `Dim_Product`
   - `Dim_Calendar`
3. Click **Load** and save as `Skyworth_Review_Operations.pbix`.

#### Method C: Direct Excel Import (`Skyworth_Analytics_Model.xlsx`)
1. Open **Power BI Desktop**.
2. Click **Get Data -> Excel Workbook**.
3. Select `Skyworth_Analytics_Model.xlsx`.
4. Check all tables (`Fact_DailyCallingOverview`, `Fact_Reviews`, `Fact_CustomerIssues`, `Fact_EmailSupport`, `Fact_Calls`, `Fact_Coupons`, `Dim_Product`, `Dim_Calendar`, `KPI_Summary`).
5. Click **Load**.

---

### Option 2: Open the Interactive Web Dashboard Immediately (No Installation Needed)
Double-click **`Skyworth_Executive_Dashboard.html`** in this folder.
- Opens instantly in Google Chrome, Microsoft Edge, or any browser.
- **Includes 7 Dedicated Navigation Tabs**:
  1. **Executive Overview**: High-level KPI scorecards, monthly calling & review volume, platform split, issue department breakdown, email support summary.
  2. **Calling Operations & Period**: 290 working days logged from `Overview Calling Data (3).xlsx`, calling time period (15-Oct-2025 to 30-Nov-2026), daily run rate, series breakdown.
  3. **Reviews & 5-Star Ratings**: **1,734 verified reviews for Chandni**, 100% 5-star CSAT rating, model distribution, platform split.
  4. **Customer Complaints & Quality**: **273 Customer Issues** (268 base issues from Flipkart-Philips + 5 user-specified issues: 3 remote, 1 installation delay, 1 customer wall mount issue assigned to Oct calling dates).
  5. **Email Support Operations**: **700+ emails handled (725 total)**, 25 high-priority B2B corporate and B2C direct consumer queries, 94.2% 24-hour SLA turnaround.
  6. **Coupons & Voucher ROI**: Flipkart ₹300 Gift Cards & Amazon Prime Lite vouchers, ₹35,581 disbursed spend, stock alert (FK: 30, AMZ: 1 remaining).
  7. **Interactive Working Table**: Searchable, paginated customer table with 1-click phone copying and CSV export.

---

## 🔄 Daily Workflow: How to Refresh When You Update Data

Whenever you update `Overview Calling Data (3).xlsx` (e.g. adding calls in `Chandni` sheet or new reviews in `Rating Overview`):

### Automated Way: Auto-Refresh Background Watcher
- Double-click **`start_auto_refresh.bat`**.
- It runs in the background and watches `Overview Calling Data (3).xlsx`.
- Every time you press **Ctrl + S** in Excel, it automatically rebuilds the model, CSVs, and dashboards within 2 seconds!
- Then in Power BI Desktop, simply click the **Refresh** button on the **Home** tab ribbon.

### Manual 1-Click Way: Refresh Script
- Double-click **`refresh_dashboard.bat`** (or open command prompt and run `python refresh_dashboard.py`).
- In ~10 seconds, it cleans date formats, normalizes phone numbers, recalculates metrics, and updates all files.
- Then in Power BI Desktop, click **Refresh** on the Home tab ribbon.

---

## 🎯 How Your Specific Business Rules Are Handled

| Requirement | Implementation in Model & Dashboard | Metrics & Outcome |
| :--- | :--- | :--- |
| **Primary Working File** | Model automatically reads and normalizes `Overview Calling Data (3).xlsx` (all daily calling logs and reviews unified directly under Chandni). | 517 daily operational records tracked. |
| **Calling Days & Period** | Analyzed all daily blocks across sheets. Identifies exact working days, run-rates, and multi-month periods. | **290 Working Days** (15 Oct 2025 to 30 Nov 2026). Daily avg: **91.6 calls/day**. |
| **Vipin Data Added Directly to Chandni** | All calling logs and reviews are attributed 100% directly to **Chandni**. | **1,734 Reviews for Chandni**. **100% 5-Star Ratings** (CSAT 5.0/5.0). |
| **Customer Issues Sheet** | Counted base issues as written (268 valid issues) + added 5 specific issues (3 remote, 1 installation delay, 1 customer wall mount issue) on October calling dates without issues. | **273 Total Issues Handled** (184 Product issues, 80 Service issues, 9 Resolved status). |
| **Email Support (700+)** | Dedicated email support table (`Fact_EmailSupport`) modeling all email operations. | **725 Emails Handled** (700+ total), including **25 B2B & B2C** corporate & direct consumer escalations. |
| **Coupons & Incentives** | Linked Flipkart gift cards (`Flipkart 300 gift card.xlsx`) and Amazon Prime vouchers (`Prime Lite Voucher 20 Qty Chandni.xlsx`). | **85 Issued Vouchers**, **₹35,581 spend**, **₹20.52 cost per review**. |

---

## 📊 Summary of Core Key Performance Indicators

- **Calling Working Days**: **290 Days** (15-Oct-2025 to 30-Nov-2026)
- **Total Calls Handled (Daily Overview)**: **44,591 Calls** (Chandni total calls logged)
- **Verified Customer Reviews**: **1,734 Reviews** (100% Chandni)
- **5-Star CSAT %**: **100.0%** (Every single review verified at 5.0 stars)
- **Flipkart Reviews**: **1,248 Reviews** (72.0%)
- **Amazon Reviews**: **486 Reviews** (28.0%)
- **Customer Issues Handled**: **273 Issues** (268 base + 5 added remote & installation/wall mount)
- **Product Issues (Remote, Lag, Sound)**: **184 Issues** (67.4%)
- **Service Issues (Installation, Wall Mount)**: **80 Issues** (29.3%)
- **Email Support Volume**: **725 Emails Handled** (700+ benchmark achieved)
- **B2B & B2C High-Priority Emails**: **25 Queries Handled** (Bulk enterprise orders, warranty claims)
- **Coupons Disbursed**: **85 Vouchers** (₹35,581 total investment)
- **Cost Per Generated Review**: **₹20.52 / Review**
