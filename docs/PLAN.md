# Newsbridge — Implementation Plan

> Belgian news, translated to your language.
> Democratizing news reporting across Belgium's linguistic divide.

## Project Status

**Backend: Complete ✅** — All REST API routes implemented and tested (10/10 tests passing)
**Frontend: In Progress** — UI components scaffolded, needs API wiring

### What's Done
- ✅ REST API with full translation caching
- ✅ Title translation during RSS polling (batch of 5)
- ✅ Article content translation on-demand
- ✅ Database schema with translated_title column
- ✅ 10 integration tests passing
- ✅ Docker Compose setup

### What's Next
- Wire SvelteKit frontend to API endpoints
- Article detail page with translation loading states
- Settings page for language selection
- PWA manifest + service worker
- End-to-end integration testing

### Handoff Document
See `/tmp/handoff-newsbridge-ui.md` for the UI implementation handoff.

A news aggregation app that ingests Belgian RSS feeds and translates articles to the user's preferred language. The MVP bridges the gap between Flemish and Francophone news for the English-speaking international community in Belgium.

## 2. Architecture

```
┌──────────────────────────────────────────────────────┐
│                     USER BROWSER                      │
│  ┌─────────────────────────────────────────────────┐  │
│  │              SvelteKit SPA (PWA)                 │  │
│  │  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │  │
│  │  │  Card     │  │ Article  │  │  Source Filter │  │  │
│  │  │  Feed    │  │ Reader   │  │  & Preferences  │  │  │
│  │  └──────────┘  └──────────┘  └───────────────┘  │  │
│  └─────────────────────────────────────────────────┘  │
└────────────────────────┬─────────────────────────────┘
                         │ HTTP (Vite proxy in Docker)
                         ▼
┌──────────────────────────────────────────────────────┐
│              DOCKER COMPOSE (monorepo)                │
│                                                       │
│  ┌──────────────────────┐  ┌───────────────────────┐  │
│  │     FastAPI Backend   │  │  SvelteKit Frontend   │  │
│  │                      │  │                       │  │
│  │ ┌──────────────────┐ │  │ ┌───────────────────┐ │  │
│  │ │  RSS Polling     │ │  │ │  Card Feed        │ │  │
│  │ │  (feedparser)    │ │  │ │  (article list)   │ │  │
│  │ └──────────────────┘ │  │ └───────────────────┘ │  │
│  │                      │  │                       │  │
│  │ ┌──────────────────┐ │  │ ┌───────────────────┐ │  │
│  │ │ Translation      │ │  │ │  Article Reader   │ │  │
│  │ │ Service          │ │  │ │  (full text)      │ │  │
│  │ └──────────────────┘ │  │ └───────────────────┘ │  │
│  │                      │  │                       │  │
│  │ ┌──────────────────┐ │  │ ┌───────────────────┐ │  │
│  │ │ REST API         │ │  │ │  API Client       │ │  │
│  │ │ Routes           │ │  │ │  (lib/api.ts)     │ │  │
│  │ └──────────────────┘ │  │ └───────────────────┘ │  │
│  │                      │  │                       │  │
│  │ ┌──────────────────┐ │  │                       │  │
│  │ │ SQLite DB        │ │  │                       │  │
│  │ │ (sources,        │ │  │                       │  │
│  │ │  articles,        │ │  │                       │  │
│  │ │  translations)    │ │  │                       │  │
│  │ └──────────────────┘ │  │                       │  │
│  └──────────────────────┘  └───────────────────────┘  │
└───────────────────────────────────────────────────────┘
                              │ host.docker.internal
                              ▼
┌───────────────────────────────────────────────────────┐
│              HOST MACHINE                              │
│                                                       │
│  ┌──────────────────────────────────────────────────┐ │
│  │           llama-server (llama.cpp)                │ │
│  │           - Model: gemma/mistral (user's choice)  │ │
│  │           - Port: 8080                            │ │
│  │           - Exposes /v1/completions              │ │
│  └──────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────┘
```

## 3. Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Backend | Python 3.12 + FastAPI | Async, great DX, auto OpenAPI docs |
| Frontend | SvelteKit (SPA) | Clean content-first UI, small bundle |
| Database | SQLite (aiosqlite) | Zero setup, single file, MVP adequate |
| RSS Parsing | feedparser | Robust, handles malformed feeds |
| Language Detection | fasttext | Tiny (~8MB), instant, reliable |
| LLM | llama.cpp `llama-server` | Local, free, full control |
| Scheduler | APScheduler | Lightweight async job scheduler |
| Deployment | Docker Compose | Reproducible, simple |

## 4. Data Model

### Tables

**sources**
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| name | TEXT | Outlet name (e.g. "De Standaard") |
| url | TEXT UNIQUE | RSS feed URL |
| source_language | TEXT | Auto-detected or set by user |
| created_at | TIMESTAMP | Ingestion timestamp |

**articles**
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| url | TEXT UNIQUE | Article URL (dedup key) |
| title | TEXT | Article title |
| source_id | INTEGER FK | References sources |
| published_at | TIMESTAMP | Original publish date |
| content | TEXT | Full article text |
| source_language | TEXT | Detected from content |
| created_at | TIMESTAMP | Ingestion timestamp |

**translations**
| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| article_id | INTEGER FK | References articles |
| target_language | TEXT | User's chosen language |
| translated_content | TEXT | Translated text |
| status | TEXT | `pending` | `completed` | `failed` |
| created_at | TIMESTAMP | |
| completed_at | TIMESTAMP | |

### Seed Data (9 Belgian outlets)

**Dutch (nl):**
1. De Standaard — `https://www.standaard.be/rss/`
2. De Morgen — `https://www.demorgen.be/rss/`
3. VRT NWS — `https://www.vrt.be/vrtnws/nl.rss`
4. Knack — `https://www.knack.be/news/index.rdf`
5. De Tijd — `https://www.tijd.be/rss/`

**French (fr):**
6. Le Soir — `https://www.lesoir.be/rss/all`
7. La Libre Belgique — `https://www.lalibre.be/rss/`
8. RTBF Info — `https://www.rtbf.be/info/radio/rss/mr/rtvbrtinforss`
9. L'Echo — `https://www.lecho.be/rss/`

## 5. API Design

### GET /health
Returns health check. Response: `{ "status": "ok" }`

### GET /sources
List all configured RSS sources.
Response: `[ { "id": 1, "name": "De Standaard", "url": "...", "source_language": "nl" } ]`

### GET /articles?source_id=X&limit=Y&offset=Z
List articles, optionally filtered by source. Returns latest first.
Response: `[ { "id": 1, "title": "...", "translated_title": "...", "source_id": 1, "source_name": "De Standaard", "published_at": "...", "source_language": "nl", "content": "...", "created_at": "..." } ]`
- `translated_title` is `null` if not yet translated
- Frontend should show `translated_title || title`

### GET /articles/{id}
Get a single article. Returns article + any cached translation.
Response:
```json
{
  "id": 1,
  "title": "...",
  "translated_title": "...",
  "source_id": 1,
  "source_name": "De Standaard",
  "published_at": "...",
  "content": "...",
  "source_language": "nl",
  "translation": {
    "id": 1,
    "target_language": "en",
    "translated_content": "...",
    "status": "completed"
  }
}
```

### POST /articles/{id}/translate
Trigger translation of an article to the user's target language.
- If a translation already exists for this article+language, return it (cached)
- If translation is in progress, return status: "in_progress"
- If no translation exists, queue it and return status: "queued"

## 6. Translation Pipeline

### Flow

```
User clicks article card
         │
         ▼
GET /articles/{id}
         │
         ▼
Backend checks SQLite for existing translation (article_id + target_language)
         │
    ┌────┴────┐
    │         │
  Found    Not found
    │         │
    ▼         ▼
 Return   POST /articles/{id}/translate
 cached    │
 translation ▼
            │
            ▼
     Translation queued (status: "queued")
            │
            ▼
     Backend polls llama-server:
     POST /v1/completions
     {
       "model": "gemma:7b",
       "prompt": "Translate from nl to en...",
       "max_tokens": 4096,
       "temperature": 0.3
     }
            │
            ▼
     Store result in translations table
     (status: "completed")
            │
            ▼
     Return translated article to frontend
```

### Title Translation (During Polling)

```
RSS fetch → Store article (translated_title = NULL) → Batch translate titles (5 at a time) → Store translated titles
```

Title translation prompt:
```
Translate this news article title from {source_lang} to {target_lang}:

{title}

Output ONLY the translated title, nothing else.
```

### Translation Prompt

```
You are a professional news translator. Translate the following
article from {source_lang} to {target_lang}.

Rules:
- Preserve all facts, names, numbers, and quotes exactly
- Maintain the original tone and journalistic style
- Keep paragraph structure identical to the original
- Do not summarize, add commentary, or omit any content
- Output ONLY the translated text, no explanations

Article title: {title}

Article content:
{content}
```

## 7. Frontend Pages

### Home Page — Card Feed
- Scrollable list of article cards
- Each card: source badge, title, timestamp
- Click → navigate to article detail
- Filter by source (sidebar or dropdown)
- Loading, empty, and error states

### Article Detail Page
- Full article title
- Source + timestamp
- Translated content (with original language badge)
- Link to original article
- Translation trigger (if not already translated)
- Loading state during translation

### Settings Page
- Global target language selection
- Language options: English, French, Dutch
- Stored in localStorage (MVP)

## 8. Implementation Phases

### Phase 1: API Layer ✅ COMPLETE
- [x] Implement REST API routes (`/articles`, `/sources`, `/articles/{id}`, `/articles/{id}/translate`)
- [x] Add translation caching logic (check DB before calling LLM)
- [x] Add title translation during polling (batch of 5)
- [x] Database schema with `translated_title` column
- [x] 10 integration tests passing

### Phase 2: Frontend UI (IN PROGRESS)
- [ ] Wire SvelteKit frontend to API endpoints
- [ ] Card feed showing translated titles
- [ ] Article detail page with translation loading states
- [ ] Settings page for language selection
- [ ] Error handling and retry logic
- [ ] Responsive design for mobile

### Phase 3: PWA & Production
- [ ] PWA manifest + service worker
- [ ] Offline caching of translated articles
- [ ] Install prompt
- [ ] Docker Compose hardening (health checks, restart policies)
- [ ] Logging and monitoring

### Phase 4: Scaling (Roadmap)
- [ ] Multi-user auth (API keys → JWT)
- [ ] Per-user language preferences (backend)
- [ ] User source management (add/remove feeds)
- [ ] Reading history + favorites
- [ ] Translation quality feedback loop
- [ ] Full-text search (FTS5 in SQLite)
- [ ] Dutch ↔ French translation pair

### Phase 2: UX Polish
- [ ] Article detail page (`/article/[id]`)
- [ ] Settings page (language selection, localStorage)
- [ ] Source filtering/sorting
- [ ] Translation loading states (progressive reveal)
- [ ] Error handling and retry logic
- [ ] Responsive design for mobile

### Phase 3: PWA & Production
- [ ] PWA manifest + service worker
- [ ] Offline caching of translated articles
- [ ] Install prompt
- [ ] Docker Compose hardening (health checks, restart policies)
- [ ] Logging and monitoring

### Phase 4: Scaling (Roadmap)
- [ ] Multi-user auth (API keys → JWT)
- [ ] Per-user language preferences (backend)
- [ ] User source management (add/remove feeds)
- [ ] Reading history + favorites
- [ ] Translation quality feedback loop
- [ ] Full-text search (FTS5 in SQLite)
- [ ] Dutch ↔ French translation pair

## 9. Configuration

All configuration via `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `LLAMA_SERVER_URL` | `http://host.docker.internal:8080` | llama.cpp server address |
| `LLM_MODEL` | `gemma:7b` | Model name for llama.cpp |
| `LLM_MAX_TOKENS` | `4096` | Max output tokens per translation |
| `LLM_TEMPERATURE` | `0.3` | Temperature for deterministic output |
| `POLL_INTERVAL` | `30` | Minutes between RSS polls |
| `DATABASE_URL` | `sqlite+aiosqlite:///./data/newsbridge.db` | SQLite connection string |

## 10. Running Locally

### Prerequisites
1. **llama.cpp** — Install and run `llama-server` on your host
   ```bash
   llama-server -m /path/to/model.gguf --port 8080
   ```

2. **Docker Compose** — Install Docker and Docker Compose

### Start the App
```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your model name and settings

# 2. Start services
docker compose up --build

# 3. Open in browser
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

### Development Mode (without Docker)
```bash
# Backend
cd backend
pip install -e ".[dev]"
python -m uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## 11. Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| RSS feeds break/change format | Medium | Robust parsing with feedparser; monitor feed health; fallback scraping later |
| llama.cpp connection fails | High | Translation gracefully degrades — show original text with "Translation unavailable" notice |
| Translation takes too long (>30s) | Medium | Progressive loading; show partial translation; cache aggressively |
| Legal issues with RSS scraping | Low | Using official RSS feeds (syndicated content); not bypassing paywalls or anti-bot |
| Docker GPU passthrough complexity | Low | llama.cpp stays on host; no GPU passthrough needed |
| SQLite doesn't scale | Low | Migration path to PostgreSQL is straightforward |
| SvelteKit static adapter + API proxy | Medium | Use Vite dev proxy during dev; consider SSR/SSG for SEO later |

## 12. Open Questions

1. **Model choice** — Which local model to use? Recommendations:
   - `gemma:7b` — Good balance of quality/speed for translation
   - `mistral:7b` — Strong multilingual capabilities
   - `mistral:7b-instruct` — Better for instruction-following prompts
   - `command-r` — Designed for translation and multilingual tasks

2. **Translation strategy** — Should we translate the full article or just headline + first 3 paragraphs? Full text is the MVP goal, but if tokens are limited, a truncated version with "read full on original site" might be practical.

3. **PWA offline** — How much translated content should be cached offline? Full article? Just headline + first paragraph?

4. **Multi-language UI** — Should the app UI itself be translatable, or stay English-only for MVP?

---

*Last updated: 2026-06-07*
*Created during grill session + scaffolding sprint*
