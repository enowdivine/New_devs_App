import json
import redis.asyncio as redis
from typing import Dict, Any
import os

# Initialize Redis client (typically configured centrally).
redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))

async def get_revenue_summary(property_id: str, tenant_id: str, month: int, year: int) -> Dict[str, Any]:
    """
    Fetches monthly revenue summary, utilizing caching to improve performance.
    """
    cache_key = f"revenue:{tenant_id}:{property_id}:{year}-{month:02d}"

    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    from app.services.reservations import calculate_monthly_revenue

    result = await calculate_monthly_revenue(property_id, tenant_id, month, year)

    await redis_client.setex(cache_key, 300, json.dumps(result))

    return result
