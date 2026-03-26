# START HERE - Quick Guide

Welcome to the **RPA-Based Financial Compliance Monitoring System**!

## 🆕 Version 2.0 - Now with Live Web Portal!

This project now offers **TWO ways** to use it:

### Option 1: Live Web Portal (Recommended for testing!)
Try the **interactive bank transaction portal** with real-time compliance monitoring!

### Option 2: CSV Batch Processing (UiPath Integration)
Process transactions from CSV files for RPA automation workflows.

---

## What is this project?

A complete, production-ready system for monitoring financial transactions using:
- **Rule-based compliance checking** (10 regulatory rules)
- **Machine Learning risk scoring** (RandomForest model)
- **REST API** (FastAPI with auto-generated docs)
- **🆕 Live Web Portal** (Real-time bank transaction interface)
- **UiPath RPA integration** (Complete workflow guide)

## 🚀 Super Quick Start (v2 Web Portal - 2 minutes!)

### Step 1: Setup & Install
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Run Pipeline (First time only)
```bash
python run_pipeline.py
```

### Step 3: Start Server & Open Portal
```bash
python api/main.py
```

Then open in browser: **http://localhost:8000/portal**

🎉 **Done!** You can now make live transactions and see real-time compliance checking!

See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for portal usage or [WEB_PORTAL_GUIDE.md](WEB_PORTAL_GUIDE.md) for details.

---

## Standard Quick Start (v1 CSV Processing - 5 minutes)

### Step 1: Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Everything
```bash
python run_pipeline.py
```

This will:
1. Generate 1000 synthetic transactions
2. Train the ML model
3. Create compliance reports

### Step 4: Start API Server
```bash
python api/main.py
```

Then open: http://localhost:8000/docs

## What gets generated?

After running the pipeline, you'll have:

```
data/transactions.csv          - 1000 synthetic transactions
models/model.pkl              - Trained ML model
outputs/compliance_report.csv - Full compliance analysis
outputs/flagged_transactions.csv - High/medium risk only
```

## Project Structure

```
rpa-finb/
├── data/              - Dataset generation
├── models/            - ML model training
├── rules/             - 10 compliance rules
├── api/               - FastAPI REST server
├── web/               - 🆕 Live web portal (v2)
├── outputs/           - Report generation
└── docs/              - All documentation
```

## Available Commands (using Makefile)

```bash
make help      # Show all available commands
make pipeline  # Run complete pipeline
make api       # Start API server
make test      # Test installation
make clean     # Remove generated files
```

## Documentation Guide

### For Different Users:

**🎯 Just Want to Try It? (v2 Web Portal)**
1. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - One-page cheat sheet
2. **[WEB_PORTAL_GUIDE.md](WEB_PORTAL_GUIDE.md)** - Complete portal guide
3. Open http://localhost:8000/portal and start!

**👨‍💻 Developers - Start with:**
1. **[README.md](README.md)** - Complete technical documentation
2. **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and flow diagrams
3. **[INSTALLATION.md](INSTALLATION.md)** - Setup and troubleshooting

**🤖 RPA Engineers - Start with:**
1. **[UIPATH_INTEGRATION.md](UIPATH_INTEGRATION.md)** - Complete UiPath workflow guide
2. **[test_transaction.json](test_transaction.json)** - Sample API request
3. API Docs: http://localhost:8000/docs

**📊 Business/Compliance - Start with:**
1. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - High-level overview
2. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick feature reference
3. Try the web portal: http://localhost:8000/portal

## Testing the System

### 1. Test Installation
```bash
python test_installation.py
```

### 2. Test Rule Engine
```bash
python rules/compliance_rules.py
```

### 3. Test API
```bash
# Start server first
python api/main.py

# In another terminal
curl http://localhost:8000/health
curl -X POST http://localhost:8000/compliance-check \
  -H "Content-Type: application/json" \
  -d @test_transaction.json
```

## Key Features

### 10 Compliance Rules
1. Large Transaction (BSA) - > $1M
2. High-Risk Country (FATF)
3. Sanctions Match (OFAC)
4. Structuring Detection
5. Rapid Transactions
6. New Account High Transaction
7. Dormant Account Activity
8. Repeated Beneficiary
9. Cross-Border High Value
10. KYC Incomplete

### ML Model
- **Algorithm**: RandomForestClassifier
- **Accuracy**: ~85-90%
- **Output**: Risk score (0-1) + label (low/medium/high)

### API Endpoints
- `GET /transactions` - Get all transactions
- `POST /predict` - ML risk prediction
- `POST /compliance-check` - Full compliance analysis
- `GET /rules` - List all rules

## UiPath Integration (Quick Overview)

1. **Read** transactions from CSV
2. **For each transaction**:
   - Build JSON request
   - POST to `/compliance-check`
   - Parse response
   - Store results
3. **Write** results to Excel

Full guide: `UIPATH_INTEGRATION.md`

## Common Issues & Solutions

### Issue: "ModuleNotFoundError"
**Solution**: Activate venv and install dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Solution**: Kill existing process or change port in `api/main.py`

### Issue: "Model not found"
**Solution**: Run pipeline first
```bash
python run_pipeline.py
```

## File Overview

| File | Purpose |
|------|---------|
| `run_pipeline.py` | Run everything at once |
| `test_installation.py` | Verify setup |
| `test_transaction.json` | Sample API request |
| `requirements.txt` | Python dependencies |
| `Makefile` | Convenient commands |
| `quickstart.sh` | Bash quick start |

## Next Steps

1. ✅ Run `python test_installation.py` to verify setup
2. ✅ Run `python run_pipeline.py` to generate data
3. ✅ Start API with `python api/main.py`
4. ✅ Test API at http://localhost:8000/docs
5. ✅ Review `UIPATH_INTEGRATION.md` for RPA workflow
6. ✅ Customize rules in `rules/compliance_rules.py`
7. ✅ Explore generated reports in `outputs/`

## Support

- **Technical Issues**: Check `INSTALLATION.md`
- **API Questions**: Check `README.md` or API docs
- **UiPath Integration**: Check `UIPATH_INTEGRATION.md`
- **Architecture**: Check `ARCHITECTURE.md`

## Performance

- Dataset generation: <2 seconds
- Model training: ~5-10 seconds
- API response: ~15-30ms per transaction
- Full pipeline (1000 txns): ~1-2 minutes

## Technologies Used

- **Python 3.8+**
- **FastAPI** - Modern web framework
- **Scikit-learn** - Machine learning
- **Pandas** - Data processing
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

## License

Educational/demonstration project. Not for production without security review.

---

**Status**: ✅ Complete & Ready

**Questions?** Read the docs in this order:
1. This file (START_HERE.md) ✓
2. README.md
3. Your role-specific guide (see above)

**Let's go!** → `python run_pipeline.py`

---
