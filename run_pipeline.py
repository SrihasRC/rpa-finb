"""
Main pipeline script to run the entire compliance monitoring system
Executes all steps in sequence:
1. Generate dataset
2. Train ML model
3. Generate compliance reports
"""

import sys
import os

# Add paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    """Run the complete pipeline"""

    print("=" * 70)
    print("RPA-BASED FINANCIAL COMPLIANCE MONITORING SYSTEM")
    print("=" * 70)

    # Step 1: Generate dataset
    print("\n" + "=" * 70)
    print("STEP 1: GENERATING SYNTHETIC DATASET")
    print("=" * 70)

    from data.generate_dataset import main as generate_dataset

    df = generate_dataset()

    # Step 2: Train model
    print("\n" + "=" * 70)
    print("STEP 2: TRAINING ML MODEL")
    print("=" * 70)

    from models.train_model import main as train_model

    train_model()

    # Step 3: Generate reports
    print("\n" + "=" * 70)
    print("STEP 3: GENERATING COMPLIANCE REPORTS")
    print("=" * 70)

    from outputs.generate_reports import generate_compliance_report

    report_df, flagged_df = generate_compliance_report()

    # Final summary
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print("\nGenerated Files:")
    print("  ✓ data/transactions.csv - Synthetic transaction dataset")
    print("  ✓ models/model.pkl - Trained ML model")
    print("  ✓ outputs/compliance_report.csv - Full compliance report")
    print("  ✓ outputs/flagged_transactions.csv - High/medium risk transactions")

    print("\nNext Steps:")
    print("  1. Start the API server: python api/main.py")
    print("  2. Test endpoints at: http://localhost:8000/docs")
    print("  3. Integrate with UiPath using the API endpoints")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
