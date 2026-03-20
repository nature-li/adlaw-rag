from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from retriever.search import search
from config.settings import settings

app = FastAPI()

llm = ChatOpenAI(
    model=settings.model,
    api_key=settings.api_key,
    base_url=settings.base_url,
    temperature=0.3,
)

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5

@app.post("/query")
async def query(req: QueryRequest):
    # 检索相关条款
    chunks = search(req.question, top_k=req.top_k)

    # 拼接上下文
    context = "\n\n".join([
        f"【{c['title']}】{c['text']}" for c in chunks
    ])

    # 调 LLM 生成回答
    messages = [
        {
            "role": "system",
            "content": "你是广告法专家，根据提供的广告法条款回答问题。回答要准确引用具体条款，如果相关条款不足以回答问题，请说明。",
        },
        {
            "role": "user",
            "content": f"问题：{req.question}\n\n相关条款：\n{context}",
        },
    ]

    resp = await llm.ainvoke(messages)
    return {
        "answer": resp.content,
        "references": [{"title": c["title"], "text": c["text"], "score": c["score"]} for c in chunks],
    }
