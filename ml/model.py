import numpy as np
import xgboost as xgb
import shap
from dataclasses import dataclass


@dataclass
class FraudPrediction:
    risk_score: float
    is_fraud: bool
    explanation: dict


class FraudDetectionModel:
    def __init__(self):
        self.model = self._build_model()
        self.explainer = shap.TreeExplainer(self.model)
        self.feature_names = [
            "amount",
            "hour_of_day",
            "is_international",
            "transaction_count_24h",
            "avg_transaction_amount",
        ]

    def _build_model(self) -> xgb.XGBClassifier:
        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            random_state=42,
            eval_metric="logloss",
        )
        X_train, y_train = self._generate_training_data()
        model.fit(X_train, y_train)
        return model

    def _generate_training_data(self):
        np.random.seed(42)
        n_samples = 1000

        legitimate = np.column_stack([
            np.random.uniform(1, 500, int(n_samples * 0.85)),
            np.random.randint(8, 22, int(n_samples * 0.85)),
            np.random.randint(0, 2, int(n_samples * 0.85)),
            np.random.randint(1, 10, int(n_samples * 0.85)),
            np.random.uniform(50, 300, int(n_samples * 0.85)),
        ])

        fraudulent = np.column_stack([
            np.random.uniform(500, 10000, int(n_samples * 0.15)),
            np.random.randint(0, 6, int(n_samples * 0.15)),
            np.ones(int(n_samples * 0.15)),
            np.random.randint(10, 50, int(n_samples * 0.15)),
            np.random.uniform(10, 100, int(n_samples * 0.15)),
        ])

        X = np.vstack([legitimate, fraudulent])
        y = np.array(
            [0] * int(n_samples * 0.85) + [1] * int(n_samples * 0.15)
        )
        return X, y

    def predict(self, features: dict) -> FraudPrediction:
        X = np.array([[
            features["amount"],
            features["hour_of_day"],
            features["is_international"],
            features["transaction_count_24h"],
            features["avg_transaction_amount"],
        ]])

        risk_score = float(self.model.predict_proba(X)[0][1])
        is_fraud = risk_score > 0.5

        shap_values = self.explainer.shap_values(X)
        explanation = {
            name: round(float(value), 4)
            for name, value in zip(self.feature_names, shap_values[0])
        }

        return FraudPrediction(
            risk_score=round(risk_score, 4),
            is_fraud=is_fraud,
            explanation=explanation,
        )


fraud_model = FraudDetectionModel()