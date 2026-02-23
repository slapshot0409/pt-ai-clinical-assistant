import anthropic
import json
from typing import List, Dict
from app.core.config import settings
from rag.vectorstore import search_similar
from models.schemas import PTInput, TreatmentPlanOutput, Citation, ExerciseItem

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)


def build_query(pt_input: PTInput) -> str:
    """Build a search query from PT input."""
    return (
        f"{pt_input.injury} {pt_input.diagnosis} "
        f"{pt_input.healing_stage.value} stage rehabilitation "
        f"{' '.join(pt_input.symptoms)}"
    )


def build_prompt(pt_input: PTInput, evidence: List[Dict]) -> str:
    """Build the Claude prompt with retrieved evidence."""
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

PATIENT ASSESSMENT:
- Injury: {pt_input.injury}
- Diagnosis: {pt_input.diagnosis}
- Symptoms: {', '.join(pt_input.symptoms)}
- Stage of Healing: {pt_input.healing_stage.value}
- Functional Limitations: {', '.join(pt_input.functional_limitations)}
- Pain Level: {pt_input.pain_level}/10
- Constraints: {', '.join(pt_input.constraints) if pt_input.constraints else 'None'}

RETRIEVED EVIDENCE:
{evidence_text}

Based ONLY on the evidence above, generate a structured treatment plan in the following JSON format:
{{
  "treatment_plan": "detailed narrative treatment plan with evidence references",
  "exercise_protocol": [
    {{
      "name": "exercise name",
      "sets": "number of sets",
      "reps": "number of reps",
      "frequency": "how often",
      "notes": "any special notes"
    }}
  ],
  "progression_criteria": ["criterion 1", "criterion 2"],
  "contraindications": ["contraindication 1", "contraindication 2"],
  "recovery_timeline": "expected recovery timeline narrative",
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
    """Run the full RAG pipeline and return a structured treatment plan."""

    # Step 1: Build search query and retrieve evidence
    query = build_query(pt_input)
    print(f"Searching for evidence: {query}")
    evidence = search_similar(query, match_count=5)
    print(f"Retrieved {len(evidence)} evidence documents")

    # Step 2: Build prompt and call Claude
    prompt = build_prompt(pt_input, evidence)
    print("Calling Claude API...")

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    # Step 3: Parse response
    response_text = message.content[0].text
    print(f"Raw response preview: {response_text[:200]}")

    # Strip markdown code fences if present
    clean = response_text.strip()
    if clean.startswith("```"):
        clean = clean.split("```")[1]
        if clean.startswith("json"):
            clean = clean[4:]
    clean = clean.strip()

    data = json.loads(clean)

    # Step 4: Build structured output
    return TreatmentPlanOutput(
        treatment_plan=data["treatment_plan"],
        exercise_protocol=[ExerciseItem(**e) for e in data["exercise_protocol"]],
        progression_criteria=data["progression_criteria"],
        contraindications=data["contraindications"],
        recovery_timeline=data["recovery_timeline"],
        citations=[Citation(**c) for c in data["citations"]],
    )
