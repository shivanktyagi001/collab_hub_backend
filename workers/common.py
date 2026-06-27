import aio_pika

RABBITMQ_URL = "amqp://guest:guest@localhost/"

async def start_rabbitmq():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)

    channel = await connection.channel()

    await channel.set_qos(prefetch_count=10)

    return connection,channel