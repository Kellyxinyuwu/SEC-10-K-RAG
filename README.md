# Tiny RAG Warm-up

**Status: Complete** — This week's ingestion/chunking phase is done. Ready for embeddings next week.

## What this project did

This project builds the **ingestion and splitting** muscle for RAG (Retrieval Augmented Generation):

1. **Extract text** from a PDF — reads all pages and joins them into one string
2. **Chunk the text** — splits it into fixed-size pieces (default 1000 chars) for embedding later

These chunks are the feed for embeddings when you add the full RAG pipeline (vector DB, retrieval, LLM).

---

## `ingest.py` — Step-by-step walkthrough

### Overview

The script does two things: (1) turn a PDF into raw text, and (2) split that text into chunks. Each step is explained below.

### Step 1: Extract text from PDF

```python
def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text() or "")
    return "\n".join(texts)
```

| Line | What it does |
|------|--------------|
| `reader = PdfReader(path)` | Opens the PDF file and creates a reader object. `path` is the file path (e.g. `"sample_10k.pdf"`). |
| `texts = []` | Empty list to collect text from each page. |
| `for page in reader.pages` | Loops over every page in the PDF. |
| `page.extract_text()` | Gets the text content from that page. Returns `None` if the page has no extractable text (e.g. image-only). |
| `or ""` | If `extract_text()` returns `None`, use `""` instead so we never append `None` to the list. |
| `"\n".join(texts)` | Joins all page texts with newlines into one long string. |

**Result:** One string containing the full document text.

---

### Step 2: Chunk the text

```python
def simple_chunk(text: str, max_chars: int = 1000) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        start = end
    return chunks
```

| Line | What it does |
|------|--------------|
| `chunks = []` | Empty list to hold the chunks. |
| `start = 0` | Index where the current chunk begins. |
| `while start < len(text)` | Continue until we've processed the whole text. |
| `end = min(start + max_chars, len(text))` | `end` is either `start + 1000` or `len(text)` if we're near the end (avoids going past the string). |
| `chunks.append(text[start:end])` | Slice the text from `start` to `end` and add it as one chunk. |
| `start = end` | Move the window forward for the next chunk. |

**Why chunk?** Embedding models and LLMs have context limits. Chunking lets you retrieve only the most relevant slices instead of the whole document. 1000 characters is a common default for experiments.

**Example:** 2500-character text with `max_chars=1000` → 3 chunks (chars 0–999, 1000–1999, 2000–2499).

---

### Step 3: The main block

```python
if __name__ == "__main__":
    pdf_path = "sample_10k.pdf"
    text = extract_text_from_pdf(pdf_path)
    chunks = simple_chunk(text, max_chars=1000)
    print(f"Total chunks: {len(chunks)}")
    print("First chunk preview:\n", chunks[0][:500] if chunks else "(no text)")
```

| Line | What it does |
|------|--------------|
| `if __name__ == "__main__":` | Runs only when you execute `python ingest.py` directly, not when the file is imported. |
| `pdf_path = "sample_10k.pdf"` | Path to the PDF (must be in the same folder or provide full path). |
| `extract_text_from_pdf(pdf_path)` | Calls the extraction function → full text as one string. |
| `simple_chunk(text, max_chars=1000)` | Splits the text into chunks of up to 1000 characters. |
| `chunks[0][:500]` | First 500 characters of the first chunk — a quick sanity check. |
| `if chunks else "(no text)"` | If the PDF had no text, avoids an error and prints a fallback message. |

---

### Summary flow

```
PDF file → extract_text_from_pdf() → full text string
         → simple_chunk() → list of chunks
         → (next week) embed each chunk → vector DB → retrieval
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Get a sample PDF

Save a long PDF as `sample_10k.pdf` in this folder. Options:

- **Direct PDF:** [Alphabet 2024 10-K](https://abc.xyz/assets/77/51/9841ad5c4fbe85b4440c47a4df8d/goog-10-k-2024.pdf) — right-click → Save as
- **SEC EDGAR:** [sec.gov/search-filings](https://www.sec.gov/search-filings) — search a company, find a 10-K, look for PDF attachments
- Any long finance document from investor relations sites

## Run

```bash
python ingest.py
```

Expected output: total chunk count and a preview of the first chunk.

## What's next

- **Next week:** Embed chunks, store in a vector DB, and build retrieval + LLM answering

---

## Git Study Notes

### `cd` (Change Directory)

| Command | Purpose |
|---------|---------|
| `cd path` | Move into the given folder |
| `cd ..` | Go up one level (parent folder) |
| `cd` or `cd ~` | Go to your home directory |

### Git commands used for this project

| Command | Purpose |
|---------|---------|
| `git init` | Turn the current folder into a Git repo (creates a `.git` folder). Do this once per project. |
| `git add .` | Stage all files for the next commit. The `.` means "everything in this directory." |
| `git commit -m "message"` | Save a snapshot of staged files with a descriptive message. |
| `git remote add origin <url>` | Link this repo to your GitHub repo. `origin` is the conventional name for the main remote. |
| `git branch -M main` | Rename the current branch to `main` (in case it was `master`). |
| `git push -u origin main` | Upload your commits to GitHub. `-u` sets `origin` as the default remote for future pushes. |

### Typical daily workflow

1. `git add .` — Stage your changes
2. `git commit -m "Describe what you did"` — Save locally
3. `git push` — Send to GitHub
