from fastapi import FastAPI
from subscriber_service.rabbitmq_connector import RabbitMQConnector
from subscriber_service.lib.decorators import consume, queue_func_mapper
import asyncio

@consume('test_queue')
async def hello(data: dict):
    return {'message': 'hello'}

async def lifespan(app):
    rmq_connector_init = RabbitMQConnector()
    await rmq_connector_init.connect()

    for rmq_connector in queue_func_mapper:
        await rmq_connector.connect()
        await rmq_connector.subscribe()
    yield
    await rmq_connector_init.disconnect()

app = FastAPI(lifespan=lifespan)


