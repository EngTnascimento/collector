import pytest
import requests

from api.models.url import CrawlerRequest
from run import app


def test_scrape_endpoint():
    url = "http://localhost:8000/crawl"

    # https://www.emptor.io/
    
    payload = CrawlerRequest(urls=["http://quotes.toscrape.com/page/1/"])
    response = requests.post(url, json=payload.model_dump())
    # assert response.status_code == 200
    # assert "data" in response.json()

    print(f"Response => {response.json()}")

    # assert response_empty.status_code == 400
    # assert response_empty.json()["detail"] == "No URLs provided"

    # Additional test cases can be added as needed


if __name__ == "__main__":
    pytest.main()
