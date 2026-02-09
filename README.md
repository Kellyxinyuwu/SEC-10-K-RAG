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
