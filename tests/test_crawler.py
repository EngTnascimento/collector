import pytest
import requests

from api.models.url import CrawlerRequest


def test_scrape_endpoint():
    endpoint = "http://localhost:8001/crawl"

    # https://www.emptor.io/

    payload = CrawlerRequest(urls=["http://quotes.toscrape.com/page/1/"])
    response = requests.post(endpoint, json=payload.model_dump())

    print(f"Response => {response.json()}")


if __name__ == "__main__":
    pytest.main()
