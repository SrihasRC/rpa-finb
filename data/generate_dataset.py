"""
Generate synthetic transaction dataset for compliance monitoring
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
NUM_TRANSACTIONS = 1000
START_DATE = datetime(2024, 1, 1)

# Reference data
HIGH_RISK_COUNTRIES = ["Iran", "North Korea", "Syria", "Venezuela", "Myanmar"]
COUNTRIES = [
    "USA",
    "UK",
    "Germany",
    "France",
    "Japan",
    "Singapore",
    "UAE",
    "Canada",
    "Australia",
] + HIGH_RISK_COUNTRIES
TRANSACTION_TYPES = ["transfer", "deposit", "withdrawal"]
ACCOUNT_STATUSES = ["active", "dormant"]
KYC_STATUSES = ["verified", "pending"]
CHANNELS = ["ATM", "online", "branch"]
BANKS = [
    "Bank_A",
    "Bank_B",
    "Bank_C",
    "Bank_D",
    "Bank_E",
    "International_Bank_X",
    "International_Bank_Y",
]


def generate_transactions(num_rows=NUM_TRANSACTIONS):
    """Generate synthetic transaction data"""

    transactions = []

    for i in range(num_rows):
        transaction_id = f"TXN{str(i + 1).zfill(6)}"
        customer_id = f"CUST{random.randint(1000, 9999)}"

        # Account details
        account_age_days = random.randint(1, 3650)  # 1 day to 10 years
        account_status = np.random.choice(ACCOUNT_STATUSES, p=[0.9, 0.1])

        # Transaction details
        # Create some patterns for suspicious transactions
        is_suspicious = random.random() < 0.15  # 15% suspicious

        if is_suspicious:
            # Make suspicious transactions more extreme
            transaction_amount = random.choice(
                [
                    random.uniform(500000, 2000000),  # Large amounts
                    random.uniform(9000, 10000) * random.randint(1, 5),  # Structuring
                ]
            )
            txn_count_last_24h = (
                random.randint(5, 15) if random.random() < 0.5 else random.randint(1, 4)
            )
            txn_count_last_7d = (
                random.randint(20, 50)
                if random.random() < 0.5
                else random.randint(5, 19)
            )
        else:
            transaction_amount = random.lognormvariate(10, 2)  # Normal distribution
            txn_count_last_24h = random.randint(0, 4)
            txn_count_last_7d = random.randint(1, 15)

        transaction_type = random.choice(TRANSACTION_TYPES)
        transaction_time = START_DATE + timedelta(
            days=random.randint(0, 365),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )

        # Geographic details
        sender_country = random.choice(COUNTRIES)
        receiver_country = random.choice(COUNTRIES)
        is_international = 1 if sender_country != receiver_country else 0

        # Make some international transactions to high-risk countries
        if is_suspicious and random.random() < 0.3:
            receiver_country = random.choice(HIGH_RISK_COUNTRIES)
            is_international = 1

        # Beneficiary details
        beneficiary_id = f"BEN{random.randint(1000, 5000)}"
        beneficiary_bank = random.choice(BANKS)

        # Customer patterns
        customer_avg_txn = transaction_amount * random.uniform(0.5, 1.5)

        # Compliance flags
        kyc_status = "verified" if random.random() < 0.85 else "pending"
        sanctions_flag = 1 if (is_suspicious and random.random() < 0.1) else 0

        # Device and channel
        device_location = random.choice(COUNTRIES)
        channel = random.choice(CHANNELS)

        # Create transaction record
        transaction = {
            "transaction_id": transaction_id,
            "customer_id": customer_id,
            "account_age_days": account_age_days,
            "account_status": account_status,
            "transaction_amount": round(transaction_amount, 2),
            "transaction_type": transaction_type,
            "transaction_time": transaction_time.strftime("%Y-%m-%d %H:%M:%S"),
            "sender_country": sender_country,
            "receiver_country": receiver_country,
            "beneficiary_id": beneficiary_id,
            "beneficiary_bank": beneficiary_bank,
            "customer_avg_txn": round(customer_avg_txn, 2),
            "txn_count_last_24h": txn_count_last_24h,
            "txn_count_last_7d": txn_count_last_7d,
            "kyc_status": kyc_status,
            "sanctions_flag": sanctions_flag,
            "device_location": device_location,
            "channel": channel,
            "is_international": is_international,
        }

        transactions.append(transaction)

    return pd.DataFrame(transactions)


def main():
    """Generate and save dataset"""
    print("Generating synthetic transaction dataset...")

    df = generate_transactions(NUM_TRANSACTIONS)

    # Save to CSV
    output_path = "data/transactions.csv"
    df.to_csv(output_path, index=False)

    print(f"Dataset generated successfully!")
    print(f"Total transactions: {len(df)}")
    print(f"Saved to: {output_path}")
    print(f"\nDataset summary:")
    print(f"- Average transaction amount: ${df['transaction_amount'].mean():.2f}")
    print(f"- Sanctions flags: {df['sanctions_flag'].sum()}")
    print(f"- International transactions: {df['is_international'].sum()}")
    print(f"- Pending KYC: {(df['kyc_status'] == 'pending').sum()}")
    print(f"- Dormant accounts: {(df['account_status'] == 'dormant').sum()}")

    return df


if __name__ == "__main__":
    main()
