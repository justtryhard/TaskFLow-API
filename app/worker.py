import asyncio
import json

import aio_pika

from app.core.rabbitmq import get_rabbit_connection


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body.decode())

        print(f"📩 Получено сообщение: {data}")

        if data["event"] == "user_registered":
            print(f"👤 Новый пользователь: {data['email']}")


async def main():
    connection = await get_rabbit_connection()

    channel = await connection.channel()
    queue = await channel.declare_queue("user_events", durable=True)

    await queue.consume(process_message)

    print("🚀 Worker запущен")
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())