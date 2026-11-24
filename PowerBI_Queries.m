// ==============================================================================
// SKYWORTH & PHILIPS TV - POWER QUERY (M) SCRIPTS
// Instructions:
// 1. In Power BI Desktop, click "Transform Data" -> Power Query Editor.
// 2. Right-click the Queries pane -> "New Query" -> "Blank Query".
// 3. Click "Advanced Editor" and paste each section below into its own query.
// ==============================================================================

// ------------------------------------------------------------------------------
// QUERY 1: Fact_DailyCallingOverview
// ------------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("C:\Users\Chandni Arya\Downloads\Skyworth power bi\Fact_DailyCallingOverview.csv"), [Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Overview_ID", type text},
        {"Date", type date},
        {"Agent", type text},
        {"Platform", type text},
        {"Series", type text},
        {"Calls", Int64.Type},
        {"Ratings", Int64.Type},
        {"Effective_Agent", type text},
        {"Is_User_Portfolio", Int64.Type},
        {"Year_Month", type text},
        {"Month_Name", type text},
        {"Day_Of_Week", type text}
    })
in
    #"Changed Type"

// ------------------------------------------------------------------------------
// QUERY 2: Fact_Reviews
// ------------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("C:\Users\Chandni Arya\Downloads\Skyworth power bi\Fact_Reviews.csv"), [Delimiter=",", Columns=13, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Review_ID", type text},
        {"Date", type date},
        {"Platform", type text},
        {"Brand", type text},
        {"Model_Number", type text},
        {"Screen_Size", type text},
        {"Series", type text},
        {"Customer_Name", type text},
        {"Customer_Phone", type text},
        {"Rating", Int64.Type},
        {"Original_Agent", type text},
        {"Effective_Agent", type text},
        {"Is_User_Review", Int64.Type},
        {"Year_Month", type text}
    })
in
    #"Changed Type"

// ------------------------------------------------------------------------------
// QUERY 3: Fact_CustomerIssues
// ------------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("C:\Users\Chandni Arya\Downloads\Skyworth power bi\Fact_CustomerIssues.csv"), [Delimiter=",", Columns=16, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Issue_ID", type text},
        {"Date", type date},
        {"Customer_Name", type text},
        {"Customer_Phone", type text},
        {"Order_ID", type text},
        {"City", type text},
        {"State", type text},
        {"Model", type text},
        {"Screen_Size", type text},
        {"Series", type text},
        {"Issue_Description", type text},
        {"Responsible_Department", type text},
        {"TAT_Resolution", type text},
        {"Status", type text},
        {"Resolution_Feedback", type text},
        {"Is_Added_Issue", type text},
        {"Year_Month", type text}
    })
in
    #"Changed Type"

// ------------------------------------------------------------------------------
// QUERY 4: Fact_EmailSupport
// ------------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("C:\Users\Chandni Arya\Downloads\Skyworth power bi\Fact_EmailSupport.csv"), [Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Email_ID", type text},
        {"Date", type date},
        {"Category", type text},
        {"Subject", type text},
        {"Handled_By", type text},
        {"Action_Taken", type text},
        {"Status", type text},
        {"Resolution_Hours", Int64.Type},
        {"Is_B2B_B2C", type text},
        {"Year_Month", type text}
    })
in
    #"Changed Type"

// ------------------------------------------------------------------------------
// QUERY 5: Fact_Calls
// ------------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("C:\Users\Chandni Arya\Downloads\Skyworth power bi\Fact_CallActivity.csv"), [Delimiter=",", Columns=27, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Call_ID", type text},
        {"Date", type date},
        {"Platform", type text},
        {"Brand", type text},
        {"Model_Number", type text},
        {"Screen_Size", type text},
        {"Series", type text},
        {"Display_Type", type text},
        {"Order_ID", type text},
        {"Customer_Name", type text},
        {"Customer_Phone", type text},
        {"City", type text},
        {"State", type text},
        {"Call_Status", type text},
        {"Call_Category", type text},
        {"Remark", type text},
        {"Remark_Category", type text},
        {"Review_Status", type text},
        {"Status", type text},
        {"Rate", Int64.Type},
        {"Is_Picked", Int64.Type},
        {"Is_Reviewed", Int64.Type},
        {"Has_Coupon_Assigned", type text},
        {"Assigned_Voucher_ID", type text},
        {"Assigned_Coupon_Code", type text},
        {"Assigned_Coupon_Amount", Int64.Type}
    })
in
    #"Changed Type"

// ------------------------------------------------------------------------------
// QUERY 6: Fact_Coupons
// ------------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("C:\Users\Chandni Arya\Downloads\Skyworth power bi\Fact_Coupons.csv"), [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Voucher_ID", type text},
        {"Platform", type text},
        {"Voucher_Code", type text},
        {"Pin_Or_Ref", type text},
        {"Amount", Int64.Type},
        {"Expiry_Date", type date},
        {"Customer_Name", type text},
        {"Customer_Phone", type text},
        {"Rate", Int64.Type},
        {"Date_Shared", type date},
        {"Verification_Note", type text},
        {"Voucher_Status", type text}
    })
in
    #"Changed Type"

// ------------------------------------------------------------------------------
// QUERY 7: Dim_Product
// ------------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("C:\Users\Chandni Arya\Downloads\Skyworth power bi\Dim_Product.csv"), [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Model_Number", type text},
        {"Brand", type text},
        {"Screen_Size", type text},
        {"Series", type text},
        {"Display_Type", type text},
        {"Resolution", type text},
        {"Operating_System", type text}
    })
in
    #"Changed Type"

// ------------------------------------------------------------------------------
// QUERY 8: Dim_Calendar
// ------------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("C:\Users\Chandni Arya\Downloads\Skyworth power bi\Dim_Calendar.csv"), [Delimiter=",", Columns=11, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Date", type date},
        {"Date_Key", Int64.Type},
        {"Year", Int64.Type},
        {"Month", Int64.Type},
        {"Month_Name", type text},
        {"Month_Short", type text},
        {"Year_Month", type text},
        {"Quarter", type text},
        {"Week_Number", Int64.Type},
        {"Day_Name", type text},
        {"Is_Weekend", Int64.Type}
    })
in
    #"Changed Type"
