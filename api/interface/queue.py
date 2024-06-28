import os

from queue_interface.queue_setup import RabbitMQConfig
from queue_interface.rabbitMQ import RabbitMQ

from api.models.items import TextContentMessage
from core.items import CompanyItem


def send_item(item: CompanyItem):
    host = os.getenv("RMQ_HOST", "127.0.0.1")
    text_queue = RabbitMQ(
        consumer=False,
        queue="text_item",
        MessageModel=TextContentMessage,
        config=RabbitMQConfig(host=host),
    )
    message = TextContentMessage(
        url=item["url"], content=item["text_content"], root_domain=item["root_domain"]
    )
    text_queue.send(message)
