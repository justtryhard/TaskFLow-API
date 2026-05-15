import json

import aio_pika

from app.core.rabbitmq import get_rabbit_connection


async def publish_user_registered(email: str):
    connection = await get_rabbit_connection()

    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            "user_exchange",
            aio_pika.ExchangeType.DIRECT,
            durable=True,
        )

        await channel.declare_queue(
            "user_events",
            durable=True,
            arguments={
                "x-dead-letter-exchange": "user_dlx",
                "x-dead-letter-routing-key": "user_events_failed",
            },
        )

        message = aio_pika.Message(
            body=json.dumps(
                {
                    "event": "user_registered",
                    "email": email,
                }
            ).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

        await exchange.publish(
            message,
            routing_key="user_events",
        )