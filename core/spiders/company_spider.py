from urllib.parse import urlparse

import scrapy

from core.items import CompanyItem


class CompanySpider(scrapy.Spider):
    name = "companySpider"

    def __init__(self, urls: list[str], *args, **kwargs):
        print(f"scannig urls => {urls}")
        super(CompanySpider, self).__init__(*args, **kwargs)
        self.start_urls = urls
        self.allowed_domains = [
            self.normalize_domain(urlparse(url).netloc) for url in urls
        ]

    def normalize_domain(self, domain):
        if domain.startswith("www."):
            domain = domain[4:]
        return domain

    def parse(self, response):  # pyright: ignore
        item = CompanyItem()
        item["url"] = response.url
        item["content"] = response.body.decode(response.encoding)
        yield item

        for href in response.css("a::attr(href)").getall():
            url = response.urljoin(href)
            if self.is_allowed_domain(url):
                yield scrapy.Request(url, callback=self.parse)

    def is_allowed_domain(self, url):
        domain = self.normalize_domain(urlparse(url).netloc)
        return domain in self.allowed_domains
