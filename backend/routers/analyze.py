# backend/routers/analyze.py

from fastapi import APIRouter

from pydantic import BaseModel

from typing import List

from services.llm_service import get_llm_response

router = APIRouter()

# 요청 본문(Request Body) 모델

# 손님이 제출하는 주문서 양식

class AnalyzeRequest(BaseModel):

    major: str          # 전공 (예: "통계학과")

    skills: List[str]      # 보유 스킬 목록 (예: ["Python", "SQL"])

    job_type: str        # 관심 직무 (예: "데이터 분석")

    experience_years: int = 0           # 경력 연수 (0이면 신입)

    preferred_company_size: str = "무관"  # 무관 / 대기업 / 중견기업 / 스타트업

# 응답 본문(Response Body) 모델

# 주방에서 손님에게 돌려주는 영수증 양식

class AnalyzeResponse(BaseModel):

    answer: str         # AI 분석 결과 텍스트

    sources: List[dict]     # 답변 근거 데이터 목록



@router.post("/analyze", response_model=AnalyzeResponse, tags=["Analyze"])

def analyze_career(request: AnalyzeRequest):

    """

    사용자의 전공·스킬·관심 직무를 기반으로 취업·공모전 맞춤 분석을 제공한다.

    현재는 목업 응답을 반환하며, 실습 8에서 Gemini API와 연결한다.

    """

    # 사용자가 입력한 데이터를 바탕으로 LLM에 전달할 질문(query)을 생성합니다.
    query = (
        f"전공: {request.major}\n"
        f"보유 스킬: {', '.join(request.skills)}\n"
        f"관심 직무: {request.job_type}\n"
        f"경력: {request.experience_years}년\n"
        f"선호 기업 형태: {request.preferred_company_size}"
    )

    # 생성된 질문과 빈 문서 목록을 LLM 서비스에 전달하여 응답을 받습니다.
    llm_result = get_llm_response(query=query, context_docs=[])

    return AnalyzeResponse(
        answer=llm_result["answer"], 
        sources=llm_result["sources"]
    )


