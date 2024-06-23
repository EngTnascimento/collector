import scrapy


class CompanyItem(scrapy.Item):
    url = scrapy.Field()
    content = scrapy.Field()
