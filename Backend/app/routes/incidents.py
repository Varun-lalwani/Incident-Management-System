from fastapi import APIRouter
from app.services.incident_service import get_all_incidents
from app.services.incident_service import (get_all_incidents, get_incident_by_id)
from fastapi import HTTPException

router = APIRouter()


@router.get("/incidents")
async def fetch_incidents():

    incidents = get_all_incidents()

    return {
        "count": len(incidents),
        "incidents": incidents
    }

@router.get("/incidents/{incident_id}")
async def fetch_incident(incident_id: str):

    incident = get_incident_by_id(incident_id)

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident