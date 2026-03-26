"""
Regulatory Rule Engine for Financial Compliance
Implements 10 compliance rules based on BSA, FATF, OFAC, etc.
"""

from typing import Dict, List, Any
import pandas as pd


class ComplianceRule:
    """Base class for compliance rules"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def check(self, transaction: Dict[str, Any]) -> bool:
        """Check if rule is triggered. Override in subclass."""
        raise NotImplementedError


class LargeTransactionRule(ComplianceRule):
    """BSA: Large transaction threshold"""

    def __init__(self, threshold: float = 1000000):
        super().__init__(
            name="Large Transaction (BSA)",
            description=f"Transaction amount exceeds ${threshold:,.0f}",
        )
        self.threshold = threshold

    def check(self, transaction: Dict[str, Any]) -> bool:
        return transaction.get("transaction_amount", 0) > self.threshold


class HighRiskCountryRule(ComplianceRule):
    """FATF: High-risk country check"""

    def __init__(self):
        super().__init__(
            name="High-Risk Country (FATF)",
            description="Transaction to/from high-risk jurisdiction",
        )
        self.high_risk_countries = [
            "Iran",
            "North Korea",
            "Syria",
            "Venezuela",
            "Myanmar",
        ]

    def check(self, transaction: Dict[str, Any]) -> bool:
        receiver = transaction.get("receiver_country", "")
        sender = transaction.get("sender_country", "")
        return (
            receiver in self.high_risk_countries or sender in self.high_risk_countries
        )


class SanctionsMatchRule(ComplianceRule):
    """OFAC: Sanctions list match"""

    def __init__(self):
        super().__init__(
            name="Sanctions Match (OFAC)",
            description="Customer or beneficiary on sanctions list",
        )

    def check(self, transaction: Dict[str, Any]) -> bool:
        return transaction.get("sanctions_flag", 0) == 1


class StructuringDetectionRule(ComplianceRule):
    """Detect potential structuring (smurfing)"""

    def __init__(self, threshold: int = 5):
        super().__init__(
            name="Structuring Detection",
            description=f"More than {threshold} transactions in 24 hours",
        )
        self.threshold = threshold

    def check(self, transaction: Dict[str, Any]) -> bool:
        return transaction.get("txn_count_last_24h", 0) > self.threshold


class RapidTransactionsRule(ComplianceRule):
    """Detect rapid transaction pattern"""

    def __init__(self, threshold: int = 20):
        super().__init__(
            name="Rapid Transactions",
            description=f"More than {threshold} transactions in 7 days",
        )
        self.threshold = threshold

    def check(self, transaction: Dict[str, Any]) -> bool:
        return transaction.get("txn_count_last_7d", 0) > self.threshold


class NewAccountHighTransactionRule(ComplianceRule):
    """New account with high transaction"""

    def __init__(self, age_threshold: int = 30, amount_threshold: float = 500000):
        super().__init__(
            name="New Account High Transaction",
            description=f"Account < {age_threshold} days with transaction > ${amount_threshold:,.0f}",
        )
        self.age_threshold = age_threshold
        self.amount_threshold = amount_threshold

    def check(self, transaction: Dict[str, Any]) -> bool:
        account_age = transaction.get("account_age_days", 999)
        amount = transaction.get("transaction_amount", 0)
        return account_age < self.age_threshold and amount > self.amount_threshold


class DormantAccountActivityRule(ComplianceRule):
    """Dormant account suddenly active with high transaction"""

    def __init__(self, amount_threshold: float = 200000):
        super().__init__(
            name="Dormant Account Activity",
            description=f"Dormant account with transaction > ${amount_threshold:,.0f}",
        )
        self.amount_threshold = amount_threshold

    def check(self, transaction: Dict[str, Any]) -> bool:
        is_dormant = transaction.get("account_status", "") == "dormant"
        amount = transaction.get("transaction_amount", 0)
        return is_dormant and amount > self.amount_threshold


class RepeatedBeneficiaryRule(ComplianceRule):
    """Detect repeated transfers to same beneficiary (requires dataset context)"""

    def __init__(self, threshold: int = 3):
        super().__init__(
            name="Repeated Beneficiary Transfers",
            description=f"Same beneficiary appears > {threshold} times",
        )
        self.threshold = threshold
        self.beneficiary_counts = {}

    def check(self, transaction: Dict[str, Any]) -> bool:
        beneficiary_id = transaction.get("beneficiary_id", "")
        customer_id = transaction.get("customer_id", "")
        key = f"{customer_id}_{beneficiary_id}"

        # Count occurrences
        self.beneficiary_counts[key] = self.beneficiary_counts.get(key, 0) + 1
        return self.beneficiary_counts[key] > self.threshold


class CrossBorderHighValueRule(ComplianceRule):
    """Cross-border high value transaction"""

    def __init__(self, threshold: float = 300000):
        super().__init__(
            name="Cross-Border High Value",
            description=f"International transaction > ${threshold:,.0f}",
        )
        self.threshold = threshold

    def check(self, transaction: Dict[str, Any]) -> bool:
        is_international = transaction.get("is_international", 0) == 1
        amount = transaction.get("transaction_amount", 0)
        return is_international and amount > self.threshold


class KYCIncompleteRule(ComplianceRule):
    """KYC not completed"""

    def __init__(self):
        super().__init__(name="KYC Incomplete", description="Customer KYC not verified")

    def check(self, transaction: Dict[str, Any]) -> bool:
        return transaction.get("kyc_status", "") != "verified"


class RuleEngine:
    """Main rule engine that applies all compliance rules"""

    def __init__(self):
        self.rules = [
            LargeTransactionRule(),
            HighRiskCountryRule(),
            SanctionsMatchRule(),
            StructuringDetectionRule(),
            RapidTransactionsRule(),
            NewAccountHighTransactionRule(),
            DormantAccountActivityRule(),
            RepeatedBeneficiaryRule(),
            CrossBorderHighValueRule(),
            KYCIncompleteRule(),
        ]

    def check_transaction(self, transaction: Dict[str, Any]) -> List[str]:
        """
        Apply all rules to a transaction
        Returns list of triggered rule names
        """
        triggered_rules = []

        for rule in self.rules:
            try:
                if rule.check(transaction):
                    triggered_rules.append(rule.name)
            except Exception as e:
                print(f"Error checking rule {rule.name}: {e}")

        return triggered_rules

    def check_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply rules to entire dataset
        Returns DataFrame with triggered rules column
        """
        results = []

        for _, row in df.iterrows():
            transaction = row.to_dict()
            triggered = self.check_transaction(transaction)
            results.append(
                {
                    "transaction_id": transaction["transaction_id"],
                    "rules_triggered": triggered,
                    "num_rules_triggered": len(triggered),
                }
            )

        return pd.DataFrame(results)

    def get_rule_summary(self) -> List[Dict[str, str]]:
        """Get summary of all rules"""
        return [
            {"name": rule.name, "description": rule.description} for rule in self.rules
        ]


def test_rules():
    """Test the rule engine with sample transactions"""

    # Test transaction 1: Large transaction
    test_txn_1 = {
        "transaction_id": "TEST001",
        "transaction_amount": 1500000,
        "account_age_days": 100,
        "sanctions_flag": 0,
        "receiver_country": "USA",
        "sender_country": "USA",
        "is_international": 0,
        "kyc_status": "verified",
        "account_status": "active",
        "txn_count_last_24h": 2,
        "txn_count_last_7d": 5,
    }

    # Test transaction 2: Multiple violations
    test_txn_2 = {
        "transaction_id": "TEST002",
        "transaction_amount": 600000,
        "account_age_days": 15,
        "sanctions_flag": 1,
        "receiver_country": "Iran",
        "sender_country": "USA",
        "is_international": 1,
        "kyc_status": "pending",
        "account_status": "active",
        "txn_count_last_24h": 8,
        "txn_count_last_7d": 25,
    }

    engine = RuleEngine()

    print("Testing Rule Engine")
    print("=" * 50)

    print("\nTest Transaction 1:")
    triggered_1 = engine.check_transaction(test_txn_1)
    print(f"Triggered rules: {triggered_1}")

    print("\nTest Transaction 2:")
    triggered_2 = engine.check_transaction(test_txn_2)
    print(f"Triggered rules: {triggered_2}")

    print("\n" + "=" * 50)
    print("All Rules:")
    for rule_info in engine.get_rule_summary():
        print(f"- {rule_info['name']}: {rule_info['description']}")


if __name__ == "__main__":
    test_rules()
