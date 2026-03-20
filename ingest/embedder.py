from sentence_transformers import SentenceTransformer
from pymilvus import MilvusClient, DataType
from config.settings import settings


def get_embedding_model():
    return SentenceTransformer(settings.embedding_model_path)


def create_collection(client: MilvusClient, collection_name: str, dim: int = 1024):
    if client.has_collection(collection_name):
        client.drop_collection(collection_name)

    schema = client.create_schema()
    schema.add_field("id", DataType.INT64, is_primary=True, auto_id=True)
    schema.add_field("text", DataType.VARCHAR, max_length=2000)
    schema.add_field("source", DataType.VARCHAR, max_length=100)
    schema.add_field("title", DataType.VARCHAR, max_length=50)
    schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=dim)

    index_params = client.prepare_index_params()
    index_params.add_index("embedding", metric_type="COSINE")

    client.create_collection(
        collection_name=collection_name,
        schema=schema,
        index_params=index_params,
    )
    print(f"collection {collection_name} created")


def ingest(chunks: list[dict]):
    model = get_embedding_model()
    client = MilvusClient(uri=settings.milvus_uri)

    create_collection(client, settings.milvus_collection)

    texts = [c["text"] for c in chunks]
    print(f"embedding {len(texts)} chunks...")
    embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)

    data = [
        {
            "text": c["text"],
            "source": c["source"],
            "title": c["title"],
            "embedding": emb.tolist(),
        }
        for c, emb in zip(chunks, embeddings)
    ]

    client.insert(collection_name=settings.milvus_collection, data=data)
    client.flush(collection_name=settings.milvus_collection)
    print(f"inserted {len(data)} chunks into milvus")
