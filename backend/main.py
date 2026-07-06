from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import health
from routers import analyze
from services import rag_service
# FastAPI 앱 객체 생성
# title과 version은 /docs 페이지에 표시된다
app = FastAPI(
    title="CareerFit AI",
    description="취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치",
    version="0.1.0"
)
# CORS 설정: React 프론트엔드(localhost:5173)의 요청을 허용한다
# 요리 비유: 다른 건물(프론트엔드)에서 오는 배달 요청을 허용하는 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(analyze.router)
# 라우터 등록은 실습 4·5·6에서 추가한다

@app.on_event("startup")
def load_rag_collection():
    """서버 시작 시 ChromaDB 컬렉션을 1회 초기화합니다 (요청마다 재계산하지 않도록)."""
    rag_service.initialize_collection()
@app.get("/")
def root():
    return {"message": "CareerFit AI 서버가 실행 중입니다."}


