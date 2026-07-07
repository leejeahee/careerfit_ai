# CareerFit AI 🚀

> 취업·공모전 데이터 기반 맞춤형 AI 포트폴리오 코치

## 📖 프로젝트 개요

**"내 스케줄과 역량에 딱 맞는 공모전과 직무를 찾을 수는 없을까?"**

취업 준비생과 스펙을 쌓고자 하는 대학생들은 넘쳐나는 정보 속에서 본인에게 맞는 공모전과 직무를 찾고, 기업이 원하는 포트폴리오 방향성을 파악하는 데 많은 어려움을 겪고 있습니다.

**CareerFit AI**는 사용자의 전공, 보유 스킬, 관심 직무를 기반으로 최적의 직무 및 공모전을 추천하고, AI가 맞춤형 커리어 코칭을 제공하는 서비스입니다. 근거 없는 환각(Hallucination) 응답을 방지하기 위해 RAG(검색 증강 생성) 기술을 도입하여, 실제 채용 데이터와 요구 스킬을 기반으로 신뢰성 있는 답변을 제공합니다.

### 🎯 타겟 사용자
- 자신의 역량으로 어떤 직무를 지원할 수 있을지 막막한 **대학생**
- 기업 맞춤형 포트폴리오를 준비하고자 하는 **취업 준비생**

### ✨ 주요 기능
- **맞춤형 커리어 코칭**: 전공/스킬/경력/선호 기업 형태를 분석해 지원 가능 직무 및 부족한 역량 가이드 제공
- **신뢰성 있는 정보 제공 (RAG)**: ChromaDB 기반 벡터 검색으로 생성형 AI의 한계를 극복하고, 답변에 사용된 실제 채용 공고 출처(회사·직무·필요 역량·관련도)를 함께 제공
- **멀티 LLM Provider 지원**: Gemini / Mistral / Ollama(로컬) / HuggingFace 중 `.env` 설정만으로 전환 가능
- **안정적인 서비스 구조**: `MOCK_MODE`로 API 장애·한도 초과 시에도 서비스 중단 없이 목업 응답 제공, Provider 예외를 공통 에러 타입으로 정규화해 사용자에게 원인별 안내 메시지 제공
- **컨테이너 배포**: Docker/Docker Compose로 볼륨 영속화된 벡터 DB와 함께 실행 가능

### 🚀 향후 확장 계획
- 학교 웹사이트/커뮤니티 SSO 연동을 통한 공고 및 학점 자동 스크랩
- 구글 캘린더 연동을 통해 사용자의 기존 스케줄을 방해하지 않는 스마트 스케줄링 추천

---

## 🛠 기술 스택

| 영역 | 기술 |
|---|---|
| **백엔드** | Python 3.11, FastAPI |
| **AI API** | Gemini / Mistral / Ollama / HuggingFace (4개 Provider 지원) |
| **데이터/검색** | Pandas(전처리), ChromaDB(벡터 검색·RAG) |
| **프론트엔드** | React, Vite, Tailwind CSS |
| **실행 환경** | Docker, Docker Compose |

---

## 🏗 아키텍처

```text
┌──────────────┐      POST /analyze      ┌──────────────────┐
│   React      │ ───────────────────────▶│   FastAPI        │
│ (Vite, 5173) │                          │   (main.py)      │
│              │◀─────────────────────── │                  │
└──────────────┘   {answer, sources}      └────────┬─────────┘
                                                    │
                                     ┌──────────────┴──────────────┐
                                     ▼                             ▼
                        rag_service.search_documents      llm_service.get_llm_response
                        (ChromaDB 벡터 검색)                (RAG 프롬프트 구성 + LLM 호출)
                                     │                             │
                                     ▼                             ▼
                          backend/chroma_db                Gemini / Mistral /
                        (영속 볼륨, 문서 임베딩)              Ollama / HuggingFace
```

- **CORS**: FastAPI `CORSMiddleware`가 `localhost:5173`(프론트엔드)의 요청만 허용
- **RAG 흐름**: 사용자 입력 → 자연어 쿼리 조합 → ChromaDB 유사도 검색(상위 3건) → 검색 결과를 근거로 프롬프트 구성 → LLM 호출 → `answer` + `sources` 반환
- **에러 격리**: RAG 검색 실패 시 문서 없이 진행(fail-safe), LLM Provider 예외는 `RateLimitError` / `AuthError` / `ProviderConnectionError` / `ProviderTimeoutError` 공통 타입으로 정규화되어 서비스가 죽지 않고 원인별 안내 메시지를 반환

### API

| Method | Path | 설명 |
|---|---|---|
| GET | `/health` | 서버 상태 확인 (Docker `HEALTHCHECK`, 모니터링용) |
| POST | `/analyze` | 전공/스킬/직무/경력/선호 기업 형태를 받아 RAG 기반 커리어 분석 결과 반환 |

`/analyze` 응답 스키마(`AnalyzeResponse`)는 `answer`(문자열)와 `sources`(회사·직무·필요 역량·관련도 배열)로 고정되어 있습니다.

---

## 🚀 시작하기 (Getting Started)

### 방법 A. 로컬에서 직접 실행

**1) 백엔드**
```bash
git clone https://github.com/ejeahee/careerfit_ai.git
cd careerfit_ai/backend

python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

`backend/.env` 파일을 생성하고 아래 값을 채웁니다.
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

```bash
uvicorn main:app --reload --port 8000
```
> `http://localhost:8000/docs` 에서 Swagger UI로 API를 바로 테스트할 수 있습니다.

**2) 프론트엔드**
```bash
cd ../frontend
npm install
npm run dev
```
> `http://localhost:5173` 에서 화면 확인 (백엔드가 8000번 포트에서 먼저 실행 중이어야 함)

### 방법 B. Docker로 실행

`backend/.env`를 위와 동일하게 준비한 뒤:
```bash
cd backend
docker compose up --build
```
- `http://localhost:8000/health` 로 정상 기동 확인
- `chroma_db` 디렉터리는 named volume(`chroma_data`)으로 영속화되어 있어, 컨테이너를 재시작해도 임베딩을 다시 계산하지 않습니다
- 컨테이너는 non-root 사용자(`appuser`)로 동작하며, 이미지 빌드 시 `chroma_db` 디렉터리 소유권을 미리 맞춰두어 볼륨 마운트 시 root 소유가 되는 문제를 방지합니다
- `HEALTHCHECK`는 콜드 스타트(임베딩 모델 로딩)를 감안해 `start-period=40s`로 설정되어 있습니다

배포용 이미지만 필요하다면:
```bash
docker build -t careerfit-ai-backend .
docker build --platform=linux/amd64 -t careerfit-ai-backend .   # arm64 → amd64 크로스 빌드 시
```

프론트엔드는 별도 컨테이너 없이 `npm run dev`(또는 `npm run build` 후 정적 호스팅)로 운용합니다.

---

## 🔄 데이터 파이프라인

```text
backend/data/jobs.csv
        │  pandas 로드 (UTF-8 → 실패 시 CP949 재시도)
        ▼
결측치 확인 → 핵심 컬럼(title, required_skills) 결측 행 제거
        ▼
중복 제거 (company + title 기준)
        ▼
스킬 키워드 표준화 (예: "python" → "Python", "ml" → "머신러닝")
        ▼
자연어 문서 변환 (RAG 검색용 텍스트 + metadata 생성)
        ▼
backend/data/rag_documents.json 저장
        ▼
서버 시작 시 rag_service.initialize_collection()
        │  파일 해시(sha256) 비교로 변경 여부 감지
        ▼
ChromaDB 컬렉션(careerfit_jobs)에 임베딩 저장 (backend/chroma_db)
        ▼
/analyze 요청 시 벡터 유사도 검색 → 상위 N건을 LLM 프롬프트 근거로 사용
```

- 전처리 스크립트는 `backend/` 폴더에서 `python data/preprocess.py`로 실행합니다.
- ChromaDB는 서버가 켜져 있는 동안 `rag_documents.json`의 해시를 비교해, 데이터가 바뀐 경우에만 컬렉션을 통째로 재생성합니다(불필요한 재임베딩 방지 + 데이터 변경 시 자동 반영 보장).
- 마감일은 `"2026-09-30"`(`-` 구분)과 `"26.09.10"`(`.` 구분) 두 포맷을 모두 지원하도록 파싱하며, 파싱 불가한 값은 월(month) 정보를 0으로 처리합니다.

---

## 📁 프로젝트 구조

```text
careerfit_ai/
├── backend/
│   ├── main.py                  # FastAPI 앱, CORS, 라우터 등록, 서버 시작 시 RAG 초기화
│   ├── routers/
│   │   ├── health.py            # GET /health
│   │   └── analyze.py           # POST /analyze (RAG 검색 → LLM 호출 → 응답)
│   ├── services/
│   │   ├── rag_service.py       # ChromaDB 컬렉션 초기화/검색, 파일 해시 기반 캐시 무효화
│   │   └── llm_service.py       # provider 라우팅, RAG 프롬프트 생성, 에러 어댑터
│   ├── data/
│   │   ├── jobs.csv             # 원본 채용 데이터
│   │   ├── preprocess.py        # 전처리 → RAG 문서 변환 파이프라인
│   │   └── rag_documents.json   # 전처리 결과물 (ChromaDB 적재 대상)
│   ├── chroma_db/               # ChromaDB 퍼시스턴트 스토리지 (Docker에서는 volume)
│   ├── Dockerfile
│   ├── compose.yaml
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # 전체 화면 구성, /analyze 호출
│   │   └── components/
│   │       ├── InputForm.jsx    # 전공/스킬/직무/경력 입력 폼
│   │       ├── ResultCard.jsx   # AI 답변(역량 평가/추천/부족 역량) 파싱 출력
│   │       └── SourceCard.jsx   # 출처(회사/직무/관련도) 카드
│   └── package.json
├── docs/                        # 기획·체크리스트·모델 벤치마크 문서
└── harness/                     # Claude/Cursor/Gemini 등 공용 개발 하네스 문서
```

---

## 🧩 개발 중 특히 어려웠던 부분

- **ChromaDB 캐시가 최초 1회 이후 갱신되지 않던 문제**: 서버를 껐다 켜도 CSV를 다시 반영한 `rag_documents.json`이 실제 검색 결과에 반영되지 않았습니다. 원인은 컬렉션이 비어있을 때만 문서를 적재하고, 이후에는 무조건 기존 데이터를 재사용했기 때문입니다. `rag_documents.json`의 SHA-256 해시를 컬렉션 메타데이터에 저장해두고, 서버 시작 시 해시가 달라졌을 때만 컬렉션을 통째로 재생성하도록 바꿔 해결했습니다.
- **날짜 포맷이 두 가지로 섞여 있던 마감일 파싱**: 강사 제공 CSV에 `"2026-09-30"`과 `"26.09.10"` 두 포맷이 혼재해 있어, `-` 하나만 처리하던 최초 파서가 점(`.`) 구분 날짜에서 조용히 실패(월=0)했습니다. 구분자별로 분리 로직을 나누고, 파싱 불가 값은 명시적으로 0을 반환하도록 정리했습니다.
- **4개 LLM Provider의 서로 다른 예외를 하나로 묶기**: Gemini(SDK 예외), Mistral/HuggingFace(HTTP 에러), Ollama(연결/타임아웃 예외)가 각각 다른 형태로 실패를 알려줘, 문자열 매칭만으로는 429(한도 초과)와 401/403(인증 실패)을 안정적으로 구분하기 어려웠습니다. HTTP status_code를 우선 확인하고, 없을 때만 알려진 에러 문구로 보조 판단하는 `_classify_provider_error` 어댑터를 만들어 Provider가 바뀌어도 사용자에게 일관된 오류 메시지를 보여주도록 했습니다.
- **Docker 배포 시 발생한 3가지 함정**: (1) `compose.yaml`에 `env_file`을 빠뜨려 `.env`가 컨테이너에 주입되지 않던 문제, (2) `chroma_db`를 볼륨으로 영속화하지 않아 컨테이너를 재시작할 때마다 임베딩을 처음부터 다시 계산하던 문제, (3) 볼륨을 non-root 사용자(`appuser`) 컨테이너에 마운트했을 때 Docker가 root 소유의 빈 디렉터리로 초기화해버려 앱이 쓰기 권한 오류를 내던 문제. 이미지 빌드 단계에서 `chroma_db` 디렉터리를 미리 `appuser` 소유로 만들어두어 볼륨이 올바른 권한으로 시딩되도록 해결했습니다.
- **헬스체크 오탐**: ChromaDB의 임베딩 모델을 최초 로딩하는 콜드 스타트 구간이 예상보다 길어, `HEALTHCHECK`의 `start-period`가 15초일 때 컨테이너가 정상 기동 중인데도 unhealthy로 표시되는 경우가 있었습니다. 이를 40초로 늘려 오탐을 없앴습니다.

---

## 📈 향후 개선 사항

- **SSO 연동 스크래핑**: 학교 웹사이트/커뮤니티 로그인 연동을 통한 공고·학점 자동 수집
- **구글 캘린더 연동**: 사용자의 기존 일정을 침범하지 않는 공모전/마감일 스케줄링 추천
- **RAG 품질 고도화**: 임베딩 모델 교체 실험, 검색 결과 재순위화(re-ranking), 청크 단위 최적화
- **데이터 확장**: 목업 CSV를 넘어 실제 채용 공고 API/크롤링 연동
- **인증/개인화**: 사용자별 이력 저장 및 추천 결과 피드백 루프 구축
- **프론트엔드 개선**: 로딩/에러 상태 UX 보강, 결과 카드 반응형 레이아웃 다듬기
- **테스트 자동화**: 전처리·RAG 검색·에러 어댑터에 대한 단위 테스트, CI 파이프라인 구축

---

## 📅 진행 현황

- [x] **1일차**: 프로젝트 기획 및 개발 환경 세팅
- [x] **2일차**: FastAPI 서버 구축 및 Gemini API 연결
- [x] **3일차**: 데이터 파이프라인 구축
- [x] **4일차**: RAG 기반 서비스 + React UI 연동 완료
- [x] **5일차**: Docker 배포 + README 최종화

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
| ✅ Docker 배포 | env 주입/볼륨 영속화/헬스체크 유예시간까지 반영한 배포 설정 |
| ✅ 문서화 | Claude/Cursor/Gemini/Continue 공용 개발 하네스(`harness/`) 구축 |

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
