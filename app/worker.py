import asyncio
import json

import aio_pika

from app.core.rabbitmq import get_rabbit_connection


async def process_message(message: aio_pika.IncomingMessage):
    try:
        data = json.loads(message.body.decode())

        print(f"Got message: {data}", flush=True)

        if data["event"] == "user_registered":
            print(f"New user: {data['email']}", flush=True)

        await message.ack()

    except Exception as e:
        print(f"Message processing failed: {e}", flush=True)
        await message.reject(requeue=False)


async def main():
    print("Worker is starting", flush=True)

    connection = await get_rabbit_connection()
    print("Connected in worker", flush=True)

    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    exchange = await channel.declare_exchange(
        "user_exchange",
        aio_pika.ExchangeType.DIRECT,
        durable=True,
    )

    dlx = await channel.declare_exchange(
        "user_dlx",
        aio_pika.ExchangeType.DIRECT,
        durable=True,
    )

    queue = await channel.declare_queue(
        "user_events",
        durable=True,
        arguments={
            "x-dead-letter-exchange": "user_dlx",
            "x-dead-letter-routing-key": "user_events_failed",
        },
    )

    failed_queue = await channel.declare_queue(
        "user_events_failed",
        durable=True,
    )

    await queue.bind(exchange, routing_key="user_events")
    await failed_queue.bind(dlx, routing_key="user_events_failed")

    await queue.consume(process_message, no_ack=False)

    print("Worker started", flush=True)

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())