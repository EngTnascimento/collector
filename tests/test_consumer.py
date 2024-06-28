import pytest
from queue_interface.rabbitMQ import RabbitMQ

from api.models.items import TextContentMessage


def process_message(message):
    print(f"Processing message {message}")


def test_text_content_consumer():
    text_queue = RabbitMQ(
        consumer=True, queue="text_item", MessageModel=TextContentMessage
    )

    text_queue.consume(process_message)

    text_queue.close()


if __name__ == "__main__":
    pytest.main()
