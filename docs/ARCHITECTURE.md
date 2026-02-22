# promPT — System Architecture

## Overview

promPT is an AI-powered Physical Therapy Clinical Decision Support System. It uses Retrieval-Augmented Generation (RAG) to retrieve real clinical evidence and generate structured, cited treatment recommendations.

---

## High-Level Data Flow

1. PT enters patient data into the Next.js frontend form
2. Frontend sends a POST request to the FastAPI backend
3. Backend validates and processes the input
4. RAG pipeline embeds the query using Voyage AI embeddings
5. Vector database (Supabase Vector) retrieves the most relevant research chunks
6. Retrieved evidence is passed as context to Claude API
7. Claude generates a structured, evidence-based treatment plan
8. Response is returned to the frontend and displayed to the PT

---

## Components

### Frontend (Next.js)
- Patient input form
- Structured results display
- Citation rendering
- Hosted on Vercel

### Backend (FastAPI)
- REST API
- Input validation via Pydantic
- Orchestrates RAG pipeline
- Hosted on Supabase or AWS

### RAG Pipeline
- Embeds incoming PT query using Voyage AI
- Queries vector database for relevant research
- Constructs prompt with retrieved context
- Calls Claude API for final response generation

### Ingestion Pipeline
- Fetches research abstracts from PubMed (and later PEDro, Cochrane)
- Chunks and embeds documents using Voyage AI
- Stores vectors in Supabase Vector

### Vector Database (Supabase Vector / pgvector)
- Stores embedded research chunks
- Performs similarity search against PT queries

### Primary Database (PostgreSQL via Supabase)
- Stores session logs
- Stores generated treatment plans
- Future: user accounts, patient records

### AI Layer
- Embedding model: Voyage AI (voyage-large-2)
- Generation model: Claude 3.5 Sonnet (Anthropic)

---

## API Endpoints (v1)

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/analyze | Submit PT input, receive treatment plan |
| GET | /api/v1/health | Health check |

---

## Key Data Models

### PT Input
- injury (string)
- symptoms (list of strings)
- diagnosis (string)
- healing_stage (enum: acute, subacute, chronic)
- functional_limitations (list of strings)
- pain_level (int 0-10)
- constraints (list of strings)

### Structured Output
- treatment_plan (string)
- exercise_protocol (list)
- progression_criteria (list)
- contraindications (list)
- recovery_timeline (string)
- citations (list of objects with title, authors, url, source)

---

## Environment Variables Required

| Variable | Purpose |
|---|---|
| ANTHROPIC_API_KEY | Claude API access |
| VOYAGE_API_KEY | Voyage AI embeddings |
| SUPABASE_URL | Supabase project URL |
| SUPABASE_KEY | Supabase service key |
| DATABASE_URL | PostgreSQL connection string |

---

## Security Notes (v1)

- All secrets via environment variables, never hardcoded
- No authentication required in v1
- Authentication (JWT) planned for v2

---

## Folder Structure
```
pt-ai-clinical-assistant/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers
│   │   ├── core/         # Config, settings
│   │   └── services/     # Business logic
│   ├── rag/              # RAG pipeline
│   ├── ingestion/        # PubMed and research ingestion
│   ├── models/           # Pydantic data models
│   └── main.py           # FastAPI entry point
├── frontend/
│   ├── app/              # Next.js app directory
│   └── components/       # React components
├── docs/                 # Architecture and documentation
└── scripts/              # Utility and ingestion scripts
```
