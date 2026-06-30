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

| 항목 | 내용 |
|------|------|
| ✅ 개발 환경 | Python 가상환경 및 FastAPI 서버 구성 |
| ✅ API 엔드포인트 | `/health`, `/jobs`, `/analyze` 구현 |
| ✅ AI 연동 | Gemini 2.5 Flash-Lite API 연결 |
| ✅ Mock Mode | `MOCK_MODE` 환경변수로 API 없이 테스트 가능 |
| ✅ 기반 구축 | RAG 기능 구현을 위한 백엔드 구조 완성 |

---

## 2일차 학습 내용

### Mock Mode
> API가 다운됐을 때 서비스 중단을 막는 안전망
> `MOCK_MODE=true` 설정 시 실제 API 호출 없이 목업 응답 반환

### 백엔드: FastAPI
> 손님 테이블 키오스크의 뒷단 — 요청을 받아 주방(DB/AI)으로 전달

- **CRUD** 가 핵심: Create / Read / Update / Delete
- 사용자 요청을 검증하고 DB·AI로 전달하는 역할

### 프론트엔드: React
> 키오스크 화면 — 사용자가 직접 보고 조작하는 영역

```
React (화면) → FastAPI (처리) → DB / AI (저장·분석)
```

- **미들웨어 (CORSMiddleware)**: 프론트와 백엔드를 이어주는 검문소
- **라우터**: 손님 요청을 담당 코너로 분류하는 안내판 (한식 → `/jobs`, 양식 → `/analyze`)
- **목업 데이터**: 실제 DB 연결 전 사용하는 임시 가짜 데이터


- [ ] 3일차: 데이터 파이프라인 구축

- [ ] 4일차: RAG 기반 서비스 + React UI

- [ ] 5일차: Docker + 포트폴리오 완성