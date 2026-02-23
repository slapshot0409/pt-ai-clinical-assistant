import anthropic
import json
from typing import List, Dict
from app.core.config import settings
from rag.vectorstore import search_similar, store_documents, needs_more_research
from ingestion.pubmed import fetch_research
from models.schemas import PTInput, TreatmentPlanOutput, Citation, ExerciseItem, ManualTherapyItem, SpecialTest

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)


def build_query(pt_input: PTInput) -> str:
    return (
        f"{pt_input.diagnosis} "
        f"{pt_input.healing_stage.value} stage rehabilitation "
        f"{' '.join(pt_input.symptoms)}"
    )


def build_prompt(pt_input: PTInput, evidence: List[Dict]) -> str:
    evidence_text = ""
    for i, doc in enumerate(evidence, 1):
        evidence_text += f"""
[{i}] Title: {doc['title']}
Authors: {', '.join(doc['authors']) if doc['authors'] else 'Unknown'}
Year: {doc['year']}
URL: {doc['url']}
Abstract: {doc['abstract']}
---
"""

    return f"""You are an expert Physical Therapy clinical decision support AI.
You must ONLY make recommendations that are directly supported by the provided research evidence.
You must NEVER hallucinate or invent medical recommendations without citation.
If the retrieved evidence is not relevant to the diagnosis, say so clearly.

PATIENT ASSESSMENT:
- Diagnosis: {pt_input.diagnosis}
- Symptoms: {', '.join(pt_input.symptoms)}
- Stage of Healing: {pt_input.healing_stage.value}
- Functional Limitations: {', '.join(pt_input.functional_limitations)}
- Pain Level: {pt_input.pain_level}/10
- Pain with Movement: {', '.join(pt_input.pain_with_movement) if pt_input.pain_with_movement else 'Not specified'}
- Tenderness to Palpation: {', '.join(pt_input.tenderness_to_palpation) if pt_input.tenderness_to_palpation else 'Not specified'}
- Constraints: {', '.join(pt_input.constraints) if pt_input.constraints else 'None'}

RETRIEVED EVIDENCE:
{evidence_text}

Based ONLY on the evidence above, generate a structured clinical response in the following JSON format:
{{
  "differential_diagnosis": [
    "Most likely diagnosis with brief rationale",
    "Alternative diagnosis 1 with brief rationale",
    "Alternative diagnosis 2 with brief rationale"
  ],
  "gold_standard": "A concise 2-3 sentence summary of the current evidence-based gold standard treatment approach for this condition based on the retrieved research, with citation numbers e.g. [1], [2]",
  "special_tests": [
    {{
      "name": "name of special orthopedic test",
      "procedure": "step by step description of how to perform the test",
      "positive_finding": "what a positive result looks like",
      "indicates": "what a positive result suggests"
    }}
  ],
  "treatment_plan": "detailed narrative treatment plan with evidence references by number e.g. [1], [2]",
  "manual_therapy": [
    {{
      "technique": "name of manual therapy technique",
      "target": "target tissue or joint",
      "rationale": "brief rationale based on evidence"
    }}
  ],
  "exercise_protocol": [
    {{
      "name": "exercise name",
      "description": "step by step instructions for how to perform the exercise",
      "sets": "number of sets",
      "reps": "number of reps or duration",
      "frequency": "how often per day or week",
      "notes": "any progressions, modifications, or special instructions"
    }}
  ],
  "progression_criteria": ["criterion 1", "criterion 2"],
  "contraindications": ["contraindication 1", "contraindication 2"],
  "recovery_timeline": "expected recovery timeline narrative based only on current patient",
  "citations": [
    {{
      "title": "article title",
      "authors": ["author1", "author2"],
      "year": "year",
      "url": "pubmed url",
      "source": "PubMed"
    }}
  ]
}}

Respond with valid JSON only. No additional text. No markdown. No code fences.
"""


def run_rag_pipeline(pt_input: PTInput) -> TreatmentPlanOutput:
    query = build_query(pt_input)
    print(f"Searching for evidence: {query}")

    if needs_more_research(query):
        print(f"Insufficient research found — fetching from PubMed for: {pt_input.diagnosis}")
        fresh_articles = fetch_research(pt_input.diagnosis + " physical therapy treatment", max_results=8)
        if fresh_articles:
            store_documents(fresh_articles, query_term=pt_input.diagnosis)
            print(f"Dynamically ingested {len(fresh_articles)} new articles")

    evidence = search_similar(query, match_count=5)
    print(f"Retrieved {len(evidence)} evidence documents")

    prompt = build_prompt(pt_input, evidence)
    print("Calling Claude API...")

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text
    print(f"Raw response preview: {response_text[:200]}")

    clean = response_text.strip()
    if clean.startswith("```"):
        clean = clean.split("```")[1]
        if clean.startswith("json"):
            clean = clean[4:]
    clean = clean.strip()

    data = json.loads(clean)

    return TreatmentPlanOutput(
        differential_diagnosis=data["differential_diagnosis"],
        gold_standard=data["gold_standard"],
        special_tests=[SpecialTest(**t) for t in data["special_tests"]],
        treatment_plan=data["treatment_plan"],
        manual_therapy=[ManualTherapyItem(**m) for m in data["manual_therapy"]],
        exercise_protocol=[ExerciseItem(**e) for e in data["exercise_protocol"]],
        progression_criteria=data["progression_criteria"],
        contraindications=data["contraindications"],
        recovery_timeline=data["recovery_timeline"],
        citations=[Citation(**c) for c in data["citations"]],
    )
