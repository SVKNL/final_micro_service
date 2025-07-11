import json
import uuid

import aio_pika


async def get_task_count_from_task_service(user_id: int) -> int:
    connection = await aio_pika.connect_robust("amqp://user:password@rabbitmq/")
    async with connection:
        channel = await connection.channel()

        result_queue = await channel.declare_queue("", exclusive=True)

        correlation_id = str(uuid.uuid4())
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=str(user_id).encode(),
                reply_to=result_queue.name,
                correlation_id=correlation_id
            ),
            routing_key="task.requests"
        )

        async for message in result_queue:
            if message.correlation_id == correlation_id:
                data = json.loads(message.body.decode())  # ← правильный способ
                await message.ack()
                if data is None:
                    data = {'watcher_count': 0}
                return data

async def publish_user_registered_event(username: str, email: str):
    connection = await aio_pika.connect_robust("amqp://user:password@rabbitmq/")
    channel = await connection.channel()
    message_body = {
        "username": username,
        "email": email,
    }
    message = aio_pika.Message(
        body=json.dumps(message_body).encode()
    )
    await channel.default_exchange.publish(
        message, routing_key="email.notifications"
    )
    await connection.close()
