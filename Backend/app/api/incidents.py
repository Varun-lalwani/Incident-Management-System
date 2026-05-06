from fastapi import APIRouter, HTTPException
from app.models.rca import RCAData
from app.services.postgres import SessionLocal
from app.models.incident import Incident
from app.services.incident_service import update_incident_state
from app.state_machine.transitions import transition_state
from app.schemas.incident import IncidentStateUpdateRequest

router = APIRouter()


@router.patch("/incidents/{incident_id}/state")
async def change_incident_state(
    incident_id: str,
    payload: IncidentStateUpdateRequest
):

    db = SessionLocal()

    try:
        # STEP 1: FETCH INCIDENT 
        incident = db.query(Incident).filter(
            Incident.incident_id == incident_id
        ).first()

        if not incident:
            raise HTTPException(404, "Incident not found")

        # STEP 2: VALIDATE STATE TRANSITION
        rca_data = payload.rca_data.model_dump() if payload.rca_data else None
        validated_state = transition_state(
            current_state=payload.current_state,
            next_state=payload.next_state,
            rca_data=rca_data,
            incident=incident   
        )

        # STEP 3: UPDATE INCIDENT IN DB
        updated_incident = update_incident_state(
            incident_id=incident_id,
            next_state=validated_state,
            rca_data=rca_data
        )

        return {
            "incident_id": updated_incident.incident_id,
            "new_state": updated_incident.state,
            "mttr_seconds": updated_incident.mttr_seconds
        }

    finally:
        db.close()