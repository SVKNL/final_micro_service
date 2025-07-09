import aio_pika
from app.config import Settings


class RabbitMQClient:
    def __init__(self):
        self.settings = Settings()
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            host=self.settings.RABBITMQ_HOST,
            port=self.settings.RABBITMQ_PORT,
            login=self.settings.RABBITMQ_USER,
            password=self.settings.RABBITMQ_PASS
        )
        self.channel = await self.connection.channel()

    async def consume(self, queue_name, callback):
        queue = await self.channel.declare_queue(queue_name)
        await queue.consume(callback)


import aio_pika
from config import Settings


class RabbitMQClient:
    def __init__(self):
        self.settings = Settings()
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(
            host=self.settings.RABBITMQ_HOST,
            port=self.settings.RABBITMQ_PORT,
            login=self.settings.RABBITMQ_USER,
            password=self.settings.RABBITMQ_PASS
        )
        self.channel = await self.connection.channel()

    async def consume(self, queue_name, callback):
        queue = await self.channel.declare_queue(queue_name)
        await queue.consume(callback)
