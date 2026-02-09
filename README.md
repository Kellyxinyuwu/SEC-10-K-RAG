# Tiny RAG Warm-up

PDF extraction and text chunking—the ingestion/splitting muscle for RAG. This is the feed for embeddings next week.

## What it does

- **`extract_text_from_pdf(path)`** — Reads a PDF and returns all page text as one string
- **`simple_chunk(text, max_chars=1000)`** — Splits text into fixed-size chunks (no overlap)

## Setup

```bash
pip install -r requirements.txt
```

## Get a sample PDF

Download a 10-K from [SEC EDGAR](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany) or use any long PDF. Save it as `sample_10k.pdf` in this folder.

## Run

```bash
python ingest.py
```

Expected output: total chunk count and a preview of the first chunk.
