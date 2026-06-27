import json
from typing import Any

from core.redis import redis_client

async def cache_get_json(key:str)->Any|None:
    raw = await redis_client.get(key)
    if raw is None:
        return None
    return json.loads(raw)


async def cache_set_json(key:str,value:Any,ttl_seconds:int=300):
    await redis_client.set(key,json.dumps(value),ex=ttl_seconds)

async def cache_delete(*keys:str):
    if keys:
        await redis_client.delete(*keys)

async def cache_delete_pattern(pattern:str):
    keys=[]
    async for key in redis_client.scan_iter(pattern):#if doenot ue redis stop and first give me those keys harmful
        key_str = key.decode("utf-8") if isinstance(key,bytes) else key
        keys.append(key_str)

    if keys:
        await redis_client.delete(*keys)
