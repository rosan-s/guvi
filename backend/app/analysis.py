from __future__ import annotations
import io
import pandas as pd
import numpy as np
import pdfplumber
from fastapi import UploadFile, HTTPException
from .ml_analytics import FinancialPredictor, AnomalyDetector, ScenarioAnalyzer, CreditRiskPredictor

REQUIRED_FIELDS = ["revenue", "expenses"]

INDUSTRY_BENCHMARKS = {
    "Manufacturing": {"net_margin": 0.08, "current_ratio": 1.5, "dso_days": 45},
    "Retail": {"net_margin": 0.05, "current_ratio": 1.3, "dso_days": 25},
    "Agriculture": {"net_margin": 0.06, "current_ratio": 1.2, "dso_days": 60},
    "Services": {"net_margin": 0.12, "current_ratio": 1.6, "dso_days": 35},
    "Logistics": {"net_margin": 0.04, "current_ratio": 1.4, "dso_days": 40},
    "E-commerce": {"net_margin": 0.03, "current_ratio": 1.2, "dso_days": 30},
}


async def parse_upload_to_df(file: UploadFile) -> pd.DataFrame:
    name = (file.filename or "").lower()
    content = await file.read()

    if name.endswith(".csv"):
        return pd.read_csv(io.BytesIO(content), on_bad_lines="skip", engine="python")
    if name.endswith(".xlsx") or name.endswith(".xls"):
        return pd.read_excel(io.BytesIO(content))
    if name.endswith(".pdf"):
        text = ""
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"
        lines = [ln for ln in text.splitlines() if "," in ln]
        if not lines:
            raise HTTPException(status_code=400, detail="PDF does not contain CSV-like data")
        return pd.read_csv(io.StringIO("\n".join(lines)), on_bad_lines="skip", engine="python")

    raise HTTPException(status_code=400, detail="Unsupported file type")


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    aliases = {
        "sales": "revenue",
        "income": "revenue",
        "turnover": "revenue",
        "cost": "expenses",
        "expense": "expenses",
        "operating_expenses": "expenses",
        "cash_in": "cash_in",
        "cash_out": "cash_out",
        "accounts_receivable": "ar",
        "receivables": "ar",
        "accounts_payable": "ap",
        "payables": "ap",
        "inventory_level": "inventory",
        "loan_obligations": "debt",
        "tax_deductions": "tax",
    }

    for src, target in aliases.items():
        if src in df.columns and target not in df.columns:
            df[target] = df[src]

    return df


def analyze_dataframe(df: pd.DataFrame, industry: str) -> dict:
    df = _normalize_columns(df)

    missing = [f for f in REQUIRED_FIELDS if f not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing)}")

    revenue = float(df["revenue"].sum())
    expenses = float(df["expenses"].sum())
    net_income = revenue - expenses
    net_margin = net_income / revenue if revenue else 0.0

    cash_in = float(df.get("cash_in", df["revenue"]).sum())
    cash_out = float(df.get("cash_out", df["expenses"]).sum())
    net_cashflow = cash_in - cash_out

    ar = float(df.get("ar", pd.Series([0])).mean())
    ap = float(df.get("ap", pd.Series([0])).mean())
    inventory = float(df.get("inventory", pd.Series([0])).mean())
    current_assets = ar + inventory + max(cash_in - cash_out, 0)
    current_liabilities = ap + float(df.get("debt", pd.Series([0])).mean())
    current_ratio = current_assets / current_liabilities if current_liabilities else 2.0

    dso_days = (ar / revenue) * 365 if revenue else 0.0

    debt = float(df.get("debt", pd.Series([0])).sum())
    dscr = net_cashflow / debt if debt else 2.0

    risk_score = _risk_score(net_margin, current_ratio, dso_days, dscr)
    creditworthiness = _credit_tier(risk_score)

    benchmarks = INDUSTRY_BENCHMARKS.get(industry, INDUSTRY_BENCHMARKS["Services"])

    # ML-based analytics
    predictor = FinancialPredictor()
    predictor.fit(df)
    forecast = predictor.forecast(periods=3)

    detector = AnomalyDetector()
    detector.fit(df)
    anomalies = detector.detect(df)

    base_analysis = {
        "industry": industry,
        "revenue": revenue,
        "expenses": expenses,
        "net_income": net_income,
        "net_margin": net_margin,
        "net_cashflow": net_cashflow,
        "current_ratio": current_ratio,
        "dso_days": dso_days,
        "dscr": dscr,
        "risk_score": risk_score,
        "creditworthiness": creditworthiness,
        "benchmarks": benchmarks,
        "flags": _risk_flags(net_margin, current_ratio, dso_days, dscr, benchmarks),
    }

    scenarios = ScenarioAnalyzer.analyze(base_analysis)
    default_probability = CreditRiskPredictor.predict_default_probability(base_analysis)
    credit_risk_factors = CreditRiskPredictor.get_risk_factors(base_analysis)

    return {
        **base_analysis,
        "forecast": forecast,
        "anomalies": anomalies,
        "scenarios": scenarios,
        "default_probability": default_probability,
        "credit_risk_factors": credit_risk_factors,
    }


def _risk_score(net_margin: float, current_ratio: float, dso_days: float, dscr: float) -> float:
    margin_score = np.clip(net_margin / 0.15, 0, 1)
    liquidity_score = np.clip((current_ratio - 1) / 1.5, 0, 1)
    dso_score = np.clip(1 - dso_days / 120, 0, 1)
    dscr_score = np.clip(dscr / 2.0, 0, 1)
    return float(round((margin_score + liquidity_score + dso_score + dscr_score) * 25, 2))


def _credit_tier(score: float) -> str:
    if score >= 80:
        return "Excellent"
    if score >= 65:
        return "Good"
    if score >= 50:
        return "Fair"
    return "High Risk"


def _risk_flags(net_margin: float, current_ratio: float, dso_days: float, dscr: float, benchmarks: dict) -> list[str]:
    flags = []
    if net_margin < benchmarks.get("net_margin", 0.08):
        flags.append("Net margin below industry benchmark")
    if current_ratio < benchmarks.get("current_ratio", 1.5):
        flags.append("Liquidity below benchmark")
    if dso_days > benchmarks.get("dso_days", 45):
        flags.append("Receivables days higher than benchmark")
    if dscr < 1.2:
        flags.append("Debt service coverage weak")
    return flags


def build_recommendations(analysis: dict) -> list[str]:
    recs = []
    
    # Profitability recommendations
    if analysis["net_margin"] < analysis["benchmarks"]["net_margin"]:
        recs.append("Review COGS and vendor contracts; negotiate bulk discounts.")
    
    # Liquidity recommendations
    if analysis["current_ratio"] < analysis["benchmarks"]["current_ratio"]:
        recs.append("Improve liquidity by tightening credit terms and accelerating collections.")
    
    # Receivables recommendations
    if analysis["dso_days"] > analysis["benchmarks"]["dso_days"]:
        recs.append("Introduce early payment incentives and automate invoice reminders.")
    
    # Debt service recommendations
    if analysis["dscr"] < 1.2:
        recs.append("Consider restructuring high-interest debt to improve cash flow.")
    
    # Credit & Risk recommendations
    if analysis.get("default_probability", 0) > 30:
        recs.append("High credit risk detected - focus on debt reduction and cash reserve building.")
    
    # Anomaly-based recommendations
    if analysis.get("anomalies"):
        recs.append("Unusual patterns detected in financial data - conduct detailed audit.")
    
    # Scenario recommendations
    scenarios = analysis.get("scenarios", {})
    if scenarios.get("pessimistic", {}).get("net_margin", 0) < 0:
        recs.append("Prepare contingency plans; pessimistic scenario shows negative margins.")
    
    # General credit recommendations
    if analysis["risk_score"] >= 65:
        recs.append("Eligible for working capital lines or invoice discounting products.")
    else:
        recs.append("Focus on profitability and cashflow stabilization before new credit.")
    
    # Forecast-based recommendations
    forecast = analysis.get("forecast", {})
    if forecast.get("revenue") and len(forecast["revenue"]) > 0:
        projected_growth = (forecast["revenue"][-1] - analysis["revenue"]) / max(analysis["revenue"], 1) * 100
        if projected_growth > 10:
            recs.append(f"Revenue growth trend detected (~{projected_growth:.1f}% over forecast period).")
        elif projected_growth < -10:
            recs.append(f"Revenue decline trend detected (~{projected_growth:.1f}%) - cost optimization urgent.")
    
    return recs[:8]  # Limit to top 8 recommendations
