from pathlib import Path
from pypdf import PdfReader

RAW_KB_FILE = Path("data/raw/company_notes.txt")

DEFAULT_KB_CONTENT = """Perplexity 是以 AI 搜索为核心定位的产品，重点在于答案组织方式、检索交互体验和信息可读性优化。它的竞争优势主要体现在搜索式问答、信息整合效率以及面向知识获取场景的产品体验。

Kimi 的核心优势在于长文本处理能力、超长上下文理解以及复杂信息整合。它在长文档阅读、资料总结和多轮上下文延续方面具备较强产品特点。

Claude 在长文本理解、安全性和稳定输出方面具备优势，常被用于复杂写作、文档处理和企业级文本任务。

AI 搜索赛道的竞争重点正在从单轮问答转向搜索、Agent、工作流与生产力工具结合。未来产品差异化将更多体现在知识整合、任务执行、专业场景适配和输出质量。
"""


def ensure_kb_file():
    RAW_KB_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not RAW_KB_FILE.exists():
        RAW_KB_FILE.write_text(DEFAULT_KB_CONTENT, encoding="utf-8")


def read_txt_file(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore")


def read_md_file(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore")


def read_pdf_file(file_bytes: bytes) -> str:
    temp_path = Path("data/raw/_temp_upload.pdf")
    temp_path.parent.mkdir(parents=True, exist_ok=True)

    with open(temp_path, "wb") as f:
        f.write(file_bytes)

    reader = PdfReader(str(temp_path))
    texts = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            texts.append(page_text)

    try:
        temp_path.unlink(missing_ok=True)
    except Exception:
        pass

    return "\n".join(texts)


def extract_text_from_upload(filename: str, file_bytes: bytes) -> str:
    lower_name = filename.lower()

    if lower_name.endswith(".txt"):
        return read_txt_file(file_bytes)
    if lower_name.endswith(".md"):
        return read_md_file(file_bytes)
    if lower_name.endswith(".pdf"):
        return read_pdf_file(file_bytes)

    raise ValueError("仅支持 txt / md / pdf 文件")


def append_to_knowledge_base(filename: str, content: str) -> str:
    ensure_kb_file()

    block = f"\n\n[来源文件: {filename}]\n{content.strip()}\n"
    with open(RAW_KB_FILE, "a", encoding="utf-8") as f:
        f.write(block)

    return str(RAW_KB_FILE)


def read_knowledge_base() -> str:
    ensure_kb_file()
    return RAW_KB_FILE.read_text(encoding="utf-8")


def clear_knowledge_base() -> str:
    ensure_kb_file()
    RAW_KB_FILE.write_text("", encoding="utf-8")
    return str(RAW_KB_FILE)


def reset_knowledge_base() -> str:
    ensure_kb_file()
    RAW_KB_FILE.write_text(DEFAULT_KB_CONTENT, encoding="utf-8")
    return str(RAW_KB_FILE)