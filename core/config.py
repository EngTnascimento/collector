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
    logger: ClassVar[logging.Logger] = logging.getLogger("generalLogger")
    items_logger: ClassVar[logging.Logger] = logging.getLogger("itemsLogger")

    def configure_logging(self):
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

        logger_handler = logging.FileHandler("logs/general.log")
        logger_handler.setLevel(logging.DEBUG)
        logger_handler.setFormatter(formatter)

        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logger_handler)

        items_handler = logging.FileHandler("logs/items.log")
        items_handler.setLevel(logging.DEBUG)
        items_handler.setFormatter(formatter)
        self.items_logger.setLevel(logging.DEBUG)
        self.items_logger.addHandler(items_handler)


class ScrapySettings(BaseSettings):
    BOT_NAME: str = "your_project_name"
    SPIDER_MODULES: list[str] = ["core.spiders"]
    NEWSPIDER_MODULE: str = "core.spiders"
    CONCURRENT_REQUESTS: int = 16
    DOWNLOAD_DELAY: int = 1
    AUTOTHROTTLE_ENABLED: bool = True
    AUTOTHROTTLE_START_DELAY: int = 5
    AUTOTHROTTLE_MAX_DELAY: int = 60
    AUTOTHROTTLE_TARGET_CONCURRENCY: float = 1.0
    AUTOTHROTTLE_DEBUG: bool = False


main_settings = MainSettings()
minio_settings = MinioSettings()
logging_settings = LoggingSettings()
scrapy_settings = ScrapySettings()
