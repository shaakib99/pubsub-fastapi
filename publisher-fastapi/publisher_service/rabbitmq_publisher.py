from publisher_service.lib.publisher_abc import PublisherABC
from publisher_service.rabbitmq_connector import RabbitMQConnector
from aio_pika import Message, IncomingMessage
import json
import asyncio
import uuid

class RabbitMQPublisher(PublisherABC):
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.response_queue_name = queue_name + '_response'
        self.rmq_connector = RabbitMQConnector.get_instance()
        self.response = None
        self.response_event = asyncio.Event()
    
    async def connect(self):
        await self.rmq_connector.connect()
        self.connection = self.rmq_connector.connection
        self.channel = self.rmq_connector.channel
        self.queue = await self.channel.declare_queue(self.queue_name)
        self.response_queue = await self.channel.declare_queue(self.response_queue_name)


    async def callback(self, message: IncomingMessage):
        async with message.process():
            if message.correlation_id == self.correlation_id:
                data = message.body.decode('utf-8')
                self.response = json.loads(data)
                await self.stop_subscirbing()
                self.response_event.set()

    async def subscribe(self):
        await self.response_queue.cancel(self.response_queue_name)
        await self.response_queue.consume(callback=self.callback, consumer_tag=self.response_queue_name)

    
    async def stop_subscirbing(self):
        await self.queue.cancel(self.queue_name)

    async def publish(self, message: dict) -> dict:
        self.correlation_id = uuid.uuid4().__str__()
        publish_message = Message(
            body=json.dumps(message).encode(),
            correlation_id=self.correlation_id,
            reply_to=self.response_queue
        )
        self.response = None
        self.response_event.clear()
        await self.channel.default_exchange.publish(publish_message, routing_key=self.queue_name)
        await self.subscribe()

        await self.response_event.wait()
  
        return self.response