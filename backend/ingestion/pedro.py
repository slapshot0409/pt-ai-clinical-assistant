import requests
import xml.etree.ElementTree as ET
from typing import List, Dict
import time

# PEDro doesn't have a public API, so we use PubMed with filters
# that target the same high-quality study types PEDro indexes:
# RCTs, systematic reviews, and clinical practice guidelines in physiotherapy

PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def classify_evidence_level(title: str, abstract: str) -> str:
    """Classify evidence level based on study type keywords."""
    text = (title + " " + abstract).lower()
    if any(k in text for k in ["systematic review", "meta-analysis", "cochrane"]):
        return "systematic_review"
    elif any(k in text for k in ["randomized controlled", "randomised controlled", "rct", "randomized trial"]):
        return "rct"
    elif any(k in text for k in ["clinical trial", "controlled trial"]):
        return "clinical_trial"
    elif any(k in text for k in ["cohort study", "case control", "observational"]):
        return "observational"
    else:
        return "standard"


def search_high_quality_pubmed(query: str, max_results: int = 10) -> List[str]:
    """Search PubMed filtered to RCTs and systematic reviews only."""
    # Filter to only return systematic reviews and RCTs in physiotherapy
    filtered_query = (
        f"({query}) AND "
        f"(physical therapy[MeSH] OR physiotherapy[tiab] OR rehabilitation[MeSH]) AND "
        f"(systematic review[pt] OR randomized controlled trial[pt] OR "
        f"meta-analysis[pt] OR clinical practice guideline[pt])"
    )

    params = {
        "db": "pubmed",
        "term": filtered_query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance",
    }

    response = requests.get(PUBMED_SEARCH_URL, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()
    ids = data["esearchresult"]["idlist"]
    print(f"Found {len(ids)} high-quality articles for: {query}")
    return ids


def fetch_abstracts(pubmed_ids: List[str]) -> List[Dict]:
    """Fetch article abstracts from PubMed."""
    if not pubmed_ids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml",
        "rettype": "abstract",
    }

    response = requests.get(PUBMED_FETCH_URL, params=params, timeout=15)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    articles = []

    for article in root.findall(".//PubmedArticle"):
        try:
            title_el = article.find(".//ArticleTitle")
            title = title_el.text if title_el is not None else ""

            abstract_el = article.find(".//AbstractText")
            abstract = abstract_el.text if abstract_el is not None else ""

            if not title or not abstract:
                continue

            authors = []
            for author in article.findall(".//Author"):
                last = author.find("LastName")
                first = author.find("ForeName")
                if last is not None:
                    name = last.text
                    if first is not None:
                        name += f" {first.text}"
                    authors.append(name)

            year_el = article.find(".//PubDate/Year")
            year = year_el.text if year_el is not None else ""

            pmid_el = article.find(".//PMID")
            pmid = pmid_el.text if pmid_el is not None else ""
            url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else ""

            evidence_level = classify_evidence_level(title, abstract)

            articles.append({
                "pmid": f"hq_{pmid}",  # prefix to distinguish from standard pubmed
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "year": year,
                "url": url,
                "source": "PubMed (High Quality)",
                "evidence_level": evidence_level,
            })
        except Exception as e:
            print(f"Error parsing article: {e}")
            continue

    return articles


def fetch_pedro_research(query: str, max_results: int = 10) -> List[Dict]:
    """Fetch high-quality PT research (RCTs + systematic reviews) via PubMed filters."""
    print(f"Searching for high-quality PT research: {query}")
    try:
        ids = search_high_quality_pubmed(query, max_results)
        if not ids:
            return []
        time.sleep(0.5)
        articles = fetch_abstracts(ids)
        print(f"Fetched {len(articles)} high-quality articles")
        return articles
    except Exception as e:
        print(f"High-quality search error: {e}")
        return []
