import asyncio
import json

import aio_pika

from app.core.rabbitmq import get_rabbit_connection


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body.decode())

        print(f"Got message: {data}", flush=True)

        if data["event"] == "user_registered":
            print(f"New user: {data['email']}", flush=True)


async def main():
    print("Worker is starting", flush=True)

    connection = await get_rabbit_connection()
    print("Connected in worker", flush=True)

    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        "user_exchange",
        aio_pika.ExchangeType.DIRECT,
        durable=True,
    )

    queue = await channel.declare_queue(
        "user_events",
        durable=True,
    )

    await queue.bind(
        exchange,
        routing_key="user_events",
    )

    await queue.consume(process_message)

    print("Worker started", flush=True)

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())