# CareerFit AI

> 취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치



## 프로젝트 개요



취업 또는 공모전을 준비할 때 불편했던 점을 해결하자.



## 기술 스택



| 영역 | 기술 |

|---|---|

| 백엔드 | Python, FastAPI |

| AI API | Gemini 2.5 Flash-Lite |

| 데이터 | Pandas, SQLite, ChromaDB |

| 프론트엔드 | React, Vite |

| 실행 환경 | Docker |

## 진행 현황



- [x] 1일차: 프로젝트 기획 및 개발 환경 세팅

- [x] 2일차: FastAPI 서버 구축 및 Gemini API 연결


## 2일차 완료 내용

* ✅ Python 개발 환경 및 FastAPI 서버 구성을 완료했습니다.
* ✅ `/health`, `/jobs`, `/analyze` API 엔드포인트를 구현했습니다.
* ✅ Gemini 2.5 Flash-Lite API를 연동해 AI 응답 기반을 구축했습니다.
* ✅ `MOCK_MODE` 환경변수를 적용해 API 없이도 테스트 가능한 환경을 구성했습니다.
* ✅ 백엔드 기본 구조를 완성하고 이후 RAG 기능 구현을 위한 기반을 마련했습니다.

# 2일차 알게된 내용
# Mock mode
API가 아플때 서비스 중단 막는 안전망

# 백엔드 : fastAPI(손님 테이블 키오스크 뒷단)
CRUD가 핵심 (create, read, update, delete기능)
fastAPI가 손님정보를 주방으로 잘 전달

## 프론트엔드 : React (키오스크화면)
React -> FastAPI -> DB/AI 순서인데 프론트랑 백엔드 이어주는게 미들웨어(CORSMilddleware)

라우터는 손님 요청 분류기임(한식, 중식 코너별 안내)
목업데이터는 임시데이터임.


- [ ] 3일차: 데이터 파이프라인 구축

- [ ] 4일차: RAG 기반 서비스 + React UI

- [ ] 5일차: Docker + 포트폴리오 완성