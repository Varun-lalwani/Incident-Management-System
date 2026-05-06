from app.services.redis_client import redis_client
from app.services.postgres import SessionLocal
from app.models.incident import Incident
from app.services.incident_service import (create_incident,)
from app.services.signal_store import store_raw_signal
from app.types.signal import SignalData

DEBOUNCE_WINDOW = 10


def process_signal(component_id: str, severity: str):

    db = SessionLocal()

    try:

        redis_key = f"debounce:{component_id}"

        cached_incident = redis_client.get(redis_key)

        if cached_incident:

            return {
                "action": "debounced",
                "incident_id": cached_incident
            }

        existing_incident = db.query(Incident).filter(
            Incident.component_id == component_id,
            Incident.state != "CLOSED"
        ).first()

        if existing_incident:


            print(f"Existing active incident found: "
                  f"{existing_incident.incident_id}"
            )
  
            data: SignalData = {
                "component_id": component_id,
                "severity": severity,
                "incident_id": existing_incident.incident_id
            }

            store_raw_signal(data)
        
            return {
                "action": "linked_to_existing_incident",
                "incident_id": existing_incident.incident_id
            }

    
        #Create new incident if no active incident exists for the component
        incident_id = f"INCIDENT_{component_id}"

        create_incident(
            incident_id=incident_id,
            component_id=component_id,
            severity=severity
        )
     
        # Set debounce key in Redis to prevent duplicate incidents for the same component
        redis_client.setex(
            redis_key,
            DEBOUNCE_WINDOW,
            incident_id
        )

        print(f"New incident created: {incident_id}")

        return {
            "action": "new_incident_created",
            "incident_id": incident_id
        }

    finally: 
        db.close()