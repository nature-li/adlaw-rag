from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM
    api_key: str = "ollama"
    base_url: str = "http://192.168.0.101:11434/v1"
    model: str = "qwen2.5:7b"

    # Embedding
    embedding_model_path: str = "/media/lyg/edata/models/bge-m3"

    # Milvus
    milvus_uri: str = "http://localhost:19530"
    milvus_collection: str = "adlaw"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
