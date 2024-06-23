import pytest

from api.models.url import CrawlerRequest
from core.crawler import Crawler


@pytest.mark.asyncio
async def test_crawler():
    crawler = Crawler()
    request = CrawlerRequest(urls=["https://www.emptor.io/"])

    # Create an async generator to receive items incrementally
    async def receive_items():
        async for item in await crawler.crawl(request):  # pyright: ignore
            print(f"item => {item}")
            yield item

    # Initialize the async generator
    items_generator = receive_items()

    # Asynchronously iterate and collect items
    received_items = []
    async for item in items_generator:
        received_items.append(item)
        print(f"Received item: {item}")

        # Perform assertions on each received item (if needed)
        assert "text" in item  # Example assertion

    # Final assertion on the collected items
    assert len(received_items) > 0  # Ensure at least one item was received
