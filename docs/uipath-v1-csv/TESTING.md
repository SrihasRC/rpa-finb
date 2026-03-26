# UiPath v1 (CSV Processing) - Testing Guide

## Overview

This guide provides comprehensive testing procedures for the UiPath v1 CSV batch processing workflow. Use this to verify correct operation before production deployment.

---

## Table of Contents

1. [Pre-Test Checklist](#1-pre-test-checklist)
2. [Unit Testing](#2-unit-testing)
3. [Integration Testing](#3-integration-testing)
4. [Performance Testing](#4-performance-testing)
5. [Error Scenario Testing](#5-error-scenario-testing)
6. [Production Readiness Testing](#6-production-readiness-testing)
7. [Test Data Generator](#7-test-data-generator)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Pre-Test Checklist

Before running any tests, verify:

### Environment Setup

- ✅ **Python Environment**:
  - Virtual environment activated
  - All requirements installed: `pip install -r requirements.txt`
  - API server running: `uvicorn api.main:app --reload`
  - API accessible at `http://localhost:8000`

- ✅ **UiPath Studio**:
  - Version 2021.10 or higher
  - Required packages installed (WebAPI, Excel, Newtonsoft.Json)
  - Workflow passes validation (F8)
  - No syntax errors or warnings

- ✅ **File System**:
  - Test directory exists: `C:\RPA\`
  - User has read/write permissions on `C:\RPA\`
  - No Excel files currently open from previous runs

### Quick Environment Verification

Run this command in project root:
```bash
python test_installation.py
```

Expected output:
```
✓ All packages installed
✓ API server running
✓ Compliance check endpoint working
✓ System ready for testing
```

---

## 2. Unit Testing

Test individual components of the workflow in isolation.

### Test 2.1: Variable Initialization

**Objective**: Verify all variables are created with correct types and defaults.

**Steps**:
1. Open workflow in UiPath Studio
2. Click **Variables** panel at bottom
3. Verify each variable from VARIABLES.md exists with correct type

**Expected Results**:
- No red underlines on variables
- All types match specification
- Scopes are correct (Main vs ForEachRow)

**Pass Criteria**: All variables present and correctly typed ✅

---

### Test 2.2: CSV Reading

**Objective**: Verify CSV file is read correctly into DataTable.

**Test Data**: Create `C:\RPA\test_small.csv`
```csv
transaction_id,customer_id,amount,transaction_type,location,is_high_risk_country,is_cash,is_round_amount,unusual_time,recipient_new,txn_count_last_24h,avg_txn_amount,customer_risk_score,days_since_last_txn,is_offshore,velocity_score,hour_of_day,day_of_week
TXN001,CUST001,500.00,deposit,New York,False,False,False,False,False,1,500.00,0.25,10,False,0.10,14,2
```

**Steps**:
1. Update `csvFilePath` variable to `"C:\RPA\test_small.csv"`
2. Add breakpoint after "Read CSV File" activity
3. Run workflow in Debug mode (F7)
4. When paused, check Locals panel:
   - `dtTransactions` should have 1 row
   - `totalRows` should equal 1
   - Columns count should be 18

**Expected Results**:
- DataTable populated with 1 row
- Column headers match CSV
- Data types correct (string, boolean, number)

**Pass Criteria**: DataTable has correct structure and data ✅

---

### Test 2.3: JSON Payload Building

**Objective**: Verify JSON payload is correctly constructed from DataRow.

**Steps**:
1. Continue from Test 2.2 breakpoint (or add new breakpoint after "Build JSON Payload")
2. In Watch panel, add `jsonPayload` variable
3. Verify JSON structure

**Expected JSON** (formatted for readability):
```json
{
  "transaction_id": "TXN001",
  "customer_id": "CUST001",
  "amount": 500.0,
  "transaction_type": "deposit",
  "location": "New York",
  "is_high_risk_country": false,
  "is_cash": false,
  "is_round_amount": false,
  "unusual_time": false,
  "recipient_new": false,
  "txn_count_last_24h": 1,
  "avg_txn_amount": 500.0,
  "customer_risk_score": 0.25,
  "days_since_last_txn": 10,
  "is_offshore": false,
  "velocity_score": 0.1,
  "hour_of_day": 14,
  "day_of_week": 2
}
```

**Validation**:
- All 18 fields present
- Boolean values are lowercase (false, not False)
- Numbers have no quotes
- Strings have quotes

**Pass Criteria**: JSON is valid and matches schema ✅

---

### Test 2.4: HTTP Request

**Objective**: Verify API call succeeds and returns expected response.

**Steps**:
1. Add breakpoint after "POST Compliance Check" activity
2. Run workflow in Debug mode
3. Check variables:
   - `httpStatusCode` should be `200`
   - `apiResponse` should be non-empty JSON string

**Expected Response Structure**:
```json
{
  "transaction_id": "TXN001",
  "risk_score": 0.15,
  "risk_level": "LOW",
  "flagged_rules": [],
  "requires_review": false,
  "timestamp": "2024-03-26T10:30:15.123456"
}
```

**Validation**:
- Status code is 200
- Response is valid JSON
- Contains all required fields

**Pass Criteria**: API responds successfully ✅

---

### Test 2.5: JSON Response Parsing

**Objective**: Verify response is correctly parsed into variables.

**Steps**:
1. Add breakpoint after all "Extract..." activities
2. Check variables in Locals panel:
   - `riskScore`: Should be Double (e.g., 0.15)
   - `riskLevel`: Should be String ("LOW")
   - `flaggedRules`: Should be String (empty or comma-separated)
   - `requiresReview`: Should be Boolean (false)

**Expected Values** (for test_small.csv):
- `riskScore`: ~0.15 (may vary slightly)
- `riskLevel`: "LOW"
- `flaggedRules`: "" (empty)
- `requiresReview`: False

**Pass Criteria**: All values extracted correctly with proper types ✅

---

### Test 2.6: Excel Writing

**Objective**: Verify results are written to Excel correctly.

**Steps**:
1. Let workflow complete fully
2. Open `C:\RPA\compliance_results.xlsx`
3. Verify structure

**Expected Excel Structure**:

| transaction_id | customer_id | amount | risk_score | risk_level | flagged_rules | requires_review | timestamp |
|----------------|-------------|--------|------------|------------|---------------|-----------------|-----------|
| TXN001 | CUST001 | 500 | 0.15 | LOW | | NO | 2024-03-26 10:30:15 |

**Validation**:
- 8 columns with correct headers
- 1 data row (plus header row)
- All values correct
- Timestamp in correct format

**Pass Criteria**: Excel file created with correct data ✅

---

## 3. Integration Testing

Test the complete workflow end-to-end with realistic data.

### Test 3.1: Small Batch Processing

**Objective**: Process 10 transactions end-to-end.

**Test Data**: Create `C:\RPA\test_10rows.csv` with 10 diverse transactions:
- 3 HIGH risk (large amounts, high-risk countries)
- 4 MEDIUM risk (moderate flags)
- 3 LOW risk (normal transactions)

**Download test data**:
```bash
# In project directory
python -c "from data.generate_dataset import generate_dataset; generate_dataset(10, 'C:/RPA/test_10rows.csv')"
```

**Steps**:
1. Update `csvFilePath` to `"C:\RPA\test_10rows.csv"`
2. Update `excelOutputPath` to `"C:\RPA\test_10_results.xlsx"`
3. Run workflow (F5)
4. Observe Output panel for log messages

**Expected Behavior**:
- All 10 transactions processed without errors
- Progress logged for each transaction: "Processing transaction 1 of 10..."
- Summary shows breakdown by risk level
- Excel file created with 10 rows

**Pass Criteria**: 
- ✅ All 10 rows processed
- ✅ No errors in Output panel
- ✅ Excel file has 10 data rows
- ✅ Risk levels vary (not all same)

---

### Test 3.2: Medium Batch Processing

**Objective**: Process 100 transactions to verify performance and stability.

**Test Data**:
```bash
python -c "from data.generate_dataset import generate_dataset; generate_dataset(100, 'C:/RPA/test_100rows.csv')"
```

**Steps**:
1. Update paths to use test_100rows.csv
2. Run workflow
3. Monitor CPU and memory usage
4. Time the execution

**Expected Performance**:
- **Execution time**: 30-60 seconds (depends on API response time)
- **Memory usage**: < 500 MB
- **CPU usage**: Moderate (30-50%)

**Expected Results**:
- Summary shows mix of risk levels (approximate):
  - HIGH: 5-15%
  - MEDIUM: 25-35%
  - LOW: 55-65%

**Pass Criteria**:
- ✅ All 100 rows processed
- ✅ Execution time < 2 minutes
- ✅ No memory leaks
- ✅ Excel file opens correctly

---

### Test 3.3: Large Batch Processing

**Objective**: Process 1000 transactions (production-scale).

**Test Data**:
```bash
python -c "from data.generate_dataset import generate_dataset; generate_dataset(1000, 'C:/RPA/test_1000rows.csv')"
```

**Steps**:
1. Update paths to use test_1000rows.csv
2. Clear any previous results
3. Run workflow
4. Verify completion

**Expected Performance**:
- **Execution time**: 5-10 minutes
- **Throughput**: ~100-200 transactions/minute

**Expected Summary** (approximate):
```
SUMMARY STATISTICS:
- Total Processed: 1000
- High Risk: 80-120
- Medium Risk: 250-350
- Low Risk: 550-650
- Requires Review: 100-150
```

**Pass Criteria**:
- ✅ All 1000 rows processed
- ✅ No timeouts or crashes
- ✅ Excel file size reasonable (~200-500 KB)
- ✅ Summary statistics are reasonable

---

## 4. Performance Testing

### Test 4.1: Response Time Measurement

**Objective**: Measure API response time per transaction.

**Steps**:
1. Add Assign activity before HTTP Request:
   - To: `startTime` (DateTime)
   - Value: `DateTime.Now`
2. Add Assign activity after HTTP Request:
   - To: `endTime` (DateTime)
   - Value: `DateTime.Now`
3. Add Assign activity to calculate duration:
   - To: `responseTime` (TimeSpan)
   - Value: `endTime.Subtract(startTime)`
4. Add Log Message:
   - Message: `"Response time: " + responseTime.TotalMilliseconds.ToString + " ms"`

**Expected Response Times**:
- **Minimum**: 10-20 ms
- **Average**: 20-50 ms
- **Maximum**: 100-200 ms

**Pass Criteria**: Average response time < 100 ms ✅

---

### Test 4.2: Throughput Testing

**Objective**: Determine maximum processing throughput.

**Test**: Process 1000 transactions and calculate rate.

**Formula**:
```
Throughput (txn/min) = Total Transactions / (Execution Time in seconds / 60)
```

**Expected Throughput**:
- **Minimum**: 100 transactions/minute
- **Target**: 150 transactions/minute
- **Optimal**: 200+ transactions/minute

**Pass Criteria**: Throughput > 100 txn/min ✅

---

## 5. Error Scenario Testing

Test workflow behavior under error conditions.

### Test 5.1: Missing CSV File

**Objective**: Verify graceful handling when input file doesn't exist.

**Steps**:
1. Set `csvFilePath` to non-existent file: `"C:\RPA\nonexistent.csv"`
2. Run workflow

**Expected Behavior**:
- Workflow should fail at Read CSV activity
- Error message should indicate file not found
- Catch block should log error: "CRITICAL ERROR: File not found..."

**Pass Criteria**: Error is caught and logged properly ✅

---

### Test 5.2: API Server Down

**Objective**: Verify handling when API is unreachable.

**Steps**:
1. Stop the API server (`Ctrl+C` in terminal running uvicorn)
2. Run workflow with valid CSV (use test_small.csv)

**Expected Behavior**:
- HTTP Request should fail
- `httpStatusCode` should be non-200 (likely 0 or connection error)
- Flow Decision should go to False branch
- Error logged: "API request failed for transaction TXN001 - Status: 0"
- Workflow continues to next transaction (doesn't crash)

**Pass Criteria**: 
- ✅ Errors logged for each transaction
- ✅ Workflow completes (doesn't crash)
- ✅ Excel file created but with 0 rows (all skipped)

---

### Test 5.3: Invalid JSON Response

**Objective**: Verify handling of malformed API responses.

**Steps**:
1. Temporarily modify API to return invalid JSON (or use mock HTTP response)
2. Run workflow

**Expected Behavior**:
- Deserialize JSON activity should throw exception
- Try-Catch should catch the error
- Error logged with stack trace

**Pass Criteria**: Error caught gracefully without crashing ✅

---

### Test 5.4: Missing CSV Columns

**Objective**: Verify handling when CSV has incorrect structure.

**Test Data**: Create `C:\RPA\test_invalid.csv` missing some columns:
```csv
transaction_id,customer_id,amount
TXN001,CUST001,500.00
```

**Steps**:
1. Update `csvFilePath` to test_invalid.csv
2. Run workflow

**Expected Behavior**:
- Read CSV succeeds (only 3 columns in DataTable)
- "Build JSON Payload" fails when accessing missing columns
- Error caught: "Column 'transaction_type' does not belong to table"
- Logged in Catch block

**Pass Criteria**: Error caught and logged ✅

---

### Test 5.5: Excel File Locked

**Objective**: Verify handling when output file is already open.

**Steps**:
1. Open `C:\RPA\compliance_results.xlsx` in Excel
2. Run workflow

**Expected Behavior**:
- Workflow processes all transactions
- Write Range activity fails (file locked)
- Error caught: "The process cannot access the file because it is being used by another process"
- Error logged in Catch block

**Pass Criteria**: Error caught and reported clearly ✅

---

### Test 5.6: API Timeout

**Objective**: Verify handling of slow API responses.

**Steps**:
1. In HTTP Request activity properties, set **Timeout** to 5000 (5 seconds)
2. Modify API to add artificial delay (or use slow network)
3. Run workflow

**Expected Behavior**:
- If response takes > 5 seconds, HTTP Request throws timeout exception
- Error logged
- Workflow continues to next transaction

**Pass Criteria**: Timeout handled gracefully ✅

---

## 6. Production Readiness Testing

Final validation before production deployment.

### Test 6.1: End-to-End Production Simulation

**Objective**: Simulate real production scenario.

**Test Data**: 
- Use production-like dataset: 500-1000 transactions
- Mix of transaction types
- Realistic distribution of risk levels

**Steps**:
1. Generate production-like data:
```bash
python -c "from data.generate_dataset import generate_dataset; generate_dataset(500, 'C:/RPA/prod_test.csv')"
```
2. Configure production-like settings:
   - `csvFilePath`: Production input path
   - `excelOutputPath`: Production output path
   - `apiBaseUrl`: Production API URL (if different)
3. Run workflow
4. Verify results

**Validation Checklist**:
- ✅ All transactions processed
- ✅ Excel file created successfully
- ✅ Risk distribution is reasonable (not all HIGH or all LOW)
- ✅ Summary statistics make sense
- ✅ Flagged rules are diverse (not all same rule)
- ✅ Review flag correlates with high risk
- ✅ Execution time acceptable
- ✅ No errors or warnings in Output panel

**Pass Criteria**: All validations pass ✅

---

### Test 6.2: Data Quality Validation

**Objective**: Verify output data integrity.

**Steps**:
1. After running production simulation, open Excel results
2. Perform spot checks:
   - **Row count**: Should match input CSV row count
   - **Transaction IDs**: Should all be unique
   - **Risk scores**: Should be between 0.0 and 1.0
   - **Risk levels**: Should only be LOW/MEDIUM/HIGH
   - **Flagged rules**: Should be valid rule names from system (BSA_*, FATF_*, OFAC_*, etc.)
   - **Requires review**: Should only be YES or NO
   - **Timestamps**: Should all be during workflow execution time

3. Statistical checks:
   - HIGH risk should have average risk_score > 0.7
   - MEDIUM risk should have average risk_score 0.4-0.7
   - LOW risk should have average risk_score < 0.4

**Pass Criteria**: All data is valid and consistent ✅

---

### Test 6.3: Idempotency Test

**Objective**: Verify running workflow multiple times produces consistent results.

**Steps**:
1. Run workflow with same input CSV
2. Save output as `results_run1.xlsx`
3. Run workflow again with same input
4. Save output as `results_run2.xlsx`
5. Compare the two files

**Expected Results**:
- Risk scores should be identical (deterministic model)
- Risk levels should be identical
- Flagged rules should be identical
- Only timestamps should differ

**Validation**:
```python
import pandas as pd
df1 = pd.read_excel('results_run1.xlsx')
df2 = pd.read_excel('results_run2.xlsx')

# Compare excluding timestamp column
cols_to_compare = ['transaction_id', 'risk_score', 'risk_level', 'flagged_rules', 'requires_review']
assert df1[cols_to_compare].equals(df2[cols_to_compare]), "Results differ between runs!"
```

**Pass Criteria**: Results are identical (except timestamps) ✅

---

## 7. Test Data Generator

### Generate Custom Test Data

Use this Python script to create custom test datasets:

```python
# save as: C:\RPA\generate_test_data.py

import pandas as pd
import random
from datetime import datetime, timedelta

def generate_test_csv(num_rows, output_path, high_risk_pct=0.1):
    """
    Generate test CSV with controlled risk distribution.
    
    Args:
        num_rows: Number of transactions to generate
        output_path: Where to save CSV
        high_risk_pct: Percentage of high-risk transactions (0.0-1.0)
    """
    data = []
    
    for i in range(num_rows):
        # Decide if this should be high risk
        is_high_risk = random.random() < high_risk_pct
        
        if is_high_risk:
            # High risk profile
            amount = random.uniform(10000, 50000)
            is_high_risk_country = True
            is_cash = random.choice([True, False])
            is_round_amount = True
            unusual_time = True
            customer_risk_score = random.uniform(0.7, 0.95)
            txn_count_last_24h = random.randint(5, 15)
        else:
            # Low risk profile
            amount = random.uniform(100, 5000)
            is_high_risk_country = False
            is_cash = False
            is_round_amount = False
            unusual_time = False
            customer_risk_score = random.uniform(0.1, 0.4)
            txn_count_last_24h = random.randint(1, 3)
        
        transaction = {
            'transaction_id': f'TXN{i+1:05d}',
            'customer_id': f'CUST{random.randint(1, num_rows//2):05d}',
            'amount': round(amount, 2),
            'transaction_type': random.choice(['wire_transfer', 'deposit', 'withdrawal', 'check']),
            'location': random.choice(['New York', 'London', 'Cayman Islands', 'Switzerland', 'Panama']),
            'is_high_risk_country': is_high_risk_country,
            'is_cash': is_cash,
            'is_round_amount': is_round_amount,
            'unusual_time': unusual_time,
            'recipient_new': random.choice([True, False]),
            'txn_count_last_24h': txn_count_last_24h,
            'avg_txn_amount': round(random.uniform(500, 10000), 2),
            'customer_risk_score': round(customer_risk_score, 2),
            'days_since_last_txn': random.randint(1, 30),
            'is_offshore': random.choice([True, False]),
            'velocity_score': round(random.uniform(0.1, 0.9), 2),
            'hour_of_day': random.randint(0, 23),
            'day_of_week': random.randint(0, 6)
        }
        data.append(transaction)
    
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"✓ Generated {num_rows} transactions at {output_path}")
    print(f"  - High risk (~): {int(num_rows * high_risk_pct)}")
    print(f"  - Low risk (~): {num_rows - int(num_rows * high_risk_pct)}")

# Usage examples:
if __name__ == "__main__":
    # Small test - 10 rows, 30% high risk
    generate_test_csv(10, 'C:/RPA/test_10_controlled.csv', high_risk_pct=0.3)
    
    # Medium test - 100 rows, 10% high risk
    generate_test_csv(100, 'C:/RPA/test_100_controlled.csv', high_risk_pct=0.1)
    
    # Production simulation - 1000 rows, 5% high risk
    generate_test_csv(1000, 'C:/RPA/test_1000_controlled.csv', high_risk_pct=0.05)
```

**Run it**:
```bash
python C:\RPA\generate_test_data.py
```

---

## 8. Troubleshooting

### Common Test Failures and Solutions

#### Test fails with "Variable not declared"
**Cause**: Variable not created or wrong scope  
**Solution**: 
- Check Variables panel - variable should exist
- Verify scope matches usage (Main for global, ForEachRow for loop variables)
- Press Ctrl+K to create variable if missing

#### Test fails with "Cannot convert String to DataTable"
**Cause**: Variable has wrong type  
**Solution**:
- In Variables panel, change Type to `System.Data.DataTable`
- Use Browse button to search for DataTable type

#### Test fails with "API request failed - Status: 0"
**Cause**: API server not running or wrong URL  
**Solution**:
- Open browser to `http://localhost:8000` - should see welcome page
- Check `apiBaseUrl` variable matches actual API URL
- Restart API: `uvicorn api.main:app --reload`

#### Test fails with "File not found"
**Cause**: CSV file path incorrect or file doesn't exist  
**Solution**:
- Open File Explorer and verify file exists at exact path
- Copy-paste full path from File Explorer to `csvFilePath` variable
- Use double backslashes: `C:\\RPA\\file.csv` or single forward slashes: `C:/RPA/file.csv`

#### Test fails with "Column does not belong to table"
**Cause**: CSV missing required columns or wrong header names  
**Solution**:
- Open CSV in Excel/Notepad
- Verify first row has all 18 column headers (see VARIABLES.md)
- Check for typos in column names (e.g., "trasaction_id" vs "transaction_id")

#### Test fails with "Cannot convert value to Double"
**Cause**: CSV has invalid data types (e.g., text in numeric field)  
**Solution**:
- Check numeric columns (amount, avg_txn_amount, etc.) have no text
- Boolean columns should be `True` or `False` (capital T/F)
- Remove any quotes around numbers

#### Test completes but Excel file is empty
**Cause**: All transactions failed HTTP request or status check  
**Solution**:
- Check Output panel for error messages
- Verify API is running and accessible
- Add Log Message before Add Data Row to confirm it's reached

#### Test is very slow (> 5 minutes for 100 rows)
**Cause**: API performance issues or network latency  
**Solution**:
- Check API logs for slow endpoints
- Monitor CPU/memory on API server
- Consider adding HTTP Request timeout
- For production, deploy API closer to RPA server (reduce network hops)

---

## Test Completion Checklist

Before deploying to production, ensure all tests pass:

### Unit Tests
- ✅ Variable initialization
- ✅ CSV reading
- ✅ JSON payload building
- ✅ HTTP request
- ✅ JSON response parsing
- ✅ Excel writing

### Integration Tests
- ✅ Small batch (10 rows)
- ✅ Medium batch (100 rows)
- ✅ Large batch (1000 rows)

### Performance Tests
- ✅ Response time < 100ms average
- ✅ Throughput > 100 txn/min

### Error Scenario Tests
- ✅ Missing CSV file
- ✅ API server down
- ✅ Invalid JSON response
- ✅ Missing CSV columns
- ✅ Excel file locked
- ✅ API timeout

### Production Readiness Tests
- ✅ End-to-end production simulation
- ✅ Data quality validation
- ✅ Idempotency test

### Documentation
- ✅ All test results documented
- ✅ Known issues logged
- ✅ Workarounds documented

---

## Test Results Template

Use this template to document test results:

```
============================================
UiPath v1 CSV Processing - Test Results
============================================

Test Date: YYYY-MM-DD
Tester: [Name]
Environment: [Dev/Test/Staging/Prod]
API Version: [Version]
UiPath Version: [Version]

--------------------------------------------
UNIT TESTS
--------------------------------------------
[ ] Variable initialization - PASS/FAIL
[ ] CSV reading - PASS/FAIL
[ ] JSON payload building - PASS/FAIL
[ ] HTTP request - PASS/FAIL
[ ] JSON response parsing - PASS/FAIL
[ ] Excel writing - PASS/FAIL

--------------------------------------------
INTEGRATION TESTS
--------------------------------------------
[ ] Small batch (10 rows) - PASS/FAIL
    - Execution time: ___ seconds
    - Errors: ___
    
[ ] Medium batch (100 rows) - PASS/FAIL
    - Execution time: ___ seconds
    - Throughput: ___ txn/min
    - Errors: ___
    
[ ] Large batch (1000 rows) - PASS/FAIL
    - Execution time: ___ seconds
    - Throughput: ___ txn/min
    - High risk count: ___
    - Medium risk count: ___
    - Low risk count: ___
    - Review required count: ___

--------------------------------------------
PERFORMANCE TESTS
--------------------------------------------
[ ] Response time - PASS/FAIL
    - Average: ___ ms
    - Min: ___ ms
    - Max: ___ ms
    
[ ] Throughput - PASS/FAIL
    - Rate: ___ txn/min

--------------------------------------------
ERROR SCENARIO TESTS
--------------------------------------------
[ ] Missing CSV file - PASS/FAIL
[ ] API server down - PASS/FAIL
[ ] Invalid JSON response - PASS/FAIL
[ ] Missing CSV columns - PASS/FAIL
[ ] Excel file locked - PASS/FAIL
[ ] API timeout - PASS/FAIL

--------------------------------------------
PRODUCTION READINESS TESTS
--------------------------------------------
[ ] End-to-end production simulation - PASS/FAIL
[ ] Data quality validation - PASS/FAIL
[ ] Idempotency test - PASS/FAIL

--------------------------------------------
OVERALL RESULT: PASS / FAIL
--------------------------------------------

Issues found:
1. ___
2. ___

Recommendations:
1. ___
2. ___

Sign-off: _______________  Date: _______________
```

---

**Document Version**: 1.0  
**Last Updated**: 2026-03-26  
**Related Documents**:
- STEP_BY_STEP.md - Workflow building guide
- VARIABLES.md - Variable reference
- ../getting-started/FLOW_GUIDE.md - Navigation guide
