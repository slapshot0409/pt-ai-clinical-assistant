from typing import List, Dict
from supabase import create_client
from app.core.config import settings
from rag.embeddings import embed_texts, embed_query

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

SIMILARITY_THRESHOLD = 0.3
MIN_RESULTS = 2

EVIDENCE_LEVEL_PRIORITY = {
    "systematic_review": 4,
    "rct": 3,
    "clinical_trial": 2,
    "observational": 1,
    "standard": 0,
}


def store_documents(articles: List[Dict], query_term: str = "") -> None:
    """Embed and store research articles in Supabase vector store."""
    texts = [f"{a['title']}. {a['abstract']}" for a in articles]
    embeddings = embed_texts(texts)

    stored = 0
    for article, embedding in zip(articles, embeddings):
        # Check if article already exists by pmid
        existing = supabase.table("research_documents").select("id").eq("pmid", article["pmid"]).execute()
        if existing.data:
            continue

        supabase.table("research_documents").insert({
            "pmid": article["pmid"],
            "title": article["title"],
            "abstract": article["abstract"],
            "authors": article["authors"],
            "year": article["year"],
            "url": article["url"],
            "source": article.get("source", "PubMed"),
            "embedding": embedding,
            "query_term": query_term,
            "evidence_level": article.get("evidence_level", "standard"),
            "source_db": article.get("source", "pubmed").lower(),
        }).execute()
        stored += 1

    print(f"Stored {stored} new documents in vector store")


def search_similar(query: str, match_count: int = 5) -> List[Dict]:
    """Search for similar documents using cosine similarity, ranked by evidence quality."""
    query_embedding = embed_query(query)

    result = supabase.rpc("match_research_documents", {
        "query_embedding": query_embedding,
        "match_count": match_count * 2,  # Fetch more, then re-rank
    }).execute()

    docs = result.data

    # Re-rank by combining similarity score with evidence level priority
    for doc in docs:
        similarity = doc.get("similarity", 0)
        evidence_priority = EVIDENCE_LEVEL_PRIORITY.get(doc.get("evidence_level", "standard"), 0)
        # Weighted score: 70% similarity, 30% evidence quality
        doc["combined_score"] = (similarity * 0.7) + (evidence_priority / 4 * 0.3)

    # Sort by combined score and return top match_count
    docs.sort(key=lambda x: x["combined_score"], reverse=True)
    return docs[:match_count]


def needs_more_research(query: str, match_count: int = 5) -> bool:
    """Check if we have sufficient relevant research for a query."""
    results = search_similar(query, match_count)
    if len(results) < MIN_RESULTS:
        return True
    top_similarity = results[0].get("similarity", 0) if results else 0
    return top_similarity < SIMILARITY_THRESHOLD
