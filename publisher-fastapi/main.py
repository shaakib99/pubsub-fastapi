from fastapi import FastAPI
from publisher_service.rabbitmq_connector import RabbitMQConnector
from publisher_service.lib.decorators import publish

async def lifespan(app):
    rmq_connector = RabbitMQConnector()
    await rmq_connector.connect()
    yield
    await rmq_connector.disconnect()


app = FastAPI(lifespan=lifespan)

@app.get('/')
@publish('test_queue', 'test_queue')
async def hello():
    return {'test': 'test'}
