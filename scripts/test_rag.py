import sys
sys.path.append("../backend")

from models.schemas import PTInput, HealingStage
from rag.pipeline import run_rag_pipeline

pt_input = PTInput(
    injury="ACL tear",
    symptoms=["knee pain", "swelling", "instability"],
    diagnosis="Grade III ACL rupture post-surgical reconstruction",
    healing_stage=HealingStage.subacute,
    functional_limitations=["unable to run", "limited knee flexion", "difficulty with stairs"],
    pain_level=4,
    constraints=["no impact activities", "no pivoting"]
)

print("Running RAG pipeline...\n")
result = run_rag_pipeline(pt_input)

print("\n=== TREATMENT PLAN ===")
print(result.treatment_plan)

print("\n=== EXERCISE PROTOCOL ===")
for ex in result.exercise_protocol:
    print(f"- {ex.name}: {ex.sets} sets x {ex.reps} reps, {ex.frequency}")

print("\n=== PROGRESSION CRITERIA ===")
for c in result.progression_criteria:
    print(f"- {c}")

print("\n=== CONTRAINDICATIONS ===")
for c in result.contraindications:
    print(f"- {c}")

print("\n=== RECOVERY TIMELINE ===")
print(result.recovery_timeline)

print("\n=== CITATIONS ===")
for cite in result.citations:
    print(f"- {cite.title} ({cite.year}) - {cite.url}")
