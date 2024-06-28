import scrapy
from scrapy import signals
from scrapy.signalmanager import dispatcher

from core.config.logging import basic_logger
from core.items import TestItem

logger = basic_logger(__name__)


class TestSpider(scrapy.Spider):
    name = "TestSpider"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
    ]

    def parse(self, response):  # pyright: ignore
        for quote in response.css("div.quote"):
            item = TestItem()

            item["text"] = quote.css("span.text::text").get()
            item["author"] = quote.css("span small.author::text").get()
            item["tags"] = quote.css("div.tags a.tag::text").getall()

            logger.debug(f"Yielding item: {item}")

            yield item

            dispatcher.send(
                signal=signals.item_scraped, item=item, response=response, spider=self
            )
