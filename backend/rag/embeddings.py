import voyageai
from typing import List
from app.core.config import settings

client = voyageai.Client(api_key=settings.VOYAGE_API_KEY, timeout=30)


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed a list of texts using Voyage AI."""
    result = client.embed(texts, model="voyage-large-2", input_type="document")
    return result.embeddings


def embed_query(query: str) -> List[float]:
    """Embed a single query using Voyage AI."""
    result = client.embed([query], model="voyage-large-2", input_type="query")
    return result.embeddings[0]
