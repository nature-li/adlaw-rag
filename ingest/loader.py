import re
from pathlib import Path


def load_text(file_path: str) -> str:
    path = Path(file_path)
    text = path.read_text(encoding="utf-8")
    # 去掉全角空格和多余空行
    text = text.replace("\u3000", " ").replace("\xa0", " ")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" +\n", "\n", text)  # 去掉行尾空格
    text = re.sub(r"\n +", "\n", text)  # 去掉行首空格
    return text.strip()


def load_all(data_dir: str) -> list[dict]:
    docs = []
    for path in Path(data_dir).glob("*.txt"):
        text = load_text(str(path))
        docs.append({"source": path.name, "text": text})
    return docs