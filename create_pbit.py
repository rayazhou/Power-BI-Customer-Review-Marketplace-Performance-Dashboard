import os
import zipfile
import json

def build_pbit():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    daily_csv = os.path.join(base_dir, 'Fact_DailyCallingOverview.csv').replace('\\', '/')
    reviews_csv = os.path.join(base_dir, 'Fact_Reviews.csv').replace('\\', '/')
    issues_csv = os.path.join(base_dir, 'Fact_CustomerIssues.csv').replace('\\', '/')
    emails_csv = os.path.join(base_dir, 'Fact_EmailSupport.csv').replace('\\', '/')
    calls_csv = os.path.join(base_dir, 'Fact_CallActivity.csv').replace('\\', '/')
    coupons_csv = os.path.join(base_dir, 'Fact_Coupons.csv').replace('\\', '/')
    product_csv = os.path.join(base_dir, 'Dim_Product.csv').replace('\\', '/')
    calendar_csv = os.path.join(base_dir, 'Dim_Calendar.csv').replace('\\', '/')

    pbit_path = os.path.join(base_dir, 'Skyworth_Review_Operations.pbit')

    # 1. Content Types
    content_types = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="png" ContentType="" />'
        '<Default Extension="json" ContentType="" />'
        '<Override PartName="/Version" ContentType="" />'
        '<Override PartName="/Settings" ContentType="application/json" />'
        '<Override PartName="/Metadata" ContentType="application/json" />'
        '<Override PartName="/DataModelSchema" ContentType="" />'
        '<Override PartName="/Report/Layout" ContentType="" />'
        '</Types>'
    )

    # 2. Version, Settings, Metadata
    version_str = '1.32'
    settings_dict = {
        "Version": 4,
        "ReportSettings": {},
        "QueriesSettings": {
            "TypeDetectionEnabled": True,
            "RelationshipImportEnabled": True,
            "Version": "2.146.304.0"
        }
    }
    metadata_dict = {
        "Version": 5,
        "AutoCreatedRelationships": [],
        "CreatedFrom": "PowerBIDesktop",
        "CreatedFromRelease": "2026.10"
    }

    # 3. DataModelSchema (TMSL JSON)
    tmsl_model = {
        "name": "Skyworth_Analytics_Model",
        "compatibilityLevel": 1550,
        "model": {
            "culture": "en-US",
            "dataAccessOptions": {
                "legacyRedirects": True,
                "returnErrorValuesAsNull": True
            },
            "defaultPowerBIDataSourceVersion": "powerBI_V3",
            "tables": [
                {
                    "name": "Fact_DailyCallingOverview",
                    "columns": [
                        {"name": "Overview_ID", "dataType": "string", "sourceColumn": "Overview_ID"},
                        {"name": "Date", "dataType": "dateTime", "sourceColumn": "Date", "formatString": "yyyy-MM-dd"},
                        {"name": "Agent", "dataType": "string", "sourceColumn": "Agent"},
                        {"name": "Platform", "dataType": "string", "sourceColumn": "Platform"},
                        {"name": "Series", "dataType": "string", "sourceColumn": "Series"},
                        {"name": "Calls", "dataType": "int64", "sourceColumn": "Calls", "formatString": "#,##0"},
                        {"name": "Ratings", "dataType": "int64", "sourceColumn": "Ratings", "formatString": "#,##0"},
                        {"name": "Effective_Agent", "dataType": "string", "sourceColumn": "Effective_Agent"},
                        {"name": "Is_User_Portfolio", "dataType": "int64", "sourceColumn": "Is_User_Portfolio"},
                        {"name": "Year_Month", "dataType": "string", "sourceColumn": "Year_Month"},
                        {"name": "Month_Name", "dataType": "string", "sourceColumn": "Month_Name"},
                        {"name": "Day_Of_Week", "dataType": "string", "sourceColumn": "Day_Of_Week"}
                    ],
                    "measures": [
                        {"name": "Total Calling Days", "expression": "DISTINCTCOUNT('Fact_DailyCallingOverview'[Date])", "formatString": "#,##0"},
                        {"name": "Total Calling Days (Chandni)", "expression": "CALCULATE(DISTINCTCOUNT('Fact_DailyCallingOverview'[Date]), 'Fact_DailyCallingOverview'[Is_User_Portfolio] = 1)", "formatString": "#,##0"},
                        {"name": "Total Calls (Chandni)", "expression": "CALCULATE(SUM('Fact_DailyCallingOverview'[Calls]), 'Fact_DailyCallingOverview'[Is_User_Portfolio] = 1)", "formatString": "#,##0"},
                        {"name": "Avg Calls Per Working Day", "expression": "DIVIDE([Total Calls (Chandni)], [Total Calling Days (Chandni)], 0)", "formatString": "#,##0.0"}
                    ],
                    "partitions": [{
                        "name": "Fact_DailyCallingOverview-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{daily_csv}"),[Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.Rtf]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}, {"Calls", Int64.Type}, {"Ratings", Int64.Type}, {"Is_User_Portfolio", Int64.Type}})',
                                "in",
                                '    #"Changed Type"'
                            ]
                        }
                    }]
                },
                {
                    "name": "Fact_Reviews",
                    "columns": [
                        {"name": "Review_ID", "dataType": "string", "sourceColumn": "Review_ID"},
                        {"name": "Date", "dataType": "dateTime", "sourceColumn": "Date", "formatString": "yyyy-MM-dd"},
                        {"name": "Platform", "dataType": "string", "sourceColumn": "Platform"},
                        {"name": "Brand", "dataType": "string", "sourceColumn": "Brand"},
                        {"name": "Model_Number", "dataType": "string", "sourceColumn": "Model_Number"},
                        {"name": "Screen_Size", "dataType": "string", "sourceColumn": "Screen_Size"},
                        {"name": "Series", "dataType": "string", "sourceColumn": "Series"},
                        {"name": "Customer_Name", "dataType": "string", "sourceColumn": "Customer_Name"},
                        {"name": "Customer_Phone", "dataType": "string", "sourceColumn": "Customer_Phone"},
                        {"name": "Rating", "dataType": "int64", "sourceColumn": "Rating"},
                        {"name": "Original_Agent", "dataType": "string", "sourceColumn": "Original_Agent"},
                        {"name": "Effective_Agent", "dataType": "string", "sourceColumn": "Effective_Agent"},
                        {"name": "Is_User_Review", "dataType": "int64", "sourceColumn": "Is_User_Review"},
                        {"name": "Year_Month", "dataType": "string", "sourceColumn": "Year_Month"}
                    ],
                    "measures": [
                        {"name": "Total Reviews (Chandni)", "expression": "CALCULATE(COUNTROWS('Fact_Reviews'), 'Fact_Reviews'[Effective_Agent] = \"Chandni\")", "formatString": "#,##0"},
                        {"name": "5-Star Rating CSAT %", "expression": "DIVIDE(CALCULATE(COUNTROWS('Fact_Reviews'), 'Fact_Reviews'[Rating] = 5), COUNTROWS('Fact_Reviews'), 1.0)", "formatString": "0.0%"},
                        {"name": "Reviews Flipkart", "expression": "CALCULATE([Total Reviews (Chandni)], 'Fact_Reviews'[Platform] = \"Flipkart\")", "formatString": "#,##0"},
                        {"name": "Reviews Amazon", "expression": "CALCULATE([Total Reviews (Chandni)], 'Fact_Reviews'[Platform] = \"Amazon\")", "formatString": "#,##0"}
                    ],
                    "partitions": [{
                        "name": "Fact_Reviews-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{reviews_csv}"),[Delimiter=",", Columns=14, Encoding=65001, QuoteStyle=QuoteStyle.Rtf]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}, {"Rating", Int64.Type}, {"Is_User_Review", Int64.Type}})',
                                "in",
                                '    #"Changed Type"'
                            ]
                        }
                    }]
                },
                {
                    "name": "Fact_CustomerIssues",
                    "columns": [
                        {"name": "Issue_ID", "dataType": "string", "sourceColumn": "Issue_ID"},
                        {"name": "Date", "dataType": "dateTime", "sourceColumn": "Date", "formatString": "yyyy-MM-dd"},
                        {"name": "Customer_Name", "dataType": "string", "sourceColumn": "Customer_Name"},
                        {"name": "Customer_Phone", "dataType": "string", "sourceColumn": "Customer_Phone"},
                        {"name": "Order_ID", "dataType": "string", "sourceColumn": "Order_ID"},
                        {"name": "City", "dataType": "string", "sourceColumn": "City"},
                        {"name": "State", "dataType": "string", "sourceColumn": "State"},
                        {"name": "Model", "dataType": "string", "sourceColumn": "Model"},
                        {"name": "Screen_Size", "dataType": "string", "sourceColumn": "Screen_Size"},
                        {"name": "Series", "dataType": "string", "sourceColumn": "Series"},
                        {"name": "Issue_Description", "dataType": "string", "sourceColumn": "Issue_Description"},
                        {"name": "Responsible_Department", "dataType": "string", "sourceColumn": "Responsible_Department"},
                        {"name": "TAT_Resolution", "dataType": "string", "sourceColumn": "TAT_Resolution"},
                        {"name": "Status", "dataType": "string", "sourceColumn": "Status"},
                        {"name": "Resolution_Feedback", "dataType": "string", "sourceColumn": "Resolution_Feedback"},
                        {"name": "Is_Added_Issue", "dataType": "string", "sourceColumn": "Is_Added_Issue"},
                        {"name": "Year_Month", "dataType": "string", "sourceColumn": "Year_Month"}
                    ],
                    "measures": [
                        {"name": "Total Customer Issues", "expression": "COUNTROWS('Fact_CustomerIssues')", "formatString": "#,##0"},
                        {"name": "Product Issues Count", "expression": "CALCULATE(COUNTROWS('Fact_CustomerIssues'), 'Fact_CustomerIssues'[Responsible_Department] = \"Product Issue\")", "formatString": "#,##0"},
                        {"name": "Service Issues Count", "expression": "CALCULATE(COUNTROWS('Fact_CustomerIssues'), 'Fact_CustomerIssues'[Responsible_Department] = \"Service Issue\")", "formatString": "#,##0"},
                        {"name": "Remote Complaints Count", "expression": "CALCULATE(COUNTROWS('Fact_CustomerIssues'), CONTAINSSTRING(LOWER('Fact_CustomerIssues'[Issue_Description]), \"remote\"))", "formatString": "#,##0"},
                        {"name": "Installation & Mount Complaints", "expression": "CALCULATE(COUNTROWS('Fact_CustomerIssues'), CONTAINSSTRING(LOWER('Fact_CustomerIssues'[Issue_Description]), \"installation\") || CONTAINSSTRING(LOWER('Fact_CustomerIssues'[Issue_Description]), \"wall mount\"))", "formatString": "#,##0"}
                    ],
                    "partitions": [{
                        "name": "Fact_CustomerIssues-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{issues_csv}"),[Delimiter=",", Columns=17, Encoding=65001, QuoteStyle=QuoteStyle.Rtf]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}})',
                                "in",
                                '    #"Changed Type"'
                            ]
                        }
                    }]
                },
                {
                    "name": "Fact_EmailSupport",
                    "columns": [
                        {"name": "Email_ID", "dataType": "string", "sourceColumn": "Email_ID"},
                        {"name": "Date", "dataType": "dateTime", "sourceColumn": "Date", "formatString": "yyyy-MM-dd"},
                        {"name": "Category", "dataType": "string", "sourceColumn": "Category"},
                        {"name": "Subject", "dataType": "string", "sourceColumn": "Subject"},
                        {"name": "Handled_By", "dataType": "string", "sourceColumn": "Handled_By"},
                        {"name": "Action_Taken", "dataType": "string", "sourceColumn": "Action_Taken"},
                        {"name": "Status", "dataType": "string", "sourceColumn": "Status"},
                        {"name": "Resolution_Hours", "dataType": "int64", "sourceColumn": "Resolution_Hours"},
                        {"name": "Is_B2B_B2C", "dataType": "string", "sourceColumn": "Is_B2B_B2C"},
                        {"name": "Year_Month", "dataType": "string", "sourceColumn": "Year_Month"}
                    ],
                    "measures": [
                        {"name": "Total Emails Handled", "expression": "COUNTROWS('Fact_EmailSupport')", "formatString": "#,##0"},
                        {"name": "B2B and B2C Emails Handled", "expression": "CALCULATE(COUNTROWS('Fact_EmailSupport'), 'Fact_EmailSupport'[Is_B2B_B2C] = \"Yes\")", "formatString": "#,##0"},
                        {"name": "General Support Emails", "expression": "CALCULATE(COUNTROWS('Fact_EmailSupport'), 'Fact_EmailSupport'[Is_B2B_B2C] = \"No\")", "formatString": "#,##0"},
                        {"name": "Email SLA Compliance %", "expression": "DIVIDE(CALCULATE(COUNTROWS('Fact_EmailSupport'), 'Fact_EmailSupport'[Resolution_Hours] <= 24), COUNTROWS('Fact_EmailSupport'), 0)", "formatString": "0.0%"}
                    ],
                    "partitions": [{
                        "name": "Fact_EmailSupport-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{emails_csv}"),[Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.Rtf]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}, {"Resolution_Hours", Int64.Type}})',
                                "in",
                                '    #"Changed Type"'
                            ]
                        }
                    }]
                },
                {
                    "name": "Fact_Calls",
                    "columns": [
                        {"name": "Call_ID", "dataType": "string", "sourceColumn": "Call_ID"},
                        {"name": "Date", "dataType": "dateTime", "sourceColumn": "Date", "formatString": "yyyy-MM-dd"},
                        {"name": "Platform", "dataType": "string", "sourceColumn": "Platform"},
                        {"name": "Brand", "dataType": "string", "sourceColumn": "Brand"},
                        {"name": "Model_Number", "dataType": "string", "sourceColumn": "Model_Number"},
                        {"name": "Screen_Size", "dataType": "string", "sourceColumn": "Screen_Size"},
                        {"name": "Series", "dataType": "string", "sourceColumn": "Series"},
                        {"name": "Display_Type", "dataType": "string", "sourceColumn": "Display_Type"},
                        {"name": "Order_ID", "dataType": "string", "sourceColumn": "Order_ID"},
                        {"name": "Customer_Name", "dataType": "string", "sourceColumn": "Customer_Name"},
                        {"name": "Customer_Phone", "dataType": "string", "sourceColumn": "Customer_Phone"},
                        {"name": "City", "dataType": "string", "sourceColumn": "City"},
                        {"name": "State", "dataType": "string", "sourceColumn": "State"},
                        {"name": "Call_Status", "dataType": "string", "sourceColumn": "Call_Status"},
                        {"name": "Call_Category", "dataType": "string", "sourceColumn": "Call_Category"},
                        {"name": "Remark", "dataType": "string", "sourceColumn": "Remark"},
                        {"name": "Remark_Category", "dataType": "string", "sourceColumn": "Remark_Category"},
                        {"name": "Review_Status", "dataType": "string", "sourceColumn": "Review_Status"},
                        {"name": "Status", "dataType": "string", "sourceColumn": "Status"},
                        {"name": "Rate", "dataType": "int64", "sourceColumn": "Rate"},
                        {"name": "Is_Picked", "dataType": "int64", "sourceColumn": "Is_Picked"},
                        {"name": "Is_Reviewed", "dataType": "int64", "sourceColumn": "Is_Reviewed"},
                        {"name": "Has_Coupon_Assigned", "dataType": "string", "sourceColumn": "Has_Coupon_Assigned"},
                        {"name": "Assigned_Voucher_ID", "dataType": "string", "sourceColumn": "Assigned_Voucher_ID"},
                        {"name": "Assigned_Coupon_Code", "dataType": "string", "sourceColumn": "Assigned_Coupon_Code"},
                        {"name": "Assigned_Coupon_Amount", "dataType": "int64", "sourceColumn": "Assigned_Coupon_Amount"}
                    ],
                    "measures": [
                        {"name": "Total Detailed Calls", "expression": "COUNTROWS('Fact_Calls')", "formatString": "#,##0"},
                        {"name": "Calls Connected", "expression": "CALCULATE(COUNTROWS('Fact_Calls'), 'Fact_Calls'[Call_Category] = \"Connected\")", "formatString": "#,##0"},
                        {"name": "Call Pick Rate %", "expression": "DIVIDE([Calls Connected], [Total Detailed Calls], 0)", "formatString": "0.0%"},
                        {"name": "Language Barrier Calls", "expression": "CALCULATE(COUNTROWS('Fact_Calls'), 'Fact_Calls'[Call_Category] = \"Language Barrier\")", "formatString": "#,##0"}
                    ],
                    "partitions": [{
                        "name": "Fact_Calls-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{calls_csv}"),[Delimiter=",", Columns=27, Encoding=65001, QuoteStyle=QuoteStyle.Rtf]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}, {"Rate", Int64.Type}, {"Is_Picked", Int64.Type}, {"Is_Reviewed", Int64.Type}, {"Assigned_Coupon_Amount", Int64.Type}})',
                                "in",
                                '    #"Changed Type"'
                            ]
                        }
                    }]
                },
                {
                    "name": "Fact_Coupons",
                    "columns": [
                        {"name": "Voucher_ID", "dataType": "string", "sourceColumn": "Voucher_ID"},
                        {"name": "Platform", "dataType": "string", "sourceColumn": "Platform"},
                        {"name": "Voucher_Code", "dataType": "string", "sourceColumn": "Voucher_Code"},
                        {"name": "Pin_Or_Ref", "dataType": "string", "sourceColumn": "Pin_Or_Ref"},
                        {"name": "Amount", "dataType": "int64", "sourceColumn": "Amount", "formatString": "₹#,##0"},
                        {"name": "Expiry_Date", "dataType": "dateTime", "sourceColumn": "Expiry_Date", "formatString": "yyyy-MM-dd"},
                        {"name": "Customer_Name", "dataType": "string", "sourceColumn": "Customer_Name"},
                        {"name": "Customer_Phone", "dataType": "string", "sourceColumn": "Customer_Phone"},
                        {"name": "Rate", "dataType": "int64", "sourceColumn": "Rate"},
                        {"name": "Date_Shared", "dataType": "dateTime", "sourceColumn": "Date_Shared", "formatString": "yyyy-MM-dd"},
                        {"name": "Verification_Note", "dataType": "string", "sourceColumn": "Verification_Note"},
                        {"name": "Voucher_Status", "dataType": "string", "sourceColumn": "Voucher_Status"}
                    ],
                    "measures": [
                        {"name": "Total Coupons", "expression": "COUNTROWS('Fact_Coupons')", "formatString": "#,##0"},
                        {"name": "Coupons Issued", "expression": "CALCULATE(COUNTROWS('Fact_Coupons'), 'Fact_Coupons'[Voucher_Status] = \"Issued / Shared\")", "formatString": "#,##0"},
                        {"name": "Coupons Available", "expression": "CALCULATE(COUNTROWS('Fact_Coupons'), 'Fact_Coupons'[Voucher_Status] = \"Available Inventory\")", "formatString": "#,##0"},
                        {"name": "Total Voucher Spend (INR)", "expression": "CALCULATE(SUM('Fact_Coupons'[Amount]), 'Fact_Coupons'[Voucher_Status] = \"Issued / Shared\")", "formatString": "₹#,##0"},
                        {"name": "Cost Per Generated Review", "expression": "DIVIDE([Total Voucher Spend (INR)], [Total Reviews (Chandni)], 0)", "formatString": "₹0.00"}
                    ],
                    "partitions": [{
                        "name": "Fact_Coupons-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{coupons_csv}"),[Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.Rtf]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Amount", Int64.Type}, {"Expiry_Date", type date}, {"Date_Shared", type date}, {"Rate", Int64.Type}})',
                                "in",
                                '    #"Changed Type"'
                            ]
                        }
                    }]
                },
                {
                    "name": "Dim_Product",
                    "columns": [
                        {"name": "Model_Number", "dataType": "string", "sourceColumn": "Model_Number"},
                        {"name": "Brand", "dataType": "string", "sourceColumn": "Brand"},
                        {"name": "Screen_Size", "dataType": "string", "sourceColumn": "Screen_Size"},
                        {"name": "Series", "dataType": "string", "sourceColumn": "Series"},
                        {"name": "Display_Type", "dataType": "string", "sourceColumn": "Display_Type"},
                        {"name": "Resolution", "dataType": "string", "sourceColumn": "Resolution"},
                        {"name": "Operating_System", "dataType": "string", "sourceColumn": "Operating_System"}
                    ],
                    "partitions": [{
                        "name": "Dim_Product-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{product_csv}"),[Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.Rtf]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])',
                                "in",
                                '    #"Promoted Headers"'
                            ]
                        }
                    }]
                },
                {
                    "name": "Dim_Calendar",
                    "columns": [
                        {"name": "Date", "dataType": "dateTime", "sourceColumn": "Date", "formatString": "yyyy-MM-dd"},
                        {"name": "Date_Key", "dataType": "int64", "sourceColumn": "Date_Key"},
                        {"name": "Year", "dataType": "int64", "sourceColumn": "Year"},
                        {"name": "Month", "dataType": "int64", "sourceColumn": "Month"},
                        {"name": "Month_Name", "dataType": "string", "sourceColumn": "Month_Name"},
                        {"name": "Month_Short", "dataType": "string", "sourceColumn": "Month_Short"},
                        {"name": "Year_Month", "dataType": "string", "sourceColumn": "Year_Month"},
                        {"name": "Quarter", "dataType": "string", "sourceColumn": "Quarter"},
                        {"name": "Week_Number", "dataType": "int64", "sourceColumn": "Week_Number"},
                        {"name": "Day_Name", "dataType": "string", "sourceColumn": "Day_Name"},
                        {"name": "Is_Weekend", "dataType": "int64", "sourceColumn": "Is_Weekend"}
                    ],
                    "partitions": [{
                        "name": "Dim_Calendar-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{calendar_csv}"),[Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.Rtf]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Date", type date}, {"Date_Key", Int64.Type}, {"Year", Int64.Type}, {"Month", Int64.Type}, {"Week_Number", Int64.Type}, {"Is_Weekend", Int64.Type}})',
                                "in",
                                '    #"Changed Type"'
                            ]
                        }
                    }]
                }
            ],
            "relationships": [
                {
                    "name": "Rel_DailyCalling_Date",
                    "fromTable": "Fact_DailyCallingOverview",
                    "fromColumn": "Date",
                    "toTable": "Dim_Calendar",
                    "toColumn": "Date"
                },
                {
                    "name": "Rel_Reviews_Date",
                    "fromTable": "Fact_Reviews",
                    "fromColumn": "Date",
                    "toTable": "Dim_Calendar",
                    "toColumn": "Date"
                },
                {
                    "name": "Rel_Reviews_Product",
                    "fromTable": "Fact_Reviews",
                    "fromColumn": "Model_Number",
                    "toTable": "Dim_Product",
                    "toColumn": "Model_Number"
                },
                {
                    "name": "Rel_Issues_Date",
                    "fromTable": "Fact_CustomerIssues",
                    "fromColumn": "Date",
                    "toTable": "Dim_Calendar",
                    "toColumn": "Date"
                },
                {
                    "name": "Rel_Emails_Date",
                    "fromTable": "Fact_EmailSupport",
                    "fromColumn": "Date",
                    "toTable": "Dim_Calendar",
                    "toColumn": "Date"
                },
                {
                    "name": "Rel_Calls_Date",
                    "fromTable": "Fact_Calls",
                    "fromColumn": "Date",
                    "toTable": "Dim_Calendar",
                    "toColumn": "Date"
                },
                {
                    "name": "Rel_Calls_Product",
                    "fromTable": "Fact_Calls",
                    "fromColumn": "Model_Number",
                    "toTable": "Dim_Product",
                    "toColumn": "Model_Number"
                }
            ]
        }
    }

    # 4. Report Layout JSON
    layout_dict = {
        "id": 0,
        "resourcePackages": [],
        "sections": [
            {
                "id": 0,
                "name": "Section_Executive_Summary",
                "displayName": "Executive Overview",
                "displayOption": 1,
                "width": 1280.0,
                "height": 720.0,
                "visualContainers": [
                    {
                        "x": 20.0, "y": 15.0, "z": 0, "width": 1240.0, "height": 55.0,
                        "config": json.dumps({
                            "name": "TitleCard",
                            "singleVisual": {
                                "visualType": "textbox",
                                "objects": {
                                    "general": [{
                                        "properties": {
                                            "paragraphs": [{
                                                "textRuns": [{
                                                    "value": "Skyworth & Philips TV - Review Operations & Executive Performance Dashboard",
                                                    "textStyle": {"fontSize": "19pt", "fontFamily": "Segoe UI Semibold", "color": "#0F172A"}
                                                }]
                                            }]
                                        }
                                    }]
                                }
                            }
                        })
                    },
                    {
                        "x": 20.0, "y": 80.0, "z": 1000, "width": 190.0, "height": 105.0,
                        "config": json.dumps({
                            "name": "CardCallingDays",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_DailyCallingOverview.Total Calling Days (Chandni)"}]}
                            }
                        })
                    },
                    {
                        "x": 225.0, "y": 80.0, "z": 2000, "width": 190.0, "height": 105.0,
                        "config": json.dumps({
                            "name": "CardCallsUser",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_DailyCallingOverview.Total Calls (Chandni)"}]}
                            }
                        })
                    },
                    {
                        "x": 430.0, "y": 80.0, "z": 3000, "width": 205.0, "height": 105.0,
                        "config": json.dumps({
                            "name": "CardReviewsPortfolio",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_Reviews.Total Reviews (Chandni)"}]}
                            }
                        })
                    },
                    {
                        "x": 650.0, "y": 80.0, "z": 4000, "width": 190.0, "height": 105.0,
                        "config": json.dumps({
                            "name": "CardIssuesTotal",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_CustomerIssues.Total Customer Issues"}]}
                            }
                        })
                    },
                    {
                        "x": 855.0, "y": 80.0, "z": 5000, "width": 190.0, "height": 105.0,
                        "config": json.dumps({
                            "name": "CardEmailsHandled",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_EmailSupport.Total Emails Handled"}]}
                            }
                        })
                    },
                    {
                        "x": 1060.0, "y": 80.0, "z": 6000, "width": 200.0, "height": 105.0,
                        "config": json.dumps({
                            "name": "CardCSAT",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_Reviews.5-Star Rating CSAT %"}]}
                            }
                        })
                    },
                    {
                        "x": 20.0, "y": 200.0, "z": 7000, "width": 780.0, "height": 495.0,
                        "config": json.dumps({
                            "name": "MonthlyTrendsChart",
                            "singleVisual": {
                                "visualType": "clusteredColumnChart",
                                "projections": {
                                    "Category": [{"queryRef": "Dim_Calendar.Year_Month"}],
                                    "Y": [
                                        {"queryRef": "Fact_DailyCallingOverview.Total Calls (Chandni)"},
                                        {"queryRef": "Fact_Reviews.Total Reviews (Chandni)"}
                                    ]
                                }
                            }
                        })
                    },
                    {
                        "x": 815.0, "y": 200.0, "z": 8000, "width": 445.0, "height": 240.0,
                        "config": json.dumps({
                            "name": "ReviewsByPlatformDonut",
                            "singleVisual": {
                                "visualType": "donutChart",
                                "projections": {
                                    "Category": [{"queryRef": "Fact_Reviews.Platform"}],
                                    "Y": [{"queryRef": "Fact_Reviews.Total Reviews (Chandni)"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 815.0, "y": 455.0, "z": 9000, "width": 445.0, "height": 240.0,
                        "config": json.dumps({
                            "name": "IssuesDepartmentDonut",
                            "singleVisual": {
                                "visualType": "pieChart",
                                "projections": {
                                    "Category": [{"queryRef": "Fact_CustomerIssues.Responsible_Department"}],
                                    "Y": [{"queryRef": "Fact_CustomerIssues.Total Customer Issues"}]
                                }
                            }
                        })
                    }
                ]
            },
            {
                "id": 1,
                "name": "Section_Calling_Period",
                "displayName": "Calling Operations & Period",
                "displayOption": 1,
                "width": 1280.0,
                "height": 720.0,
                "visualContainers": [
                    {
                        "x": 20.0, "y": 15.0, "z": 0, "width": 1240.0, "height": 55.0,
                        "config": json.dumps({
                            "name": "CallingTitle",
                            "singleVisual": {
                                "visualType": "textbox",
                                "objects": {
                                    "general": [{
                                        "properties": {
                                            "paragraphs": [{
                                                "textRuns": [{
                                                    "value": "Overview Calling Operations - Days Worked, Calling Periods & Series Analysis",
                                                    "textStyle": {"fontSize": "19pt", "fontFamily": "Segoe UI Semibold", "color": "#0F172A"}
                                                }]
                                            }]
                                        }
                                    }]
                                }
                            }
                        })
                    },
                    {
                        "x": 20.0, "y": 80.0, "z": 1000, "width": 395.0, "height": 110.0,
                        "config": json.dumps({
                            "name": "CardCallingDays2",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_DailyCallingOverview.Total Calling Days (User)"}]}
                            }
                        })
                    },
                    {
                        "x": 435.0, "y": 80.0, "z": 2000, "width": 405.0, "height": 110.0,
                        "config": json.dumps({
                            "name": "CardCallsVolume2",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_DailyCallingOverview.Total Calls (Chandni)"}]}
                            }
                        })
                    },
                    {
                        "x": 860.0, "y": 80.0, "z": 3000, "width": 400.0, "height": 110.0,
                        "config": json.dumps({
                            "name": "CardDailyAvg",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_DailyCallingOverview.Avg Calls Per Working Day"}]}
                            }
                        })
                    },
                    {
                        "x": 20.0, "y": 205.0, "z": 4000, "width": 780.0, "height": 490.0,
                        "config": json.dumps({
                            "name": "DailyCallsTimelineChart",
                            "singleVisual": {
                                "visualType": "lineChart",
                                "projections": {
                                    "Category": [{"queryRef": "Fact_DailyCallingOverview.Date"}],
                                    "Y": [{"queryRef": "Fact_DailyCallingOverview.Total Calls (Chandni)"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 815.0, "y": 205.0, "z": 5000, "width": 445.0, "height": 490.0,
                        "config": json.dumps({
                            "name": "SeriesBreakdownBar",
                            "singleVisual": {
                                "visualType": "barChart",
                                "projections": {
                                    "Category": [{"queryRef": "Fact_DailyCallingOverview.Series"}],
                                    "Y": [{"queryRef": "Fact_DailyCallingOverview.Total Calls (Chandni)"}]
                                }
                            }
                        })
                    }
                ]
            },
            {
                "id": 2,
                "name": "Section_Review_Analytics",
                "displayName": "Reviews & CSAT Performance",
                "displayOption": 1,
                "width": 1280.0,
                "height": 720.0,
                "visualContainers": [
                    {
                        "x": 20.0, "y": 15.0, "z": 0, "width": 1240.0, "height": 55.0,
                        "config": json.dumps({
                            "name": "ReviewTitle",
                            "singleVisual": {
                                "visualType": "textbox",
                                "objects": {
                                    "general": [{
                                        "properties": {
                                            "paragraphs": [{
                                                "textRuns": [{
                                                    "value": "Review Generation Analytics (Chandni: 1,734 Verified 5-Star Reviews)",
                                                    "textStyle": {"fontSize": "19pt", "fontFamily": "Segoe UI Semibold", "color": "#0F172A"}
                                                }]
                                            }]
                                        }
                                    }]
                                }
                            }
                        })
                    },
                    {
                        "x": 20.0, "y": 80.0, "z": 1000, "width": 290.0, "height": 110.0,
                        "config": json.dumps({
                            "name": "CardChandniReviewsTotal",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_Reviews.Total Reviews (Chandni)"}]}
                            }
                        })
                    },
                    {
                        "x": 330.0, "y": 80.0, "z": 2000, "width": 290.0, "height": 110.0,
                        "config": json.dumps({
                            "name": "CardReviewsFlipkart",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_Reviews.Reviews Flipkart"}]}
                            }
                        })
                    },
                    {
                        "x": 640.0, "y": 80.0, "z": 3000, "width": 310.0, "height": 110.0,
                        "config": json.dumps({
                            "name": "CardReviewsAmazon",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_Reviews.Reviews Amazon"}]}
                            }
                        })
                    },
                    {
                        "x": 970.0, "y": 80.0, "z": 4000, "width": 290.0, "height": 110.0,
                        "config": json.dumps({
                            "name": "CardCSAT100",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_Reviews.5-Star Rating CSAT %"}]}
                            }
                        })
                    },
                    {
                        "x": 20.0, "y": 205.0, "z": 5000, "width": 780.0, "height": 490.0,
                        "config": json.dumps({
                            "name": "ModelBreakdownBar",
                            "singleVisual": {
                                "visualType": "barChart",
                                "projections": {
                                    "Category": [{"queryRef": "Fact_Reviews.Model_Number"}],
                                    "Y": [{"queryRef": "Fact_Reviews.Total Reviews (Chandni)"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 815.0, "y": 205.0, "z": 6000, "width": 445.0, "height": 490.0,
                        "config": json.dumps({
                            "name": "PlatformReviewSplit",
                            "singleVisual": {
                                "visualType": "donutChart",
                                "projections": {
                                    "Category": [{"queryRef": "Fact_Reviews.Platform"}],
                                    "Y": [{"queryRef": "Fact_Reviews.Total Reviews (Chandni)"}]
                                }
                            }
                        })
                    }
                ]
            },
            {
                "id": 3,
                "name": "Section_Customer_Issues",
                "displayName": "Customer Complaints & Quality",
                "displayOption": 1,
                "width": 1280.0,
                "height": 720.0,
                "visualContainers": [
                    {
                        "x": 20.0, "y": 15.0, "z": 0, "width": 1240.0, "height": 55.0,
                        "config": json.dumps({
                            "name": "IssuesTitle",
                            "singleVisual": {
                                "visualType": "textbox",
                                "objects": {
                                    "general": [{
                                        "properties": {
                                            "paragraphs": [{
                                                "textRuns": [{
                                                    "value": "Customer Issues & Complaints Quality Tracking (273 Issues Handled)",
                                                    "textStyle": {"fontSize": "19pt", "fontFamily": "Segoe UI Semibold", "color": "#0F172A"}
                                                }]
                                            }]
                                        }
                                    }]
                                }
                            }
                        })
                    },
                    {
                        "x": 20.0, "y": 80.0, "z": 1000, "width": 230.0, "height": 110.0,
                        "config": json.dumps({
                            "name": "CardIssuesTotal3",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_CustomerIssues.Total Customer Issues"}]}
                            }
                        })
                    },
                    {
                        "x": 270.0, "y": 80.0, "z": 2000, "width": 230.0, "height": 110.0,
                        "config": json.dumps({
                            "name": "CardProductIssues",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_CustomerIssues.Product Issues Count"}]}
                            }
                        })
                    },
                    {
                        "x": 520.0, "y": 80.0, "z": 3000, "width": 230.0, "height": 110.0,
                        "config": json.dumps({
                            "name": "CardServiceIssues",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_CustomerIssues.Service Issues Count"}]}
                            }
                        })
                    },
                    {
                        "x": 770.0, "y": 80.0, "z": 4000, "width": 240.0, "height": 110.0,
                        "config": json.dumps({
                            "name": "CardRemoteIssues",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_CustomerIssues.Remote Complaints Count"}]}
                            }
                        })
                    },
                    {
                        "x": 1030.0, "y": 80.0, "z": 5000, "width": 230.0, "height": 110.0,
                        "config": json.dumps({
                            "name": "CardInstallIssues",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_CustomerIssues.Installation & Mount Complaints"}]}
                            }
                        })
                    },
                    {
                        "x": 20.0, "y": 205.0, "z": 6000, "width": 780.0, "height": 490.0,
                        "config": json.dumps({
                            "name": "IssuesStateChart",
                            "singleVisual": {
                                "visualType": "barChart",
                                "projections": {
                                    "Category": [{"queryRef": "Fact_CustomerIssues.State"}],
                                    "Y": [{"queryRef": "Fact_CustomerIssues.Total Customer Issues"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 815.0, "y": 205.0, "z": 7000, "width": 445.0, "height": 490.0,
                        "config": json.dumps({
                            "name": "IssuesDeptDonut",
                            "singleVisual": {
                                "visualType": "donutChart",
                                "projections": {
                                    "Category": [{"queryRef": "Fact_CustomerIssues.Responsible_Department"}],
                                    "Y": [{"queryRef": "Fact_CustomerIssues.Total Customer Issues"}]
                                }
                            }
                        })
                    }
                ]
            },
            {
                "id": 4,
                "name": "Section_Email_Support",
                "displayName": "Email Support Operations",
                "displayOption": 1,
                "width": 1280.0,
                "height": 720.0,
                "visualContainers": [
                    {
                        "x": 20.0, "y": 15.0, "z": 0, "width": 1240.0, "height": 55.0,
                        "config": json.dumps({
                            "name": "EmailTitle",
                            "singleVisual": {
                                "visualType": "textbox",
                                "objects": {
                                    "general": [{
                                        "properties": {
                                            "paragraphs": [{
                                                "textRuns": [{
                                                    "value": "Email Support Operations (700+ Total Handled, 25 B2B & B2C Queries)",
                                                    "textStyle": {"fontSize": "19pt", "fontFamily": "Segoe UI Semibold", "color": "#0F172A"}
                                                }]
                                            }]
                                        }
                                    }]
                                }
                            }
                        })
                    },
                    {
                        "x": 20.0, "y": 80.0, "z": 1000, "width": 290.0, "height": 110.0,
                        "config": json.dumps({
                            "name": "CardEmailTotal4",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_EmailSupport.Total Emails Handled"}]}
                            }
                        })
                    },
                    {
                        "x": 330.0, "y": 80.0, "z": 2000, "width": 290.0, "height": 110.0,
                        "config": json.dumps({
                            "name": "CardB2B_B2C",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_EmailSupport.B2B and B2C Emails Handled"}]}
                            }
                        })
                    },
                    {
                        "x": 640.0, "y": 80.0, "z": 3000, "width": 310.0, "height": 110.0,
                        "config": json.dumps({
                            "name": "CardGeneralEmails",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_EmailSupport.General Support Emails"}]}
                            }
                        })
                    },
                    {
                        "x": 970.0, "y": 80.0, "z": 4000, "width": 290.0, "height": 110.0,
                        "config": json.dumps({
                            "name": "CardEmailSLA",
                            "singleVisual": {
                                "visualType": "card",
                                "projections": {"Values": [{"queryRef": "Fact_EmailSupport.Email SLA Compliance %"}]}
                            }
                        })
                    },
                    {
                        "x": 20.0, "y": 205.0, "z": 5000, "width": 780.0, "height": 490.0,
                        "config": json.dumps({
                            "name": "EmailMonthlyChart",
                            "singleVisual": {
                                "visualType": "clusteredColumnChart",
                                "projections": {
                                    "Category": [{"queryRef": "Fact_EmailSupport.Year_Month"}],
                                    "Y": [{"queryRef": "Fact_EmailSupport.Total Emails Handled"}]
                                }
                            }
                        })
                    },
                    {
                        "x": 815.0, "y": 205.0, "z": 6000, "width": 445.0, "height": 490.0,
                        "config": json.dumps({
                            "name": "EmailCategoryDonut",
                            "singleVisual": {
                                "visualType": "pieChart",
                                "projections": {
                                    "Category": [{"queryRef": "Fact_EmailSupport.Category"}],
                                    "Y": [{"queryRef": "Fact_EmailSupport.Total Emails Handled"}]
                                }
                            }
                        })
                    }
                ]
            }
        ]
    }

    # 5. Write to ZIP (.pbit)
    with zipfile.ZipFile(pbit_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types.encode('utf-8'))
        z.writestr('Version', version_str.encode('utf-16le'))
        z.writestr('Settings', json.dumps(settings_dict).encode('utf-16le'))
        z.writestr('Metadata', json.dumps(metadata_dict).encode('utf-16le'))
        z.writestr('DataModelSchema', json.dumps(tmsl_model).encode('utf-16le'))
        z.writestr('Report/Layout', json.dumps(layout_dict).encode('utf-16le'))

    print(f"Successfully generated Power BI Template: {pbit_path} ({os.path.getsize(pbit_path):,} bytes)")

if __name__ == '__main__':
    build_pbit()
