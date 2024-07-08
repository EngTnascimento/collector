import pandas as pd
import pytest

from collector import Collector


def test_crawl():
    websites = [
        "https://www.cactus.se/",
        "https://www.asset-intertech.com/",
        "https://www.geomatic.dk/",
    ]

    collector = Collector(websites, concurrent=True, max_workers=5)
    collector.crawl()

    df = pd.read_parquet("websites_data.parquet", engine="fastparquet")

    print(df)


if __name__ == "__main__":
    pytest.main()
