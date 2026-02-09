"""
Tiny RAG warm-up: PDF extraction and text chunking.
This is the feed for embeddings next week.
"""
from pypdf import PdfReader


def extract_text_from_pdf(path: str) -> str:
    """Extract all text from a PDF, one page at a time, joined by newlines."""
    reader = PdfReader(path)
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text() or "")
    return "\n".join(texts)


def simple_chunk(text: str, max_chars: int = 1000) -> list[str]:
    """Split text into chunks of at most max_chars characters (no overlap)."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        start = end
    return chunks


if __name__ == "__main__":
    pdf_path = "sample_10k.pdf"
    text = extract_text_from_pdf(pdf_path)
    chunks = simple_chunk(text, max_chars=1000)
    print(f"Total chunks: {len(chunks)}")
    print("First chunk preview:\n", chunks[0][:500] if chunks else "(no text)")
