import json 
import aio_pika
from core.rabbitmq import channel

async def publish_message(queue_name:str,data:dict):
    await channel.declare_queue(queue_name,durable=True)

    message = aio_pika.Message(
        body=json.dumps(data).encode(),
        delivery_mode=aio_pika.DeliveryMode.PERISTENT,
    )

    await channel.declare_exchange.publish(
        message,routing_key=queue_name
    )