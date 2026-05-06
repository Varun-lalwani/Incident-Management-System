from datetime import datetime

from fastapi import FastAPI
from app.state_machine.transitions import transition_state
from app.api.signals import router as signal_router
from app.api.incidents import router as incident_router
from app.routes.incidents import router as incidents_router
from app.services.postgres import SessionLocal
from app.models.incident import Incident


from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.core.limiter import limiter 



from app.api.health import router as health_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.state.limiter = limiter 
app.add_middleware(SlowAPIMiddleware)
app.include_router(signal_router)
app.include_router(incident_router)

app.include_router(health_router)
app.include_router(incidents_router)


@app.get("/")
async def root():
    return {"message": "IMS Running"}


@app.post("/test-transition")
async def test_transition():

    fake_incident = Incident(
        incident_id="TEST_1",
        component_id="CACHE",
        severity="P2",
        state="RESOLVED",
        created_at=datetime.utcnow()
    )

    new_state = transition_state(
        current_state="RESOLVED",
        next_state="CLOSED",
        rca_data={
            "root_cause": "DB connection pool exhausted",
            "fix_applied": "Increased pool size",
            "prevention_steps": "Add monitoring alerts"
        },
        incident=fake_incident
    )

    return {
        "new_state": new_state
    }