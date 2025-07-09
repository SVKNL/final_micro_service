import logging
from fastapi import FastAPI
from models.email_event import EmailEvent
from utils.rabbitmq import RabbitMQClient

app = FastAPI()
logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.rabbit = RabbitMQClient()

    async def start_consumer(self):
        await self.rabbit.connect()
        await self.rabbit.consume(
            queue_name="email.notifications",
            callback=self.handle_email_event
        )

    async def handle_email_event(self, message):
        try:
            event = EmailEvent(**message.body)
            await self.send_email(event)
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    async def send_email(self, event: EmailEvent):
        # Здесь можно добавить реальную отправку писем
        # Для примера просто логируем
        logger.info(f"Sending email to {event.email}: {event.template}")


import logging
from fastapi import FastAPI
from models.email_event import EmailEvent
from utils.rabbitmq import RabbitMQClient

app = FastAPI()
logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.rabbit = RabbitMQClient()

    async def start_consumer(self):
        await self.rabbit.connect()
        await self.rabbit.consume(
            queue_name="email.notifications",
            callback=self.handle_email_event
        )

    async def handle_email_event(self, message):
        try:
            event = EmailEvent(**message.body)
            await self.send_email(event)
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    async def send_email(self, event: EmailEvent):
        # email sending immitation
        logger.info(f"Sending email to {event.email}: {event.template}")
