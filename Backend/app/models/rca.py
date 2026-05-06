from pydantic import BaseModel
class RCAData(BaseModel):

    root_cause: str

    fix_applied:str
    
    prevention_steps: str