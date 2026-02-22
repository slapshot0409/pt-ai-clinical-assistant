import sys
sys.path.append("../backend")

from ingestion.pubmed import fetch_research

results = fetch_research("ACL rehabilitation physical therapy", max_results=3)

for article in results:
    print("---")
    print(f"Title: {article['title']}")
    print(f"Authors: {', '.join(article['authors'][:3])}")
    print(f"Year: {article['year']}")
    print(f"URL: {article['url']}")
    print(f"Abstract: {article['abstract'][:200]}...")
