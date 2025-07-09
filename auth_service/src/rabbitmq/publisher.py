from aio_pika import Message, ExchangeType


async def publish_registration_event(user_id: str, email: str):
    connection = await connect_to_rabbitmq()
    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        EXCHANGE_NAME,
        ExchangeType.DIRECT
    )

    message = Message(
        body=json.dumps({
            "type": "user_registered",
            "data": {
                "user_id": user_id,
                "email": email
            }
        }).encode()
    )

    await exchange.publish(message, routing_key=EMAIL_QUEUE)


