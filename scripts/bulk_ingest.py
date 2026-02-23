import sys
sys.path.append("../backend")

from ingestion.pubmed import fetch_research
from rag.vectorstore import store_documents
import time

CONDITIONS = [
    "ACL reconstruction rehabilitation physical therapy",
    "rotator cuff tear physical therapy treatment",
    "lateral ankle sprain rehabilitation",
    "patellofemoral pain syndrome exercise treatment",
    "lumbar disc herniation physical therapy",
    "shoulder impingement syndrome rehabilitation",
    "Achilles tendinopathy exercise treatment",
    "knee osteoarthritis physical therapy",
    "plantar fasciitis treatment rehabilitation",
    "cervical radiculopathy physical therapy",
    "hip labral tear rehabilitation",
    "tennis elbow lateral epicondylitis treatment",
    "frozen shoulder adhesive capsulitis treatment",
    "meniscus tear rehabilitation physical therapy",
    "carpal tunnel syndrome physical therapy",
    "IT band syndrome rehabilitation running",
    "hamstring strain rehabilitation return to sport",
    "low back pain exercise therapy treatment",
    "biceps tendinopathy rehabilitation",
    "tibial stress fracture rehabilitation",
]

total_stored = 0

for i, condition in enumerate(CONDITIONS):
    print(f"\n[{i+1}/{len(CONDITIONS)}] Ingesting: {condition}")
    try:
        articles = fetch_research(condition, max_results=8)
        if articles:
            store_documents(articles, query_term=condition)
            total_stored += len(articles)
            print(f"Stored {len(articles)} articles")
        # Wait 25 seconds between each condition to respect both rate limits
        if i < len(CONDITIONS) - 1:
            print("Waiting 25 seconds before next condition...")
            time.sleep(25)
    except Exception as e:
        print(f"Error: {e}")
        print("Waiting 60 seconds before retrying...")
        time.sleep(60)
        continue

print(f"\n✅ Bulk ingestion complete. Total articles stored: {total_stored}")
