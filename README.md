# RPA-Based Financial Compliance Monitoring System

A comprehensive system for monitoring financial transactions using rule-based compliance checks and machine learning risk scoring, designed for integration with UiPath RPA workflows.

## 🆕 Version 2.0 - Now with Live Web Portal!

**NEW**: Interactive bank transaction portal with real-time compliance monitoring!  
👉 Access at: `http://localhost:8000/portal` (after starting the API)  
📖 See [WEB_PORTAL_GUIDE.md](WEB_PORTAL_GUIDE.md) for details

## Overview

This system provides **TWO ways** to monitor transactions:

### v1: CSV + Batch Processing (UiPath Integration)
- Process transactions from CSV files
- Batch compliance checking
- UiPath RPA workflow integration
- Generate compliance reports

### v2: Live Web Portal (Real-time Banking Simulation)
- **NEW!** Interactive bank transaction interface
- Real-time compliance checking
- Live dashboard and analytics
- Transaction history tracking
- Professional banking UI

Both versions use the same compliance engine:
- 10 regulatory compliance rules (BSA, FATF, OFAC, etc.)
- Machine learning risk scoring
- Combined risk assessment logic

## Project Structure

```
rpa-finb/
├── data/
│   ├── generate_dataset.py      # Synthetic dataset generator
│   └── transactions.csv          # Generated transaction data
├── models/
│   ├── train_model.py           # ML model training script
│   └── model.pkl                # Trained RandomForest model
├── rules/
│   └── compliance_rules.py      # 10 regulatory compliance rules
├── api/
│   └── main.py                  # FastAPI backend server
├── web/                         # 🆕 v2 Web Portal
│   ├── index.html               # Bank transaction interface
│   └── static/
│       └── js/
│           └── app.js           # Frontend logic
├── outputs/
│   ├── generate_reports.py      # Report generation script
│   ├── compliance_report.csv    # Full compliance analysis
│   └── flagged_transactions.csv # High/medium risk transactions
├── requirements.txt             # Python dependencies
├── run_pipeline.py             # Main pipeline executor
├── README.md                   # This file
└── WEB_PORTAL_GUIDE.md         # 🆕 Web portal documentation
```

## Features

### 1. Synthetic Dataset Generation
- 1000 realistic transaction records
- 18 features including amount, countries, KYC status, sanctions flags
- Simulates normal and suspicious transaction patterns

### 2. Regulatory Rule Engine
Implements 10 compliance rules:
1. **Large Transaction (BSA)** - Transactions > $1,000,000
2. **High-Risk Country (FATF)** - Transfers to Iran, North Korea, Syria, etc.
3. **Sanctions Match (OFAC)** - Flagged entities
4. **Structuring Detection** - > 5 transactions in 24 hours
5. **Rapid Transactions** - > 20 transactions in 7 days
6. **New Account High Transaction** - Account < 30 days with > $500K
7. **Dormant Account Activity** - Dormant account with > $200K
8. **Repeated Beneficiary** - Multiple transfers to same beneficiary
9. **Cross-Border High Value** - International transfers > $300K
10. **KYC Incomplete** - Unverified customer status

### 3. Machine Learning Risk Scoring
- **Model**: RandomForestClassifier
- **Features**: Transaction amount, account age, transaction frequency, geographic data
- **Output**: Risk score (0-1) and risk label (low/medium/high)
- **Performance**: Balanced accuracy with class weighting

### 4. FastAPI Backend
Three main endpoints:
- `GET /transactions` - Retrieve transaction dataset
- `POST /predict` - ML risk prediction for a transaction
- `POST /compliance-check` - Complete compliance analysis

### 5. Final Risk Determination
Combined logic:
- **HIGH**: Sanctions flag OR risk score > 0.8
- **MEDIUM**: ≥2 rules triggered OR risk score > 0.5
- **LOW**: Otherwise

## Installation

1. **Clone/Setup Project**
```bash
cd rpa-finb
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

## Usage

### 🚀 Quick Start (v2 Web Portal)

**Experience the live banking portal:**

```bash
# 1. Run pipeline (first time only)
python run_pipeline.py

# 2. Start API server
python api/main.py

# 3. Open browser
# Visit: http://localhost:8000/portal
```

**That's it!** You now have a live bank transaction portal with real-time compliance monitoring.

See [WEB_PORTAL_GUIDE.md](WEB_PORTAL_GUIDE.md) for detailed portal usage.

---

### Quick Start: Run Complete Pipeline (v1)

Execute the entire workflow in one command:
```bash
python run_pipeline.py
```

This will:
1. Generate synthetic dataset
2. Train ML model
3. Generate compliance reports

### Step-by-Step Execution

**1. Generate Dataset**
```bash
python data/generate_dataset.py
```
Output: `data/transactions.csv`

**2. Train ML Model**
```bash
python models/train_model.py
```
Output: `models/model.pkl`

**3. Generate Reports**
```bash
python outputs/generate_reports.py
```
Outputs:
- `outputs/compliance_report.csv`
- `outputs/flagged_transactions.csv`

**4. Start API Server**
```bash
python api/main.py
```
Server runs at: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

## API Usage Examples

### 1. Get All Transactions
```bash
curl http://localhost:8000/transactions?limit=10
```

### 2. Predict Risk Score
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST1234",
    "account_age_days": 100,
    "account_status": "active",
    "transaction_amount": 750000,
    "transaction_type": "transfer",
    "transaction_time": "2024-03-01 10:30:00",
    "sender_country": "USA",
    "receiver_country": "UAE",
    "beneficiary_id": "BEN5678",
    "beneficiary_bank": "Bank_A",
    "customer_avg_txn": 500000,
    "txn_count_last_24h": 3,
    "txn_count_last_7d": 8,
    "kyc_status": "verified",
    "sanctions_flag": 0,
    "device_location": "USA",
    "channel": "online",
    "is_international": 1
  }'
```

### 3. Full Compliance Check
```bash
curl -X POST http://localhost:8000/compliance-check \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST1234",
    "account_age_days": 15,
    "account_status": "active",
    "transaction_amount": 1200000,
    "transaction_type": "transfer",
    "transaction_time": "2024-03-01 10:30:00",
    "sender_country": "USA",
    "receiver_country": "Iran",
    "beneficiary_id": "BEN5678",
    "beneficiary_bank": "International_Bank_X",
    "customer_avg_txn": 50000,
    "txn_count_last_24h": 7,
    "txn_count_last_7d": 25,
    "kyc_status": "pending",
    "sanctions_flag": 0,
    "device_location": "USA",
    "channel": "online",
    "is_international": 1
  }'
```

Response:
```json
{
  "transaction_id": "TXN12345678",
  "rules_triggered": [
    "Large Transaction (BSA)",
    "High-Risk Country (FATF)",
    "Structuring Detection",
    "Rapid Transactions",
    "New Account High Transaction",
    "Cross-Border High Value",
    "KYC Incomplete"
  ],
  "num_rules_triggered": 7,
  "risk_score": 0.9234,
  "risk_label": "high",
  "final_risk": "HIGH"
}
```

## UiPath Integration Guide

### Integration Architecture

```
UiPath Workflow
    ↓
Read transactions.csv
    ↓
For each transaction:
    ↓
HTTP Request → POST /compliance-check
    ↓
Receive: {rules_triggered, risk_score, final_risk}
    ↓
Write to Excel/Database
    ↓
Generate final report
```

### UiPath Workflow Steps

1. **Setup**
   - Install UiPath.WebAPI.Activities package
   - Configure base URL: `http://localhost:8000`

2. **Read Transactions**
   ```
   Use "Read CSV" activity
   File: data/transactions.csv
   Output: transactionsDT (DataTable)
   ```

3. **Process Each Transaction**
   ```
   For Each Row in transactionsDT:
     - Build JSON request body
     - HTTP Request activity
       - Method: POST
       - Endpoint: /compliance-check
       - Body: transaction JSON
     - Parse JSON response
     - Extract: rules_triggered, risk_score, final_risk
     - Add to results DataTable
   ```

4. **HTTP Request Configuration**
   ```
   Activity: HTTP Request
   URL: http://localhost:8000/compliance-check
   Method: POST
   Headers: 
     Content-Type: application/json
   Body: 
     {
       "customer_id": row("customer_id").ToString(),
       "account_age_days": CInt(row("account_age_days")),
       "account_status": row("account_status").ToString(),
       "transaction_amount": CDbl(row("transaction_amount")),
       ...
     }
   Output: responseJSON
   ```

5. **Parse Response**
   ```
   Deserialize JSON activity
   Input: responseJSON
   Output: complianceResult (JObject)
   
   Extract values:
   - finalRisk = complianceResult("final_risk").ToString()
   - riskScore = CDbl(complianceResult("risk_score"))
   - rulesTriggered = complianceResult("rules_triggered").ToString()
   ```

6. **Generate Report**
   ```
   Use "Write Range" activity
   File: compliance_results.xlsx
   DataTable: resultsDT
   ```

### Sample UiPath Variables

| Variable Name | Type | Description |
|--------------|------|-------------|
| transactionsDT | DataTable | Input transactions |
| resultsDT | DataTable | Compliance results |
| currentTransaction | DataRow | Current row being processed |
| requestBody | String | JSON request body |
| responseJSON | String | API response |
| complianceResult | JObject | Parsed response |
| finalRisk | String | HIGH/MEDIUM/LOW |
| riskScore | Double | 0.0 to 1.0 |

### Error Handling in UiPath

```
Try-Catch Block:
  Try:
    - HTTP Request to API
    - Parse response
    - Store results
  Catch (Exception ex):
    - Log error to file
    - Add error row to results
    - Continue with next transaction
```

### Performance Optimization

- **Batch Processing**: Process transactions in batches of 100
- **Parallel Processing**: Use Parallel For Each for independent transactions
- **Connection Pooling**: Reuse HTTP client connections
- **Timeout Settings**: Set appropriate timeouts (30-60 seconds)

## Output Files

### compliance_report.csv
Complete analysis of all transactions:
- transaction_id
- customer_id
- transaction_amount
- rules_triggered
- num_rules_triggered
- risk_score
- final_risk

### flagged_transactions.csv
Filtered list of MEDIUM and HIGH risk transactions sorted by risk score.

## Technical Details

### Dataset Schema
```python
{
  'transaction_id': str,
  'customer_id': str,
  'account_age_days': int,
  'account_status': str,  # active/dormant
  'transaction_amount': float,
  'transaction_type': str,  # transfer/deposit/withdrawal
  'transaction_time': str,  # YYYY-MM-DD HH:MM:SS
  'sender_country': str,
  'receiver_country': str,
  'beneficiary_id': str,
  'beneficiary_bank': str,
  'customer_avg_txn': float,
  'txn_count_last_24h': int,
  'txn_count_last_7d': int,
  'kyc_status': str,  # verified/pending
  'sanctions_flag': int,  # 0/1
  'device_location': str,
  'channel': str,  # ATM/online/branch
  'is_international': int  # 0/1
}
```

### ML Model Details
- **Algorithm**: RandomForestClassifier
- **Trees**: 100
- **Max Depth**: 10
- **Class Weight**: Balanced
- **Features**: 13 (numeric + encoded categorical)
- **Target**: Binary (suspicious/normal)

## Testing

### Test Rule Engine
```bash
python rules/compliance_rules.py
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# List all rules
curl http://localhost:8000/rules

# Get transaction summary
curl http://localhost:8000/transactions/summary
```

## Constraints & Design Decisions

- **Simplicity**: Modular, easy-to-understand code
- **No Deep Learning**: Uses RandomForest for interpretability
- **No Microservices**: Single FastAPI application
- **CSV-based**: Simple file formats for UiPath integration
- **Synthetic Data**: Realistic patterns without real PII

## Future Enhancements

- [ ] Real-time transaction streaming
- [ ] Database integration (PostgreSQL)
- [ ] Advanced ML models (XGBoost, LightGBM)
- [ ] Web dashboard for visualization
- [ ] Authentication and API keys
- [ ] Webhook notifications for high-risk transactions
- [ ] Integration with actual OFAC/FATF APIs

## Dependencies

- **FastAPI**: REST API framework
- **Uvicorn**: ASGI server
- **Pandas**: Data manipulation
- **Scikit-learn**: Machine learning
- **Pydantic**: Data validation
- **Joblib**: Model serialization

## License

This is an educational project demonstrating RPA integration with compliance systems.

## Contact & Support

For questions or issues, refer to the plan_context.txt file for system specifications.

---

**Status**: ✅ Operational
**Version**: 1.0.0
**Last Updated**: 2024
