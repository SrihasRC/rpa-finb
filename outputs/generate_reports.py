"""
Generate compliance reports and flagged transactions
"""

import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rules.compliance_rules import RuleEngine
from models.train_model import RiskModel


def generate_compliance_report():
    """Generate comprehensive compliance report for all transactions"""

    print("=" * 60)
    print("GENERATING COMPLIANCE REPORTS")
    print("=" * 60)

    # Load dataset
    data_path = "data/transactions.csv"
    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}")
        return

    print("\n1. Loading dataset...")
    df = pd.read_csv(data_path)
    print(f"   Loaded {len(df)} transactions")

    # Load model
    model_path = "models/model.pkl"
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        return

    print("\n2. Loading ML model...")
    risk_model = RiskModel()
    risk_model.load(model_path)

    # Initialize rule engine
    print("\n3. Initializing rule engine...")
    rule_engine = RuleEngine()

    # Process each transaction
    print("\n4. Processing transactions...")
    results = []

    for idx, row in df.iterrows():
        if idx % 100 == 0:
            print(f"   Processed {idx}/{len(df)} transactions...")

        txn_dict = row.to_dict()

        # Apply compliance rules
        rules_triggered = rule_engine.check_transaction(txn_dict)

        # Get ML prediction
        ml_result = risk_model.predict_risk(txn_dict)
        risk_score = ml_result["risk_score"]

        # Determine final risk
        final_risk = determine_final_risk(txn_dict, rules_triggered, risk_score)

        results.append(
            {
                "transaction_id": txn_dict["transaction_id"],
                "customer_id": txn_dict["customer_id"],
                "transaction_amount": txn_dict["transaction_amount"],
                "transaction_type": txn_dict["transaction_type"],
                "sender_country": txn_dict["sender_country"],
                "receiver_country": txn_dict["receiver_country"],
                "rules_triggered": "|".join(rules_triggered)
                if rules_triggered
                else "None",
                "num_rules_triggered": len(rules_triggered),
                "risk_score": round(risk_score, 4),
                "final_risk": final_risk,
            }
        )

    print(f"   Processed all {len(df)} transactions")

    # Create reports DataFrame
    report_df = pd.DataFrame(results)

    # Save full compliance report
    print("\n5. Saving reports...")
    os.makedirs("outputs", exist_ok=True)

    compliance_report_path = "outputs/compliance_report.csv"
    report_df.to_csv(compliance_report_path, index=False)
    print(f"   ✓ Compliance report: {compliance_report_path}")

    # Filter and save flagged transactions (MEDIUM or HIGH risk)
    flagged_df = report_df[report_df["final_risk"].isin(["MEDIUM", "HIGH"])].copy()
    flagged_df = flagged_df.sort_values("risk_score", ascending=False)

    flagged_report_path = "outputs/flagged_transactions.csv"
    flagged_df.to_csv(flagged_report_path, index=False)
    print(f"   ✓ Flagged transactions: {flagged_report_path}")

    # Generate summary statistics
    print("\n" + "=" * 60)
    print("COMPLIANCE REPORT SUMMARY")
    print("=" * 60)

    print(f"\nTotal Transactions: {len(report_df)}")
    print(f"\nRisk Distribution:")
    print(
        f"  HIGH:   {(report_df['final_risk'] == 'HIGH').sum():4d} ({(report_df['final_risk'] == 'HIGH').sum() / len(report_df) * 100:.1f}%)"
    )
    print(
        f"  MEDIUM: {(report_df['final_risk'] == 'MEDIUM').sum():4d} ({(report_df['final_risk'] == 'MEDIUM').sum() / len(report_df) * 100:.1f}%)"
    )
    print(
        f"  LOW:    {(report_df['final_risk'] == 'LOW').sum():4d} ({(report_df['final_risk'] == 'LOW').sum() / len(report_df) * 100:.1f}%)"
    )

    print(
        f"\nFlagged Transactions: {len(flagged_df)} ({len(flagged_df) / len(report_df) * 100:.1f}%)"
    )

    print(f"\nAverage Risk Score: {report_df['risk_score'].mean():.4f}")
    print(f"Max Risk Score: {report_df['risk_score'].max():.4f}")

    print(
        f"\nTransactions with Rules Triggered: {(report_df['num_rules_triggered'] > 0).sum()}"
    )
    print(
        f"Average Rules per Transaction: {report_df['num_rules_triggered'].mean():.2f}"
    )

    # Top triggered rules
    print("\nMost Frequently Triggered Rules:")
    all_rules = []
    for rules_str in report_df["rules_triggered"]:
        if rules_str != "None":
            all_rules.extend(rules_str.split("|"))

    if all_rules:
        rule_counts = pd.Series(all_rules).value_counts()
        for rule, count in rule_counts.head(5).items():
            print(f"  {rule}: {count} ({count / len(report_df) * 100:.1f}%)")

    # High-risk transactions details
    print("\n" + "=" * 60)
    print("HIGH RISK TRANSACTIONS (Top 10)")
    print("=" * 60)

    high_risk = (
        report_df[report_df["final_risk"] == "HIGH"]
        .sort_values("risk_score", ascending=False)
        .head(10)
    )

    for idx, row in high_risk.iterrows():
        print(f"\nTransaction: {row['transaction_id']}")
        print(f"  Amount: ${row['transaction_amount']:,.2f}")
        print(f"  Route: {row['sender_country']} → {row['receiver_country']}")
        print(f"  Risk Score: {row['risk_score']:.4f}")
        print(f"  Rules: {row['rules_triggered']}")

    print("\n" + "=" * 60)
    print("REPORT GENERATION COMPLETED")
    print("=" * 60)

    return report_df, flagged_df


def determine_final_risk(
    transaction: dict, rules_triggered: list, risk_score: float
) -> str:
    """
    Determine final risk level
    Same logic as in API
    """
    if transaction.get("sanctions_flag") == 1:
        return "HIGH"

    if risk_score > 0.8:
        return "HIGH"

    if len(rules_triggered) >= 2:
        return "MEDIUM"

    if len(rules_triggered) == 1 or risk_score > 0.5:
        return "MEDIUM"

    return "LOW"


if __name__ == "__main__":
    generate_compliance_report()
