# UiPath Integration Guide

## Overview
This guide provides detailed instructions for integrating the Financial Compliance Monitoring System with UiPath Studio.

## Prerequisites

1. **UiPath Studio** installed (Community or Enterprise)
2. **Compliance API** running at `http://localhost:8000`
3. **UiPath.WebAPI.Activities** package installed

## Step-by-Step Integration

### Step 1: Create New UiPath Project

1. Open UiPath Studio
2. Create new Process: "Financial_Compliance_Monitor"
3. Install packages:
   - UiPath.WebAPI.Activities
   - UiPath.Excel.Activities

### Step 2: Configure Variables

Create the following variables in UiPath:

| Variable | Type | Default Value | Scope |
|----------|------|---------------|-------|
| baseURL | String | "http://localhost:8000" | Global |
| transactionsPath | String | "data/transactions.csv" | Global |
| outputPath | String | "compliance_results.xlsx" | Global |
| transactionsDT | DataTable | - | Global |
| resultsDT | DataTable | - | Global |
| currentRow | DataRow | - | ForEach Loop |
| requestJSON | String | - | ForEach Loop |
| responseJSON | String | - | ForEach Loop |
| complianceData | JObject | - | ForEach Loop |

### Step 3: Build Main Workflow

#### 3.1 Read Transactions
```
Activity: Read CSV
  FilePath: transactionsPath
  Output: transactionsDT
  Delimiter: ","
  HasHeaders: True
```

#### 3.2 Initialize Results DataTable
```
Activity: Build Data Table
  Output: resultsDT
  
  Columns:
  - transaction_id (String)
  - customer_id (String)
  - transaction_amount (Double)
  - rules_triggered (String)
  - num_rules_triggered (Int32)
  - risk_score (Double)
  - risk_label (String)
  - final_risk (String)
  - processing_status (String)
```

#### 3.3 Process Each Transaction
```
Activity: For Each Row in Data Table
  Input: transactionsDT
  Output: currentRow
  
  Body (Sequence):
    1. Build JSON Request
    2. HTTP Request to API
    3. Parse Response
    4. Add to Results
    5. Error Handling
```

### Step 4: Build JSON Request Body

```
Activity: Assign
  Variable: requestJSON
  Value: 
  "{" + 
  """customer_id"": """ + currentRow("customer_id").ToString() + """," +
  """account_age_days"": " + currentRow("account_age_days").ToString() + "," +
  """account_status"": """ + currentRow("account_status").ToString() + """," +
  """transaction_amount"": " + currentRow("transaction_amount").ToString() + "," +
  """transaction_type"": """ + currentRow("transaction_type").ToString() + """," +
  """transaction_time"": """ + currentRow("transaction_time").ToString() + """," +
  """sender_country"": """ + currentRow("sender_country").ToString() + """," +
  """receiver_country"": """ + currentRow("receiver_country").ToString() + """," +
  """beneficiary_id"": """ + currentRow("beneficiary_id").ToString() + """," +
  """beneficiary_bank"": """ + currentRow("beneficiary_bank").ToString() + """," +
  """customer_avg_txn"": " + currentRow("customer_avg_txn").ToString() + "," +
  """txn_count_last_24h"": " + currentRow("txn_count_last_24h").ToString() + "," +
  """txn_count_last_7d"": " + currentRow("txn_count_last_7d").ToString() + "," +
  """kyc_status"": """ + currentRow("kyc_status").ToString() + """," +
  """sanctions_flag"": " + currentRow("sanctions_flag").ToString() + "," +
  """device_location"": """ + currentRow("device_location").ToString() + """," +
  """channel"": """ + currentRow("channel").ToString() + """," +
  """is_international"": " + currentRow("is_international").ToString() +
  "}"
```

**Alternative (Recommended): Use Serialize JSON**
```
Activity: Serialize JSON
  Input: New Dictionary(Of String, Object) From {
    {"customer_id", currentRow("customer_id").ToString()},
    {"account_age_days", CInt(currentRow("account_age_days"))},
    {"account_status", currentRow("account_status").ToString()},
    {"transaction_amount", CDbl(currentRow("transaction_amount"))},
    {"transaction_type", currentRow("transaction_type").ToString()},
    {"transaction_time", currentRow("transaction_time").ToString()},
    {"sender_country", currentRow("sender_country").ToString()},
    {"receiver_country", currentRow("receiver_country").ToString()},
    {"beneficiary_id", currentRow("beneficiary_id").ToString()},
    {"beneficiary_bank", currentRow("beneficiary_bank").ToString()},
    {"customer_avg_txn", CDbl(currentRow("customer_avg_txn"))},
    {"txn_count_last_24h", CInt(currentRow("txn_count_last_24h"))},
    {"txn_count_last_7d", CInt(currentRow("txn_count_last_7d"))},
    {"kyc_status", currentRow("kyc_status").ToString()},
    {"sanctions_flag", CInt(currentRow("sanctions_flag"))},
    {"device_location", currentRow("device_location").ToString()},
    {"channel", currentRow("channel").ToString()},
    {"is_international", CInt(currentRow("is_international"))}
  }
  Output: requestJSON
```

### Step 5: HTTP Request Configuration

```
Activity: HTTP Request
  Endpoint: baseURL + "/compliance-check"
  Method: POST
  Headers: 
    Accept: application/json
    Content-Type: application/json
  Body: requestJSON
  BodyFormat: application/json
  Output: responseJSON
  TimeoutMS: 30000
```

### Step 6: Parse API Response

```
Activity: Deserialize JSON
  JsonString: responseJSON
  Output: complianceData
```

Extract values:
```
Activity: Multiple Assign

transaction_id = complianceData("transaction_id").ToString()
rules_triggered = String.Join("; ", complianceData("rules_triggered").Select(Function(x) x.ToString()))
num_rules_triggered = CInt(complianceData("num_rules_triggered"))
risk_score = CDbl(complianceData("risk_score"))
risk_label = complianceData("risk_label").ToString()
final_risk = complianceData("final_risk").ToString()
```

### Step 7: Add Results to DataTable

```
Activity: Add Data Row
  DataTable: resultsDT
  ArrayRow: {
    currentRow("transaction_id").ToString(),
    currentRow("customer_id").ToString(),
    CDbl(currentRow("transaction_amount")),
    rules_triggered,
    num_rules_triggered,
    risk_score,
    risk_label,
    final_risk,
    "SUCCESS"
  }
```

### Step 8: Error Handling

Wrap the HTTP Request in Try-Catch:

```
Try-Catch Activity:

  Try:
    - HTTP Request
    - Parse Response
    - Add to Results
    
  Catch (System.Exception):
    - Log Message: "Error processing " + currentRow("transaction_id").ToString() + ": " + exception.Message
    - Add Data Row (Error):
        {
          currentRow("transaction_id").ToString(),
          currentRow("customer_id").ToString(),
          CDbl(currentRow("transaction_amount")),
          "ERROR",
          0,
          0.0,
          "error",
          "ERROR",
          "FAILED: " + exception.Message
        }
```

### Step 9: Write Results to Excel

```
Activity: Write Range
  WorkbookPath: outputPath
  SheetName: "Compliance Results"
  DataTable: resultsDT
  AddHeaders: True
  StartingCell: "A1"
```

### Step 10: Generate Summary Report

```
Activity: Build Data Table (summaryDT)
  Columns:
  - Metric (String)
  - Value (String)

Add summary rows:
- Total Transactions: resultsDT.Rows.Count.ToString()
- High Risk: resultsDT.Select("[final_risk] = 'HIGH'").Count().ToString()
- Medium Risk: resultsDT.Select("[final_risk] = 'MEDIUM'").Count().ToString()
- Low Risk: resultsDT.Select("[final_risk] = 'LOW'").Count().ToString()
- Failed: resultsDT.Select("[final_risk] = 'ERROR'").Count().ToString()
- Avg Risk Score: resultsDT.AsEnumerable().Where(Function(r) r("risk_score") IsNot Nothing AndAlso CDbl(r("risk_score")) > 0).Average(Function(r) CDbl(r("risk_score"))).ToString("F4")

Activity: Write Range
  WorkbookPath: outputPath
  SheetName: "Summary"
  DataTable: summaryDT
  AddHeaders: True
```

## Advanced Features

### Batch Processing

For large datasets (>1000 transactions), use batch processing:

```
For Each batchDT In SplitDataTable(transactionsDT, 100):
  Process batch
  Write intermediate results
  Clear memory
```

### Parallel Processing

Use Parallel For Each for independent transactions:

```
Activity: Parallel For Each
  Input: transactionsDT.AsEnumerable()
  NumberOfParallelThreads: 5
  Body: Process single transaction
```

**Note**: Ensure thread-safe operations when writing to shared DataTable.

### Retry Logic

Add retry mechanism for failed API calls:

```
Activity: Retry Scope
  NumberOfRetries: 3
  RetryInterval: 00:00:05
  Body: HTTP Request
```

### Progress Tracking

```
Activity: Log Message
  Message: "Processed " + (currentIndex + 1).ToString() + " / " + transactionsDT.Rows.Count.ToString()
  Level: Info
  
Activity: Update Progress Bar (if using custom UI)
```

## Testing the Integration

### Test 1: Single Transaction
1. Create test CSV with 1 transaction
2. Run workflow
3. Verify API call and response

### Test 2: Small Batch
1. Use 10 transactions
2. Verify all processed correctly
3. Check error handling

### Test 3: Full Dataset
1. Process entire dataset (1000 transactions)
2. Verify performance
3. Check results accuracy

## Performance Benchmarks

| Transactions | Processing Time | Throughput |
|-------------|-----------------|------------|
| 10 | ~5 seconds | 2 txn/sec |
| 100 | ~45 seconds | 2.2 txn/sec |
| 1000 | ~7 minutes | 2.4 txn/sec |

**Note**: Performance depends on API response time and network latency.

## Troubleshooting

### Issue 1: Connection Refused
**Symptom**: HTTP request fails with connection error
**Solution**: 
- Ensure API is running: `python api/main.py`
- Check firewall settings
- Verify baseURL is correct

### Issue 2: JSON Parsing Error
**Symptom**: Deserialize JSON activity fails
**Solution**:
- Log responseJSON to check format
- Verify API returned valid JSON
- Check for API errors in response

### Issue 3: Slow Processing
**Symptom**: Workflow takes too long
**Solution**:
- Enable parallel processing
- Increase timeout values
- Use batch processing
- Optimize API server performance

### Issue 4: Missing Data
**Symptom**: Some fields are null/empty
**Solution**:
- Add null checks before accessing JObject properties
- Use default values for missing fields
- Validate input data completeness

## Best Practices

1. **Logging**: Log all API requests and responses for debugging
2. **Validation**: Validate input data before API call
3. **Error Handling**: Always use Try-Catch for HTTP requests
4. **Configuration**: Store URLs and paths in Config file
5. **Monitoring**: Track processing progress and errors
6. **Testing**: Test with small datasets first
7. **Security**: Use HTTPS in production, implement API authentication

## Sample Workflow Structure

```
Main.xaml
│
├── Initialize
│   ├── Read Config
│   └── Create Results DataTable
│
├── Read Transactions CSV
│
├── For Each Transaction
│   ├── Build JSON Request
│   ├── Try-Catch
│   │   ├── HTTP Request
│   │   ├── Parse Response
│   │   └── Add to Results
│   └── Log Progress
│
├── Write Results to Excel
│
└── Generate Summary Report
```

## Additional Resources

- **UiPath Documentation**: https://docs.uipath.com
- **HTTP Request Activity**: https://docs.uipath.com/activities/docs/http-request
- **JSON Handling**: https://docs.uipath.com/activities/docs/deserialize-json

## Support

For API-specific issues, check:
- API logs: Console output from `python api/main.py`
- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

---

**Document Version**: 1.0
**Last Updated**: 2024
**Tested with**: UiPath Studio 2023.10+
