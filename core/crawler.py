import asyncio

from scrapy import signals
from scrapy.crawler import CrawlerRunner, Deferred
from scrapy.signalmanager import dispatcher
from scrapy.utils.reactor import asyncioreactor
from twisted.internet import reactor

from api.models.url import CrawlerRequest
from core.config import logging_settings, scrapy_settings
from core.spiders.company_spider import CompanySpider

logging_settings.configure_logging()

try:
    asyncioreactor.install()
except Exception as e:
    if "reactor already installed" not in str(e):
        raise


class Crawler:
    def __init__(self):
        self.runner = CrawlerRunner(scrapy_settings.model_dump())
        self.items = []
        dispatcher.connect(self.__item_scraped, signal=signals.item_scraped)

    def __item_scraped(self, item, response, spider):
        logging_settings.items_logger.info(f"Item scraped: {item}")
        logging_settings.logger.info(f"Item scraped: {item}")
        logging_settings.items_logger.debug(f"Respose: {response}")
        logging_settings.items_logger.debug(f"Spider: {spider}")
        # self.items.append(item)

    def __crawl(self, urls: list[str]):
        try:
            logging_settings.logger.info(f"Starting crawl with URLs: {urls}")
            d: Deferred = self.runner.crawl(CompanySpider, start_urls=urls)
            d.addBoth(lambda _: reactor.stop())  # pyright: ignore
            reactor.run()  # pyright: ignore
            logging_settings.logger.info("Crawl finished successfully.")
            return d
        except Exception as e:
            logging_settings.logger.error(f"Error during crawl: {e}", exc_info=True)
            raise

    async def crawl(self, request: CrawlerRequest):
        logging_settings.logger.info(f"Handling crawler for {request.urls}")
        await self.__crawl(request.urls)
        return []
