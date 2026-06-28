import json 
import aio_pika
import core.rabbitmq as rabbitmq

async def publish_message(queue_name:str,data:dict):
    channel = rabbitmq.channel

    if channel is None:
        raise RuntimeError("RabbitMQ channel is not initialized")

    await channel.declare_queue(queue_name,durable=True)

    message = aio_pika.Message(
        body=json.dumps(data).encode(),
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
    )

    await channel.default_exchange.publish(
        message,
        routing_key=queue_name
    )