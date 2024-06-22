import scrapy


class CompanyItem(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    # Add more fields as needed
