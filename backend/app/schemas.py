from pydantic import BaseModel, Field
from typing import List, Dict, Any
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
