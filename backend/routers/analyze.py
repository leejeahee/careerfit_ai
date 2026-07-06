# backend/routers/analyze.py (RAG 연결 최종 버전)

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services.rag_service import search_documents
from services.llm_service import get_llm_response

router = APIRouter()

class AnalyzeRequest(BaseModel):
    major: str
    skills: List[str]
    job_type: str
    experience_years: int = 0
    preferred_company_size: str = "무관"

class AnalyzeResponse(BaseModel):
    answer: str
    sources: List[dict]

@router.post("/analyze", response_model=AnalyzeResponse, tags=["Analyze"])
def analyze_career(request: AnalyzeRequest):
    """RAG 기반 역량 분석: ChromaDB 검색 → Gemini 답변 → sources 반환"""
    query = (
        f"전공: {request.major}, 보유 스킬: {', '.join(request.skills)}, "
        f"관심 직무: {request.job_type}, 경력: {request.experience_years}년, "
        f"선호 기업 형태: {request.preferred_company_size}"
    )

    try:
        context_docs = search_documents(query, n_results=3)
    except Exception as e:
        print(f"⚠️  RAG 검색 실패, 문서 없이 진행합니다: {e}")
        context_docs = []

    result = get_llm_response(query=query, context_docs=context_docs)
    return AnalyzeResponse(answer=result["answer"], sources=result["sources"])