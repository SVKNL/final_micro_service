import asyncio
from fastapi import FastAPI
from rabbitmq_consumer import start_consumer

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_consumer())

@app.get("/")
def root():
    return {"status": "email-service is running"}
