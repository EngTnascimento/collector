from urllib.parse import urlparse

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from core.config import logging_settings as logset
from core.items import CompanyItem

logset.configure_logging(__name__)


class CompanySpider(scrapy.Spider):
    name = "companySpider"

    def __init__(self, start_urls: list[str], *args, **kwargs):
        super(CompanySpider, self).__init__(*args, **kwargs)

        self.start_urls = start_urls
        self.allowed_domains = [
            self.normalize_domain(urlparse(url).netloc) for url in start_urls
        ]
        self.rules = (
            Rule(
                LinkExtractor(allow=(), restrict_css="a"), callback="parse", follow=True
            ),
        )
        logset.logger.debug(f"Allowed Domains: {self.allowed_domains}")
        self.visited_urls: set = set()

    def normalize_domain(self, domain):
        if domain.startswith("www."):
            domain = domain[4:]
        return domain

    def parse(self, response):  # pyright: ignore
        item = CompanyItem()
        item["url"] = response.url
        parsed_url = urlparse(response.url)
        self.root_domain = self.normalize_domain(parsed_url.netloc)
        item["root_domain"] = self.root_domain
        item["full_content"] = response.text
        item["text_content"] = response.css("*::text").getall()

        yield item

        for href in response.css("a::attr(href)").getall():
            url = response.urljoin(href)
            visited = url in self.visited_urls
            if self.is_allowed_domain(url) and not visited:
                self.visited_urls.add(url)
                yield scrapy.Request(url, callback=self.parse)

    def is_allowed_domain(self, url):
        domain = self.normalize_domain(urlparse(url).netloc)
        return domain in self.allowed_domains
