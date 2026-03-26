# Quick Reference Card - v2 Web Portal

## 🚀 Getting Started (30 seconds)

```bash
python run_pipeline.py    # First time only
python api/main.py        # Start server
```

Then open: **http://localhost:8000/portal**

---

## 📊 Dashboard Cards

| Card | Meaning |
|------|---------|
| Account Balance | Current balance ($125,450 demo) |
| Today's Transactions | Count of transactions made today |
| Flagged Transactions | High/Medium risk count |
| Account Status | Active/Dormant |

---

## 💳 Making a Transaction

1. **Transaction Type** → Transfer/Deposit/Withdrawal
2. **Amount** → Enter in USD
3. **Countries** → Select sender & receiver
4. **Beneficiary** → Enter name
5. **Channel** → Online/Branch/ATM
6. **Submit** → Click "Process Transaction"

⏱️ Results appear in **<1 second**

---

## 🚦 Risk Levels

| Color | Risk | Meaning |
|-------|------|---------|
| 🔴 RED | HIGH | Sanctions/Critical rules/Score >80% |
| 🟡 YELLOW | MEDIUM | Multiple rules/Score 50-80% |
| 🟢 GREEN | LOW | Clean/Score <50% |

---

## ⚖️ 10 Compliance Rules

1. **Large Transaction** - >$1M
2. **High-Risk Country** - Iran, NK, Syria
3. **Sanctions Match** - Flagged entities
4. **Structuring** - >5 txns in 24h
5. **Rapid Transactions** - >20 txns in 7d
6. **New Account High** - <30d + >$500K
7. **Dormant Activity** - Dormant + >$200K
8. **Repeated Beneficiary** - Same >3 times
9. **Cross-Border High** - International + >$300K
10. **KYC Incomplete** - Unverified status

---

## 🧪 Test Scenarios

### Normal Transaction ✅
```
Amount: $5,000
Route: USA → USA
Result: LOW RISK
```

### Large Amount 🚨
```
Amount: $1,500,000
Route: USA → Canada
Result: HIGH RISK (Rule 1)
```

### High-Risk Country 🚨
```
Amount: $50,000
Route: USA → Iran
Result: HIGH RISK (Rule 2)
```

### Structuring Pattern 🚨
```
Do 6+ transactions quickly
Amount: $9,000 each
Result: MEDIUM/HIGH RISK (Rule 4)
```

---

## 📱 Features

- ✅ Real-time processing
- ✅ Auto-calculation (txn counts, international flag)
- ✅ Transaction history (last 50)
- ✅ localStorage persistence
- ✅ Visual risk indicators
- ✅ Rule breakdown display
- ✅ ML risk score (0-100%)

---

## 🔧 Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Tab | Navigate form fields |
| Enter | Submit transaction |
| Esc | Close modal |

---

## 🎨 UI Elements

### Transaction Form (Left)
- Input fields for transaction details
- Auto-validation
- Submit button with loading state

### Results Panel (Right)
- Risk score card (colored by level)
- Transaction ID
- Rules triggered list
- Risk analysis breakdown

### History Section (Bottom)
- Recent transactions list
- Expandable cards
- Clear history button

---

## 🔗 API Endpoints Used

```
POST /compliance-check
GET /health
GET /rules
```

---

## ⚡ Performance

- Transaction: **15-30ms**
- Page Load: **<1 second**
- History: **<100ms**

---

## 💾 Data Storage

- **Location**: Browser localStorage
- **Key**: `transactions`
- **Limit**: 50 transactions
- **Clear**: "Clear History" button

---

## 🔍 Troubleshooting

### "Connection Error"
→ Start API: `python api/main.py`

### "Model not loaded"
→ Run pipeline: `python run_pipeline.py`

### History not saving
→ Check browser localStorage permissions

---

## 📚 Documentation

- **This Card** - Quick reference
- **WEB_PORTAL_GUIDE.md** - Full guide
- **README.md** - Project overview
- **UIPATH_INTEGRATION.md** - RPA integration

---

## 🌐 Access URLs

| URL | Purpose |
|-----|---------|
| http://localhost:8000/portal | Web Portal |
| http://localhost:8000/docs | API Docs |
| http://localhost:8000/health | Health Check |

---

## 🎯 Quick Test Flow

```
1. Open portal
2. Select "Transfer"
3. Enter "$750,000"
4. USA → UAE
5. Enter beneficiary name
6. Click Submit
7. See MEDIUM risk (cross-border high value)
8. Check history below
```

---

**Version**: 2.0  
**Status**: Production Ready  
**Browser**: Chrome/Firefox/Safari/Edge

---

**Pro Tip**: Try entering >$1M to see HIGH risk (Large Transaction rule) 💡
