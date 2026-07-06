# backend/services/llm_service.py
# RAG 연결 + LLM_MODEL 기반 provider 분기 + Ollama 통합 버전

import os
import requests
from dotenv import load_dotenv


# =========================
# 1. 환경변수 로드
# =========================

# .env 파일을 읽습니다.
# [요리] 비유: 비법 소스 보관함을 여는 단계입니다.
load_dotenv()

# MOCK_MODE=true이면 실제 LLM API를 호출하지 않습니다.
# [요리] 비유: 진짜 셰프를 부르지 않고 시식용 샘플 응답만 내는 상태입니다.
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

# .env에서 사용할 모델명을 읽습니다.
# 예:
# - gemini-2.5-flash-lite
# - gemini-2.5-flash
# - mistral-small-latest
# - ollama:llama3.2:3b
# - huggingface:Qwen/Qwen2.5-0.5B-Instruct
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash-lite")

# provider별 API Key를 읽습니다.
# [요리] 비유: 셰프별 출입증입니다.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Ollama는 로컬 서버 주소를 사용합니다.
# 기본 주소는 http://localhost:11434 입니다.
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


# =========================
# 2. LLM_MODEL → provider/model 분리
# =========================

def get_provider_and_model(model_name: str) -> tuple[str, str]:
    """
    LLM_MODEL 값을 보고 어떤 LLM provider를 사용할지 결정합니다.

    [요리] 비유:
    주문서에 적힌 셰프 이름을 보고
    Gemini 셰프, Mistral 셰프, Ollama 로컬 셰프, HuggingFace 셰프 중
    누구에게 보낼지 정합니다.
    """

    # 예: ollama:llama3.2:3b
    # provider = ollama
    # model = llama3.2:3b
    if model_name.startswith("ollama:"):
        return "ollama", model_name.replace("ollama:", "", 1)

    # 예: huggingface:Qwen/Qwen2.5-0.5B-Instruct
    # provider = huggingface
    # model = Qwen/Qwen2.5-0.5B-Instruct
    if model_name.startswith("huggingface:"):
        return "huggingface", model_name.replace("huggingface:", "", 1)

    # "ollama"/"huggingface"만 쓰고 실제 모델 ID(콜론 뒤)를 빠뜨린 흔한 오타를 명확히 잡습니다.
    if model_name in ("ollama", "huggingface"):
        raise ValueError(
            f"LLM_MODEL='{model_name}'에 실제 모델 ID가 빠졌습니다. "
            f"'{model_name}:모델이름' 형식으로 지정하세요."
        )

    # 예: mistral-small-latest
    if model_name.startswith("mistral"):
        return "mistral", model_name

    # 예: gemini-2.5-flash-lite
    if model_name.startswith("gemini"):
        return "gemini", model_name

    raise ValueError(
        f"인식할 수 없는 LLM_MODEL입니다: '{model_name}'. "
        "gemini-*, mistral-*, ollama:모델, huggingface:모델 형식만 지원합니다."
    )


# 앱 실행 시점에 provider와 실제 모델명을 계산합니다.
PROVIDER, PROVIDER_MODEL = get_provider_and_model(LLM_MODEL)


# =========================
# 3. RAG 프롬프트 생성
# =========================

def build_rag_prompt(query: str, context_docs: list) -> str:
    """
    사용자 질문 + RAG 검색 문서 → LLM 프롬프트 구성

    [요리] 비유:
    query는 손님의 주문,
    context_docs는 레시피 카드,
    prompt는 셰프에게 전달하는 최종 주문서입니다.
    """

    if context_docs:
        context_text = "\n".join([
            f"""
[공고 {i + 1}]
{doc.get("text", "")}

출처: {doc.get("metadata", {}).get("company", "")} — {doc.get("metadata", {}).get("title", "")}
필요 역량: {doc.get("metadata", {}).get("required_skills", "")}
유사도 거리: {doc.get("distance", "")}
""".strip()
            for i, doc in enumerate(context_docs)
        ])

        context_section = f"""
[참고 데이터 — 실제 취업·공모전 공고]
{context_text}

위 데이터를 반드시 근거로 사용해 답변하세요.
답변에서 어떤 공고를 참고했는지 명시하세요.
검색된 데이터에 없는 회사명, 조건, 공모전 정보는 지어내지 마세요.
"""
    else:
        context_section = """
[참고 데이터 없음]
제공된 자료만으로는 판단하기 어렵습니다.
일반적인 커리어 조언만 간단히 제공하세요.
"""

    return f"""당신은 취업·공모전 전문 커리어 코치입니다.
다음 지원자 정보와 참고 데이터를 바탕으로 맞춤형 조언을 한국어로 제공하세요.

[지원자 정보]
{query}

{context_section}

[답변 형식]
1. 현재 역량 평가 (2문장 이내)
2. 추천 공고 또는 공모전 (1~2개, 이유 포함)
3. 부족한 역량 및 준비 방향 (3가지 이내)

[중요 규칙]
- 반드시 한국어로 답변하세요.
- 참고 데이터가 있으면 반드시 그 데이터를 근거로 답변하세요.
- 참고 데이터가 부족하면 "제공된 자료만으로는 판단하기 어렵습니다"라고 말하세요.
- 간결하고 실용적으로 작성하세요.
""".strip()


# =========================
# 4. sources 응답 생성
# =========================

def build_sources(context_docs: list) -> list:
    """
    RAG 검색 문서를 API 응답용 sources 형식으로 변환합니다.

    [요리] 비유:
    어떤 레시피 카드를 참고했는지 영수증처럼 정리하는 단계입니다.
    """

    sources = []

    for doc in context_docs:
        metadata = doc.get("metadata", {})

        sources.append({
            "company": metadata.get("company", ""),
            "title": metadata.get("title", ""),
            "required_skills": metadata.get("required_skills", ""),
            "job_type": metadata.get("job_type", ""),
            "distance": doc.get("distance", 0),
        })

    return sources

    # =========================
# 5. Gemini 호출
# =========================

def call_gemini(prompt: str) -> str:
    """
    Gemini API를 호출합니다.

    [요리] 비유:
    Google 외부 셰프에게 주문서를 보내는 단계입니다.
    """

    if not GEMINI_API_KEY:
        raise AuthError("GEMINI_API_KEY가 .env에 없습니다.")

    import google.generativeai as genai

    genai.configure(api_key=GEMINI_API_KEY)

    # 기존처럼 모델명을 코드에 고정하지 않고,
    # .env의 LLM_MODEL 값을 사용합니다.
    model = genai.GenerativeModel(PROVIDER_MODEL)

    try:
        response = model.generate_content(prompt)
    except Exception as e:
        raise _classify_provider_error(e) from e

    return response.text


# =========================
# 6. Mistral 호출
# =========================

def call_mistral(prompt: str) -> str:
    """
    Mistral API를 호출합니다.

    [요리] 비유:
    Gemini 셰프가 바쁠 때 Mistral 셰프에게 같은 주문서를 보내는 단계입니다.
    """

    if not MISTRAL_API_KEY:
        raise AuthError("MISTRAL_API_KEY가 .env에 없습니다.")

    url = "https://api.mistral.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": PROVIDER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise _classify_provider_error(e) from e

    data = response.json()

    return data["choices"][0]["message"]["content"]


# =========================
# 7. Ollama 호출 — 통합 버전
# =========================

def call_ollama(prompt: str) -> str:
    """
    Ollama 로컬 추론 서버를 호출합니다.

    기존 backend/services/ollama_service.py의 기능을
    llm_service.py 안으로 통합한 함수입니다.

    [요리] 비유:
    외부 셰프가 아니라 내 노트북 안의 로컬 셰프에게
    주문서를 직접 전달하는 단계입니다.
    """

    url = f"{OLLAMA_BASE_URL}/api/generate"

    payload = {
        # 예:
        # LLM_MODEL=ollama:llama3.2:3b
        # PROVIDER_MODEL=llama3.2:3b
        "model": PROVIDER_MODEL,

        # /api/generate는 messages가 아니라 prompt를 사용합니다.
        "prompt": prompt,

        # False이면 응답을 한 번에 받습니다.
        "stream": False,
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]

    except requests.exceptions.ConnectionError as e:
        raise ProviderConnectionError(
            "Ollama 서버에 연결할 수 없습니다. "
            "`ollama serve` 또는 `ollama run llama3.2:3b`를 실행했는지 확인하세요."
        ) from e

    except requests.exceptions.Timeout as e:
        raise ProviderTimeoutError(
            "Ollama 응답 시간이 초과되었습니다. "
            "더 작은 모델을 사용하거나 timeout 값을 늘려보세요."
        ) from e

    except requests.exceptions.RequestException as e:
        raise _classify_provider_error(e) from e


# =========================
# 8. HuggingFace 호출
# =========================

def call_huggingface(prompt: str) -> str:
    """
    HuggingFace InferenceClient를 호출합니다.

    [요리] 비유:
    HuggingFace 모델 창고에서 특정 셰프를 골라
    주문서를 보내는 단계입니다.
    """

    if not HUGGINGFACE_TOKEN:
        raise AuthError("HUGGINGFACE_TOKEN이 .env에 없습니다.")

    from huggingface_hub import InferenceClient

    client = InferenceClient(
        model=PROVIDER_MODEL,
        token=HUGGINGFACE_TOKEN,
    )

    try:
        response = client.chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            max_tokens=700,
        )
    except Exception as e:
        raise _classify_provider_error(e) from e

    message = response.choices[0].message

    # huggingface_hub 버전에 따라 message가 객체처럼 오거나 dict처럼 올 수 있어 대비합니다.
    if hasattr(message, "content"):
        return message.content

    return message["content"]

    # =========================
# 9. provider에 따라 실제 LLM 호출
# =========================

class LLMError(Exception):
    """모든 LLM Provider 공통 에러의 기반 클래스."""


class RateLimitError(LLMError):
    """API 사용량/요청 한도 초과 (HTTP 429)."""


class AuthError(LLMError):
    """인증 실패 — API Key/Token이 없거나 유효하지 않음."""


class ProviderConnectionError(LLMError):
    """Provider 서버에 연결할 수 없음."""


class ProviderTimeoutError(LLMError):
    """Provider 응답이 제한 시간 내에 오지 않음."""


def _classify_provider_error(e: Exception) -> LLMError:
    """
    Provider별로 다른 예외(requests의 HTTPError, huggingface_hub/Gemini SDK 예외 등)를
    공통 LLMError 계열로 변환하는 어댑터입니다.
    가능하면 실제 HTTP status_code를 우선 보고, 없으면 알려진 에러 문구로 보조 판단합니다.
    """
    # requests 계열(Mistral/HuggingFace)은 e.response.status_code,
    # google-generativeai/api_core 계열(Gemini)은 e.code에 HTTP 상태코드를 담습니다.
    status_code = getattr(getattr(e, "response", None), "status_code", None) or getattr(e, "code", None)
    error_msg = str(e)

    if (
        status_code == 429
        or "RESOURCE_EXHAUSTED" in error_msg
        or "429 Client Error" in error_msg
        or "429 Too Many Requests" in error_msg
    ):
        return RateLimitError(error_msg)

    if (
        status_code in (401, 403)
        or "401 Client Error" in error_msg
        or "403 Client Error" in error_msg
        or "Invalid username or password" in error_msg
    ):
        return AuthError(error_msg)

    return LLMError(error_msg)


def call_llm(prompt: str) -> str:
    """
    PROVIDER 값에 따라 실제 호출할 LLM을 선택합니다.

    [요리] 비유:
    주문서는 하나지만,
    오늘 부를 셰프가 누구인지에 따라 전달 경로를 바꿉니다.
    """

    if PROVIDER == "gemini":
        return call_gemini(prompt)

    if PROVIDER == "mistral":
        return call_mistral(prompt)

    if PROVIDER == "ollama":
        return call_ollama(prompt)

    if PROVIDER == "huggingface":
        return call_huggingface(prompt)

    raise ValueError(f"지원하지 않는 LLM provider입니다: {PROVIDER}")


# =========================
# 10. FastAPI 라우터에서 사용할 최종 함수
# =========================

def get_llm_response(query: str, context_docs: list) -> dict:
    """
    RAG 문서와 함께 LLM 응답을 생성합니다.

    반환 구조:
    {
        "answer": "...",
        "sources": [...]
    }
    """

    sources = build_sources(context_docs)

    # MOCK_MODE=true이면 실제 API 호출 없이 구조만 확인합니다.
    if MOCK_MODE:
        return {
            "answer": (
                f"[MOCK 응답] 질문: '{query}', 참고 문서 수: {len(context_docs)}개. "
                f"현재 설정 모델: {LLM_MODEL}, provider: {PROVIDER}. "
                "MOCK_MODE=false 설정 시 실제 응답을 받습니다."
            ),
            "sources": sources,
        }

    try:
        # 1) RAG 프롬프트 생성
        prompt = build_rag_prompt(query, context_docs)

        # 2) .env의 LLM_MODEL에 따라 실제 LLM 호출
        answer = call_llm(prompt)

        # 3) 기존 응답 구조 유지
        return {
            "answer": answer,
            "sources": sources,
        }

    except RateLimitError:
        return {
            "answer": (
                "[API 한도 초과] 현재 선택된 LLM API 한도에 도달했습니다. "
                ".env에서 MOCK_MODE=true로 전환하거나 "
                "LLM_MODEL을 다른 모델로 바꿔보세요."
            ),
            "sources": sources,
        }

    except AuthError as e:
        return {
            "answer": (
                f"[인증 오류] {PROVIDER} 인증에 실패했습니다: {e} "
                ".env에서 해당 provider의 API Key/Token을 확인하세요."
            ),
            "sources": sources,
        }

    except ProviderConnectionError as e:
        return {"answer": f"[연결 오류] {e}", "sources": sources}

    except ProviderTimeoutError as e:
        return {"answer": f"[시간 초과] {e}", "sources": sources}

    except LLMError as e:
        return {
            "answer": (
                f"[오류] 현재 모델: {LLM_MODEL}, provider: {PROVIDER}. "
                f"오류 내용: {e}"
            ),
            "sources": sources,
        }