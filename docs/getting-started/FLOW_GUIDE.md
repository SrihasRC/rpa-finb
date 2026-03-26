# 🚀 GETTING STARTED - Complete Flow Guide

**Welcome!** This guide will take you through the entire system step-by-step.

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [What You Can Do](#what-you-can-do)
3. [Installation & Setup](#installation--setup)
4. [Choosing Your Path](#choosing-your-path)
5. [Quick Test](#quick-test)
6. [Next Steps](#next-steps)

---

## System Overview

You have a **Financial Compliance Monitoring System** with:
- ✅ **10 regulatory compliance rules** (BSA, FATF, OFAC, etc.)
- ✅ **ML risk scoring model** (RandomForest)
- ✅ **REST API backend** (FastAPI)
- ✅ **Two different usage modes** (v1 and v2)

---

## What You Can Do

### **Option 1: v1 - CSV Batch Processing (UiPath RPA)**
**Best for:** Automation, bulk processing, RPA workflows

**What it does:**
- Read transactions from Excel/CSV files
- Send each transaction to API for compliance checking
- Get results back (rules triggered, risk score, final risk)
- Write results to Excel output file
- Generate compliance reports

**Use case:** Automate daily batch processing of 100s/1000s of transactions

---

### **Option 2: v2 - Live Web Portal**
**Best for:** Manual testing, demos, live transaction simulation

**What it does:**
- Open a bank transaction portal in browser
- Submit transactions one-by-one like a real bank
- See instant compliance results (<1 second)
- View transaction history and dashboard
- Visual risk indicators (red/yellow/green)

**Use case:** Test the system, demonstrate to stakeholders, manual monitoring

---

### **Option 3: v2 Web + UiPath Automation**
**Best for:** Automated web testing, end-to-end testing

**What it does:**
- Use UiPath to automate the web portal
- Fill forms automatically
- Submit transactions
- Extract results from web page
- Generate test reports

**Use case:** Automated testing of the web interface, regression testing

---

## Installation & Setup

### Step 1: Initial Setup (5 minutes)

```bash
# 1. Navigate to project
cd /path/to/rpa-finb

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt
```

### Step 2: Generate Data & Train Model (2 minutes)

```bash
# Run complete pipeline
python run_pipeline.py
```

**This will:**
- Generate 1000 synthetic transactions → `data/transactions.csv`
- Train ML model → `models/model.pkl`
- Create compliance reports → `outputs/`

### Step 3: Start API Server

```bash
# Start server (keep this running)
python api/main.py
```

**Server will run at:** `http://localhost:8000`

**You should see:**
```
✓ Model loaded successfully
✓ Dataset loaded: 1000 transactions
INFO: Uvicorn running on http://0.0.0.0:8000
```

### Step 4: Verify Installation

Open browser → http://localhost:8000/docs

You should see **Swagger API documentation**.

✅ **Setup Complete!**

---

## Choosing Your Path

Now choose which version you want to use:

### 🎯 Path A: Just Want to Try It Quickly?

**→ Go to v2 Web Portal**

1. Open browser: `http://localhost:8000/portal`
2. Fill out transaction form
3. Click "Process Transaction"
4. See instant results!

**Guide:** `docs/getting-started/QUICK_TEST.md`

---

### 🤖 Path B: Want to Build RPA Automation (CSV Processing)?

**→ Use v1 - CSV Batch Processing**

This is the **traditional RPA approach**:
- Read from Excel/CSV
- Process via API
- Write to Excel/CSV

**Guide:** `docs/uipath-v1-csv/README.md`

**Includes:**
- Step-by-step UiPath workflow creation
- Every activity configuration
- Variable setup
- Error handling
- Testing procedures

---

### 🌐 Path C: Want to Automate the Web Portal?

**→ Use v2 - Web Portal Automation**

This is **modern UI automation**:
- Open web portal
- Fill forms automatically
- Submit transactions
- Extract results from UI

**Guide:** `docs/uipath-v2-web/README.md`

**Includes:**
- Web automation workflow
- Selector creation
- Form filling
- Data extraction
- Screenshot capture

---

## Quick Test

### Test the System (1 minute)

**Option 1: Test via Web Portal**

1. Open: `http://localhost:8000/portal`
2. Enter:
   - Type: Transfer
   - Amount: 1500000
   - Sender: USA
   - Receiver: Canada
   - Beneficiary: Test User
   - Channel: Online
3. Click "Process Transaction"
4. **Expected Result:** RED (HIGH RISK) - "Large Transaction (BSA)" rule triggered

**Option 2: Test via API (curl)**

```bash
curl -X POST http://localhost:8000/compliance-check \
  -H "Content-Type: application/json" \
  -d @test_transaction.json
```

**Option 3: Test via API Docs**

1. Open: `http://localhost:8000/docs`
2. Find `/compliance-check` endpoint
3. Click "Try it out"
4. Use example request
5. Click "Execute"

---

## Next Steps

### For Each Path:

#### Path A: Web Portal User
1. ✅ Test the portal
2. 📖 Read: `docs/getting-started/WEB_PORTAL_USER_GUIDE.md`
3. 🧪 Try all 5 test scenarios
4. 📊 Explore dashboard features

#### Path B: RPA Developer (CSV Processing)
1. 📖 Read: `docs/uipath-v1-csv/README.md`
2. 🛠️ Install UiPath Studio
3. 📝 Follow step-by-step workflow creation
4. 🧪 Test with sample CSV
5. 📊 Review output reports

#### Path C: RPA Developer (Web Automation)
1. 📖 Read: `docs/uipath-v2-web/README.md`
2. 🛠️ Install UiPath Studio + Browser extension
3. 📝 Follow web automation guide
4. 🧪 Test automated form filling
5. 📊 Verify result extraction

---

## Documentation Structure

```
rpa-finb/
├── docs/
│   ├── getting-started/           ← START HERE
│   │   ├── FLOW_GUIDE.md         ← This file
│   │   ├── QUICK_TEST.md         ← Quick testing guide
│   │   ├── INSTALLATION.md       ← Detailed setup
│   │   └── WEB_PORTAL_USER_GUIDE.md
│   │
│   ├── uipath-v1-csv/            ← For CSV/Excel RPA
│   │   ├── README.md             ← Overview
│   │   ├── STEP_BY_STEP.md       ← Detailed activities
│   │   ├── WORKFLOW_GUIDE.md     ← Complete workflow
│   │   └── TESTING.md            ← Testing guide
│   │
│   ├── uipath-v2-web/            ← For Web Portal RPA
│   │   ├── README.md             ← Overview
│   │   ├── STEP_BY_STEP.md       ← Detailed activities
│   │   ├── WORKFLOW_GUIDE.md     ← Complete workflow
│   │   └── TESTING.md            ← Testing guide
│   │
│   ├── api/                      ← API Documentation
│   │   ├── ENDPOINTS.md          ← All endpoints
│   │   └── EXAMPLES.md           ← Usage examples
│   │
│   └── architecture/             ← Technical Details
│       ├── SYSTEM_DESIGN.md
│       └── COMPLIANCE_RULES.md
│
└── [rest of project files...]
```

---

## Visual Flow

```
┌─────────────────────────────────────────────────────────┐
│  START: Do you have the system running?                 │
└────────────────────┬────────────────────────────────────┘
                     │
                ┌────▼────┐
                │   NO    │
                └────┬────┘
                     │
        ┌────────────▼─────────────┐
        │  Follow Installation     │
        │  (5 minutes)             │
        │  1. Setup venv           │
        │  2. Install packages     │
        │  3. Run pipeline         │
        │  4. Start API server     │
        └────────────┬─────────────┘
                     │
                ┌────▼────┐
                │  YES    │
                └────┬────┘
                     │
        ┌────────────▼─────────────────────┐
        │  What do you want to do?         │
        └──┬───────────┬──────────────┬───┘
           │           │              │
    ┌──────▼─────┐ ┌──▼──────┐ ┌────▼──────┐
    │  Just Test │ │ CSV RPA │ │  Web RPA  │
    │  Manually  │ │ (v1)    │ │  (v2)     │
    └──────┬─────┘ └──┬──────┘ └────┬──────┘
           │          │              │
           │          │              │
    ┌──────▼─────────┐│              │
    │ Open Portal    ││              │
    │ localhost:8000 ││              │
    │ /portal        ││              │
    └────────────────┘│              │
                      │              │
              ┌───────▼──────┐ ┌─────▼────────┐
              │ Install      │ │ Install      │
              │ UiPath       │ │ UiPath +     │
              │ Studio       │ │ Browser Ext  │
              └───────┬──────┘ └─────┬────────┘
                      │              │
              ┌───────▼──────┐ ┌─────▼────────┐
              │ Follow       │ │ Follow       │
              │ CSV Guide    │ │ Web Guide    │
              │ Step-by-Step │ │ Step-by-Step │
              └───────┬──────┘ └─────┬────────┘
                      │              │
              ┌───────▼──────┐ ┌─────▼────────┐
              │ Read CSV     │ │ Automate     │
              │ → API        │ │ Web Form     │
              │ → Excel Out  │ │ → Extract    │
              └──────────────┘ └──────────────┘
```

---

## Common Questions

### Q: Which version should I use?

**A:** Depends on your goal:

| Goal | Use |
|------|-----|
| Learn the system quickly | v2 Web Portal (manual) |
| Automate CSV processing | v1 UiPath (CSV) |
| Automate web testing | v2 UiPath (Web) |
| Demonstrate to stakeholders | v2 Web Portal (manual) |
| Process 1000s of transactions | v1 UiPath (CSV) |

### Q: Can I use both v1 and v2?

**A:** Yes! They work together:
- Use v2 web portal for testing
- Use v1 CSV processing for production batches
- Both use the same API backend

### Q: Do I need UiPath?

**A:** No! You can:
- Use the web portal manually (v2)
- Call the API from any programming language
- Use curl/Postman for testing

UiPath is optional for automation.

### Q: Is there a difference in the API?

**A:** No! Both v1 and v2 use the **same API endpoint** (`/compliance-check`).

The difference is:
- **v1**: UiPath reads CSV → calls API → writes Excel
- **v2**: UiPath automates web browser → same results

### Q: Which is better for learning?

**A:** Start with **v2 Web Portal** (manual testing), then move to **v1 UiPath** (automation).

---

## Quick Reference Card

### Essential URLs
```
Web Portal:    http://localhost:8000/portal
API Docs:      http://localhost:8000/docs
Health Check:  http://localhost:8000/health
Rules List:    http://localhost:8000/rules
```

### Essential Commands
```bash
# Start server
python api/main.py

# Run pipeline (first time)
python run_pipeline.py

# Test installation
python test_installation.py

# Using Makefile
make pipeline    # Run complete pipeline
make api         # Start API server
make test        # Run tests
```

### Essential Files
```
Input:  data/transactions.csv           (generated data)
Model:  models/model.pkl                (trained model)
Output: outputs/compliance_report.csv   (results)
        outputs/flagged_transactions.csv (high/medium risk)
```

---

## Support & Help

### Getting Help

1. **Check the docs** in order:
   - This file (FLOW_GUIDE.md)
   - Your chosen path guide
   - Step-by-step activity guide
   - Troubleshooting section

2. **Common Issues:**
   - Server not starting → Check if port 8000 is free
   - Model not loaded → Run `python run_pipeline.py` first
   - Connection error → Ensure API server is running

3. **Test Health:**
   ```bash
   curl http://localhost:8000/health
   ```

---

## Summary

### You Are Here: 🎯 START

**Next Steps:**

1. ✅ Complete installation (if not done)
2. ✅ Choose your path (A, B, or C)
3. ✅ Read the relevant guide
4. ✅ Start building!

**Recommended Learning Path:**

```
Day 1: Setup + Quick Test (Web Portal)
Day 2: Learn API (via Swagger docs)
Day 3: Build v1 UiPath (CSV processing)
Day 4: Build v2 UiPath (Web automation)
Day 5: Customize & extend
```

---

## Ready? Let's Go! 🚀

**Pick your starting point:**

- 🌐 **Test Web Portal** → Open http://localhost:8000/portal
- 🤖 **Build CSV RPA** → Read `docs/uipath-v1-csv/README.md`
- 🎯 **Build Web RPA** → Read `docs/uipath-v2-web/README.md`

---

**Version**: 2.0  
**Last Updated**: March 2024  
**Status**: ✅ Complete

**Good luck!** 💪
