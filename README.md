# promPT

An AI-powered Physical Therapy Clinical Decision Support System that generates evidence-based treatment plans using Retrieval-Augmented Generation (RAG) from trusted medical research databases.

## Overview

Physical therapists input patient data and the system retrieves relevant clinical evidence from PubMed, embeds it using Voyage AI, and generates structured, cited clinical recommendations using Claude AI. The system will never hallucinate medical recommendations without evidence citations.

## Features

- **Differential Diagnosis** — lettered list of possible diagnoses with rationale
- **Recommended Special Tests** — orthopedic tests with procedure, positive findings, and clinical significance
- **Treatment Plan** — evidence-based narrative with numbered citations
- **Manual Therapy** — specific techniques with target tissue and rationale
- **Exercise Protocol** — detailed step-by-step exercise instructions with sets, reps, frequency
- **Progression Criteria** — objective criteria for advancing treatment
- **Contraindications** — safety considerations
- **Recovery Timeline** — patient-specific expected recovery
- **Evidence Citations** — numbered, clickable links to supporting PubMed research

## Clinical Input Fields

- Diagnosis
- Symptoms
- Pain with Movement
- Tenderness to Palpation
- Stage of Healing (Acute / Subacute / Chronic)
- Functional Limitations
- Pain Level (0-10)
- Constraints

## Evidence Sources

- PubMed (via NCBI E-utilities API)
- 156+ research articles across 20 common PT conditions
- Dynamic ingestion — automatically fetches new research for unknown conditions
- Duplicate prevention — never stores the same article twice

## Architecture
```
PT Input Form (Next.js)
       ↓
FastAPI Backend
       ↓
RAG Pipeline
       ↓
Voyage AI Embeddings
       ↓
Supabase Vector Database (pgvector)
       ↓
Claude AI (claude-opus-4-5)
       ↓
Structured Clinical Output
```

## Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI |
| Frontend | Next.js 16, React, Tailwind CSS |
| Database | PostgreSQL via Supabase |
| Vector DB | Supabase Vector (pgvector) |
| Embeddings | Voyage AI (voyage-large-2) |
| AI Generation | Anthropic Claude (claude-opus-4-5) |
| Research API | PubMed NCBI E-utilities |

## Project Structure
```
pt-ai-clinical-assistant/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── analyze.py      # POST /api/v1/analyze endpoint
│   │   └── core/
│   │       └── config.py       # Environment variable management
│   ├── ingestion/
│   │   └── pubmed.py           # PubMed research fetching
│   ├── models/
│   │   └── schemas.py          # Pydantic data models
│   ├── rag/
│   │   ├── embeddings.py       # Voyage AI embedding
│   │   ├── pipeline.py         # RAG pipeline with dynamic ingestion
│   │   └── vectorstore.py      # Supabase vector storage and search
│   └── main.py                 # FastAPI entry point
├── frontend/
│   └── app/
│       └── page.tsx            # PT input form and results display
├── scripts/
│   ├── bulk_ingest.py          # Bulk PubMed ingestion script
│   ├── test_pubmed.py          # PubMed ingestion test
│   ├── test_rag.py             # RAG pipeline test
│   └── test_vectorstore.py     # Vector store test
└── docs/
    └── ARCHITECTURE.md         # System architecture documentation
```

## Environment Variables

Create a `.env` file in the `backend/` directory:
```
ANTHROPIC_API_KEY=your_anthropic_api_key
VOYAGE_API_KEY=your_voyage_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_service_role_key
DATABASE_URL=your_database_url
```

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

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/health | Health check |
| POST | /api/v1/analyze | Submit PT input, receive treatment plan |

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
- ⬜ Phase 10 — Deployment

## License

MIT
