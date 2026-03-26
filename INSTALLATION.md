# Installation Guide

## Quick Setup

### Option 1: Using Virtual Environment (Recommended)

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the pipeline
python run_pipeline.py

# 5. Start API server
python api/main.py
```

### Option 2: Using System Python (if allowed)

```bash
# Install dependencies
pip install -r requirements.txt --user

# Run the pipeline
python3 run_pipeline.py

# Start API server
python3 api/main.py
```

### Option 3: Using Docker (Coming Soon)

## Verify Installation

Run the test script to verify everything is working:

```bash
python test_installation.py
```

You should see:
```
✓ All tests passed! System is ready to use.
```

## Manual Step-by-Step Execution

If you prefer to run each step manually:

### 1. Generate Dataset
```bash
python data/generate_dataset.py
```
Output: `data/transactions.csv`

### 2. Train ML Model
```bash
python models/train_model.py
```
Output: `models/model.pkl`

### 3. Generate Reports
```bash
python outputs/generate_reports.py
```
Outputs:
- `outputs/compliance_report.csv`
- `outputs/flagged_transactions.csv`

### 4. Start API Server
```bash
python api/main.py
```
Server: `http://localhost:8000`
Docs: `http://localhost:8000/docs`

## Testing the API

Once the server is running, test the endpoints:

### Health Check
```bash
curl http://localhost:8000/health
```

### Get Transactions
```bash
curl http://localhost:8000/transactions?limit=5
```

### Check Compliance
```bash
curl -X POST http://localhost:8000/compliance-check \
  -H "Content-Type: application/json" \
  -d @test_transaction.json
```

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Make sure you activated the virtual environment and installed dependencies

### Issue: Port 8000 already in use
**Solution**: Change port in `api/main.py` or kill the process using port 8000

### Issue: Model not found
**Solution**: Run `python models/train_model.py` first to train and save the model

### Issue: Dataset not found
**Solution**: Run `python data/generate_dataset.py` first to generate the dataset

## System Requirements

- Python 3.8+
- 500MB free disk space
- 2GB RAM minimum (4GB recommended)
- Internet connection (for initial package installation)

## Package Versions

The system has been tested with:
- FastAPI 0.109.0
- Uvicorn 0.27.0
- Pandas 2.1.4
- NumPy 1.26.3
- Scikit-learn 1.4.0
- Pydantic 2.5.3
