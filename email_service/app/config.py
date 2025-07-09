from pydantic import BaseSettings


class Settings(BaseSettings):
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASS: str = "guest"
    NOTIFICATIONS_QUEUE: str = "email.notifications"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
