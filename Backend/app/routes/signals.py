from fastapi import APIRouter
from app.models.signal import Signal
from app.services.debounce import process_signal

router = APIRouter()


@router.post("/signals")
async def ingest_signal(signal: Signal):

    debounce_result = process_signal(
        signal.component_id,
        signal.severity
    )

    return {
        "status": "received",
        "component_id": signal.component_id,
        "severity": signal.severity,
        "debounce_result": debounce_result,
        "timestamp": signal.timestamp
    }