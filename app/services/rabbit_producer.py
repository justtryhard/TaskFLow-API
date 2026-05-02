import json

import aio_pika

from app.core.rabbitmq import get_rabbit_connection


async def publish_user_registered(email: str):
    connection = await get_rabbit_connection()

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue("user_events", durable=True)

        message = aio_pika.Message(
            body=json.dumps({"event": "user_registered", "email": email}).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await channel.default_exchange.publish(
            message,
            routing_key=queue.name,
        )