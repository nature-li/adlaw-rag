from dotenv import load_dotenv

load_dotenv()

from ingest.loader import load_all
from ingest.chunker import chunk_docs
from ingest.embedder import ingest

if __name__ == "__main__":
    print("loading docs...")
    docs = load_all("data")
    print(f"loaded {len(docs)} docs")

    print("chunking...")
    chunks = chunk_docs(docs)
    print(f"got {len(chunks)} chunks")

    print("ingesting...")
    ingest(chunks)
    print("done")
