from typing import List, Dict
from supabase import create_client
from app.core.config import settings
from rag.embeddings import embed_texts, embed_query

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

SIMILARITY_THRESHOLD = 0.3
MIN_RESULTS = 2


def store_documents(articles: List[Dict], query_term: str = "") -> None:
    """Embed and store research articles in Supabase vector store."""
    texts = [f"{a['title']}. {a['abstract']}" for a in articles]
    embeddings = embed_texts(texts)

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
            "source": article["source"],
            "embedding": embedding,
            "query_term": query_term,
        }).execute()

    print(f"Stored {len(articles)} documents in vector store")


def search_similar(query: str, match_count: int = 5) -> List[Dict]:
    """Search for similar documents using cosine similarity."""
    query_embedding = embed_query(query)

    result = supabase.rpc("match_research_documents", {
        "query_embedding": query_embedding,
        "match_count": match_count,
    }).execute()

    return result.data


def needs_more_research(query: str, match_count: int = 5) -> bool:
    """Check if we have sufficient relevant research for a query."""
    results = search_similar(query, match_count)
    if len(results) < MIN_RESULTS:
        return True
    top_similarity = results[0].get("similarity", 0) if results else 0
    return top_similarity < SIMILARITY_THRESHOLD
