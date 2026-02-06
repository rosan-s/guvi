"""
ML-based Financial Analytics Module
Includes: Forecasting, Anomaly Detection, Risk Prediction, Scenario Analysis
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from scipy import stats


class FinancialPredictor:
    """Predict revenue and expense trends using Linear Regression"""

    def __init__(self):
        self.revenue_model = LinearRegression()
        self.expense_model = LinearRegression()
        self.scaler = StandardScaler()

    def fit(self, df: pd.DataFrame) -> None:
        """Train forecasting models on historical data"""
        if len(df) < 2:
            return

        X = np.arange(len(df)).reshape(-1, 1)
        revenue = df.get("revenue", pd.Series([0])).values
        expenses = df.get("expenses", pd.Series([0])).values

        if len(X) > 1 and len(revenue) > 1:
            self.revenue_model.fit(X, revenue)
            self.expense_model.fit(X, expenses)

    def forecast(self, periods: int = 3) -> Dict[str, List[float]]:
        """Forecast next N periods"""
        if not hasattr(self, "revenue_model"):
            return {"revenue": [], "expenses": [], "net_margin": []}

        X_future = np.arange(periods).reshape(-1, 1)

        try:
            revenue_forecast = self.revenue_model.predict(X_future).tolist()
            expense_forecast = self.expense_model.predict(X_future).tolist()
            net_margin_forecast = [
                (r - e) / r if r > 0 else 0
                for r, e in zip(revenue_forecast, expense_forecast)
            ]

            return {
                "revenue": [max(0, v) for v in revenue_forecast],
                "expenses": [max(0, v) for v in expense_forecast],
                "net_margin": net_margin_forecast,
            }
        except Exception:
            return {"revenue": [], "expenses": [], "net_margin": []}


class AnomalyDetector:
    """Detect financial anomalies using Isolation Forest"""

    def __init__(self, contamination: float = 0.1):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.scaler = StandardScaler()
        self.is_fitted = False

    def fit(self, df: pd.DataFrame) -> None:
        """Train anomaly detection model"""
        features = self._extract_features(df)
        if len(features) < 2:
            return

        try:
            scaled = self.scaler.fit_transform(features)
            self.model.fit(scaled)
            self.is_fitted = True
        except Exception:
            pass

    def detect(self, df: pd.DataFrame) -> List[str]:
        """Detect anomalies in financial data"""
        if not self.is_fitted or len(df) < 1:
            return []

        features = self._extract_features(df)
        if len(features) < 1:
            return []

        try:
            scaled = self.scaler.transform(features)
            predictions = self.model.predict(scaled)
            anomalies = []

            for idx, pred in enumerate(predictions):
                if pred == -1:  # -1 indicates anomaly
                    anomalies.append(f"Unusual pattern detected in period {idx + 1}")

            return anomalies
        except Exception:
            return []

    def _extract_features(self, df: pd.DataFrame) -> np.ndarray:
        """Extract features for anomaly detection"""
        revenue = df.get("revenue", pd.Series([0])).values
        expenses = df.get("expenses", pd.Series([0])).values
        cash_in = df.get("cash_in", revenue).values
        cash_out = df.get("cash_out", expenses).values

        if len(revenue) == 0:
            return np.array([]).reshape(0, 4)

        features = np.column_stack([
            revenue,
            expenses,
            cash_in - cash_out,  # net cashflow
            (revenue - expenses) / (revenue + 1e-9),  # net margin
        ])

        return np.nan_to_num(features, 0)


class ScenarioAnalyzer:
    """Scenario analysis: Optimistic, Base, Pessimistic cases"""

    @staticmethod
    def analyze(analysis_result: Dict) -> Dict[str, Dict]:
        """Generate 3 scenarios based on current metrics"""
        revenue = analysis_result.get("revenue", 0)
        expenses = analysis_result.get("expenses", 0)
        net_margin = analysis_result.get("net_margin", 0.1)

        scenarios = {
            "pessimistic": ScenarioAnalyzer._calculate_scenario(
                revenue * 0.85,  # 15% revenue decline
                expenses * 1.1,  # 10% expense increase
            ),
            "base": {
                "revenue": revenue,
                "expenses": expenses,
                "net_margin": net_margin,
                "description": "Current trajectory based on historical data",
            },
            "optimistic": ScenarioAnalyzer._calculate_scenario(
                revenue * 1.2,  # 20% revenue growth
                expenses * 0.95,  # 5% expense reduction
            ),
        }

        return scenarios

    @staticmethod
    def _calculate_scenario(revenue: float, expenses: float) -> Dict:
        """Calculate metrics for a scenario"""
        net_income = revenue - expenses
        net_margin = net_income / revenue if revenue > 0 else 0

        return {
            "revenue": max(0, revenue),
            "expenses": max(0, expenses),
            "net_income": net_income,
            "net_margin": net_margin,
        }


class CreditRiskPredictor:
    """Predict probability of credit default using historical patterns"""

    @staticmethod
    def predict_default_probability(analysis_result: Dict) -> float:
        """
        Predict default probability (0-100%) based on financial metrics.
        Uses logistic regression logic.
        """
        risk_score = analysis_result.get("risk_score", 50)
        net_margin = analysis_result.get("net_margin", 0)
        current_ratio = analysis_result.get("current_ratio", 1)
        dscr = analysis_result.get("dscr", 1.5)

        # Normalize scores
        margin_score = max(0, min(1, (net_margin + 0.1) / 0.25))  # Scale: -0.1 to 0.15
        liquidity_score = max(0, min(1, current_ratio / 2.0))  # Scale: 0 to 2
        dscr_score = max(0, min(1, dscr / 2.5))  # Scale: 0 to 2.5

        # Calculate risk: high margin/liquidity/dscr = low default probability
        composite = 1 - (margin_score * 0.3 + liquidity_score * 0.4 + dscr_score * 0.3)
        default_probability = max(0, min(100, composite * 100))

        return round(default_probability, 2)

    @staticmethod
    def get_risk_factors(analysis_result: Dict) -> List[str]:
        """Identify key risk factors"""
        factors = []
        net_margin = analysis_result.get("net_margin", 0)
        current_ratio = analysis_result.get("current_ratio", 1)
        dso_days = analysis_result.get("dso_days", 0)
        dscr = analysis_result.get("dscr", 1.5)

        if net_margin < 0.05:
            factors.append("Low profitability margins (< 5%)")
        if current_ratio < 1.0:
            factors.append("Liquidity crisis risk (current ratio < 1.0)")
        if dso_days > 90:
            factors.append("Extended payment collection period (>90 days)")
        if dscr < 1.0:
            factors.append("Cannot cover debt service from operating cash flow")
        if len(factors) == 0:
            factors.append("No major credit risk factors identified")

        return factors
