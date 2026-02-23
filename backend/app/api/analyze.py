from fastapi import APIRouter, HTTPException
from models.schemas import PTInput, TreatmentPlanOutput
from rag.pipeline import run_rag_pipeline

router = APIRouter()


@router.post("/analyze", response_model=TreatmentPlanOutput)
async def analyze(pt_input: PTInput):
    """Accept PT input and return an evidence-based treatment plan."""
    try:
        result = run_rag_pipeline(pt_input)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
