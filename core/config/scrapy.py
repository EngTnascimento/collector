from typing import ClassVar

from pydantic_settings import BaseSettings


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
    TWISTED_REACTOR: ClassVar[str] = (
        "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
    )
