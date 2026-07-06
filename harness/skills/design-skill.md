# CareerFit AI Design Skill

## 목적
CareerFit AI React UI를 "취업·공모전 데이터 기반 AI 포트폴리오 코치"에 맞는
전문성 + 친근함을 가진 화면으로 만든다. 대상 사용자는 대학생이다.

Tailwind CSS 유틸리티 클래스 기준으로 작성한다. 커스텀 CSS(`App.css` 등)를
새로 추가하지 않는다.

---

## 1. 컬러 팔레트

| 역할 | Tailwind 클래스 | 용도 |
| --- | --- | --- |
| Primary | `bg-blue-500` / `hover:bg-blue-600` | 주요 액션 버�튼(분석 요청), 포커스 링(`focus:ring-blue-500`) |
| Secondary | `border-emerald-500` | AI 분석 결과(ResultCard)를 강조하는 좌측 accent border |
| Background | `bg-slate-50` (페이지) / `bg-white` (카드) | 페이지 배경과 카드 배경을 구분해 카드가 "떠 보이게" 한다 |
| Text | `text-slate-700` (제목) / `text-slate-600` (본문) / `text-slate-500` (보조 설명) | 정보 위계를 3단계로만 나눈다 |
| Border | `border-slate-200` (카드 테두리) / `border-slate-300` (입력창 테두리) | 카드와 입력창을 시각적으로 구분 |
| Error | `bg-red-50` / `border-red-200` / `text-red-700` | 에러 메시지 박스 전용, 다른 곳에는 쓰지 않는다 |

색상은 이 표에 없는 임의의 색(`purple-500`, `pink-400` 등)을 추가하지 않는다.
새 상태가 필요하면 이 표를 먼저 갱신한다.

---

## 2. 타이포그래피 규칙

| 용도 | Tailwind 클래스 | 예시 |
| --- | --- | --- |
| 서비스 타이틀 (H1) | `text-2xl font-bold text-slate-800` | "CareerFit AI" |
| 서비스 설명 (subtitle) | `text-sm text-slate-500` | 헤더 아래 한 줄 소개 |
| 카드 제목 (H2) | `text-lg font-semibold text-slate-700` | "AI 분석 결과", "참고한 공고 출처" |
| 입력 라벨 | `text-sm font-medium text-slate-600` | InputForm의 각 입력 필드 라벨 |
| 본문/답변 텍스트 | `text-sm leading-relaxed` | ResultCard의 AI 답변 (줄바꿈 보존: `whitespace-pre-line`) |
| 보조 설명 / 메타 정보 | `text-xs text-slate-500` | SourceCard의 필수 스킬 표기 등 |

규칙:
- 폰트 크기는 `text-xs / text-sm / text-lg / text-2xl` 4단계만 사용한다. 그 사이 크기(`text-base`, `text-xl` 등)를 섞지 않는다.
- 본문 문단에는 항상 `leading-relaxed`를 붙여 긴 AI 답변도 읽기 편하게 한다.
- 굵기는 `font-medium`(라벨) / `font-semibold`(카드 제목) / `font-bold`(H1) 3단계만 사용한다.

---

## 3. 컴포넌트 구조

### App (`frontend/src/App.jsx`)
- 역할: 레이아웃 셸 + 상태 관리(`result`, `isLoading`, `error`) + API 호출.
- 시각 구조: `min-h-screen bg-slate-50` 배경 위에 `max-w-2xl mx-auto` 중앙 정렬 컬럼.
- 자식 렌더링 순서: `InputForm` → (있으면) 에러 박스 → (로딩 중이면) 로딩 문구 → (성공하면) `ResultCard` + `SourceCard`.
- App은 직접 카드 스타일(배경/그림자/테두리)을 갖지 않는다. 카드 스타일은 항상 자식 컴포넌트가 책임진다.

### InputForm
- 역할: 전공 / 보유 스킬(쉼표 구분) / 관심 직무 3개 입력 + 제출 버튼.
- 카드 스타일: `bg-white rounded-xl shadow-sm border border-slate-200 p-6` (모든 카드형 컴포넌트의 기본값).
- 버튼 상태: 입력값이 하나라도 비어 있거나 `isLoading`이면 `disabled:bg-slate-300`으로 비활성화. 로딩 중에는 라벨을 "분석 중..."으로 바꾼다.
- 확장 시에도 이 파일 하나만 수정한다 (App.jsx를 건드리지 않는다).

### ResultCard
- 역할: `answer`(string) 하나만 받아서 보여준다.
- 시각 정체성: `border-l-4 border-emerald-500`로 "AI가 만든 결과"임을 다른 카드와 구분한다.
- 제목에 이모지(`📊`)를 써서 발표 화면에서 한눈에 구분되게 한다.
- 존재하지 않는 필드(`matched_skills`, `missing_skills`, `recommended_projects`, `confidence`)를 표시하려 하지 않는다 — 실제 API가 주지 않는다.

### SourceCard
- 역할: `sources`(배열) 표시. 각 항목은 `company`, `title`, `required_skills`, `distance`만 가진다.
- 빈 배열 처리: 카드 자체를 숨기지 않고 "참고한 공고 데이터가 없습니다" 문구가 담긴 `bg-slate-50` 박스를 대신 보여준다 (empty state도 반드시 눈에 보여야 한다).
- 존재하지 않는 필드(`type`, `matched_reason`)를 표시하려 하지 않는다.
- `distance`(유사도 거리)를 사용자에게 보여줄 때는 원값(예: `0.6372`) 그대로 노출하지 않고, "관련도 높음/보통" 같은 말로 바꾸는 것을 우선 검토한다 — 아직 미구현이면 이 파일에 TODO로 남긴다.

---

## 4. 레이아웃 규칙

- 페이지 폭: `max-w-2xl mx-auto` 고정. 새 섹션을 추가해도 이 폭을 벗어나지 않는다.
- 페이지 여백: `py-10 px-4` (App 최상위 컨테이너).
- 카드 내부 여백: `p-6` (모든 카드 공통).
- 카드 간 세로 간격: `space-y-4` (ResultCard와 SourceCard 사이 등 결과 블록끼리).
- 카드 공통 형태: `rounded-xl shadow-sm border border-slate-200` — SourceCard 내부 각 항목처럼 카드 안에 하위 리스트가 있으면 `border-b border-slate-100`으로 구분하고 `last:border-0`으로 마지막 항목 테두리를 없앤다.
- 반응형: 모바일 우선. 현재 폭(`max-w-2xl`)은 데스크톱에서도 좁게 유지해 발표 화면 가독성을 우선한다. 별도 `md:`/`lg:` 브레이크포인트는 실제로 넓은 레이아웃이 필요할 때만 추가한다.

---

## 5. 금지 사항

- `sources`를 조건 없이 숨기지 않는다. 비어 있어도 empty state 문구로 보여준다.
- 존재하지 않는 API 필드(`matched_skills`, `missing_skills`, `recommended_projects`, `confidence`, `type`, `matched_reason`)를 화면에 넣지 않는다. 필요하면 먼저 백엔드 스키마부터 논의한다.
- 실제 `sources`에 없는 회사명·채용 조건·공모전 정보를 화면에서 지어내지 않는다.
- 과도한 애니메이션(`animate-bounce`, 커스텀 keyframe 등)을 넣지 않는다. `transition-colors` 정도의 짧은 전환만 허용한다.
- React 코드(`.jsx`, `.tsx`)에 API Key, `.env` 값을 절대 하드코딩하지 않는다.
- 이 파일의 팔레트 표(1번 섹션)에 없는 색을 임의로 추가하지 않는다.
- 카드 스타일(`rounded-xl shadow-sm border ...`)을 컴포넌트마다 다르게 새로 정의하지 않는다 — 항상 4번 레이아웃 규칙의 공통값을 재사용한다.

---

## 발표용 기준
발표자가 화면을 보며 다음을 설명할 수 있어야 한다.
1. 사용자가 무엇을 입력하는가? (전공 / 스킬 / 관심 직무)
2. AI가 어떤 분석 결과를 주는가? (ResultCard의 `answer`)
3. 어떤 공고 데이터가 근거인가? (SourceCard의 `sources`)
