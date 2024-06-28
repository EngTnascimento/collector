from queue_interface.rabbitMQ import RabbitMQ

from api.models.items import TextContentMessage
from core.items import CompanyItem


def send_item(item: CompanyItem):
    text_queue = RabbitMQ(queue="text_item", MessageModel=TextContentMessage)
    message = TextContentMessage(
        url=item["url"], content=item["text_content"], root_domain=item["root_domain"]
    )
    text_queue.send(message)
