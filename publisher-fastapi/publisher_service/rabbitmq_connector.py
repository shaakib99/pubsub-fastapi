from aio_pika import connect
import os

class RabbitMQConnector:
    instance = None
    def __init__(self):
        self.connection = None
        self.channel = None

    async def connect(self):
        host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.connection = await connect(host=host)
        if not self.connection.connected:
            raise Exception(f"RabbitMQ is not connected to {host}")
        self.channel = await self.connection.channel()


    
    async def disconnect(self):
        await self.channel.close()
        await self.connection.close()
    
    @staticmethod
    def get_instance() -> "RabbitMQConnector":
        if RabbitMQConnector.instance is None:
            RabbitMQConnector.instance = RabbitMQConnector()
        return RabbitMQConnector.instance