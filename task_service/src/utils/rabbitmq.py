import asyncio

from src.api.v1.services.task import TaskService as service
import aio_pika

async def handle_task_request(channel, method, properties, body):
    user_id = int(body.decode())
    task_count = service.get_tasks_watched_and_executed_count(user_id)
    await channel.default_exchange.publish(
        aio_pika.Message(body=str(task_count).encode()),
        routing_key=properties.reply_to,
        correlation_id=properties.correlation_id
    )
    await method.ack()


async def listen_for_requests():
    connection = await aio_pika.connect_robust("amqp://user:password@localhost/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("task.requests", durable=True)

        await queue.consume(handle_task_request)
        print("Listening for requests on task.requests queue...")
        await asyncio.Future()


@app.on_event("startup")
async def startup():
    asyncio.create_task(listen_for_requests())