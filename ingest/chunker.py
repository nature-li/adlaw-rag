import re


def chunk_by_article(
    text: str, source: str, chunk_size: int = 300, overlap: int = 50
) -> list[dict]:
    """按条款切割，每条为一个 chunk，过长则滑动窗口切割"""
    chunks = []

    # 按条款分割（第X条）
    pattern = r"(第[一二三四五六七八九十百]+条)"
    parts = re.split(pattern, text)

    current_article = ""
    current_title = ""

    for i, part in enumerate(parts):
        if re.match(pattern, part):
            current_title = part
        else:
            if current_title:
                content = current_title + part.strip()
                # 如果太长就按 chunk_size 切
                if len(content) <= chunk_size:
                    chunks.append(
                        {
                            "source": source,
                            "title": current_title,
                            "text": content,
                        }
                    )
                else:
                    # 滑动窗口切割
                    for j in range(0, len(content), chunk_size - overlap):
                        chunk = content[j : j + chunk_size]
                        if len(chunk) > 50:  # 过滤太短的
                            chunks.append(
                                {
                                    "source": source,
                                    "title": current_title,
                                    "text": chunk,
                                }
                            )
                current_title = ""

    return chunks


def chunk_docs(
    docs: list[dict], chunk_size: int = 300, overlap: int = 50
) -> list[dict]:
    chunks = []
    for doc in docs:
        chunks.extend(chunk_by_article(doc["text"], doc["source"], chunk_size, overlap))
    return chunks
