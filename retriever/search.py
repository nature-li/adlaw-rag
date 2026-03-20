from sentence_transformers import SentenceTransformer
from pymilvus import MilvusClient
from config.settings import settings

_model = None
_client = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.embedding_model_path)
    return _model


def get_client():
    global _client
    if _client is None:
        _client = MilvusClient(uri=settings.milvus_uri)
    return _client


def search(query: str, top_k: int = 5) -> list[dict]:
    model = get_model()
    client = get_client()

    query_embedding = model.encode([query])[0].tolist()

    results = client.search(
        collection_name=settings.milvus_collection,
        data=[query_embedding],
        limit=top_k,
        output_fields=["text", "title", "source"],
    )

    chunks = []
    for hit in results[0]:
        chunks.append({
            "title": hit["entity"]["title"],
            "text": hit["entity"]["text"],
            "source": hit["entity"]["source"],
            "score": hit["distance"],
        })
    return chunks