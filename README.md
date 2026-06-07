# Newsbridge

> Belgian news, translated to your language.
> Democratizing news reporting across Belgium's linguistic divide.

A news aggregation app that scrapes Belgian RSS feeds and translates articles to the user's preferred language — democratizing news reporting across Belgium's linguistic divide.

## Status

**Backend: Complete ✅** — 10/10 tests passing
**Frontend: In Progress** — UI components scaffolded, needs API wiring

See [docs/PLAN.md](docs/PLAN.md) for the full implementation plan and current status.

## Stack

- **Backend:** Python / FastAPI + SQLite
- **Frontend:** SvelteKit (PWA)
- **Translation:** Local LLM via llama.cpp `llama-server`
- **Deployment:** Docker Compose

## Prerequisites

1. [llama.cpp](https://github.com/ggerganov/llama.cpp) with `llama-server` running on your host machine
2. [Docker](https://docs.docker.com/get-docker/) + [Docker Compose](https://docs.docker.com/compose/install/)

## Quick Start

```bash
# 1. Ensure llama-server is running on your host
#    llama-server -m /path/to/model --port 8080

# 2. Configure environment
cp .env.example .env
# Edit .env with your LLM model name and settings

# 3. Start
docker compose up --build
```

- **Backend API:** http://localhost:8000
- **Frontend:** http://localhost:5173

## Architecture

```
newsbridge/
├── backend/          # FastAPI: RSS ingestion, translation, API
├── frontend/         # SvelteKit: card feed, reading view
├── docker-compose.yml
├── .env.example
└── README.md
```

The llama.cpp `llama-server` runs on the host machine. Docker services connect to it via `host.docker.internal`.
