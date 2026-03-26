# UiPath v1 Variables Reference

## Overview

This document lists **all variables** used in the UiPath v1 (CSV Processing) workflow with complete details for quick reference.

---

## Variable Quick Reference Table

| Variable Name | Type | Scope | Default Value | Description |
|---------------|------|-------|---------------|-------------|
| `csvFilePath` | String | Main | `"C:\RPA\input_transactions.csv"` | Path to input CSV file containing transactions |
| `excelOutputPath` | String | Main | `"C:\RPA\compliance_results.xlsx"` | Path where Excel results will be saved |
| `apiBaseUrl` | String | Main | `"http://localhost:8000"` | Base URL of the FastAPI compliance server |
| `dtTransactions` | DataTable | Main | - | DataTable holding all transactions from CSV |
| `dtResults` | DataTable | Main | - | DataTable holding processed results for Excel output |
| `rowIndex` | Int32 | ForEachRow | `0` | Counter for current row number (1-based) |
| `totalRows` | Int32 | Main | `0` | Total number of transactions to process |
| `CurrentRow` | DataRow | ForEachRow | - | Current transaction row (auto-created by For Each Row) |
| `jsonPayload` | String | ForEachRow | - | JSON string sent in API request body |
| `apiResponse` | String | ForEachRow | - | Raw JSON response from API |
| `httpStatusCode` | Int32 | ForEachRow | - | HTTP status code (200 = success) |
| `jsonResponse` | JObject | ForEachRow | - | Parsed JSON response object |
| `riskScore` | Double | ForEachRow | - | Extracted risk score (0.0-1.0) |
| `riskLevel` | String | ForEachRow | - | Extracted risk level (LOW/MEDIUM/HIGH) |
| `flaggedRules` | String | ForEachRow | - | Comma-separated list of flagged compliance rules |
| `requiresReview` | Boolean | ForEachRow | - | Whether transaction requires manual review |
| `summaryMessage` | String | Main | - | Summary statistics message for logging |
| `exception` | Exception | Catch | - | Exception object in error handling (auto-created) |

---

## Detailed Variable Descriptions

### Configuration Variables

#### csvFilePath
- **Type**: `System.String`
- **Scope**: `Main`
- **Default**: `"C:\RPA\input_transactions.csv"`
- **Purpose**: Specifies the location of the input CSV file containing transactions
- **How to Create**: 
  1. Assign activity: To = `csvFilePath` (Ctrl+K)
  2. Select Type: `String`
  3. Value = `"C:\RPA\input_transactions.csv"`
- **Notes**: 
  - Must be absolute path
  - File must exist before workflow runs
  - CSV must have 18 columns (see CSV format below)

#### excelOutputPath
- **Type**: `System.String`
- **Scope**: `Main`
- **Default**: `"C:\RPA\compliance_results.xlsx"`
- **Purpose**: Specifies where the Excel output file will be saved
- **How to Create**: Same as csvFilePath
- **Notes**:
  - File will be overwritten if it exists
  - Parent directory must exist
  - No need to create file manually

#### apiBaseUrl
- **Type**: `System.String`
- **Scope**: `Main`
- **Default**: `"http://localhost:8000"`
- **Purpose**: Base URL for the compliance API server
- **How to Create**: Same as csvFilePath
- **Notes**:
  - Change to production URL when deploying
  - No trailing slash
  - Must include protocol (http:// or https://)

---

### Data Storage Variables

#### dtTransactions
- **Type**: `System.Data.DataTable`
- **Scope**: `Main`
- **Default**: None (populated by Read CSV)
- **Purpose**: Stores all transaction data read from CSV file
- **How to Create**:
  1. In Read CSV activity, Output field
  2. Type `dtTransactions` and press Ctrl+K
  3. Select Type: Browse → Search "DataTable" → Select `System.Data.DataTable`
- **Structure**: 18 columns matching CSV headers
- **Notes**: 
  - Automatically populated by Read CSV activity
  - Access columns: `dtTransactions.Rows(0)("column_name")`
  - Get row count: `dtTransactions.Rows.Count`

#### dtResults
- **Type**: `System.Data.DataTable`
- **Scope**: `Main`
- **Default**: `New DataTable` (then columns added)
- **Purpose**: Stores processed results to write to Excel
- **How to Create**:
  1. Assign activity: To = `dtResults`, Value = `New DataTable`
  2. Use Invoke Code to add columns (see Step 5.2 in STEP_BY_STEP.md)
- **Structure**: 8 columns:
  - `transaction_id` (String)
  - `customer_id` (String)
  - `amount` (Double)
  - `risk_score` (Double)
  - `risk_level` (String)
  - `flagged_rules` (String)
  - `requires_review` (String)
  - `timestamp` (String)
- **Notes**: Rows added dynamically in For Each loop

---

### Loop Control Variables

#### rowIndex
- **Type**: `System.Int32`
- **Scope**: `ForEachRow` (the For Each Row activity)
- **Default**: `0`
- **Purpose**: Tracks current row number for logging progress
- **How to Create**: Assign activity inside loop
- **Usage**: 
  - Initialize to 0 at start of loop
  - Increment by 1 each iteration: `rowIndex = rowIndex + 1`
- **Notes**: 1-based index (starts at 1 after first increment)

#### totalRows
- **Type**: `System.Int32`
- **Scope**: `Main`
- **Default**: `0`
- **Purpose**: Stores total transaction count for progress reporting
- **How to Create**: Assign activity
- **Value**: `dtTransactions.Rows.Count`
- **Notes**: Set once after reading CSV, before loop

#### CurrentRow
- **Type**: `System.Data.DataRow`
- **Scope**: `ForEachRow`
- **Default**: Auto-created by For Each Row activity
- **Purpose**: Represents the current transaction row being processed
- **How to Create**: Automatically created - don't manually create
- **Usage**: Access columns via `CurrentRow("column_name")`
- **Example**: `CurrentRow("transaction_id").ToString`

---

### API Request Variables

#### jsonPayload
- **Type**: `System.String`
- **Scope**: `ForEachRow`
- **Default**: None (built each iteration)
- **Purpose**: Holds JSON string sent to API in request body
- **How to Create**: Assign or Invoke Code activity
- **Format**: JSON object with 18 transaction fields
- **Example**:
```json
{
  "transaction_id": "TXN001",
  "customer_id": "CUST001",
  "amount": 15000.00,
  ...
}
```
- **Notes**: Must match API schema exactly

#### apiResponse
- **Type**: `System.String`
- **Scope**: `ForEachRow`
- **Default**: None (set by HTTP Request)
- **Purpose**: Stores raw JSON response from API
- **How to Create**: In HTTP Request activity, Result property
- **Example Response**:
```json
{
  "transaction_id": "TXN001",
  "risk_score": 0.85,
  "risk_level": "HIGH",
  "flagged_rules": ["BSA_LARGE_CASH", "FATF_HIGH_RISK"],
  "requires_review": true,
  "timestamp": "2024-03-26T10:30:15"
}
```

#### httpStatusCode
- **Type**: `System.Int32`
- **Scope**: `ForEachRow`
- **Default**: None (set by HTTP Request)
- **Purpose**: HTTP response status code
- **How to Create**: In HTTP Request activity, ResponseStatusCode property
- **Values**:
  - `200` = Success
  - `400` = Bad Request (invalid JSON)
  - `422` = Validation Error (missing fields)
  - `500` = Server Error
- **Usage**: Check `httpStatusCode = 200` before parsing response

---

### Parsed Response Variables

#### jsonResponse
- **Type**: `Newtonsoft.Json.Linq.JObject`
- **Scope**: `ForEachRow`
- **Default**: None (created by Deserialize JSON)
- **Purpose**: Parsed JSON object for easy field access
- **How to Create**: 
  1. Deserialize JSON activity
  2. JsonString = `apiResponse`
  3. JsonObject = `jsonResponse` (Ctrl+K)
  4. Type: Browse → Search "JObject" → `Newtonsoft.Json.Linq.JObject`
- **Usage**: Access fields like `jsonResponse("risk_score")`

#### riskScore
- **Type**: `System.Double`
- **Scope**: `ForEachRow`
- **Default**: None
- **Purpose**: Numeric risk score from API (0.0 to 1.0)
- **How to Create**: Assign activity
- **Value**: `CDbl(jsonResponse("risk_score").ToString)`
- **Range**: 0.0 (lowest risk) to 1.0 (highest risk)

#### riskLevel
- **Type**: `System.String`
- **Scope**: `ForEachRow`
- **Default**: None
- **Purpose**: Categorical risk level from API
- **How to Create**: Assign activity
- **Value**: `jsonResponse("risk_level").ToString`
- **Possible Values**: `"LOW"`, `"MEDIUM"`, `"HIGH"`

#### flaggedRules
- **Type**: `System.String`
- **Scope**: `ForEachRow`
- **Default**: None (empty if no rules flagged)
- **Purpose**: Comma-separated list of compliance rules that were triggered
- **How to Create**: Assign activity
- **Value**: `String.Join(", ", jsonResponse("flagged_rules").Select(Function(x) x.ToString))`
- **Example**: `"BSA_LARGE_CASH, FATF_HIGH_RISK, OFAC_SANCTIONED"`
- **Notes**: Empty string if no rules flagged

#### requiresReview
- **Type**: `System.Boolean`
- **Scope**: `ForEachRow`
- **Default**: None
- **Purpose**: Boolean flag indicating if manual review is needed
- **How to Create**: Assign activity
- **Value**: `CBool(jsonResponse("requires_review").ToString)`
- **Usage**: Convert to string for Excel: `If(requiresReview, "YES", "NO")`

---

### Reporting Variables

#### summaryMessage
- **Type**: `System.String`
- **Scope**: `Main`
- **Default**: None (built at end)
- **Purpose**: Formatted summary statistics message
- **How to Create**: Output of Invoke Code activity (see Step 11.1)
- **Example Content**:
```
SUMMARY STATISTICS:
- Total Processed: 1000
- High Risk: 45
- Medium Risk: 230
- Low Risk: 725
- Requires Review: 52
```
- **Usage**: Logged to console and shown in message box

---

### Error Handling Variables

#### exception
- **Type**: `System.Exception`
- **Scope**: Catch block
- **Default**: Auto-created by Try-Catch
- **Purpose**: Contains error information when exception occurs
- **How to Create**: Automatically created - don't manually create
- **Usage**: Access error details:
  - `exception.Message` - Error message
  - `exception.StackTrace` - Full stack trace
  - `exception.Source` - Source of error

---

## Variable Scope Best Practices

### Main Scope
Use for variables that need to be accessed throughout the entire workflow:
- Configuration (paths, URLs)
- Data tables (input and output)
- Summary statistics

### ForEachRow Scope
Use for variables that only exist within the loop iteration:
- Current row processing variables
- API request/response variables
- Parsed data for current transaction

### Why Scope Matters
- **Performance**: Scoped variables are cleaned up after use
- **Memory**: Prevents accumulation of data across iterations
- **Clarity**: Makes it clear which variables are temporary vs persistent

---

## CSV Input Format

The input CSV must have exactly these 18 columns in this order:

1. `transaction_id` - String (e.g., "TXN001")
2. `customer_id` - String (e.g., "CUST001")
3. `amount` - Number (e.g., 15000.00)
4. `transaction_type` - String (e.g., "wire_transfer")
5. `location` - String (e.g., "Cayman Islands")
6. `is_high_risk_country` - Boolean (True/False)
7. `is_cash` - Boolean (True/False)
8. `is_round_amount` - Boolean (True/False)
9. `unusual_time` - Boolean (True/False)
10. `recipient_new` - Boolean (True/False)
11. `txn_count_last_24h` - Integer (e.g., 5)
12. `avg_txn_amount` - Number (e.g., 12000.00)
13. `customer_risk_score` - Number 0-1 (e.g., 0.75)
14. `days_since_last_txn` - Integer (e.g., 2)
15. `is_offshore` - Boolean (True/False)
16. `velocity_score` - Number 0-1 (e.g., 0.85)
17. `hour_of_day` - Integer 0-23 (e.g., 23)
18. `day_of_week` - Integer 0-6 (e.g., 5)

**Important Notes**:
- Booleans must be `True` or `False` (capital T/F)
- Numbers must not have quotes
- Strings must not have internal commas (or escape them)

---

## Excel Output Format

The output Excel file has 8 columns:

1. `transaction_id` - Original transaction ID
2. `customer_id` - Original customer ID
3. `amount` - Original transaction amount
4. `risk_score` - Calculated risk score (0.0-1.0)
5. `risk_level` - Risk category (LOW/MEDIUM/HIGH)
6. `flagged_rules` - Comma-separated rule names
7. `requires_review` - "YES" or "NO"
8. `timestamp` - Processing timestamp (YYYY-MM-DD HH:MM:SS)

---

## Type Conversion Reference

### Common Type Conversions in UiPath

| From Type | To Type | Expression | Example |
|-----------|---------|------------|---------|
| String | Double | `CDbl(value)` | `CDbl("15000.50")` → 15000.5 |
| String | Int32 | `CInt(value)` | `CInt("42")` → 42 |
| String | Boolean | `CBool(value)` | `CBool("True")` → True |
| Double | String | `.ToString` | `15000.5.ToString` → "15000.5" |
| Int32 | String | `.ToString` | `42.ToString` → "42" |
| Boolean | String | `.ToString` | `True.ToString` → "True" |
| DataRow field | Any | `CType(row("col"), Type)` | `CDbl(row("amount"))` |
| Object | String | `.ToString` | `obj.ToString` |

### Boolean Expressions

- **Equals**: `value = 200` or `value.Equals(200)`
- **Not equals**: `value <> 200` or `Not value.Equals(200)`
- **Greater than**: `value > 100`
- **Less than**: `value < 100`
- **And**: `value1 And value2` or `value1 AndAlso value2` (short-circuit)
- **Or**: `value1 Or value2` or `value1 OrElse value2` (short-circuit)
- **Not**: `Not value`

---

## Variable Debugging Tips

### View Variable Values During Execution

1. **Breakpoints**: Click left margin to add breakpoint, run in Debug mode (F7)
2. **Log Message**: Add `Log Message` with `variableName.ToString`
3. **Watch Panel**: In Debug mode, add variables to Watch panel
4. **Immediate Panel**: In Debug mode, type variable name to see current value

### Common Variable Errors

**Error**: "Variable not declared"  
**Fix**: Make sure variable is created with Ctrl+K and has correct scope

**Error**: "Cannot convert type String to DataTable"  
**Fix**: Check variable type - must be `System.Data.DataTable`, not String

**Error**: "Object reference not set to an instance"  
**Fix**: Variable is Nothing/null - initialize it first (e.g., `New DataTable`)

**Error**: "Index was outside the bounds of the array"  
**Fix**: ArrayRow element count must match DataTable column count exactly

---

## Quick Variable Checklist

Before running workflow, verify:

- ✅ All String variables have double quotes in default values
- ✅ All DataTable variables use `System.Data.DataTable` type
- ✅ All JObject variables use `Newtonsoft.Json.Linq.JObject` type
- ✅ Loop variables (rowIndex, jsonPayload, etc.) have ForEachRow scope
- ✅ Global variables (dtTransactions, totalRows, etc.) have Main scope
- ✅ No variables show red underline (indicates type mismatch)
- ✅ File paths use backslashes on Windows: `C:\folder\file.csv`
- ✅ Boolean values in CSV are capitalized: True/False (not true/false)

---

**Document Version**: 1.0  
**Last Updated**: 2026-03-26  
**Related Documents**: 
- STEP_BY_STEP.md - Complete workflow guide
- TESTING.md - Testing procedures
- ../getting-started/FLOW_GUIDE.md - Navigation guide
