import logging
from scrapy import signals
from scrapy.signalmanager import dispatcher

from core.config import logging_settings as logset

logset.configure_logging(__name__)


class SignalHandler:
    def start(self):
        dispatcher.connect(self.engine_started, signal=signals.engine_started)
        dispatcher.connect(self.engine_stopped, signal=signals.engine_stopped)
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
        dispatcher.connect(self.item_scraped, signal=signals.item_scraped)
        dispatcher.connect(self.item_dropped, signal=signals.item_dropped)
        dispatcher.connect(self.request_scheduled, signal=signals.request_scheduled)
        dispatcher.connect(self.request_dropped, signal=signals.request_dropped)
        dispatcher.connect(self.response_received, signal=signals.response_received)
        dispatcher.connect(self.response_downloaded, signal=signals.response_downloaded)

    def engine_started(self):
        logset.logger.info("Scrapy engine started")

    def engine_stopped(self):
        logset.logger.info("Scrapy engine stopped")

    def spider_opened(self, spider):
        logset.logger.info(f"Spider {spider.name} opened")

    def spider_closed(self, spider, reason):
        logset.logger.info(f"Spider {spider.name} closed: {reason}")

    def item_scraped(self, item, response, spider):
        pass

    def item_dropped(self, item, response, spider, exception):
        logset.logger.warning(f"Item dropped: {item} (exception: {exception})")
        logset.logger.debug(f"Response: {response}")
        logset.logger.debug(f"Spider: {spider.name}")

    def request_scheduled(self, request, spider):
        logset.logger.debug(f"Request scheduled: {request} for spider {spider.name}")

    def request_dropped(self, request, spider):
        logset.logger.warning(f"Request dropped: {request} for spider {spider.name}")

    def response_received(self, response, request, spider):
        logset.logger.debug(
            f"Response received: {response} for request {request} in spider {spider.name}"
        )

    def response_downloaded(self, response, request, spider):
        logset.logger.debug(
            f"Response downloaded: {response} for request {request} in spider {spider.name}"
        )
