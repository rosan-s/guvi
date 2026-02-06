from pydantic import BaseModel, Field
from typing import List, Dict, Any, Union
import pandas as pd


class AnalysisRequest(BaseModel):
    industry: str = "Services"
    records: List[Dict[str, Any]] = Field(default_factory=list)

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.records)


class AnalysisResponse(BaseModel):
    industry: str
    revenue: float
    expenses: float
    net_income: float
    net_margin: float
    net_cashflow: float
    current_ratio: float
    dso_days: float
    dscr: float
    risk_score: float
    creditworthiness: str
    benchmarks: Dict[str, float]
    flags: List[str]
    recommendations: List[str]
    # Advanced AI features
    forecast: Dict[str, List[float]] = Field(default_factory=dict)
    anomalies: List[str] = Field(default_factory=list)
    scenarios: Dict[str, Dict[str, Union[float, str]]] = Field(default_factory=dict)
    default_probability: float = 0.0
    credit_risk_factors: List[str] = Field(default_factory=list)

