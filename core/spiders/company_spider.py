import scrapy

from core.


class CompanySpider(scrapy.Spider):
    name = "companySpider"

    def __init__(self, domain=None, *args, **kwargs):
        super(CompanySpider, self).__init__(*args, **kwargs)
        self.allowed_domains = [domain]
        self.start_urls = [f"http://{domain}"]

    def parse(self, response):  # pyright: ignore
        # Extract specific data of interest
        for data in response.css("article, div.content, .product"):
            item = {}
            item["title"] = data.css("h1::text").get()
            item["description"] = data.css(".description::text").get()
            item["image_url"] = data.css("img::attr(src)").get()
            item["link"] = data.css("a::attr(href)").get()
            yield item

        for href in response.css("a::attr(href)").getall():
            url = response.urljoin(href)

            yield scrapy.Request(url, callback=self.parse)
