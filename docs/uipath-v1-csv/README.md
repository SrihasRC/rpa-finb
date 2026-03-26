# UiPath v1: CSV Batch Processing - Complete Guide

**Purpose:** Automate reading transactions from CSV/Excel, send to API for compliance checking, and generate Excel reports.

**Difficulty:** Intermediate  
**Time to Build:** 1-2 hours  
**Prerequisites:** UiPath Studio installed

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [What You'll Build](#what-youll-build)
3. [Prerequisites](#prerequisites)
4. [Workflow Architecture](#workflow-architecture)
5. [Step-by-Step Guide](#step-by-step-guide)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

---

## Overview

### What This Workflow Does

```
Input: data/transactions.csv (1000 rows)
         ↓
[UiPath reads CSV]
         ↓
[For each transaction]
    → Build JSON
    → POST to /compliance-check API
    → Receive results
    → Store in DataTable
         ↓
[Write to Excel]
         ↓
Output: compliance_results.xlsx
        compliance_summary.xlsx
```

### Key Features

- ✅ Reads CSV/Excel input
- ✅ Calls REST API for each transaction
- ✅ Handles errors gracefully
- ✅ Generates Excel reports with formatting
- ✅ Creates summary statistics
- ✅ Logs all activities
- ✅ Processes ~2-3 transactions/second

---

## What You'll Build

### Final Outputs

1. **compliance_results.xlsx**
   - All transactions with compliance results
   - Columns: Transaction ID, Amount, Risk Level, Rules Triggered, etc.
   - Conditional formatting (RED/YELLOW/GREEN)

2. **compliance_summary.xlsx**
   - Summary statistics
   - Total transactions, risk distribution
   - Chart/pivot table

3. **process_log.txt**
   - Execution log
   - Errors and warnings
   - Processing time

---

## Prerequisites

### 1. Software Required

- ✅ **UiPath Studio** (2023.10 or later)
- ✅ **Python 3.8+** (for API server)
- ✅ **Excel** (for viewing outputs)

### 2. UiPath Packages Required

Install these packages in UiPath Studio:

| Package | Version | Purpose |
|---------|---------|---------|
| UiPath.WebAPI.Activities | Latest | HTTP requests |
| UiPath.Excel.Activities | Latest | Excel operations |
| UiPath.System.Activities | Latest | Data tables, loops |

**How to install:**
1. Go to **Manage Packages** in UiPath Studio
2. Search for each package
3. Click **Install**

### 3. System Setup

Before starting UiPath workflow:

```bash
# 1. Start API server (keep running)
cd /path/to/rpa-finb
python api/main.py

# 2. Verify API is running
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "dataset_loaded": true
}
```

---

## Workflow Architecture

### Project Structure

```
Financial_Compliance_RPA_v1/
├── Main.xaml                    # Main workflow
├── Workflows/
│   ├── ReadTransactions.xaml   # Read CSV
│   ├── ProcessTransaction.xaml # API call
│   ├── WriteResults.xaml       # Write Excel
│   └── GenerateSummary.xaml    # Create summary
├── Data/
│   ├── Config.xlsx             # Configuration
│   └── transactions.csv        # Input data
└── Output/
    ├── compliance_results.xlsx
    ├── compliance_summary.xlsx
    └── process_log.txt
```

### Workflow Flow

```
Main.xaml
    │
    ├─→ Initialize (Config, Variables, DataTables)
    │
    ├─→ ReadTransactions.xaml
    │      └─ Read CSV into DataTable
    │
    ├─→ For Each Row in DataTable
    │      │
    │      └─→ ProcessTransaction.xaml
    │             ├─ Build JSON request
    │             ├─ HTTP POST to API
    │             ├─ Parse JSON response
    │             └─ Add to results DataTable
    │
    ├─→ WriteResults.xaml
    │      └─ Write DataTable to Excel with formatting
    │
    └─→ GenerateSummary.xaml
           └─ Create summary statistics
```

---

## Step-by-Step Guide

→ **Continue to:** `docs/uipath-v1-csv/STEP_BY_STEP.md` for detailed activity creation

---

## Quick Start (Summary)

### Phase 1: Project Setup (10 mins)

1. Create new **Process** in UiPath Studio
2. Name: `Financial_Compliance_RPA_v1`
3. Install required packages
4. Create folder structure

### Phase 2: Main Workflow (30 mins)

1. Create `Main.xaml`
2. Add initialization sequence
3. Add Read CSV activity
4. Add For Each loop
5. Add Write Excel activity

### Phase 3: Sub-Workflows (40 mins)

1. Create `ProcessTransaction.xaml`
2. Create `WriteResults.xaml`
3. Create `GenerateSummary.xaml`
4. Add error handling

### Phase 4: Testing (20 mins)

1. Test with 10 transactions
2. Verify API calls
3. Check Excel output
4. Test error scenarios

---

## Testing

### Test Scenarios

#### Test 1: Basic Run (10 transactions)

**Input:** First 10 rows from `transactions.csv`

**Steps:**
1. Modify CSV to keep only 10 rows
2. Run workflow
3. Check output Excel

**Expected:**
- ✅ All 10 transactions processed
- ✅ Excel file created
- ✅ No errors in log

#### Test 2: Error Handling

**Input:** Add invalid data (negative amount)

**Steps:**
1. Add row with negative amount
2. Run workflow
3. Check error handling

**Expected:**
- ✅ Error logged
- ✅ Error row in output with "ERROR" status
- ✅ Processing continues for other rows

#### Test 3: Full Dataset (1000 transactions)

**Input:** Complete `transactions.csv`

**Steps:**
1. Run with full dataset
2. Monitor progress
3. Check completion time

**Expected:**
- ✅ ~1000 transactions processed
- ✅ Processing time: 7-10 minutes
- ✅ All results in Excel

---

## Troubleshooting

### Common Issues

#### Issue 1: "Connection refused" error

**Symptom:** HTTP Request fails

**Solution:**
1. Check API server is running: `python api/main.py`
2. Verify URL: `http://localhost:8000`
3. Test in browser: http://localhost:8000/health

#### Issue 2: "Model not loaded" error

**Symptom:** API returns 503 error

**Solution:**
```bash
# Run pipeline to train model
python run_pipeline.py
```

#### Issue 3: Excel file not created

**Symptom:** No output file

**Solution:**
1. Check folder permissions
2. Close Excel if file is open
3. Check DataTable has data

#### Issue 4: Slow processing

**Symptom:** Very slow (>10 mins for 1000 rows)

**Solution:**
1. Check network latency
2. Verify API server performance
3. Consider parallel processing (advanced)

---

## Performance Tips

### Optimization

1. **Batch Processing**
   - Process in batches of 100
   - Write intermediate results

2. **Parallel Processing** (Advanced)
   - Use Parallel For Each
   - Set MaxDegreeOfParallelism to 5

3. **Connection Pooling**
   - Reuse HTTP client
   - Keep connections alive

### Expected Performance

| Transactions | Time | Throughput |
|--------------|------|------------|
| 10 | ~5 sec | 2 txn/sec |
| 100 | ~45 sec | 2.2 txn/sec |
| 1000 | ~7 min | 2.4 txn/sec |

---

## Next Steps

1. ✅ Build basic workflow → Follow `STEP_BY_STEP.md`
2. ✅ Test with sample data
3. ✅ Add advanced features:
   - Email notifications
   - Database logging
   - Retry logic
   - Dashboard integration

---

## Related Documentation

- **Detailed Activities:** `STEP_BY_STEP.md`
- **Variable Reference:** `VARIABLES.md`
- **API Documentation:** `../api/ENDPOINTS.md`
- **Testing Guide:** `TESTING.md`

---

**Ready to build?** → Continue to `STEP_BY_STEP.md` for detailed instructions!
