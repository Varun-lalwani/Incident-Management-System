from pydantic import BaseModel
from typing import Optional, Dict, Any


class RCAData(BaseModel):
    root_cause: str
    fix_applied: str
    prevention_steps: str


class IncidentStateUpdateRequest(BaseModel):
    current_state: str
    next_state: str
    rca_data: Optional[RCAData] = None