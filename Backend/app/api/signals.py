from fastapi import APIRouter, Request
from app.models.signal import Signal
from app.services.debounce import process_signal
from app.services.signal_store import store_raw_signal
from app.services.queue_service import (enqueue_signal)

from app.core.limiter import limiter

router = APIRouter()


@router.post("/signals")
@limiter.limit("5/minute")
async def ingest_signal(request: Request, signal: Signal):

    signal_dict = signal.model_dump(mode="json")

    enqueue_signal(signal_dict)

    
    mongo_id = store_raw_signal(signal_dict)

    result = process_signal(signal.component_id, signal.severity)

    return {
        "status": "received",
        "mongo_id": mongo_id,
        "debounce_result": result
    }