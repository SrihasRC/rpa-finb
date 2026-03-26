# UiPath v1 (CSV Processing) - Step-by-Step Guide

## Overview

This guide provides **literal, activity-by-activity instructions** for building the UiPath v1 automation that processes CSV files through the compliance API.

**Total time to build**: ~45-60 minutes  
**Difficulty**: Beginner to Intermediate  
**Prerequisites**: UiPath Studio installed, Python API running

---

## Table of Contents

1. [Project Setup](#1-project-setup)
2. [Define Variables](#2-define-variables)
3. [Initialize Workflow](#3-initialize-workflow)
4. [Read CSV File](#4-read-csv-file)
5. [Process Each Transaction](#5-process-each-transaction)
6. [Build API Request](#6-build-api-request)
7. [Send HTTP Request](#7-send-http-request)
8. [Parse JSON Response](#8-parse-json-response)
9. [Write Results to Excel](#9-write-results-to-excel)
10. [Error Handling](#10-error-handling)
11. [Logging and Reporting](#11-logging-and-reporting)
12. [Final Testing](#12-final-testing)

---

## 1. Project Setup

### Step 1.1: Create New Project

1. Open **UiPath Studio**
2. Click **Process** (not Library or Template)
3. In the "New Blank Process" window:
   - **Name**: `ComplianceMonitoring_CSV`
   - **Location**: Choose your preferred folder
   - **Description**: `RPA v1 - Batch CSV processing for financial compliance monitoring`
4. Click **Create**

### Step 1.2: Install Required Packages

1. In UiPath Studio, go to **Manage Packages** (top ribbon or Ctrl+P)
2. Click **Official** tab
3. Search and install the following packages:
   - **UiPath.WebAPI.Activities** (for HTTP requests) - Install latest stable version
   - **UiPath.Excel.Activities** (for Excel operations) - Install latest stable version
   - **Newtonsoft.Json** (for JSON handling) - Install latest stable version
4. Click **Save** and wait for installation to complete

### Step 1.3: Verify Main Workflow

1. In the **Project** panel (left side), you should see `Main.xaml`
2. Double-click `Main.xaml` to open it
3. You should see an empty workflow canvas

---

## 2. Define Variables

We'll define variables as we build the workflow. Here's a complete reference for quick lookup:

| Variable Name | Type | Scope | Default Value | Purpose |
|---------------|------|-------|---------------|---------|
| `csvFilePath` | String | Main | `"C:\RPA\input_transactions.csv"` | Path to input CSV |
| `excelOutputPath` | String | Main | `"C:\RPA\compliance_results.xlsx"` | Path to output Excel |
| `apiBaseUrl` | String | Main | `"http://localhost:8000"` | API base URL |
| `dtTransactions` | DataTable | Main | - | Holds CSV data |
| `dtResults` | DataTable | Main | - | Holds results for Excel |
| `rowIndex` | Int32 | ForEach | `0` | Current row counter |
| `totalRows` | Int32 | Main | `0` | Total transactions |
| `currentRow` | DataRow | ForEach | - | Current transaction row |
| `jsonPayload` | String | ForEach | - | API request JSON |
| `apiResponse` | String | ForEach | - | API response JSON |
| `httpStatusCode` | Int32 | ForEach | - | HTTP status code |
| `riskScore` | Double | ForEach | - | Parsed risk score |
| `riskLevel` | String | ForEach | - | Parsed risk level |
| `flaggedRules` | String | ForEach | - | Comma-separated rules |
| `requiresReview` | Boolean | ForEach | - | Review flag |

**Note**: We'll create these variables step-by-step in the sections below. Don't create them all at once.

---

## 3. Initialize Workflow

### Step 3.1: Add Flowchart Container

1. In the **Activities** panel (left side), search for `Flowchart`
2. Drag **Flowchart** activity onto the canvas inside `Main.xaml`
3. In the Properties panel (right side):
   - **DisplayName**: `Compliance Monitoring Flowchart`

### Step 3.2: Add Start Node - Assign Activity (Initialize Paths)

1. Inside the Flowchart, search for `Assign` in Activities
2. Drag **Assign** activity onto the flowchart canvas
3. Connect the **Start** node to this Assign activity (click and drag the arrow)
4. Click on the Assign activity to open its properties:
   - **DisplayName**: `Initialize File Paths`
   - Click inside the **To** field: Type `csvFilePath` and press **Ctrl+K** to create variable
     - In the popup, **Name**: `csvFilePath`, **Variable type**: `String`, **Scope**: `Main`, click **OK**
   - In the **Value** field: Type `"C:\RPA\input_transactions.csv"`

### Step 3.3: Add Second Assign (Output Path)

1. Drag another **Assign** activity below the first one
2. Connect the first Assign to this one (drag arrow from bottom of first to top of second)
3. Configure:
   - **DisplayName**: `Initialize Output Path`
   - **To**: `excelOutputPath` (press Ctrl+K to create variable, Type: String, Scope: Main)
   - **Value**: `"C:\RPA\compliance_results.xlsx"`

### Step 3.4: Add Third Assign (API URL)

1. Drag another **Assign** activity
2. Connect to previous Assign
3. Configure:
   - **DisplayName**: `Set API Base URL`
   - **To**: `apiBaseUrl` (Ctrl+K, String, Main)
   - **Value**: `"http://localhost:8000"`

### Step 3.5: Add Log Message (Start Notification)

1. Search for `Log Message` in Activities
2. Drag **Log Message** activity and connect to the API URL assign
3. Configure:
   - **DisplayName**: `Log Process Start`
   - **Level**: `Info` (from dropdown)
   - **Message**: `"Starting Compliance Monitoring Process - v1 CSV Mode"`

---

## 4. Read CSV File

### Step 4.1: Add Read CSV Activity

1. Search for `Read CSV` in Activities panel
2. Drag **Read CSV** activity onto flowchart and connect to the Log Message
3. Configure properties:
   - **DisplayName**: `Read Input CSV File`
   - **File path**: `csvFilePath` (the variable we created)
   - **Output DataTable**: Click in the field, type `dtTransactions`, press **Ctrl+K**
     - **Name**: `dtTransactions`
     - **Variable type**: Click dropdown → Browse → Search for `DataTable` → Select `System.Data.DataTable`
     - **Scope**: `Main`
     - Click **OK**

### Step 4.2: Add Row Count Assignment

1. Drag **Assign** activity and connect to Read CSV
2. Configure:
   - **DisplayName**: `Count Total Rows`
   - **To**: `totalRows` (Ctrl+K, type: Int32, scope: Main)
   - **Value**: `dtTransactions.Rows.Count`

### Step 4.3: Add Log Message (Row Count)

1. Drag **Log Message** activity
2. Connect to the row count Assign
3. Configure:
   - **DisplayName**: `Log Total Transactions`
   - **Level**: `Info`
   - **Message**: `"Total transactions to process: " + totalRows.ToString`

---

## 5. Process Each Transaction

### Step 5.1: Initialize Results DataTable

1. Drag **Assign** activity
2. Connect to the log message
3. Configure:
   - **DisplayName**: `Initialize Results DataTable`
   - **To**: `dtResults` (Ctrl+K, type: DataTable, scope: Main)
   - **Value**: `New DataTable`

### Step 5.2: Add Column Headers to Results

1. Drag **Invoke Code** activity
2. Connect to Initialize Results DataTable
3. Configure:
   - **DisplayName**: `Add Result Columns`
   - Click **Edit Code** button
   - In the code editor window, paste this code:

```vb
dtResults.Columns.Add("transaction_id", GetType(String))
dtResults.Columns.Add("customer_id", GetType(String))
dtResults.Columns.Add("amount", GetType(Double))
dtResults.Columns.Add("risk_score", GetType(Double))
dtResults.Columns.Add("risk_level", GetType(String))
dtResults.Columns.Add("flagged_rules", GetType(String))
dtResults.Columns.Add("requires_review", GetType(String))
dtResults.Columns.Add("timestamp", GetType(String))
```

4. Click **Save**
5. In the **Arguments** section at the bottom of Invoke Code properties:
   - Click **Add argument**
   - **Name**: `dtResults`
   - **Direction**: `In/Out`
   - **Type**: `DataTable`
   - **Value**: `dtResults`

### Step 5.3: Add For Each Row Loop

1. Search for `For Each Row` in Activities
2. Drag **For Each Row** activity
3. Connect to Add Result Columns
4. Configure:
   - **DisplayName**: `Process Each Transaction`
   - **DataTable**: `dtTransactions` (from dropdown or type it)
   - The loop automatically creates a variable `CurrentRow` of type `DataRow`

### Step 5.4: Add Row Counter Inside Loop

1. **Inside** the For Each Row activity's **Body** section, drag an **Assign** activity
2. Configure:
   - **DisplayName**: `Initialize Row Index`
   - **To**: `rowIndex` (Ctrl+K, type: Int32, scope: ForEachRow - make sure scope is the loop, not Main!)
   - **Value**: `0`

3. Drag another **Assign** below it
4. Configure:
   - **DisplayName**: `Increment Row Index`
   - **To**: `rowIndex`
   - **Value**: `rowIndex + 1`

### Step 5.5: Add Progress Log

1. Still inside the For Each Row body, drag **Log Message**
2. Configure:
   - **DisplayName**: `Log Progress`
   - **Level**: `Info`
   - **Message**: `"Processing transaction " + rowIndex.ToString + " of " + totalRows.ToString + " - ID: " + CurrentRow("transaction_id").ToString`

---

## 6. Build API Request

### Step 6.1: Add Assign Activity (Build JSON Payload)

1. Inside For Each Row, after the Log Progress, drag **Assign** activity
2. Configure:
   - **DisplayName**: `Build JSON Payload`
   - **To**: `jsonPayload` (Ctrl+K, String, scope: ForEachRow)
   - **Value**: Paste this multi-line string (all one line in UiPath):

```
"{" + """transaction_id"": """ + CurrentRow("transaction_id").ToString + """, " + """customer_id"": """ + CurrentRow("customer_id").ToString + """, " + """amount"": " + CurrentRow("amount").ToString + ", " + """transaction_type"": """ + CurrentRow("transaction_type").ToString + """, " + """location"": """ + CurrentRow("location").ToString + """, " + """is_high_risk_country"": " + CurrentRow("is_high_risk_country").ToString.ToLower + ", " + """is_cash"": " + CurrentRow("is_cash").ToString.ToLower + ", " + """is_round_amount"": " + CurrentRow("is_round_amount").ToString.ToLower + ", " + """unusual_time"": " + CurrentRow("unusual_time").ToString.ToLower + ", " + """recipient_new"": " + CurrentRow("recipient_new").ToString.ToLower + ", " + """txn_count_last_24h"": " + CurrentRow("txn_count_last_24h").ToString + ", " + """avg_txn_amount"": " + CurrentRow("avg_txn_amount").ToString + ", " + """customer_risk_score"": " + CurrentRow("customer_risk_score").ToString + ", " + """days_since_last_txn"": " + CurrentRow("days_since_last_txn").ToString + ", " + """is_offshore"": " + CurrentRow("is_offshore").ToString.ToLower + ", " + """velocity_score"": " + CurrentRow("velocity_score").ToString + ", " + """hour_of_day"": " + CurrentRow("hour_of_day").ToString + ", " + """day_of_week"": " + CurrentRow("day_of_week").ToString + "}"
```

**Note**: This is complex. Alternatively, use the simpler approach in Step 6.2.

### Step 6.2: Alternative - Use Deserialize/Serialize (Recommended)

Instead of Step 6.1, use this approach:

1. Drag **Invoke Code** activity
2. Configure:
   - **DisplayName**: `Build JSON from DataRow`
   - Click **Edit Code**, paste:

```vb
Dim jsonDict As New Dictionary(Of String, Object)
jsonDict("transaction_id") = CurrentRow("transaction_id").ToString
jsonDict("customer_id") = CurrentRow("customer_id").ToString
jsonDict("amount") = CDbl(CurrentRow("amount"))
jsonDict("transaction_type") = CurrentRow("transaction_type").ToString
jsonDict("location") = CurrentRow("location").ToString
jsonDict("is_high_risk_country") = CBool(CurrentRow("is_high_risk_country"))
jsonDict("is_cash") = CBool(CurrentRow("is_cash"))
jsonDict("is_round_amount") = CBool(CurrentRow("is_round_amount"))
jsonDict("unusual_time") = CBool(CurrentRow("unusual_time"))
jsonDict("recipient_new") = CBool(CurrentRow("recipient_new"))
jsonDict("txn_count_last_24h") = CInt(CurrentRow("txn_count_last_24h"))
jsonDict("avg_txn_amount") = CDbl(CurrentRow("avg_txn_amount"))
jsonDict("customer_risk_score") = CDbl(CurrentRow("customer_risk_score"))
jsonDict("days_since_last_txn") = CInt(CurrentRow("days_since_last_txn"))
jsonDict("is_offshore") = CBool(CurrentRow("is_offshore"))
jsonDict("velocity_score") = CDbl(CurrentRow("velocity_score"))
jsonDict("hour_of_day") = CInt(CurrentRow("hour_of_day"))
jsonDict("day_of_week") = CInt(CurrentRow("day_of_week"))

jsonPayload = Newtonsoft.Json.JsonConvert.SerializeObject(jsonDict)
```

3. Add Arguments:
   - **CurrentRow**: In, DataRow, `CurrentRow`
   - **jsonPayload**: Out, String, `jsonPayload` (create if needed)

---

## 7. Send HTTP Request

### Step 7.1: Add HTTP Request Activity

1. Search for `HTTP Request` in Activities (from UiPath.WebAPI.Activities package)
2. Drag **HTTP Request** activity after the JSON building step
3. Configure properties (in Properties panel on right):
   - **DisplayName**: `POST Compliance Check`
   - **Endpoint**: `apiBaseUrl + "/compliance-check"`
   - **Method**: `POST` (select from dropdown)
   - **Body**: Click the `...` button, then:
     - **Type**: `application/json`
     - **Content**: `jsonPayload`
   - **Headers**: Leave empty (default headers are fine)
   - **Result**: Click in field, type `apiResponse` (Ctrl+K, String, scope: ForEachRow)
   - **ResponseStatusCode**: Click in field, type `httpStatusCode` (Ctrl+K, Int32, scope: ForEachRow)

### Step 7.2: Add Status Code Check

1. Drag **Flow Decision** activity after HTTP Request
2. Configure:
   - **DisplayName**: `Check HTTP Success`
   - **Condition**: `httpStatusCode = 200`
   - This creates True and False branches

### Step 7.3: Add Error Log for Failed Requests (False Branch)

1. On the **False** branch of the Flow Decision, drag **Log Message**
2. Configure:
   - **DisplayName**: `Log API Error`
   - **Level**: `Error`
   - **Message**: `"API request failed for transaction " + CurrentRow("transaction_id").ToString + " - Status: " + httpStatusCode.ToString`
3. After this Log Message, add **Continue** activity (searches for "Continue") - this skips to next iteration

---

## 8. Parse JSON Response

### Step 8.1: Add Deserialize JSON Activity (True Branch)

1. On the **True** branch of the HTTP success check, drag **Deserialize JSON** activity
2. Configure:
   - **DisplayName**: `Parse API Response`
   - **JsonString**: `apiResponse`
   - **JsonObject**: Click field, type `jsonResponse` (Ctrl+K, type: JObject - search for Newtonsoft.Json.Linq.JObject, scope: ForEachRow)

### Step 8.2: Extract Risk Score

1. Drag **Assign** activity
2. Configure:
   - **DisplayName**: `Extract Risk Score`
   - **To**: `riskScore` (Ctrl+K, Double, scope: ForEachRow)
   - **Value**: `CDbl(jsonResponse("risk_score").ToString)`

### Step 8.3: Extract Risk Level

1. Drag **Assign** activity
2. Configure:
   - **DisplayName**: `Extract Risk Level`
   - **To**: `riskLevel` (Ctrl+K, String, scope: ForEachRow)
   - **Value**: `jsonResponse("risk_level").ToString`

### Step 8.4: Extract Flagged Rules

1. Drag **Assign** activity
2. Configure:
   - **DisplayName**: `Extract Flagged Rules`
   - **To**: `flaggedRules` (Ctrl+K, String, scope: ForEachRow)
   - **Value**: `String.Join(", ", jsonResponse("flagged_rules").Select(Function(x) x.ToString))`

### Step 8.5: Extract Requires Review

1. Drag **Assign** activity
2. Configure:
   - **DisplayName**: `Extract Review Flag`
   - **To**: `requiresReview` (Ctrl+K, Boolean, scope: ForEachRow)
   - **Value**: `CBool(jsonResponse("requires_review").ToString)`

---

## 9. Write Results to Excel

### Step 9.1: Add Row to Results DataTable

1. Drag **Add Data Row** activity
2. Configure:
   - **DisplayName**: `Add Result Row`
   - **DataTable**: `dtResults`
   - **ArrayRow**: Click the `{}` button and paste:

```vb
{
    CurrentRow("transaction_id").ToString,
    CurrentRow("customer_id").ToString,
    CDbl(CurrentRow("amount")),
    riskScore,
    riskLevel,
    flaggedRules,
    If(requiresReview, "YES", "NO"),
    DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss")
}
```

### Step 9.2: Write to Excel (Outside Loop)

**Important**: This step goes **OUTSIDE** the For Each Row loop, after it completes.

1. After the For Each Row activity ends, drag **Write Range** activity
2. Configure:
   - **DisplayName**: `Write Results to Excel`
   - **Workbook path**: `excelOutputPath`
   - **Sheet name**: `"Compliance Results"`
   - **Data table**: `dtResults`
   - **Add headers**: ✓ (checked)
   - **Starting cell**: `"A1"`

### Step 9.3: Add Completion Log

1. Drag **Log Message** after Write Range
2. Configure:
   - **DisplayName**: `Log Completion`
   - **Level**: `Info`
   - **Message**: `"Process completed! Results written to " + excelOutputPath + " - Total rows: " + totalRows.ToString`

---

## 10. Error Handling

### Step 10.1: Add Try-Catch Wrapper

1. Right-click on the entire flowchart content
2. Select **Surround with** → **Try Catch**
3. The entire workflow moves inside the **Try** section

### Step 10.2: Configure Catch Block

1. In the **Catches** section of Try Catch, click **Add new catch**
2. Select **System.Exception** from exception type dropdown
3. Inside the Catch block, drag **Log Message**
4. Configure:
   - **DisplayName**: `Log Critical Error`
   - **Level**: `Error`
   - **Message**: `"CRITICAL ERROR: " + exception.Message + " | StackTrace: " + exception.StackTrace`

### Step 10.3: Add Retry Logic (Optional Advanced)

For production robustness, you can add retry logic inside the For Each loop for HTTP requests:

1. Surround the HTTP Request activity with **Retry Scope**
2. Configure Retry Scope:
   - **DisplayName**: `Retry API Request`
   - **NumberOfRetries**: `3`
   - **RetryInterval**: `00:00:02` (2 seconds)

---

## 11. Logging and Reporting

### Step 11.1: Add Summary Statistics

After the Write Range activity (outside all loops):

1. Drag **Invoke Code** activity
2. Configure:
   - **DisplayName**: `Calculate Summary Stats`
   - Click **Edit Code**, paste:

```vb
Dim highRiskCount As Integer = dtResults.Select("risk_level = 'HIGH'").Length
Dim mediumRiskCount As Integer = dtResults.Select("risk_level = 'MEDIUM'").Length
Dim lowRiskCount As Integer = dtResults.Select("risk_level = 'LOW'").Length
Dim reviewRequiredCount As Integer = dtResults.Select("requires_review = 'YES'").Length

summaryMessage = "SUMMARY STATISTICS:" + Environment.NewLine + _
                 "- Total Processed: " + totalRows.ToString + Environment.NewLine + _
                 "- High Risk: " + highRiskCount.ToString + Environment.NewLine + _
                 "- Medium Risk: " + mediumRiskCount.ToString + Environment.NewLine + _
                 "- Low Risk: " + lowRiskCount.ToString + Environment.NewLine + _
                 "- Requires Review: " + reviewRequiredCount.ToString
```

3. Add Arguments:
   - **dtResults**: In, DataTable, `dtResults`
   - **totalRows**: In, Int32, `totalRows`
   - **summaryMessage**: Out, String, `summaryMessage` (Ctrl+K to create new variable, String, Main)

### Step 11.2: Log Summary

1. Drag **Log Message** after the Invoke Code
2. Configure:
   - **DisplayName**: `Log Summary Statistics`
   - **Level**: `Info`
   - **Message**: `summaryMessage`

### Step 11.3: Add Message Box (Optional)

For desktop testing, you can show a popup:

1. Drag **Message Box** activity
2. Configure:
   - **DisplayName**: `Show Completion Dialog`
   - **Caption**: `"Compliance Processing Complete"`
   - **Text**: `summaryMessage + Environment.NewLine + Environment.NewLine + "Results saved to: " + excelOutputPath`
   - **Buttons**: `OK`

---

## 12. Final Testing

### Step 12.1: Verify All Variables

1. Click on **Variables** panel at bottom of UiPath Studio
2. Verify all variables have correct **Type** and **Scope**
3. No variables should show errors (red underline)

### Step 12.2: Validate Workflow

1. Click **Validate** button in top ribbon (or press F8)
2. Check **Output** panel for any errors
3. Fix any validation errors before running

### Step 12.3: Create Test CSV

Create a file `C:\RPA\input_transactions.csv` with this content:

```csv
transaction_id,customer_id,amount,transaction_type,location,is_high_risk_country,is_cash,is_round_amount,unusual_time,recipient_new,txn_count_last_24h,avg_txn_amount,customer_risk_score,days_since_last_txn,is_offshore,velocity_score,hour_of_day,day_of_week
TXN001,CUST001,15000.00,wire_transfer,Cayman Islands,True,False,True,True,True,5,12000.00,0.75,2,True,0.85,23,5
TXN002,CUST002,500.00,deposit,New York,False,False,False,False,False,1,500.00,0.25,10,False,0.10,14,2
```

### Step 12.4: Start API Server

1. Open terminal/command prompt
2. Navigate to project directory: `cd C:\path\to\rpa-finb`
3. Activate virtual environment: `venv\Scripts\activate`
4. Start API: `uvicorn api.main:app --reload`
5. Verify API is running: Open browser to `http://localhost:8000`

### Step 12.5: Run the Workflow

1. In UiPath Studio, click **Run** (or press F5)
2. Watch the **Output** panel for log messages
3. Workflow should complete without errors
4. Check `C:\RPA\compliance_results.xlsx` - should contain 2 rows of results

### Step 12.6: Debug Issues

If errors occur:

1. **CSV not found**: Verify path in `csvFilePath` variable matches actual file location
2. **API connection failed**: Ensure API is running on `http://localhost:8000`
3. **JSON parsing error**: Check CSV data format - booleans should be True/False, numbers should not have quotes
4. **Excel write failed**: Close Excel file if it's open, check write permissions on folder

---

## Workflow Summary Diagram

```
START
  ↓
[Initialize File Paths] → csvFilePath, excelOutputPath, apiBaseUrl
  ↓
[Read CSV File] → dtTransactions
  ↓
[Count Total Rows] → totalRows
  ↓
[Initialize Results DataTable] → dtResults + columns
  ↓
[FOR EACH ROW in dtTransactions]
  ↓
  [Build JSON Payload] → jsonPayload
  ↓
  [HTTP POST to /compliance-check] → apiResponse, httpStatusCode
  ↓
  [Status = 200?]
    ├─ NO → [Log Error] → Continue
    └─ YES → [Parse JSON Response]
              ↓
              [Extract: riskScore, riskLevel, flaggedRules, requiresReview]
              ↓
              [Add Row to dtResults]
[END FOR EACH]
  ↓
[Write Range to Excel] → compliance_results.xlsx
  ↓
[Calculate Summary Statistics]
  ↓
[Log Summary]
  ↓
END
```

---

## Next Steps

After completing this workflow:

1. ✅ Review **VARIABLES.md** for complete variable reference
2. ✅ Review **TESTING.md** for comprehensive testing procedures
3. ✅ Read **../getting-started/FLOW_GUIDE.md** to understand where this fits in the overall system
4. 🔄 Consider building **UiPath v2 (Web Portal)** for live transaction monitoring

---

## Troubleshooting

### Common Issues and Solutions

**Issue**: "Activity validation failed: Type 'DataTable' not found"  
**Solution**: Make sure to select `System.Data.DataTable` (not just typing "DataTable")

**Issue**: "HTTP Request failed with 404"  
**Solution**: Verify API endpoint is `/compliance-check` and API is running

**Issue**: "Cannot deserialize JSON"  
**Solution**: Add Log Message before Deserialize to see actual `apiResponse` content - check for error messages from API

**Issue**: "Add Data Row failed - column count mismatch"  
**Solution**: Verify ArrayRow has exactly 8 elements matching dtResults column count

**Issue**: "For Each Row not iterating"  
**Solution**: Check dtTransactions has data - add Log Message with `dtTransactions.Rows.Count.ToString`

---

## Performance Tips

1. **Batch Processing**: For 1000+ transactions, consider processing in batches of 100 and writing intermediate results
2. **Parallel Processing**: UiPath Enterprise can use Parallel For Each for faster processing
3. **API Optimization**: If API is slow, increase timeout in HTTP Request properties
4. **Memory Management**: For very large CSVs (100k+ rows), use Read Range with filtering instead of loading entire file

---

## Documentation References

- **Architecture**: `docs/architecture/ARCHITECTURE.md`
- **API Endpoints**: `docs/api/ENDPOINTS.md`
- **Installation**: `docs/getting-started/INSTALLATION.md`
- **Quick Reference**: `QUICK_REFERENCE.md`

---

**Document Version**: 1.0  
**Last Updated**: 2026-03-26  
**Author**: RPA Compliance Monitoring Team
