import aio_pika
import json
import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")

async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body.decode())
        print(f"[email-service] Отправка письма на {data['email']}... 🎉")
        print(f"Привет, {data['username']}! Спасибо за регистрацию.\n")

async def start_consumer():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("email.notifications", durable=True)
    await queue.consume(on_message)
    print("[email-service] Слушаем email.notifications...")
    await connection.ready()
    await queue.consume(on_message)
    await aio_pika.connect_robust(RABBITMQ_URL)
