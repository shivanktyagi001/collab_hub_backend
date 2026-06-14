import json
import asyncio
import contextlib
from websocket.connection_manager import manager
from core.redis import redis_client


channel_tasks: dict[int, asyncio.Task] = {}

async def publish_event(
        channel_id:int,
        event:dict,
):
    await redis_client.publish(
        f"channel:{channel_id}",
        json.dumps(event)
    )


async def ensure_channel_subscription(channel_id: int):
    task = channel_tasks.get(channel_id)

    if task and not task.done():
        return

    channel_tasks[channel_id] = asyncio.create_task(
        subscribe_channel(channel_id)
    )


async def stop_channel_subscription(channel_id: int):
    task = channel_tasks.pop(channel_id, None)

    if not task:
        return

    task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await task

async def subscribe_channel(channel_id:int):
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(
        f"channel:{channel_id}"
    )

    try:
        while True:
            message = await pubsub.get_message(
                ignore_subscribe_messages=True
            )

            if message:
                data = json.loads(message["data"])
                await manager.broadcast(
                    channel_id,
                    data
                )

            await asyncio.sleep(0.01)
    except asyncio.CancelledError:
        raise
    finally:
        with contextlib.suppress(Exception):
            await pubsub.unsubscribe(f"channel:{channel_id}")
        with contextlib.suppress(Exception):
            await pubsub.close()

