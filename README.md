# CareerFit AI 🚀

> 취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치

## 📖 프로젝트 개요

**"내 스케줄과 역량에 딱 맞는 공모전과 직무를 찾을 수는 없을까?"**

취업 준비생과 스펙을 쌓고자 하는 대학생들은 넘쳐나는 정보 속에서 본인에게 맞는 공모전과 직무를 찾고, 기업이 원하는 포트폴리오 방향성을 파악하는 데 많은 어려움을 겪고 있습니다. 

**CareerFit AI**는 사용자의 전공, 보유 스킬, 관심 직무를 기반으로 최적의 직무 및 공모전을 추천하고, AI가 맞춤형 커리어 코칭을 제공하는 서비스입니다. 근거 없는 환각(Hallucination) 응답을 방지하기 위해 RAG(검색 증강 생성) 기술을 도입하여, 실제 채용 데이터와 요구 스킬을 기반으로 신뢰성 있는 답변을 제공합니다.

## 🎯 타겟 사용자
- 자신의 역량으로 어떤 직무를 지원할 수 있을지 막막한 **대학생**
- 기업 맞춤형 포트폴리오를 준비하고자 하는 **취업 준비생**

## ✨ 주요 기능 (Key Features)
- **맞춤형 커리어 코칭**: 사용자의 전공/스킬 정보를 분석하여 지원 가능 직무 및 부족한 역량 가이드 제공
- **신뢰성 있는 정보 제공 (RAG 구축 완료)**: ChromaDB 기반 RAG로 생성형 AI의 한계를 극복하고 실제 채용 데이터 출처(Sources) 제공
- **안정적인 서비스 구조**: API 장애 시에도 서비스가 중단되지 않는 Mock Mode 지원

### 🚀 향후 확장 계획
- 학교 웹사이트/커뮤니티 SSO 연동을 통한 공고 및 학점 자동 스크랩
- 구글 캘린더 연동을 통해 사용자의 기존 스케줄을 방해하지 않는 스마트 스케줄링 추천

---

## 🛠 기술 스택

| 영역 | 기술 |
|---|---|
| **백엔드** | Python 3.11, FastAPI |
| **AI API** | Gemini / Mistral / Ollama / HuggingFace (4개 Provider 지원) |
| **데이터베이스** | Pandas, ChromaDB |
| **프론트엔드** | React, Vite, Tailwind CSS |
| **실행 환경** | Docker |

---

## ⚙️ 서비스 흐름 (Service Flow)

```text
1. 사용자 입력 (React) : 전공, 스킬, 관심 직무, 경험 연수 입력 
2. 서버 요청 (FastAPI) : 백엔드의 `/analyze` 엔드포인트 호출
3. AI 분석 (Gemini) : 사용자의 정보와 DB의 채용 데이터를 기반으로 맞춤형 프롬프트 작성 후 호출
4. 결과 반환 (React) : 맞춤형 조언과 출처(근거 데이터) 화면 출력
```

---

## 🚀 시작하기 (Getting Started)

### 1. 환경 설정
```bash
# 저장소 클론 및 백엔드 디렉토리 이동
git clone https://github.com/ejeahee/careerfit_ai.git
cd careerfit_ai/backend

# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# 패키지 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`backend` 폴더 내에 `.env` 파일을 생성하고 다음 값을 입력합니다.
```ini
# 사용할 provider의 API Key만 채우면 됩니다
GEMINI_API_KEY=당신의_제미나이_API_키
MISTRAL_API_KEY=당신의_미스트랄_API_키
HUGGINGFACE_TOKEN=당신의_허깅페이스_토큰

MOCK_MODE=false

# gemini-2.5-flash-lite / mistral-small-latest /
# ollama:llama3.2:3b / huggingface:모델제공자/모델이름 중 택 1
LLM_MODEL=gemini-2.5-flash-lite

# Ollama 사용 시 로컬 서버 주소 (기본값 그대로 두면 됨)
OLLAMA_BASE_URL=http://localhost:11434
```

### 3. 백엔드 서버 실행
```bash
uvicorn main:app --reload --port 8000
```
> 서버가 실행되면 `http://localhost:8000/docs` 에서 Swagger UI를 통해 API 테스트가 가능합니다!

### 4. 프론트엔드 실행
```bash
cd ../frontend
npm install
npm run dev
```
> `http://localhost:5173` 에서 화면을 확인할 수 있습니다. (백엔드가 8000번 포트에서 먼저 실행 중이어야 합니다)

---

## 📅 진행 현황

- [x] **1일차**: 프로젝트 기획 및 개발 환경 세팅
- [x] **2일차**: FastAPI 서버 구축 및 Gemini API 연결
- [x] **3일차**: 데이터 파이프라인 구축
- [x] **4일차**: RAG 기반 서비스 + React UI 연동 완료
- [ ] **5일차**: Docker + 포트폴리오 완성

### 완료 내용

| 항목 | 내용 |
|------|------|
| ✅ 개발 환경 | Python 가상환경 및 FastAPI 서버 구성 |
| ✅ API 엔드포인트 | `/health`, `/analyze` 구현 |
| ✅ AI 연동 | Gemini/Mistral/Ollama/HuggingFace 4개 Provider 지원 |
| ✅ Mock Mode | `MOCK_MODE` 환경변수로 API 없이 테스트 가능 |
| ✅ RAG 구축 | ChromaDB 기반 채용공고 검색 및 근거(Sources) 제공, 데이터 변경 시 자동 캐시 갱신 |
| ✅ 에러 처리 | Provider별 예외를 공통 타입(RateLimit/Auth/Connection/Timeout)으로 정규화하는 어댑터 구조 |
| ✅ 프론트엔드 | React + Tailwind CSS 기반 입력/결과 화면 연동, 채용 사이트 스타일 UI |
| ✅ 문서화 | Claude/Cursor/Gemini/Continue 공용 개발 하네스(`harness/`) 구축 |

### 오늘 진행한 주요 작업 (2026-07-06)

**🐛 버그 수정**
- `preprocess.py` 마감일 파싱: `"26.09.10"` 같은 점(`.`) 구분 날짜 포맷을 못 읽던 문제 수정
- ChromaDB 캐시가 최초 1회 이후 절대 갱신되지 않던 문제 → 파일 해시 비교 기반 자동 재로드로 수정
- `sources`의 `required_skills`가 항상 빈 값이던 문제(메타데이터 누락) 수정
- Gemini SDK의 `ResourceExhausted` 예외가 429로 분류 안 되던 에러 어댑터 버그 수정

**🧹 코드 정리 (Dead Code 제거)**
- 실사용되지 않던 `/jobs` 라우터, 중복 스모크테스트 스크립트(`test_search.py`) 삭제
- 아무 데서도 읽지 않던 SQLite 저장 파이프라인 전체 제거 → 채용데이터 흐름을 ChromaDB 단일 경로로 통일
- 미사용 import, 항상 `False`였던 `is_startup` 필드 제거

**🔗 RAG · 프론트-백엔드 연동**
- `experience_years`(경력), `preferred_company_size`(선호 기업 형태) 입력을 프론트엔드까지 연결해 실제 분석 프롬프트에 반영
- `distance`(유사도 거리) 원시값 대신 "관련도 %" + 색상 배지로 사용자 친화적으로 변환

**🛡️ 에러 처리 리팩토링**
- Gemini/Mistral/Ollama/HuggingFace 4개 Provider의 서로 다른 예외를 문자열 매칭 대신 공통 예외 타입(`RateLimitError`, `AuthError`, `ProviderConnectionError`, `ProviderTimeoutError`)으로 정규화

**🎨 UI 개선**
- 상단 로고 헤더, 채용 필터 스타일 입력 폼, 회사 아바타·스킬 태그·관련도 배지가 있는 채용 리스팅 스타일로 개선
- AI 답변을 "현재 역량 평가 / 추천 공고 / 부족한 역량" 3개 섹션으로 파싱해 표시 (형식이 다르면 원문 그대로 폴백)

**📚 문서화**
- Claude Code / Cursor / Gemini / Continue / Google AI Studio가 공통으로 참조하는 `harness/` 문서 체계 구축 (`MAIN_HARNESS.md`, `ROUTING.md`, 역할별 agent/skill/check 파일)
- 문서에 남아있던 실제 코드와 어긋나는 내용(존재하지 않는 API 필드, 깨진 파일 참조 등) 정리

### 학습 노트

#### Mock Mode
> API가 다운됐을 때 서비스 중단을 막는 안전망
> `MOCK_MODE=true` 설정 시 실제 API 호출 없이 목업 응답 반환

#### 백엔드: FastAPI
> 손님 테이블 키오스크의 뒷단 — 요청을 받아 주방(DB/AI)으로 전달
- **CRUD** 가 핵심: Create / Read / Update / Delete
- 사용자 요청을 검증하고 DB·AI로 전달하는 역할

#### 프론트엔드: React
> 키오스크 화면 — 사용자가 직접 보고 조작하는 영역
- **미들웨어 (CORSMiddleware)**: 프론트와 백엔드를 이어주는 검문소
- **라우터**: 손님 요청을 담당 코너로 분류하는 안내판 (`/health`, `/analyze`)
- **목업 데이터**: 실제 DB 연결 전 사용하는 임시 가짜 데이터