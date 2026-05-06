from app.services.postgres import SessionLocal
from app.models.incident import Incident
from datetime import datetime, timezone
from fastapi import HTTPException

def update_incident_state(
        incident_id,
        next_state,
        rca_data=None
):
    
    db = SessionLocal()

    try:

        incident = db.query(Incident).filter(
            Incident.incident_id == incident_id 
        ).first()
   
        if not incident:
            raise HTTPException(
                status_code=404,
                detail="Incident not found"
            )
    
        incident.state = next_state

        if rca_data:
            incident.root_cause = rca_data.get("root_cause")
            incident.fix_applied = rca_data.get("fix_applied")
            incident.prevention_steps = rca_data.get("prevention_steps")

        if next_state == "CLOSED":

            resolved_time = datetime.now(timezone.utc).replace(tzinfo=None)
        
            incident.resolved_at = resolved_time

            mttr = (
                resolved_time - incident.created_at
            ).total_seconds()

            incident.mttr_seconds = int(mttr)
    
        db.commit()

        db.refresh(incident)

        return incident

    finally: 
       db.close()

def create_incident(
    incident_id,
    component_id,
    severity
):
    
    db = SessionLocal()

    try:
        existing = db.query(Incident).filter(
            Incident.incident_id == incident_id
        ).first()

        if existing:
            return existing

        incident = Incident(
            incident_id=incident_id,
            component_id=component_id,
            severity=severity
        )

        db.add(incident)
        db.commit()
        db.refresh(incident)

        return incident
    
    finally:
        db.close()


def get_all_incidents():

    db = SessionLocal()

    incidents = db.query(Incident).all()

    result = []

    for incident in incidents:

        result.append({
            "incident_id": incident.incident_id,
            "component_id": incident.component_id,
            "state": incident.state,
            "created_at": incident.created_at,
        })

    db.close()

    return result

def get_incident_by_id(incident_id):

    db = SessionLocal()

    incident = db.query(Incident).filter(
        Incident.incident_id == incident_id
    ).first()

    db.close()

    if not incident:
        return None

    return {
        "incident_id": incident.incident_id,
        "component_id": incident.component_id,
        "state": incident.state,
        "created_at": incident.created_at
    }
