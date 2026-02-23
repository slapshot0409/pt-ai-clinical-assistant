from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class HealingStage(str, Enum):
    acute = "acute"
    subacute = "subacute"
    chronic = "chronic"


class PTInput(BaseModel):
    injury: str = Field(..., description="Type of injury")
    symptoms: List[str] = Field(..., description="List of symptoms")
    diagnosis: str = Field(..., description="Clinical diagnosis")
    healing_stage: HealingStage = Field(..., description="Stage of healing")
    functional_limitations: List[str] = Field(..., description="Functional limitations")
    pain_level: int = Field(..., ge=0, le=10, description="Pain level 0-10")
    constraints: List[str] = Field(default=[], description="Treatment constraints")


class Citation(BaseModel):
    title: str
    authors: List[str]
    year: str
    url: str
    source: str


class ExerciseItem(BaseModel):
    name: str
    sets: Optional[str] = None
    reps: Optional[str] = None
    frequency: Optional[str] = None
    notes: Optional[str] = None


class TreatmentPlanOutput(BaseModel):
    treatment_plan: str
    exercise_protocol: List[ExerciseItem]
    progression_criteria: List[str]
    contraindications: List[str]
    recovery_timeline: str
    citations: List[Citation]
