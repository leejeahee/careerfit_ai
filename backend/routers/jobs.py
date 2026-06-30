# backend/routers/jobs.py

from fastapi import APIRouter

from typing import List

router = APIRouter()



# 목업 데이터: 3일차에 실제 CSV 데이터로 교체한다

MOCK_JOBS = [
    {
        "id": 1,
        "company": "카카오",
        "title": "백엔드 개발자",
        "required_skills": ["Python", "FastAPI", "MySQL", "Git"],
        "preferred_skills": ["Docker", "Redis", "AWS", "Kafka"],
        "description": "카카오 서비스의 백엔드 API를 개발하고 운영합니다.",
        "deadline": "2026-08-31"
    },
    {
        "id": 2,
        "company": "네이버",
        "title": "서버 개발자",
        "required_skills": ["Java", "Spring Boot", "MySQL", "REST API"],
        "preferred_skills": ["Kubernetes", "MSA", "CI/CD"],
        "description": "네이버 플랫폼의 서버 시스템을 개발하고 유지합니다.",
        "deadline": "2026-09-15"
    },
    {
        "id": 3,
        "company": "토스",
        "title": "핀테크 백엔드 개발자",
        "required_skills": ["Python", "Django", "PostgreSQL", "Linux"],
        "preferred_skills": ["gRPC", "Redis", "보안", "AWS"],
        "description": "토스의 금융 서비스 백엔드 시스템을 개발합니다.",
        "deadline": "2026-08-20"
    },
    {
        "id": 4,
        "company": "삼성SDS",
        "title": "데이터 분석가",
        "required_skills": ["Python", "SQL", "통계분석", "Excel"],
        "preferred_skills": ["R", "Tableau", "머신러닝", "시각화"],
        "description": "데이터 분석을 통해 비즈니스 인사이트를 도출합니다.",
        "deadline": "2026-09-01"
    },
    {
        "id": 5,
        "company": "LG CNS",
        "title": "데이터 엔지니어",
        "required_skills": ["Python", "SQL", "Spark", "Hadoop"],
        "preferred_skills": ["Airflow", "AWS", "Kafka", "ETL"],
        "description": "대용량 데이터 파이프라인을 설계하고 운영합니다.",
        "deadline": "2026-08-25"
    },
    {
        "id": 6,
        "company": "현대자동차",
        "title": "ML 엔지니어",
        "required_skills": ["Python", "PyTorch", "머신러닝", "통계"],
        "preferred_skills": ["MLflow", "Docker", "NLP", "컴퓨터비전"],
        "description": "자동차 서비스 개선을 위한 ML 모델을 개발합니다.",
        "deadline": "2026-09-30"
    }
]



@router.get("/jobs", tags=["Jobs"])

def get_jobs():

    """

    취업 공고 목록을 반환하는 엔드포인트.

    현재는 목업 데이터를 반환하며, 3일차에 실제 데이터로 교체한다.

    """

    return {

        "count": len(MOCK_JOBS),

        "jobs": MOCK_JOBS

    }



@router.get("/jobs/{job_id}", tags=["Jobs"])

def get_job_by_id(job_id: int):

    """

    특정 공고의 상세 정보를 반환한다.

    """

    for job in MOCK_JOBS:

        if job["id"] == job_id:

            return job

    # 찾지 못한 경우

    from fastapi import HTTPException

    raise HTTPException(status_code=404, detail=f"공고 ID {job_id}를 찾을 수 없습니다.")