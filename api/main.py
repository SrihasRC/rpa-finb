"""
FastAPI Backend for Financial Compliance Monitoring System
Provides REST API endpoints for compliance checking and risk prediction
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rules.compliance_rules import RuleEngine
from models.train_model import RiskModel

# Initialize FastAPI app
app = FastAPI(
    title="Financial Compliance Monitoring API",
    description="REST API for transaction compliance checking and risk scoring",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
rule_engine = RuleEngine()
risk_model = RiskModel()
transactions_df = None


# Pydantic models for request/response
class Transaction(BaseModel):
    """Transaction model for API requests"""

    transaction_id: Optional[str] = None
    customer_id: str
    account_age_days: int = Field(ge=0)
    account_status: str
    transaction_amount: float = Field(gt=0)
    transaction_type: str
    transaction_time: str
    sender_country: str
    receiver_country: str
    beneficiary_id: str
    beneficiary_bank: str
    customer_avg_txn: float = Field(ge=0)
    txn_count_last_24h: int = Field(ge=0)
    txn_count_last_7d: int = Field(ge=0)
    kyc_status: str
    sanctions_flag: int = Field(ge=0, le=1)
    device_location: str
    channel: str
    is_international: int = Field(ge=0, le=1)


class RiskPredictionResponse(BaseModel):
    """Response model for risk prediction"""

    risk_score: float
    risk_label: str


class ComplianceCheckResponse(BaseModel):
    """Response model for compliance check"""

    transaction_id: str
    rules_triggered: List[str]
    num_rules_triggered: int
    risk_score: float
    risk_label: str
    final_risk: str


class TransactionSummary(BaseModel):
    """Summary statistics for transactions"""

    total_transactions: int
    avg_amount: float
    total_sanctions: int
    total_international: int
    pending_kyc: int
    dormant_accounts: int


# Mount static files
web_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web"
)
if os.path.exists(web_dir):
    app.mount(
        "/static", StaticFiles(directory=os.path.join(web_dir, "static")), name="static"
    )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Load model and data on startup"""
    global risk_model, transactions_df

    try:
        # Load trained model
        model_path = "models/model.pkl"
        if os.path.exists(model_path):
            risk_model.load(model_path)
            print("✓ Model loaded successfully")
        else:
            print("⚠ Warning: Model not found. Please train the model first.")

        # Load transactions dataset
        data_path = "data/transactions.csv"
        if os.path.exists(data_path):
            transactions_df = pd.read_csv(data_path)
            print(f"✓ Dataset loaded: {len(transactions_df)} transactions")
        else:
            print(
                "⚠ Warning: Dataset not found. /transactions endpoint will be unavailable."
            )

    except Exception as e:
        print(f"✗ Error during startup: {e}")


# API Endpoints


@app.get("/")
async def root():
    """Root endpoint - Redirect to web portal or show API info"""
    return {
        "name": "Financial Compliance Monitoring API",
        "version": "1.0.0",
        "status": "operational",
        "web_portal": "/portal",
        "api_docs": "/docs",
        "endpoints": {
            "GET /portal": "Open web transaction portal",
            "GET /transactions": "Retrieve all transactions",
            "GET /transactions/summary": "Get transaction summary statistics",
            "POST /predict": "Predict risk score for a transaction",
            "POST /compliance-check": "Full compliance check with rules and ML",
            "GET /rules": "List all compliance rules",
        },
    }


@app.get("/portal", response_class=HTMLResponse)
async def web_portal():
    """Serve the web transaction portal"""
    web_index = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web", "index.html"
    )

    if not os.path.exists(web_index):
        raise HTTPException(status_code=404, detail="Web portal not found")

    with open(web_index, "r") as f:
        return HTMLResponse(content=f.read())


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": risk_model.model is not None,
        "dataset_loaded": transactions_df is not None,
    }


@app.get("/transactions", response_model=List[Dict[str, Any]])
async def get_transactions(limit: Optional[int] = None):
    """
    Retrieve all transactions from dataset

    Args:
        limit: Optional limit on number of transactions to return
    """
    if transactions_df is None:
        raise HTTPException(status_code=503, detail="Dataset not loaded")

    df = transactions_df if limit is None else transactions_df.head(limit)
    return df.to_dict(orient="records")


@app.get("/transactions/summary", response_model=TransactionSummary)
async def get_transaction_summary():
    """Get summary statistics for all transactions"""
    if transactions_df is None:
        raise HTTPException(status_code=503, detail="Dataset not loaded")

    return TransactionSummary(
        total_transactions=len(transactions_df),
        avg_amount=float(transactions_df["transaction_amount"].mean()),
        total_sanctions=int(transactions_df["sanctions_flag"].sum()),
        total_international=int(transactions_df["is_international"].sum()),
        pending_kyc=int((transactions_df["kyc_status"] == "pending").sum()),
        dormant_accounts=int((transactions_df["account_status"] == "dormant").sum()),
    )


@app.get("/rules")
async def get_rules():
    """Get list of all compliance rules"""
    return {
        "total_rules": len(rule_engine.rules),
        "rules": rule_engine.get_rule_summary(),
    }


@app.post("/predict", response_model=RiskPredictionResponse)
async def predict_risk(transaction: Transaction):
    """
    Predict risk score for a transaction using ML model

    Args:
        transaction: Transaction data

    Returns:
        Risk score (0-1) and risk label (low/medium/high)
    """
    if risk_model.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Convert to dict
        txn_dict = transaction.dict()

        # Predict risk
        result = risk_model.predict_risk(txn_dict)

        return RiskPredictionResponse(
            risk_score=result["risk_score"], risk_label=result["risk_label"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/compliance-check", response_model=ComplianceCheckResponse)
async def compliance_check(transaction: Transaction):
    """
    Perform full compliance check on a transaction:
    1. Apply all regulatory rules
    2. Get ML risk prediction
    3. Determine final risk level

    Args:
        transaction: Transaction data

    Returns:
        Complete compliance analysis with rules triggered and risk assessment
    """
    if risk_model.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Convert to dict
        txn_dict = transaction.dict()

        # Generate transaction ID if not provided
        if not txn_dict.get("transaction_id"):
            import uuid

            txn_dict["transaction_id"] = f"TXN{str(uuid.uuid4())[:8].upper()}"

        # Apply compliance rules
        rules_triggered = rule_engine.check_transaction(txn_dict)

        # Get ML risk prediction
        ml_result = risk_model.predict_risk(txn_dict)
        risk_score = ml_result["risk_score"]
        ml_risk_label = ml_result["risk_label"]

        # Determine final risk level based on combined logic
        final_risk = determine_final_risk(txn_dict, rules_triggered, risk_score)

        return ComplianceCheckResponse(
            transaction_id=txn_dict["transaction_id"],
            rules_triggered=rules_triggered,
            num_rules_triggered=len(rules_triggered),
            risk_score=risk_score,
            risk_label=ml_risk_label,
            final_risk=final_risk,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compliance check error: {str(e)}")


def determine_final_risk(
    transaction: dict, rules_triggered: List[str], risk_score: float
) -> str:
    """
    Determine final risk level based on combined rules and ML prediction

    Logic:
    - If sanctions flag = 1 → HIGH
    - Else if risk_score > 0.8 → HIGH
    - Else if num_rules_triggered >= 2 → MEDIUM
    - Else → LOW

    Args:
        transaction: Transaction dictionary
        rules_triggered: List of triggered rule names
        risk_score: ML model risk score

    Returns:
        Final risk level: 'HIGH', 'MEDIUM', or 'LOW'
    """
    # Critical rule: Sanctions
    if transaction.get("sanctions_flag") == 1:
        return "HIGH"

    # High ML confidence
    if risk_score > 0.8:
        return "HIGH"

    # Multiple rules triggered
    if len(rules_triggered) >= 2:
        return "MEDIUM"

    # Single rule or low risk
    if len(rules_triggered) == 1 or risk_score > 0.5:
        return "MEDIUM"

    return "LOW"


# Development server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
