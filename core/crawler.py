from scrapy.crawler import CrawlerProcess, CrawlerRunner, Deferred
from scrapy.utils.defer import deferred_to_future
from twisted.internet.asyncioreactor import install as install_asyncio_reactor
from twisted.internet import reactor, defer
from api.models.url import CrawlerRequest
from core.config import logging_settings as logset
from core.config import scrapy_settings
from core.handler import SignalHandler
from core.spiders.company_spider import CompanySpider
from core.spiders.simple_spider import TestSpider
from scrapy.utils.reactor import is_asyncio_reactor_installed
from fastapi import HTTPException
from scrapy.utils.reactor import install_reactor
import threading
import asyncio


logset.configure_logging(__name__)


class Crawler:
    def __init__(self):
        self.signal_handler = SignalHandler()
        self.process = CrawlerProcess(settings=scrapy_settings.model_dump())
        self.items = []
        self.is_reactor_running = False
        self.lock = threading.Lock()
        self.signal_handler.start()


    async def __crawl(self, urls: list[str]):
        try:
            logset.logger.info(f"Starting crawl with URLs: {urls}")
            if not self.is_reactor_running:
                reactor_thread = threading.Thread(target=reactor.run, kwargs={'installSignalHandlers': False})
                reactor_thread.start()
                self.is_reactor_running = True

            def __crawl_spider():
                deferred = self.process.crawl(CompanySpider, start_urls=urls)
                deferred.addBoth(lambda _: reactor.callFromThread(reactor.stop))

            with self.lock:
                reactor.callFromThread(__crawl_spider)

            logset.logger.info("Crawl finished successfully.")

        except Exception as e:
            logset.logger.error(f"Error during crawl: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))

    async def crawl(self, request: CrawlerRequest):
        logset.logger.info(f"Handling crawler for {request.urls}")
        try:
            await self.__crawl(request.urls)
            return []
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
