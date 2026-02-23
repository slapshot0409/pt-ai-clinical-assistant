import sys
sys.path.append("../backend")

from ingestion.pubmed import fetch_research
from ingestion.pedro import fetch_pedro_research
from rag.vectorstore import store_documents
from supabase import create_client
import time
from datetime import datetime, timedelta

# Import settings
sys.path.insert(0, "../backend")
from app.core.config import settings

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

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

# High priority conditions to also fetch from PEDro
PEDRO_CONDITIONS = [
    "ACL reconstruction rehabilitation",
    "rotator cuff rehabilitation",
    "low back pain exercise therapy",
    "knee osteoarthritis physiotherapy",
    "shoulder impingement physiotherapy",
    "patellofemoral pain physiotherapy",
    "Achilles tendinopathy exercise",
    "ankle sprain rehabilitation",
    "plantar fasciitis physiotherapy",
    "cervical radiculopathy physiotherapy",
]

total_stored = 0

print(f"\n{'='*60}")
print(f"promPT Weekly Research Refresh")
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*60}\n")

# Step 1: Refresh PubMed articles
print("PHASE 1: PubMed Refresh")
print("-" * 40)

for i, condition in enumerate(CONDITIONS):
    print(f"\n[{i+1}/{len(CONDITIONS)}] PubMed: {condition}")
    try:
        articles = fetch_research(condition, max_results=8)
        if articles:
            store_documents(articles, query_term=condition)
            total_stored += len(articles)
        if i < len(CONDITIONS) - 1:
            print("Waiting 25 seconds...")
            time.sleep(25)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(60)
        continue

# Step 2: Fetch from PEDro
print("\n\nPHASE 2: PEDro Refresh")
print("-" * 40)

for i, condition in enumerate(PEDRO_CONDITIONS):
    print(f"\n[{i+1}/{len(PEDRO_CONDITIONS)}] PEDro: {condition}")
    try:
        articles = fetch_pedro_research(condition, max_results=10)
        if articles:
            store_documents(articles, query_term=condition)
            total_stored += len(articles)
        time.sleep(5)
    except Exception as e:
        print(f"Error: {e}")
        continue

print(f"\n{'='*60}")
print(f"Refresh Complete!")
print(f"New articles stored: {total_stored}")
print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"{'='*60}\n")
