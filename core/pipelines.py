from api.interface.queue import send_item
from core.config.logging import basic_logger

logger = basic_logger(__name__)


class ItemPipeline:
    def process_item(self, item, spider):
        logger.info(f"Enqueuing item for {item['url']}")
        send_item(item)
        return item
