# UiPath v2 (Web Portal Automation) - Overview

## Introduction

UiPath v2 automates the **live web transaction portal** for real-time compliance monitoring. Unlike v1 which processes CSV files in batches, v2 interacts with the web-based banking portal to submit individual transactions and extract compliance results.

---

## What is v2?

**v2 = Web Browser Automation** for live transaction submission

### Key Differences from v1

| Aspect | v1 (CSV Batch) | v2 (Web Portal) |
|--------|---------------|-----------------|
| **Input Source** | CSV file on disk | Manual data or database |
| **Processing Mode** | Batch (all at once) | Interactive (one at a time) |
| **Technology** | HTTP Request activities | Browser automation (UI.Vision or Selenium) |
| **Output** | Excel file | Screenshots + extracted data |
| **Use Case** | Bulk historical analysis | Real-time transaction testing |
| **UiPath Activities** | Read CSV, HTTP Request, Write Range | Open Browser, Type Into, Click, Get Text |
| **Speed** | Fast (API direct) | Slower (browser rendering) |
| **User Interaction** | Unattended | Can be attended or unattended |

### When to Use v2

Use v2 when you need to:
- ✅ Test individual transactions through the web UI
- ✅ Verify web portal functionality
- ✅ Demonstrate compliance checking to stakeholders
- ✅ Submit transactions from sources other than CSV (database, manual input)
- ✅ Capture screenshots as audit evidence
- ✅ Simulate end-user behavior

Use v1 when you need to:
- ✅ Process large batches (100+ transactions)
- ✅ Maximize speed and efficiency
- ✅ Run unattended on schedule
- ✅ Minimize resource usage

---

## Architecture Overview

```
┌─────────────────┐
│   UiPath v2     │
│   Workflow      │
└────────┬────────┘
         │
         │ 1. Open Browser
         ↓
┌─────────────────────────┐
│  Web Portal             │
│  http://localhost:8000  │
│  /portal                │
└────────┬────────────────┘
         │
         │ 2. Fill Form & Submit
         ↓
┌─────────────────────────┐
│  Frontend JavaScript    │
│  (web/static/js/app.js) │
└────────┬────────────────┘
         │
         │ 3. POST /compliance-check
         ↓
┌─────────────────────────┐
│  FastAPI Backend        │
│  (api/main.py)          │
└────────┬────────────────┘
         │
         │ 4. Process & Return JSON
         ↑
┌────────┴────────────────┐
│  Compliance Engine      │
│  - ML Model             │
│  - 10 Rules             │
└─────────────────────────┘
         │
         │ 5. Display Results
         ↓
┌─────────────────────────┐
│  Results Card           │
│  (Risk Score, Level,    │
│   Flagged Rules)        │
└─────────────────────────┘
         │
         │ 6. Extract Results
         ↑
┌────────┴────────────────┐
│  UiPath v2              │
│  - Get Text activities  │
│  - Screenshot           │
│  - Write to Excel/Log   │
└─────────────────────────┘
```

---

## Workflow Overview

### High-Level Steps

1. **Initialize Browser**
   - Open Chrome/Edge
   - Navigate to `http://localhost:8000/portal`
   - Wait for page load

2. **Input Transaction Data**
   - Type into form fields (Transaction ID, Customer ID, Amount, etc.)
   - Set checkboxes (Cash transaction, High-risk country, etc.)
   - Select dropdowns (Transaction type, Location)

3. **Submit Transaction**
   - Click "Check Compliance" button
   - Wait for results to appear

4. **Extract Results**
   - Get risk score from results card
   - Get risk level (LOW/MEDIUM/HIGH)
   - Get flagged rules list
   - Get review requirement flag

5. **Store Results**
   - Write to Excel row
   - Save screenshot (optional)
   - Log to UiPath Orchestrator

6. **Repeat or Close**
   - Process next transaction or close browser

---

## Prerequisites

### System Requirements

- **UiPath Studio**: 2021.10 or higher
- **Browser**: Chrome or Edge (latest version)
- **UiPath Packages**:
  - `UiPath.UIAutomation.Activities` (Browser automation)
  - `UiPath.Excel.Activities` (Excel operations)
  - `UiPath.System.Activities` (Screenshot, delays)

### Environment Setup

1. **API Server Running**:
   ```bash
   cd /path/to/rpa-finb
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   uvicorn api.main:app --reload
   ```

2. **Web Portal Accessible**:
   - Open browser to `http://localhost:8000/portal`
   - Verify form loads correctly
   - Test manual submission works

3. **Browser Extension** (Optional but recommended):
   - Install UiPath Extension for Chrome/Edge
   - This improves selector reliability

---

## Project Structure

```
docs/uipath-v2-web/
├── README.md              ← You are here (Overview)
├── STEP_BY_STEP.md        ← Detailed workflow building guide
├── SELECTORS.md           ← Web element selectors reference
└── TESTING.md             ← Testing procedures

Related files:
├── web/index.html         ← Web portal HTML
├── web/static/js/app.js   ← Frontend JavaScript
└── api/main.py            ← Backend API (includes /portal endpoint)
```

---

## Quick Start Guide

### 1. Start the Web Portal

```bash
# Terminal 1: Start API
cd rpa-finb
source venv/bin/activate
uvicorn api.main:app --reload
```

Open browser to verify: `http://localhost:8000/portal`

### 2. Create UiPath Project

1. Open UiPath Studio
2. Create new **Process** project
3. Name: `ComplianceMonitoring_WebPortal`
4. Install required packages (see Prerequisites)

### 3. Build the Workflow

Follow the detailed guide in **STEP_BY_STEP.md** to:
- Add browser automation activities
- Configure selectors
- Build data extraction logic
- Add error handling

### 4. Test the Workflow

Follow **TESTING.md** to verify:
- Browser opens correctly
- Form fields are filled
- Results are extracted accurately

---

## Sample Transaction

Use this sample data for testing:

```
Transaction ID: TXN001
Customer ID: CUST001
Amount: 15000.00
Transaction Type: Wire Transfer
Location: Cayman Islands
Is High-Risk Country: ✓ (checked)
Is Cash: □ (unchecked)
Is Round Amount: ✓ (checked)
Unusual Time: ✓ (checked)
Recipient New: ✓ (checked)
Txn Count Last 24h: 5
Avg Txn Amount: 12000.00
Customer Risk Score: 0.75
Days Since Last Txn: 2
Is Offshore: ✓ (checked)
Velocity Score: 0.85
Hour of Day: 23
Day of Week: 5
```

**Expected Results**:
- Risk Score: ~0.85-0.92
- Risk Level: HIGH
- Flagged Rules: BSA_LARGE_CASH, FATF_HIGH_RISK, OFAC_SANCTIONED (several)
- Requires Review: YES

---

## Common Use Cases

### Use Case 1: Single Transaction Testing

**Scenario**: Compliance officer wants to test a suspicious transaction manually.

**Workflow**:
1. Officer provides transaction details (amount, customer, etc.)
2. RPA bot opens web portal
3. Bot fills in all fields with provided data
4. Bot submits and extracts results
5. Bot saves screenshot as PDF for audit trail
6. Bot writes results to Excel report

**Benefits**:
- Fast (no manual typing)
- Consistent (no human error)
- Auditable (screenshot evidence)

---

### Use Case 2: Database-Driven Testing

**Scenario**: Test recent transactions from database through web UI.

**Workflow**:
1. Bot queries database for last 50 transactions
2. For each transaction:
   - Navigate to web portal
   - Fill form with database values
   - Submit and extract results
   - Save to Excel
3. Generate summary report

**Benefits**:
- Automated end-to-end testing
- Validates web UI works correctly
- Compares with direct API results (v1) for consistency

---

### Use Case 3: Regression Testing

**Scenario**: After portal updates, verify functionality still works.

**Workflow**:
1. Bot runs through 10 predefined test transactions
2. Compares results with expected baseline
3. Flags any discrepancies
4. Generates pass/fail report

**Benefits**:
- Automated QA testing
- Fast regression validation
- Early detection of UI bugs

---

## Performance Characteristics

### Speed

- **Single transaction**: 5-10 seconds (including browser load)
- **Subsequent transactions** (browser already open): 3-5 seconds each
- **Throughput**: ~10-20 transactions/minute

**Note**: Much slower than v1 (100+ txn/min) due to browser rendering overhead.

### Resource Usage

- **Memory**: 300-500 MB (browser process)
- **CPU**: Moderate during page load, low otherwise
- **Disk**: Minimal (unless saving many screenshots)

### Scalability

- **Recommended**: < 100 transactions per run
- **Maximum**: 500 transactions (browser may become slow)
- **For larger batches**: Use v1 (CSV processing) instead

---

## Integration with v1

You can combine v1 and v2 in hybrid workflows:

### Hybrid Workflow 1: Bulk + Spot Check

1. Use **v1** to process 1000 transactions via CSV
2. Identify HIGH risk transactions requiring review
3. Use **v2** to re-process those through web UI for visual verification
4. Save screenshots as audit evidence

### Hybrid Workflow 2: Validation

1. Process same transaction through both v1 and v2
2. Compare results (risk_score, risk_level should match)
3. Flag any discrepancies for investigation

---

## Troubleshooting

### Browser doesn't open
- Verify Chrome/Edge is installed
- Install UiPath browser extension
- Check `browserType` variable is set to "Chrome" or "Edge"

### Form fields not filled
- Check selectors in SELECTORS.md
- Use UiPath UI Explorer to verify selectors
- Add delays if page loads slowly

### Results not extracted
- Verify form submission worked (results card appeared)
- Check selector for results elements
- Add "Wait for Element" activity before extraction

### Slow performance
- Close unnecessary browser tabs/windows
- Disable browser extensions (except UiPath)
- Use headless mode for faster execution (see STEP_BY_STEP.md)

---

## Next Steps

1. **Read STEP_BY_STEP.md** - Build the workflow step-by-step
2. **Reference SELECTORS.md** - Find all web element selectors
3. **Follow TESTING.md** - Validate your workflow
4. **See ../getting-started/FLOW_GUIDE.md** - Understand overall system

---

## Related Documentation

- **v1 Documentation**: `docs/uipath-v1-csv/` - CSV batch processing
- **Web Portal User Guide**: `WEB_PORTAL_GUIDE.md` - Manual portal usage
- **API Documentation**: `docs/api/ENDPOINTS.md` - API reference
- **Architecture**: `docs/architecture/ARCHITECTURE.md` - System design

---

## Comparison: v1 vs v2 Decision Matrix

| Requirement | Recommended Version |
|-------------|-------------------|
| Process 1000+ transactions | v1 (CSV) |
| Process < 50 transactions | v2 (Web) |
| Need screenshots for audit | v2 (Web) |
| Maximum speed required | v1 (CSV) |
| Validate web UI functionality | v2 (Web) |
| Scheduled batch processing | v1 (CSV) |
| Ad-hoc manual testing | v2 (Web) |
| Integration with external systems via API | v1 (CSV) |
| Demonstrate to stakeholders | v2 (Web) |
| Production monitoring (unattended) | v1 (CSV) |

---

**Document Version**: 1.0  
**Last Updated**: 2026-03-26  
**Next**: Read [STEP_BY_STEP.md](./STEP_BY_STEP.md) to build the workflow
