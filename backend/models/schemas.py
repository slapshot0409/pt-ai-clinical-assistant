from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class HealingStage(str, Enum):
    acute = "acute"
    subacute = "subacute"
    chronic = "chronic"


class PTInput(BaseModel):
    symptoms: List[str] = Field(..., description="List of symptoms")
    diagnosis: str = Field(..., description="Clinical diagnosis")
    healing_stage: HealingStage = Field(..., description="Stage of healing")
    functional_limitations: List[str] = Field(..., description="Functional limitations")
    pain_level: int = Field(..., ge=0, le=10, description="Pain level 0-10")
    pain_with_movement: List[str] = Field(default=[], description="Movements that cause pain")
    tenderness_to_palpation: List[str] = Field(default=[], description="Locations of tenderness")
    constraints: List[str] = Field(default=[], description="Treatment constraints")


class Citation(BaseModel):
    title: str
    authors: List[str]
    year: str
    url: str
    source: str


class ExerciseItem(BaseModel):
    name: str
    description: Optional[str] = None
    sets: Optional[str] = None
    reps: Optional[str] = None
    frequency: Optional[str] = None
    notes: Optional[str] = None


class ManualTherapyItem(BaseModel):
    technique: str
    target: str
    rationale: Optional[str] = None


class SpecialTest(BaseModel):
    name: str
    procedure: str
    positive_finding: str
    indicates: str


class TreatmentPlanOutput(BaseModel):
    differential_diagnosis: List[str]
    gold_standard: str
    special_tests: List[SpecialTest]
    treatment_plan: str
    manual_therapy: List[ManualTherapyItem]
    exercise_protocol: List[ExerciseItem]
    progression_criteria: List[str]
    contraindications: List[str]
    recovery_timeline: str
    citations: List[Citation]
