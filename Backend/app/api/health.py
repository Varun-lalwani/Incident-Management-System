from fastapi import APIRouter

from app.services.redis_client import redis_client

router = APIRouter()

@router.get("/health")
async def health_check():

    redis_status = redis_client.ping()

    return {
        "status": "healthy",
        "redis": redis_status
    }

