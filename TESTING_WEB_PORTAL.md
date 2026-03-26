# Testing the Transaction Submission Workflow

## Quick Start Guide

### 1. Start the API Server

```bash
cd /home/srihasrc/Music/rpa-finb
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn api.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process...
```

### 2. Open the Web Portal

Open your browser and navigate to:
```
http://localhost:8000/portal
```

You should see the **FinCompliance** dashboard with:
- **Left Sidebar** - Dark navigation menu
- **Main Area** - Dashboard with statistics (initially all zeros)

### 3. Navigate to "Check Transaction" Page

Click on **"Check Transaction"** in the left sidebar (second item with search icon)

This page has:
- **Left Panel**: Transaction form with fields:
  - Transaction Type (dropdown)
  - Amount
  - Sender Country
  - Receiver Country
  - Beneficiary Name
  - Channel
  - Submit button: "Check Compliance"
  
- **Right Panel**: Compliance results (initially empty, says "Submit a transaction to see results")

### 4. Submit a Test Transaction

Fill in the form with sample data:

**Low Risk Transaction:**
- Transaction Type: `Deposit`
- Amount: `500.00`
- Sender Country: `United States`
- Receiver Country: `United States`
- Beneficiary Name: `John Smith`
- Channel: `Online Banking`

Click **"Check Compliance"** button.

**What happens:**
1. Button changes to "Processing..." with spinner
2. Loading state appears
3. Backend API is called: `POST /compliance-check`
4. ML model + 10 compliance rules run
5. Results appear in right panel:
   - Risk Score (0.00-1.00)
   - Risk Level (LOW/MEDIUM/HIGH badge)
   - Manual Review flag
   - Flagged compliance rules (if any)
6. Transaction is stored in localStorage
7. Dashboard statistics update

**High Risk Transaction:**
- Transaction Type: `Transfer`
- Amount: `25000.00`
- Sender Country: `United States`
- Receiver Country: `Iran` ← **High-risk country**
- Beneficiary Name: `ACME Corp`
- Channel: `ATM`

This should trigger:
- Risk Score: ~0.85-0.95
- Risk Level: **HIGH**
- Flagged Rules: BSA_LARGE_CASH, FATF_HIGH_RISK, OFAC_SANCTIONED, etc.
- Review Required: **YES**

### 5. View Transaction History

Click **"Transaction History"** in sidebar to see all processed transactions in a table.

### 6. Monitor Live Transactions

Click **"Live Monitor"** to see recent transactions in card view (auto-refreshes every 5 seconds).

### 7. Export Reports

Click **"Reports"** to export data:
- CSV format
- JSON format
- Summary text report

---

## How This Triggers the Backend

### Flow Diagram

```
[Web Form] 
    ↓ (User clicks "Check Compliance")
[JavaScript - app.js]
    ↓ (Builds transaction object)
[HTTP POST to /compliance-check]
    ↓
[FastAPI Backend - api/main.py]
    ↓ (Validates input)
[Compliance Engine]
    ├─→ [ML Model - models/risk_model.pkl]
    └─→ [10 Compliance Rules - rules/compliance_rules.py]
    ↓ (Calculates risk)
[JSON Response]
    ↓
[JavaScript displays results]
    ↓
[Results shown in right panel]
    ↓
[Transaction stored in localStorage]
    ↓
[Dashboard updates]
```

### API Endpoint Details

**Endpoint**: `POST http://localhost:8000/compliance-check`

**Request Body** (automatically built by JavaScript):
```json
{
  "transaction_id": "TXN1234567890",
  "customer_id": "CUST1234",
  "amount": 15000.00,
  "transaction_type": "transfer",
  "location": "Iran",
  "is_high_risk_country": true,
  "is_cash": false,
  "is_round_amount": true,
  "unusual_time": false,
  "recipient_new": true,
  "txn_count_last_24h": 5,
  "avg_txn_amount": 12000.00,
  "customer_risk_score": 0.45,
  "days_since_last_txn": 3,
  "is_offshore": true,
  "velocity_score": 0.75,
  "hour_of_day": 14,
  "day_of_week": 3
}
```

**Response**:
```json
{
  "transaction_id": "TXN1234567890",
  "risk_score": 0.89,
  "risk_level": "HIGH",
  "flagged_rules": [
    "BSA_LARGE_CASH",
    "FATF_HIGH_RISK",
    "OFAC_SANCTIONED"
  ],
  "requires_review": true,
  "timestamp": "2024-03-26T14:30:45.123456"
}
```

---

## UiPath Integration

### How UiPath v2 Uses This

The UiPath v2 workflow automates this exact process:

1. **Open Browser** → `http://localhost:8000/portal`
2. **Click** → "Check Transaction" in sidebar
3. **Type Into** → Fill all form fields
4. **Click** → "Check Compliance" button
5. **Wait** → For results to appear
6. **Get Text** → Extract risk score, level, rules
7. **Take Screenshot** → Save as audit evidence
8. **Write to Excel** → Save results

### Key Selectors for UiPath

**Form Fields:**
- Transaction Type: `#transactionType`
- Amount: `#amount`
- Sender Country: `#senderCountry`
- Receiver Country: `#receiverCountry`
- Beneficiary Name: `#beneficiaryName`
- Channel: `#channel`

**Submit Button:**
- ID: `#submitBtn`
- Text: "Check Compliance"

**Results:**
- Risk Score: First large number in `#complianceResults`
- Risk Level: Badge in `#complianceResults` containing "RISK"
- Flagged Rules: List items in `#complianceResults`

See `docs/uipath-v2-web/SELECTORS.md` for complete reference.

---

## Troubleshooting

### "API server not connected" message

**Issue**: API is not running  
**Solution**:
```bash
cd /home/srihasrc/Music/rpa-finb
source venv/bin/activate
uvicorn api.main:app --reload
```

### Form submit does nothing

**Issue**: JavaScript not loaded  
**Solution**: 
- Open browser DevTools (F12)
- Check Console for errors
- Verify `app.js` is loaded: Network tab → look for `app.js` (200 OK)

### Results don't appear

**Issue**: Backend error or slow response  
**Solution**:
- Check API terminal for errors
- Look at Network tab in DevTools
- Check request/response in Network → compliance-check

### "Check Transaction" page doesn't show

**Issue**: Navigation not working  
**Solution**:
- Hard refresh: Ctrl+F5
- Clear browser cache
- Check browser console for JavaScript errors

---

## Testing Different Risk Scenarios

### Scenario 1: Clean Transaction (LOW)
- Amount: < $5,000
- Domestic (USA → USA)
- Normal business hours
- Expected: Risk ~0.15, LOW, No flags

### Scenario 2: Moderate Risk (MEDIUM)
- Amount: $10,000
- Domestic but round amount
- New beneficiary
- Expected: Risk ~0.45, MEDIUM, 1-2 flags

### Scenario 3: High Risk (HIGH)
- Amount: > $20,000
- To high-risk country (Iran, North Korea, Syria)
- Cash transaction (ATM)
- Round amount
- Expected: Risk ~0.85, HIGH, 4+ flags

### Scenario 4: Critical Risk (HIGH)
- Amount: > $50,000
- International to sanctioned country
- Unusual time (late night)
- New recipient
- Multiple transactions today
- Expected: Risk ~0.95, HIGH, 6+ flags, Review Required

---

## Next Steps

After testing the web portal:

1. **Try UiPath v1 (CSV)**: Process batch transactions via API
   - See `docs/uipath-v1-csv/STEP_BY_STEP.md`
   
2. **Build UiPath v2 (Web)**: Automate the web form
   - See `docs/uipath-v2-web/STEP_BY_STEP.md`
   
3. **Export Reports**: Use Reports page to export transaction data

4. **Review Compliance Rules**: Check Rules page to see all 10 rules

---

**Last Updated**: 2026-03-26  
**Version**: 2.0 (Multi-page redesign)
