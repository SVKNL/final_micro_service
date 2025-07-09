import asyncio
import json

from aio_pika import connect_robust, IncomingMessage, Message
from src.api.v1.services.task import TasksService
from src.utils.unit_of_work import UnitOfWork


async def handle_task_request(message: IncomingMessage, default_exchange):
    async with message.process():
        user_id = int(message.body.decode())
        service = TasksService(unit_of_work=UnitOfWork())
        task_count = await service.get_tasks_watched_and_executed_count(user_id)
        if task_count is None:
            task_count = {'watcher_count': 100}
        await default_exchange.publish(

                Message(
                    body=json.dumps(task_count).encode(),
                    correlation_id=message.correlation_id,
                    reply_to=message.reply_to
                ),
                routing_key=message.reply_to,
            )


async def listen_for_requests():
    while True:
        try:
            connection = await connect_robust("amqp://user:password@rabbitmq/")
            break
        except Exception:
            print("RabbitMQ not ready, retrying in 3 seconds...")
            await asyncio.sleep(3)

    async with connection:
        channel = await connection.channel()
        default_exchange = channel.default_exchange

        queue = await channel.declare_queue("task.requests", durable=True)

        async def on_message(message: IncomingMessage):
            await handle_task_request(message, default_exchange)  # <- передаём exchange сюда

        await queue.consume(on_message)
        print("Listening for requests on task.requests queue...")
        await asyncio.Future()  # бесконечное ожидание
