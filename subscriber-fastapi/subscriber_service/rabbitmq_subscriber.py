from subscriber_service.lib.subscriber_abc import SubscriberABC
from subscriber_service.rabbitmq_connector import RabbitMQConnector
from aio_pika import Message, IncomingMessage
from typing import Callable
import json

class RabbitMQSubscriber(SubscriberABC):
    def __init__(self, queue_name: str, callback: Callable):
        self.queue_name = queue_name
        self.rmq_connector = RabbitMQConnector.get_instance()
        self.queue_callback = callback
    
    async def connect(self):
        await self.rmq_connector.connect()
        self.connection = self.rmq_connector.connection
        self.channel = self.rmq_connector.channel
        self.queue = await self.channel.declare_queue(self.queue_name)
    
    async def callback(self, message: IncomingMessage):
        async with message.process():
            data = json.loads(message.body.decode('utf-8'))
            res = await self.queue_callback(data)
            print(f"Recieved data [x]: {data} ")
            if message.reply_to:
                await self.channel.declare_queue(message.reply_to)
            await self.publish(res, message)

    async def subscribe(self):
        await self.queue.cancel(self.queue_name)
        await self.queue.consume(self.callback, consumer_tag=self.queue_name)

    async def stop_subscirbing(self):
        await self.queue.cancel(self.queue_name)
    
    async def publish(self, message: dict, extra_data: IncomingMessage):
        response = Message(
            body=json.dumps(message).encode(),
            correlation_id=extra_data.correlation_id
        )
        await self.channel.default_exchange.publish(response, routing_key=extra_data.reply_to)

    