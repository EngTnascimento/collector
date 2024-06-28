import scrapy


class CompanyItem(scrapy.Item):
    url = scrapy.Field()
    root_domain = scrapy.Field()
    full_content = scrapy.Field()
    text_content = scrapy.Field()


class TestItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
