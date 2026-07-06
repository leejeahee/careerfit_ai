import chromadb
import hashlib
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CHROMA_PATH = str(BASE_DIR / "chroma_db")
RAG_JSON = str(BASE_DIR / "data" / "rag_documents.json")
COLLECTION_DESCRIPTION = "CareerFit AI 취업·공모전 데이터"

client = chromadb.PersistentClient(path=CHROMA_PATH)


def _file_hash(path: str) -> str:
    """파일 내용의 해시를 계산합니다. rag_documents.json 변경 여부를 감지하는 데 사용합니다."""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def get_or_create_collection() -> chromadb.Collection:
    """
    ChromaDB 컬렉션을 가져오거나, 비어있거나 rag_documents.json이 바뀌었으면 RAG 문서를 다시 로드합니다.
    요리 비유: 레시피 북을 열고, 비어있거나 레시피 카드가 바뀌었으면 다시 채워넣습니다.
    """
    collection = client.get_or_create_collection(
        name="careerfit_jobs",
        metadata={"description": COLLECTION_DESCRIPTION}
    )

    current_hash = _file_hash(RAG_JSON)
    stored_hash = (collection.metadata or {}).get("source_hash")

    if collection.count() == 0 or stored_hash != current_hash:
        print("⚠️  ChromaDB가 비어있거나 원본 데이터가 변경되었습니다. RAG 문서를 다시 저장합니다...")
        _load_documents(collection)
        collection.modify(metadata={
            "description": COLLECTION_DESCRIPTION,
            "source_hash": current_hash
        })

    return collection


def _load_documents(collection: chromadb.Collection) -> None:
    """rag_documents.json에서 문서를 읽어 ChromaDB를 완전히 새로 채웁니다."""
    with open(RAG_JSON, "r", encoding="utf-8") as f:
        documents = json.load(f)

    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    collection.add(
        documents=[doc["text"] for doc in documents],
        metadatas=[doc["metadata"] for doc in documents],
        ids=[doc["doc_id"] for doc in documents]
    )
    print(f"✅ {collection.count()}개 문서 저장 완료")


def search_documents(query: str, n_results: int = 3) -> list:
    """
    사용자 질문과 의미적으로 유사한 문서를 ChromaDB에서 검색합니다.

    Args:
        query: 사용자 질문 텍스트
        n_results: 반환할 문서 수 (기본값 3)

    Returns:
        [{"text": str, "metadata": dict, "distance": float}, ...]
    """
    collection = get_or_create_collection()

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count())
    )

    return [
        {
            "text": text,
            "metadata": metadata,
            "distance": round(distance, 4)
        }
        for text, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )
    ]