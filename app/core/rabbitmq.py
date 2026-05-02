import asyncio

import aio_pika

from app.core.config import settings


async def get_rabbit_connection():
    retries = 10

    for i in range(retries):
        try:
            connection = await aio_pika.connect_robust(
                f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/"
            )
            print("Connected to RabbitMQ")
            return connection

        except Exception as e:
            print(f"RabbitMQ not ready, retry {i+1}/{retries}")
            await asyncio.sleep(2)

    raise Exception("Failed to connect to RabbitMQ")