from core.config import logging_settings as logset

logset.configure_logging(__name__)


class ItemPipeline:
    def process_item(self, item, spider):
        logset.items_logger.debug(f"Item scraped:\n{item['text_content']}")
        return item
