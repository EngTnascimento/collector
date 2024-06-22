import asyncio
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from scrapy import signals
from api.models.url import UrlList

class Crawler:
    def __init__(self):
        self.process = CrawlerProcess(get_project_settings())
        self.items = []
        dispatcher.connect(self._item_scraped, signal=signals.item_scraped)

    def _item_scraped(self, item, response, spider):
        self.items.append(item)

    async def crawl(self, urls: UrlList):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._crawl, urls)
        return self.items


