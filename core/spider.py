import scrapy

class MySpider(scrapy.Spider):
    name = 'myspider'

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls', [])

    def parse(self, response):
        for text in response.css('*::text').getall():
            yield {'text': text.strip()}

        for next_page in response.css('a::attr(href)').getall():
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
