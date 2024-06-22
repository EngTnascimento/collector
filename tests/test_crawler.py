import pytest

from api.models.url import CrawlerRequest
from core.crawler import Crawler


@pytest.mark.asyncio
async def test_crawler():
    crawler = Crawler()
    request = CrawlerRequest(urls=["https://www.emptor.io/"])
    items = await crawler.crawl(request)
    print(f"Items => {items}")
    assert items is not None
