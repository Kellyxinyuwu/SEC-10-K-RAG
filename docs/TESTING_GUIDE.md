# Testing Guide

## Run tests

```bash
# Install dev deps
pip install -r requirements.txt
pip install pytest httpx

# Run all tests
python3 -m pytest tests/

# Verbose
python3 -m pytest tests/ -v

# Specific file
python3 -m pytest tests/test_rag.py -v
```

## Test structure

```
tests/
├── conftest.py      # Fixtures (TestClient)
├── test_rag.py      # Unit: infer_ticker_from_query, build_rag_prompt
├── test_ingest.py   # Unit: chunk_with_overlap, load_txt
└── test_api.py      # Integration: /, /health, /ask (mocked)
```

## What's tested

### API (`test_api.py`) — 7 tests

| Test | What it checks |
|------|----------------|
| `test_returns_200` | Root `/` returns 200 and includes docs link |
| `test_health_returns_json` | `/health` returns JSON with `status`, `database`, `ollama` |
| `test_health_200_when_all_ok` | Health returns 200 when DB and Ollama are OK |
| `test_health_503_when_db_fails` | Health returns 503 when DB fails |
| `test_ask_returns_answer_when_auth_disabled` | `/ask` returns answer when auth is disabled |
| `test_ask_respects_k_param` | `/ask` respects the `k` parameter |
| `test_ask_requires_q` | `/ask` returns 422 when `q` is missing |

### Ingest (`test_ingest.py`) — 6 tests

| Test | What it checks |
|------|----------------|
| `test_short_text_single_chunk` | Short text → single chunk |
| `test_long_text_multiple_chunks` | Long text → multiple chunks with overlap |
| `test_empty_text_returns_empty_list` | Empty text → empty list |
| `test_chunk_size_not_exceeded` | Chunk size stays within limit |
| `test_loads_file` | `load_txt` reads file contents |
| `test_ignores_encoding_errors` | `load_txt` handles encoding errors |

### RAG (`test_rag.py`) — 9 tests

| Test | What it checks |
|------|----------------|
| `test_alphabet_returns_googl` | "Alphabet" → GOOGL |
| `test_google_returns_googl` | "Google" → GOOGL |
| `test_apple_returns_aapl` | "Apple" → AAPL |
| `test_microsoft_returns_msft` | "Microsoft" → MSFT |
| `test_unknown_returns_none` | Unknown query → `None` |
| `test_case_insensitive` | Case-insensitive ticker matching |
| `test_includes_context_and_question` | Prompt includes context and question |
| `test_citation_instructions` | Prompt includes citation instructions |
| `test_context_numbering` | Context numbering in prompt |

## Mocks

- `/ask` mocks `answer_with_rag` — no Ollama/DB needed
- `/health` mocks `check_database` and `check_ollama` for 200/503 cases

Tests run without PostgreSQL or Ollama.
