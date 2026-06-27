import asyncio
import json

from workers.common import start_rabbitmq


async def start_worker():

    connection, channel = await start_rabbitmq()

    try:

        queue = await channel.declare_queue(
            "analytics_queue",
            durable=True,
        )

        async with queue.iterator() as iterator:

            async for message in iterator:

                async with message.process():

                    data = json.loads(message.body)

                    print("Received:", data)

    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(start_worker())