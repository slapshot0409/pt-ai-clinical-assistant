# promPT

An AI-powered Physical Therapy Clinical Decision Support System that generates evidence-based treatment plans using Retrieval-Augmented Generation (RAG) from trusted medical research databases.

## Overview

Physical therapists input patient data including injury, symptoms, diagnosis, healing stage, functional limitations, pain level, and constraints. The system retrieves relevant clinical evidence and generates structured, cited treatment recommendations.

## Evidence Sources

- PubMed
- PEDro
- Cochrane Library
- CINAHL
- Open-access clinical journals

## Outputs

- Treatment plan
- Exercise protocol
- Progression criteria
- Contraindications
- Expected recovery timeline
- Citations with links to supporting research

## Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | Next.js (React) |
| Database | PostgreSQL (Supabase) |
| Vector DB | Supabase Vector / Pinecone |
| AI | Claude API, OpenAI Embeddings |
| Hosting | Vercel (frontend), Supabase/AWS (backend) |

## License

MIT
