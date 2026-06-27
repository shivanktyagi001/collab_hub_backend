import aio_pika
RABBITMQ_URL = "amqp://guest:guest@localhost/"

connection = None
channel = None


async def connect_rabbitmq():
    global connection,channel

    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = connection.channel()

    await channel.set_qos(prefetch_count=10)

    print("rabbitMq")



async def close_rabbitmq():
    global connection
    if connection:
        await connection.close()
