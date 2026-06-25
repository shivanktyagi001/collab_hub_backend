from fastapi import HTTPException,Request,status
from core.redis import redis_client


def get_client_ip(request:Request)->str:
    forwarded = request.headers.get("x-forwarded-for")

    if forwarded:
        return forwarded.split(",")[0].strip()
    
    if request.client and request.client.host:
        return request.client.host
    
    return "unknown"



async def enforce_rate_limit(
        key:str,
        max_requests:int,
        window_seconds:int,
):
    count = await redis_client.incr(key)
    if count == 1:
        await redis_client.expire(key,window_seconds)

    if count>max_requests:
        ttl = await redis_client.ttl(key)
        retry_after  = (
            ttl if ttl and ttl>0 else window_seconds
        )

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many requests. Try again in {retry_after} seconds.",
        )
    
async def rate_limit_register(request:Request):
    ip = get_client_ip(request)

    await enforce_rate_limit(
        key=f"rl:register:{ip}",
        max_requests=5,
        window_seconds=60,
    )

async def rate_limit_login(request:Request):
    ip = get_client_ip(request)
    await enforce_rate_limit(
        key=f"rl:login:{ip}",
        max_requests=10,
        window_seconds=60,
    )

async def rate_limit_send_message(user_id: int):
    await enforce_rate_limit(
        key=f"rl:send_message:user:{user_id}",
        max_requests=30,
        window_seconds=60,
    )







    