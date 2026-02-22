import requests
import xml.etree.ElementTree as ET
from typing import List, Dict


PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def search_pubmed(query: str, max_results: int = 10) -> List[str]:
    """Search PubMed and return a list of article IDs."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
    }
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data["esearchresult"]["idlist"]


def fetch_abstracts(pubmed_ids: List[str]) -> List[Dict]:
    """Fetch abstracts for a list of PubMed IDs."""
    if not pubmed_ids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml",
        "rettype": "abstract",
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()

    articles = []
    root = ET.fromstring(response.content)

    for article in root.findall(".//PubmedArticle"):
        try:
            title = article.findtext(".//ArticleTitle") or "No title"
            abstract = article.findtext(".//AbstractText") or "No abstract available"
            pmid = article.findtext(".//PMID") or ""

            authors = []
            for author in article.findall(".//Author"):
                last = author.findtext("LastName") or ""
                fore = author.findtext("ForeName") or ""
                if last:
                    authors.append(f"{last} {fore}".strip())

            year = article.findtext(".//PubDate/Year") or "Unknown"

            articles.append({
                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "year": year,
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                "source": "PubMed",
            })
        except Exception as e:
            print(f"Error parsing article: {e}")
            continue

    return articles


def fetch_research(query: str, max_results: int = 10) -> List[Dict]:
    """Main function: search PubMed and return full article data."""
    print(f"Searching PubMed for: {query}")
    ids = search_pubmed(query, max_results)
    print(f"Found {len(ids)} articles")
    articles = fetch_abstracts(ids)
    print(f"Fetched {len(articles)} abstracts")
    return articles
