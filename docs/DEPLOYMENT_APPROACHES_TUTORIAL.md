# Deployment Approaches Tutorial

This tutorial explains the two main ways to run the SEC-10-K-RAG project: **Full Command Reference** (DB in Docker, API on host) and **Docker Compose** (DB + API in Docker). It covers the differences, pros and cons, and when to use each approach.

---

## Overview

| Aspect | Full Command Reference | Docker Compose Alternative |
|--------|------------------------|----------------------------|
| **Docker usage** | Database only (`docker compose up -d db`) | Database + API (`docker compose up -d --build`) |
| **Where API runs** | On your machine via `uvicorn` | Inside a Docker container |
| **API port** | 8001 | 8000 |
| **Ollama** | Must run locally on host | Same (Ollama stays on host either way) |
| **Ingest** | Run locally | Run locally (Docker API may have connectivity issues) |
| **Steps** | 9 explicit steps | Fewer steps; one command starts DB + API |

---

## Approach 1: Full Command Reference

**What it does:** Only the database runs in Docker. The API, ingest, and all Python scripts run directly on your machine.

### Step-by-step commands

1. **Clone and setup environment**
   ```bash
   cd SEC-10-K-RAG
   python3 -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   pip3 install -r requirements.txt
   pip3 install -e .
   ```

2. **Edit download script** — Set `COMPANY_NAME` and `COMPANY_EMAIL` in `scripts/download_financial_docs.py`

3. **Download 10-K filings**
   ```bash
   python3 scripts/download_financial_docs.py
   ```

4. **Start database (Docker)**
   ```bash
   docker compose up -d db
   ```
   PostgreSQL with pgvector runs on **port 5433**.

5. **Ingest documents**
   ```bash
   export DATABASE_URL="postgresql://postgres:postgres@localhost:5433/rag_db"
   python3 -m tiny_rag.ingest
   ```

6. **Pull Ollama model**
   ```bash
   ollama pull llama3.2
   ```

7. **Start API server**
   ```bash
   export DATABASE_URL="postgresql://postgres:postgres@localhost:5433/rag_db"
   uvicorn tiny_rag.api:app --host 0.0.0.0 --port 8001
   ```
   API runs at **http://localhost:8001**.

8. **Test**
   ```bash
   curl http://localhost:8001/health
   curl "http://localhost:8001/ask?q=What%20are%20Alphabet%27s%20main%20risks%3F"
   ```

9. **Optional: run evaluation**
   ```bash
   export DATABASE_URL="postgresql://postgres:postgres@localhost:5433/rag_db"
   python3 -m tiny_rag.eval
   ```

### Pros

- **Simpler networking** — The API runs on your machine, so it talks to Ollama at `localhost:11434` and the DB at `localhost:5433` without Docker networking.
- **Easier development** — Edit code, run tests, and debug without rebuilding images.
- **Fewer moving parts** — No `host.docker.internal` or Docker networking to troubleshoot.
- **More reliable** — Avoids the "empty reply from server" issues mentioned in the README.

### Cons

- **Local setup required** — You need Python, venv, and dependencies installed on your machine.
- **Environment differences** — Your setup may differ from others (Python version, OS, etc.).
- **More manual steps** — You start the DB, then the API, and manage env vars yourself.

---

## Approach 2: Docker Compose (DB + API)

**What it does:** Both the database and the API run in Docker containers. Ingest still runs on the host (due to connectivity issues on some setups).

### Step-by-step commands

1. **Setup (one-time)**
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip3 install -r requirements.txt && pip3 install -e .
   ```

2. **Edit `COMPANY_NAME` and `COMPANY_EMAIL`** in `scripts/download_financial_docs.py`

3. **Download 10-K filings**
   ```bash
   python3 scripts/download_financial_docs.py
   ```

4. **Start DB + API**
   ```bash
   docker compose up -d --build
   ```

5. **Ingest (from host)**
   ```bash
   export DATABASE_URL="postgresql://postgres:postgres@localhost:5433/rag_db"
   python3 -m tiny_rag.ingest
   ```

6. **Test API (Docker)**
   ```bash
   curl http://localhost:8000/health
   curl "http://localhost:8000/ask?q=What%20are%20Alphabet%27s%20main%20risks%3F"
   ```

7. **If Docker API returns empty response** — Run the API locally instead:
   ```bash
   docker compose stop api
   export DATABASE_URL="postgresql://postgres:postgres@localhost:5433/rag_db"
   uvicorn tiny_rag.api:app --host 0.0.0.0 --port 8001
   ```

### Pros

- **One command** — `docker compose up -d --build` starts both DB and API.
- **Reproducible** — Same Python version and dependencies for everyone.
- **Portable** — Others can run it without installing Python or managing venvs.
- **Closer to production** — Mirrors how services are typically run in containers.

### Cons

- **Ollama on the host** — The API container must reach Ollama via `host.docker.internal:11434`. This works on Mac/Windows but can fail on Linux or with certain network setups.
- **Slower iteration** — Code changes usually require rebuilding the image.
- **Harder debugging** — Logs and debugging happen inside the container.

---

## Why Put Both DB and API in Docker?

The Docker Compose approach runs both the database and the API in containers. Reasons for this:

1. **Single command to run everything** — One `docker compose up` instead of starting DB and API separately.
2. **Consistent environment** — Same Python version and dependencies for all developers.
3. **Production-like setup** — In production, both DB and API typically run in containers.
4. **Easier onboarding** — New contributors can run the app without installing Python or setting up a venv.

The tradeoff is that the API container must reach **Ollama on the host**. The `docker-compose.yml` uses `host.docker.internal` for this, which can be unreliable (especially on Linux). That’s why the README suggests falling back to running the API locally if you hit connectivity issues.

### How the Docker API reaches Ollama

From `docker-compose.yml`:

```yaml
environment:
  OLLAMA_HOST: http://host.docker.internal:11434
extra_hosts:
  - "host.docker.internal:host-gateway"
```

- `host.docker.internal` is a special hostname that points to the host machine from inside a container.
- It works on Mac and Windows; on Linux it may need extra configuration.
- If Ollama isn’t running on the host, or networking fails, the API will return empty responses.

---

## Comparison Summary

| Criterion | Full Command Reference | Docker Compose |
|-----------|------------------------|----------------|
| **Best for** | Development, learning, debugging | Sharing, demos, CI, reproducibility |
| **Reliability** | Higher (no Docker–host networking) | Can fail on some setups |
| **Setup effort** | More steps, local Python required | Fewer steps, one command |
| **Iteration speed** | Fast (no rebuilds) | Slower (rebuild on code changes) |
| **Portability** | Depends on local Python | Same environment for everyone |

---

## Practical Recommendation

- **Development / learning:** Use the **Full Command Reference** (DB in Docker, API on host). It’s simpler and more reliable.
- **Sharing / demos / CI:** Use **Docker Compose** (DB + API) when you want a single, reproducible way to run the whole stack.

---

## Related docs

- [README.md](../README.md) — Quick start and commands
- [DOCKER_GUIDE.md](DOCKER_GUIDE.md) — Docker files and usage
- [PRODUCTION_OPTIMIZATIONS.md](PRODUCTION_OPTIMIZATIONS.md) — Production deployment
