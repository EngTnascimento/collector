import logging
from typing import ClassVar

from pydantic_settings import BaseSettings


class MainSettings(BaseSettings):
    app_port: int = 8000


class MinioSettings(BaseSettings):
    minio_key: str = "admin"
    minio_secret: str = "SsG7Wh0gAT"
    minio_endpoint: str = "http://localhost:9000"


class LoggingSettings(BaseSettings):
    logger: logging.Logger = logging.getLogger()
    items_logger: logging.Logger = logging.getLogger()

    def configure_logging(self, name: str):
        self.logger = logging.getLogger(f"general: {name}")
        self.items_logger = logging.getLogger(f"items: {name}")

        formatter = logging.Formatter(
            "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
        )

        logger_handler = logging.FileHandler("logs/general.log")
        logger_handler.setLevel(logging.DEBUG)
        logger_handler.setFormatter(formatter)
        logger_console_handler = logging.StreamHandler()
        logger_console_handler.setLevel(logging.DEBUG)

        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logger_handler)
        self.logger.addHandler(logger_console_handler)

        items_handler = logging.FileHandler("logs/items.log")
        items_handler.setLevel(logging.DEBUG)
        items_handler.setFormatter(formatter)
        for handler in self.items_logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                self.items_logger.removeHandler(handler)
        self.items_logger.setLevel(logging.DEBUG)
        self.items_logger.addHandler(items_handler)


class ScrapySettings(BaseSettings):
    BOT_NAME: str = "Company Crawler"
    SPIDER_MODULES: list[str] = ["core.spiders"]
    NEWSPIDER_MODULE: str = "core.spiders"
    CONCURRENT_REQUESTS: int = 16
    DOWNLOAD_DELAY: int = 1
    AUTOTHROTTLE_ENABLED: bool = True
    AUTOTHROTTLE_START_DELAY: int = 5
    AUTOTHROTTLE_MAX_DELAY: int = 60
    AUTOTHROTTLE_TARGET_CONCURRENCY: float = 1.0
    AUTOTHROTTLE_DEBUG: bool = False
    ITEM_PIPELINES: dict = {"core.pipelines.ItemPipeline": 100}
    TWISTED_REACTOR: ClassVar[str] = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'



main_settings = MainSettings()
minio_settings = MinioSettings()
logging_settings = LoggingSettings()
scrapy_settings = ScrapySettings()
