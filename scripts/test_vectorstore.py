import sys
sys.path.append("../backend")

from ingestion.pubmed import fetch_research
from rag.vectorstore import store_documents, search_similar

# Step 1: Fetch articles from PubMed
print("Fetching articles from PubMed...")
articles = fetch_research("ACL rehabilitation physical therapy", max_results=3)

# Step 2: Store in vector database
print("Embedding and storing in Supabase...")
store_documents(articles)

# Step 3: Test similarity search
print("\nSearching for similar documents...")
results = search_similar("knee rehabilitation exercises after ACL surgery", match_count=3)

for r in results:
    print("---")
    print(f"Title: {r['title']}")
    print(f"Similarity: {r['similarity']:.4f}")
    print(f"URL: {r['url']}")
