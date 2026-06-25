from collections import defaultdict
from core.redis import redis_client #Reference Counting
class PresenceManager:

    def _key(self,user_id:int)-> str:
        return f"online:user:{user_id}"
    
    async def connect(self,user_id:int) -> bool:
        key = self._key(user_id)
        count = await redis_client.incr(key)
        await redis_client.expire(key,300)
        return count ==1
    async def disconnect(self,user_id:int)-> bool:
        key = self._key(user_id)
        count = await redis_client.decr(key)
        if(count<=0):
            await redis_client.delete(key)
            return True
        await redis_client.expire(key,300)
        return False
        
       
    async def is_online(self,user_id:int) -> bool:
        return await redis_client.exists(self._key(user_id))>0
    async def get_online_users(self):
        user_ids = []
        # SCAN scans the database in background chunks without freezing Redis
        async for key in redis_client.scan_iter("online:user:*"):
            # key might come back as bytes depending on your client config, so decode it
            key_str = key.decode("utf-8") if isinstance(key, bytes) else key
            user_ids.append(int(key_str.split(":")[-1]))
        return user_ids

        
presence_manager = PresenceManager()