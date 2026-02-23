# promPT

An AI-powered Physical Therapy Clinical Decision Support System that generates evidence-based treatment plans using Retrieval-Augmented Generation (RAG) from trusted medical research databases.

## Live Application

- **Frontend:** https://prompt-frontend-ten.vercel.app
- **Backend API:** https://prompt-backend.fly.dev

---

## Overview

Physical therapists input patient assessment data and promPT:
1. Searches a vector database of 298+ peer-reviewed research articles
2. Automatically fetches new research from PubMed if the condition is not yet in the database
3. Prioritizes systematic reviews and RCTs over lower-quality evidence
4. Generates structured, cited clinical recommendations using Claude AI
5. Never hallucinates — every recommendation is grounded in retrieved evidence

---

## Clinical Output Sections

| Section | Description |
|---|---|
| Differential Diagnosis | Lettered list of possible diagnoses with rationale |
| Evidence-Based Gold Standard ⭐ | Current best-practice summary from highest-quality evidence |
| Recommended Special Tests | Orthopedic tests with procedure, positive findings, and significance |
| Treatment Plan | Evidence-based narrative with numbered citations |
| Manual Therapy | Specific techniques with target tissue and rationale |
| Exercise Protocol | Step-by-step exercise instructions with sets, reps, frequency |
| Progression Criteria | Objective criteria for advancing treatment |
| Contraindications | Safety considerations |
| Recovery Timeline | Patient-specific expected recovery |
| Evidence Citations | Numbered, clickable links to PubMed research |

---

## Clinical Input Fields

- Diagnosis
- Symptoms
- Pain with Movement
- Tenderness to Palpation
- Stage of Healing (Acute / Subacute / Chronic)
- Functional Limitations
- Pain Level (0-10)
- Constraints

---

## Research Database

- **298+ articles** across 20 common PT conditions
- **Evidence quality breakdown:**
  - Systematic Reviews: 73
  - RCTs: 28
  - Clinical Trials: 12
  - Standard Articles: 185
- **Dynamic ingestion** — automatically fetches from PubMed when a new condition is encountered
- **Evidence scoring** — results ranked by combining similarity score (70%) and evidence quality (30%)
- **Duplicate prevention** — never stores the same article twice

### Evidence Quality Hierarchy
```
Systematic Review / Meta-Analysis  ← highest priority
        ↓
Randomized Controlled Trial (RCT)
        ↓
Clinical Trial
        ↓
Observational Study
        ↓
Standard Article                   ← lowest priority
```

---

## Architecture
```
PT Input Form (Next.js / Vercel)
         ↓
FastAPI Backend (Fly.io)
         ↓
RAG Pipeline
    ↓           ↓
PubMed      High-Quality PubMed
(standard)  (RCTs + Systematic Reviews)
         ↓
Voyage AI Embeddings (voyage-large-2)
         ↓
Supabase Vector Database (pgvector)
Evidence Quality Re-ranking
         ↓
Claude AI (claude-opus-4-5)
         ↓
Structured Clinical Output
```

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI |
| Frontend | Next.js 16, React, Tailwind CSS |
| Database | PostgreSQL via Supabase |
| Vector DB | Supabase pgvector |
| Embeddings | Voyage AI (voyage-large-2) |
| AI Generation | Anthropic Claude (claude-opus-4-5) |
| Research Sources | PubMed NCBI E-utilities (standard + high-quality filter) |
| Backend Hosting | Fly.io |
| Frontend Hosting | Vercel |

---

## Project Structure
```
pt-ai-clinical-assistant/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── analyze.py          # POST /api/v1/analyze endpoint
│   │   └── core/
│   │       └── config.py           # Environment variable management
│   ├── ingestion/
│   │   ├── pubmed.py               # Standard PubMed ingestion
│   │   └── pedro.py                # High-quality RCT/systematic review ingestion
│   ├── models/
│   │   └── schemas.py              # Pydantic data models
│   ├── rag/
│   │   ├── embeddings.py           # Voyage AI embeddings
│   │   ├── pipeline.py             # RAG pipeline with dual-source dynamic ingestion
│   │   └── vectorstore.py          # Supabase vector storage with evidence re-ranking
│   ├── Dockerfile                  # Docker configuration for Fly.io
│   ├── fly.toml                    # Fly.io deployment configuration
│   └── main.py                     # FastAPI entry point
├── frontend/
│   ├── app/
│   │   └── page.tsx                # PT input form and results display
│   ├── vercel.json                 # Vercel deployment configuration
│   └── .env.production             # Production environment variables
├── scripts/
│   ├── bulk_ingest.py              # Bulk PubMed ingestion for 20 conditions
│   ├── weekly_refresh.py           # Weekly research refresh script
│   ├── test_pubmed.py              # PubMed ingestion test
│   ├── test_rag.py                 # RAG pipeline test
│   └── test_vectorstore.py         # Vector store test
└── docs/
    └── ARCHITECTURE.md             # System architecture documentation
```

---

## Environment Variables

Create a `.env` file in the `backend/` directory:
```
ANTHROPIC_API_KEY=your_anthropic_api_key
VOYAGE_API_KEY=your_voyage_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_service_role_key
DATABASE_URL=your_database_url
```

---

## Running Locally

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npx next dev -p 3000
```

Visit `http://localhost:3000`

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/health | Health check |
| POST | /api/v1/analyze | Submit PT assessment, receive treatment plan |

---

## Deployment

### Backend (Fly.io)
```bash
cd backend
flyctl deploy
```

### Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

### Weekly Research Refresh
```bash
cd backend
source venv/bin/activate
python3 ../scripts/weekly_refresh.py
```

---

## Development Phases

- ✅ Phase 1 — GitHub repository and project scaffold
- ✅ Phase 2 — System architecture definition
- ✅ Phase 3 — FastAPI backend scaffold
- ✅ Phase 4 — Next.js frontend scaffold
- ✅ Phase 5 — PubMed research ingestion pipeline
- ✅ Phase 6 — Vector database and embeddings
- ✅ Phase 7 — RAG pipeline with Claude AI
- ✅ Phase 8 — Frontend/backend integration
- ✅ Phase 9 — Bulk research ingestion and dynamic fetching
- ✅ Phase 10 — Production deployment (Fly.io + Vercel)
- ✅ Phase 11 — High-quality evidence ingestion and evidence quality scoring

## Planned Features

- RBAC with Clerk (user authentication and roles)
- Save and review past patient sessions
- PDF export of treatment plans
- Mobile-optimized UI
- Automated weekly research refresh via cron job

---

## License

MIT
