# AdLaw-RAG

基于 RAG（检索增强生成）的广告法知识库问答系统。输入问题，自动检索相关广告法条款，结合 LLM 生成准确回答并引用具体条文。

![Python](https://img.shields.io/badge/python-3.12-blue)
![LangChain](https://img.shields.io/badge/LangChain-1.2-green)
![Milvus](https://img.shields.io/badge/Milvus-2.4-blue)

## 系统架构

```
用户问题
    ↓
bge-m3 Embedding     将问题向量化
    ↓
Milvus 向量检索      COSINE 相似度，返回 top-k 条款
    ↓
LLM（Qwen2.5）       结合检索结果生成回答
    ↓
返回：回答 + 引用条款 + 相似度分数
```

## 技术栈

| 模块 | 技术 |
|------|------|
| Embedding 模型 | BAAI/bge-m3（本地，1024维，中文效果好） |
| 向量数据库 | Milvus 2.4（本地，企业级） |
| LLM | Qwen2.5:7b（Ollama，兼容 OpenAI 接口） |
| RAG 框架 | LangChain |
| HTTP 服务 | FastAPI |
| chunk 策略 | 按条款切割 + 滑动窗口 |

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`：

```ini
API_KEY=ollama
BASE_URL=http://localhost:11434/v1
MODEL=qwen2.5:7b
EMBEDDING_MODEL_PATH=/path/to/bge-m3
MILVUS_URI=http://localhost:19530
MILVUS_COLLECTION=adlaw
```

### 3. 下载模型

```bash
# bge-m3 embedding 模型
python download_model.py

# LLM（Ollama）
ollama pull qwen2.5:7b
```

### 4. 启动 Milvus

```bash
DOCKER_VOLUME_DIRECTORY=/your/data/path docker compose -f docker-compose-milvus.yml up -d
```

### 5. 导入广告法文档

```bash
python ingest_run.py
```

输出示例：

```
loaded 1 docs
got 116 chunks
embedding 116 chunks...
inserted 116 chunks into milvus
done
```

### 6. 启动服务

```bash
bash start_api.sh
```

### 7. 查询

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "广告中可以使用最好最优等词语吗"}'
```

返回示例：

```json
{
  "answer": "根据《中华人民共和国广告法》第九条规定，广告中禁止使用'国家级'、'最高级'、'最佳'等用语。因此，'最好'、'最优'等词语属于最高级范畴，不得在广告中使用。",
  "references": [
    {
      "title": "第九条",
      "text": "第九条广告不得有下列情形：（三）使用'国家级'、'最高级'、'最佳'等用语...",
      "score": 0.569
    }
  ]
}
```

## 项目结构

```
adlaw-rag/
├── ingest/
│   ├── loader.py       # 文档读取和清洗
│   ├── chunker.py      # 按条款切割，滑动窗口
│   └── embedder.py     # bge-m3 向量化 + Milvus 入库
├── retriever/
│   └── search.py       # 向量检索，返回 top-k 条款
├── api/
│   └── main.py         # FastAPI 服务，检索 + LLM 生成
├── config/
│   └── settings.py     # 统一配置
├── tests/
│   └── test_retriever.py
├── data/               # 广告法文本（gitignore）
├── ingest_run.py       # 一键导入入口
├── docker-compose-milvus.yml
└── requirements.txt
```

## Chunk 策略

按广告法条款（第X条）切割，每条对应一个 chunk，保留条款完整性。超过 300 字的条款用滑动窗口（overlap=50）切割，避免语义截断。

共切出 116 个 chunk，覆盖广告法全部 80+ 条款。
