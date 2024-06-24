import scrapy
from scrapy import signals
from scrapy.signalmanager import dispatcher
from core.items import TestItem
from core.config import logging_settings as logset

logset.configure_logging(__name__)

class TestSpider(scrapy.Spider):
    name = "TestSpider"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
    ]

    # def __init__(self, start_urls: list[str], *args, **kwargs):
    #     super(TestSpider, self).__init__(*args, **kwargs)
    #     self.start_urls = start_urls


    def parse(self, response):
        for quote in response.css('div.quote'):
            
            item = TestItem()

            item["text"] = quote.css('span.text::text').get()
            item["author"] = quote.css('span small.author::text').get()
            item["tags"] = quote.css('div.tags a.tag::text').getall()

            logset.logger.debug(f"Yielding item: {item}")

            yield item

            dispatcher.send(
                signal=signals.item_scraped, item=item, response=response, spider=self
            )
        
        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
