from pydantic import BaseModel
from datetime import datetime

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request



class Signal(BaseModel):
    component_id: str
    severity: str
    message: str
    timestamp: datetime