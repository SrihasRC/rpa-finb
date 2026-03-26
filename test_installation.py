"""
Quick test script to verify installation and basic functionality
"""

import sys


def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")

    required_packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("sklearn", "Scikit-learn"),
        ("pydantic", "Pydantic"),
        ("joblib", "Joblib"),
    ]

    failed = []

    for module, name in required_packages:
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT FOUND")
            failed.append(name)

    if failed:
        print(f"\nFailed to import: {', '.join(failed)}")
        print("Please install missing packages: pip install -r requirements.txt")
        return False

    print("✓ All packages imported successfully\n")
    return True


def test_project_structure():
    """Test that all required files and directories exist"""
    import os

    print("Testing project structure...")

    required_items = [
        ("data", "dir"),
        ("models", "dir"),
        ("rules", "dir"),
        ("api", "dir"),
        ("outputs", "dir"),
        ("requirements.txt", "file"),
        ("run_pipeline.py", "file"),
        ("README.md", "file"),
        ("data/generate_dataset.py", "file"),
        ("models/train_model.py", "file"),
        ("rules/compliance_rules.py", "file"),
        ("api/main.py", "file"),
        ("outputs/generate_reports.py", "file"),
    ]

    failed = []

    for item, item_type in required_items:
        if item_type == "dir":
            exists = os.path.isdir(item)
        else:
            exists = os.path.isfile(item)

        if exists:
            print(f"  ✓ {item}")
        else:
            print(f"  ✗ {item} - NOT FOUND")
            failed.append(item)

    if failed:
        print(f"\nMissing items: {', '.join(failed)}")
        return False

    print("✓ All required files and directories exist\n")
    return True


def test_rule_engine():
    """Test the compliance rule engine"""
    print("Testing rule engine...")

    try:
        from rules.compliance_rules import RuleEngine

        engine = RuleEngine()

        # Test transaction with multiple violations
        test_txn = {
            "transaction_id": "TEST001",
            "transaction_amount": 1500000,
            "account_age_days": 15,
            "sanctions_flag": 1,
            "receiver_country": "Iran",
            "sender_country": "USA",
            "is_international": 1,
            "kyc_status": "pending",
            "account_status": "active",
            "txn_count_last_24h": 8,
            "txn_count_last_7d": 25,
            "beneficiary_id": "BEN001",
            "customer_id": "CUST001",
        }

        triggered = engine.check_transaction(test_txn)

        print(f"  ✓ Rule engine initialized")
        print(f"  ✓ Test transaction checked")
        print(f"  ✓ Rules triggered: {len(triggered)}")
        print(f"    {', '.join(triggered[:3])}...")

        return True

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 70)
    print("FINANCIAL COMPLIANCE MONITORING SYSTEM - INSTALLATION TEST")
    print("=" * 70)
    print()

    tests = [
        ("Package Imports", test_imports),
        ("Project Structure", test_project_structure),
        ("Rule Engine", test_rule_engine),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ✗ Test failed with error: {e}\n")
            results.append((test_name, False))

    print("=" * 70)
    print("TEST RESULTS")
    print("=" * 70)

    all_passed = True
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False

    print("=" * 70)

    if all_passed:
        print("\n✓ All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("  1. Run the pipeline: python run_pipeline.py")
        print("  2. Start the API: python api/main.py")
        print("  3. Check the docs: http://localhost:8000/docs")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
