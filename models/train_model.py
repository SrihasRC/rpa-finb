"""
Train ML model for risk scoring
Uses RandomForestClassifier to predict transaction risk
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
import os


class RiskModel:
    """ML model for transaction risk assessment"""

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100, max_depth=10, random_state=42, class_weight="balanced"
        )
        self.label_encoders = {}
        self.feature_columns = []

    def create_target_label(self, df: pd.DataFrame) -> pd.Series:
        """
        Create synthetic target label based on risk indicators
        Returns binary label: 1 (suspicious) or 0 (normal)
        """
        suspicious = (
            # Large transactions
            (df["transaction_amount"] > 500000)
            |
            # Sanctions flag
            (df["sanctions_flag"] == 1)
            |
            # High transaction frequency
            (df["txn_count_last_24h"] > 5)
            | (df["txn_count_last_7d"] > 20)
            |
            # New account with high transaction
            ((df["account_age_days"] < 30) & (df["transaction_amount"] > 300000))
            |
            # Dormant account activity
            ((df["account_status"] == "dormant") & (df["transaction_amount"] > 100000))
            |
            # International high value
            ((df["is_international"] == 1) & (df["transaction_amount"] > 200000))
            |
            # KYC incomplete
            (df["kyc_status"] != "verified")
        )

        return suspicious.astype(int)

    def prepare_features(self, df: pd.DataFrame, fit: bool = True) -> pd.DataFrame:
        """
        Prepare features for model training/prediction

        Args:
            df: Input dataframe
            fit: If True, fit label encoders (use for training only)

        Returns:
            DataFrame with prepared features
        """
        df_prep = df.copy()

        # Categorical columns to encode
        categorical_cols = [
            "account_status",
            "transaction_type",
            "kyc_status",
            "channel",
            "sender_country",
            "receiver_country",
        ]

        # Encode categorical variables
        for col in categorical_cols:
            if col in df_prep.columns:
                if fit:
                    self.label_encoders[col] = LabelEncoder()
                    df_prep[f"{col}_encoded"] = self.label_encoders[col].fit_transform(
                        df_prep[col].astype(str)
                    )
                else:
                    if col in self.label_encoders:
                        # Handle unseen categories
                        df_prep[f"{col}_encoded"] = df_prep[col].apply(
                            lambda x: (
                                self.label_encoders[col].transform([str(x)])[0]
                                if str(x) in self.label_encoders[col].classes_
                                else -1
                            )
                        )
                    else:
                        df_prep[f"{col}_encoded"] = -1

        # Select numerical features
        feature_cols = [
            "transaction_amount",
            "account_age_days",
            "txn_count_last_24h",
            "txn_count_last_7d",
            "customer_avg_txn",
            "is_international",
            "sanctions_flag",
            "account_status_encoded",
            "transaction_type_encoded",
            "kyc_status_encoded",
            "channel_encoded",
            "sender_country_encoded",
            "receiver_country_encoded",
        ]

        # Store feature columns for later use
        if fit:
            self.feature_columns = [
                col for col in feature_cols if col in df_prep.columns
            ]

        return df_prep[self.feature_columns]

    def train(self, df: pd.DataFrame):
        """
        Train the risk model

        Args:
            df: Training dataframe with transaction data

        Returns:
            Dictionary with training metrics
        """
        print("Preparing features...")

        # Create target label
        y = self.create_target_label(df)

        # Prepare features
        X = self.prepare_features(df, fit=True)

        print(f"Dataset: {len(X)} transactions")
        print(f"Features: {len(self.feature_columns)}")
        print(f"Suspicious transactions: {y.sum()} ({y.mean() * 100:.1f}%)")

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        print("\nTraining model...")
        self.model.fit(X_train, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]

        print("\n" + "=" * 60)
        print("MODEL EVALUATION")
        print("=" * 60)

        print("\nClassification Report:")
        print(
            classification_report(y_test, y_pred, target_names=["Normal", "Suspicious"])
        )

        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

        print(f"\nROC AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")

        # Feature importance
        feature_importance = pd.DataFrame(
            {
                "feature": self.feature_columns,
                "importance": self.model.feature_importances_,
            }
        ).sort_values("importance", ascending=False)

        print("\nTop 10 Important Features:")
        print(feature_importance.head(10).to_string(index=False))

        return {
            "accuracy": (y_pred == y_test).mean(),
            "roc_auc": roc_auc_score(y_test, y_pred_proba),
            "feature_importance": feature_importance,
        }

    def predict_risk(self, transaction: dict) -> dict:
        """
        Predict risk for a single transaction

        Args:
            transaction: Dictionary with transaction features

        Returns:
            Dictionary with risk_score and risk_label
        """
        # Convert to DataFrame
        df = pd.DataFrame([transaction])

        # Prepare features
        X = self.prepare_features(df, fit=False)

        # Predict
        risk_score = self.model.predict_proba(X)[0, 1]

        # Determine risk label
        if risk_score < 0.3:
            risk_label = "low"
        elif risk_score < 0.7:
            risk_label = "medium"
        else:
            risk_label = "high"

        return {"risk_score": float(risk_score), "risk_label": risk_label}

    def predict_batch(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Predict risk for multiple transactions

        Args:
            df: DataFrame with transaction data

        Returns:
            DataFrame with risk scores and labels
        """
        X = self.prepare_features(df, fit=False)
        risk_scores = self.model.predict_proba(X)[:, 1]

        risk_labels = pd.cut(
            risk_scores, bins=[0, 0.3, 0.7, 1.0], labels=["low", "medium", "high"]
        )

        return pd.DataFrame(
            {
                "transaction_id": df["transaction_id"],
                "risk_score": risk_scores,
                "risk_label": risk_labels,
            }
        )

    def save(self, filepath: str):
        """Save model to disk"""
        model_data = {
            "model": self.model,
            "label_encoders": self.label_encoders,
            "feature_columns": self.feature_columns,
        }
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")

    def load(self, filepath: str):
        """Load model from disk"""
        model_data = joblib.load(filepath)
        self.model = model_data["model"]
        self.label_encoders = model_data["label_encoders"]
        self.feature_columns = model_data["feature_columns"]
        print(f"Model loaded from {filepath}")


def main():
    """Train and save the risk model"""

    # Load dataset
    data_path = "data/transactions.csv"

    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}")
        print("Please run generate_dataset.py first")
        return

    print("Loading dataset...")
    df = pd.read_csv(data_path)

    print(f"Loaded {len(df)} transactions")

    # Create and train model
    model = RiskModel()
    metrics = model.train(df)

    # Save model
    os.makedirs("models", exist_ok=True)
    model.save("models/model.pkl")

    # Test prediction on sample transaction
    print("\n" + "=" * 60)
    print("TESTING PREDICTION")
    print("=" * 60)

    sample_txn = df.iloc[0].to_dict()
    result = model.predict_risk(sample_txn)

    print(f"\nSample transaction: {sample_txn['transaction_id']}")
    print(f"Amount: ${sample_txn['transaction_amount']:,.2f}")
    print(f"Risk Score: {result['risk_score']:.4f}")
    print(f"Risk Label: {result['risk_label']}")

    print("\n" + "=" * 60)
    print("Model training completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
