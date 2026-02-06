from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .config import settings
from .db import get_db, init_db
from .analysis import analyze_dataframe, parse_upload_to_df, build_recommendations
from .schemas import AnalysisResponse, AnalysisRequest
from .integrations import bank_a_summary, bank_b_summary

app = FastAPI(title="Financial Health Assessment Tool", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"] ,
)


def verify_api_key(x_api_key: str = Header(default="")):
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResponse, dependencies=[Depends(verify_api_key)])
async def analyze_file(file: UploadFile = File(...), industry: str = "Services", db: Session = Depends(get_db)):
    df = await parse_upload_to_df(file)
    analysis = analyze_dataframe(df, industry=industry)
    recommendations = build_recommendations(analysis)
    return AnalysisResponse(**analysis, recommendations=recommendations)


@app.post("/analyze-json", response_model=AnalysisResponse, dependencies=[Depends(verify_api_key)])
def analyze_json(payload: AnalysisRequest, db: Session = Depends(get_db)):
    analysis = analyze_dataframe(payload.to_dataframe(), industry=payload.industry)
    recommendations = build_recommendations(analysis)
    return AnalysisResponse(**analysis, recommendations=recommendations)


@app.get("/integrations/bank-a", dependencies=[Depends(verify_api_key)])
def get_bank_a_summary():
    return bank_a_summary()


@app.get("/integrations/bank-b", dependencies=[Depends(verify_api_key)])
def get_bank_b_summary():
    return bank_b_summary()
