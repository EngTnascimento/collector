import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse

import aiohttp
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Collector:
    def __init__(
        self,
        websites: list[str],
        file_path: str,
        max_urls=200,
        concurrent=False,
        pause=False,
        timeout=10,
        max_workers=10,
    ) -> None:
        self.websites = websites
        self.max_urls = max_urls
        self.concurrent = concurrent
        self.pause = pause
        self.ua = UserAgent()
        self.timeout = timeout
        self.max_workers = max_workers
        self.file_path = file_path

    async def fetch(self, session, url):
        headers = {
            "User-Agent": self.ua.random,
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
        }
        try:
            async with session.get(
                url, headers=headers, timeout=self.timeout
            ) as response:
                if (
                    response.status == 200
                    and "text/html" in response.headers["Content-Type"]
                ):
                    return await response.text()
                else:
                    logging.warning(
                        f"Skipped non-HTML content or bad status at URL: {url}"
                    )
                    return None
        except asyncio.TimeoutError:
            logging.warning(f"Timeout occurred for URL: {url}. Skipping.")
        except aiohttp.ClientError as e:
            logging.error(f"Request failed for {url}: {e}")
        return None

    async def extract_text(self, session, url, visited_urls, url_count, domain_text):
        logging.info(f"Processing URL: {url}")
        visited_urls.add(url)
        url_count[urlparse(url).netloc] += 1

        html = await self.fetch(session, url)
        if html is None:
            return

        soup = BeautifulSoup(html, "html.parser")

        for script_or_style in soup(["script", "style", "span"]):
            script_or_style.decompose()

        text = soup.get_text(separator=" ", strip=True)
        logging.debug(f"Extracted text: {text[:500]}")
        domain_text[urlparse(url).netloc].append(text)

        if self.concurrent:
            await self.follow_links_concurrently(
                session, url, visited_urls, url_count, domain_text, soup
            )
        else:
            await self.follow_links(
                session, url, visited_urls, url_count, domain_text, soup
            )

    def should_process_url(self, url) -> bool:
        excluded_patterns = [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".zip", ".tar.gz"]
        return not any(pattern in url for pattern in excluded_patterns)

    async def follow_links_concurrently(
        self, session, url, visited_urls, url_count, domain_text, soup
    ):
        links = soup.find_all("a", href=True)
        tasks = []
        for link in links:
            href = link["href"]
            full_url = urljoin(url, href)
            if (
                self.should_process_url(full_url)
                and urlparse(full_url).netloc == urlparse(url).netloc
            ):
                if (
                    full_url not in visited_urls
                    and url_count[urlparse(url).netloc] < self.max_urls
                ):
                    logging.info(f"Following link: {full_url}")
                    tasks.append(
                        self.extract_text(
                            session, full_url, visited_urls, url_count, domain_text
                        )
                    )

        await asyncio.gather(*tasks)

    async def follow_links(
        self, session, url, visited_urls, url_count, domain_text, soup
    ):
        links = soup.find_all("a", href=True)
        for link in links:
            href = link["href"]
            full_url = urljoin(url, href)
            if (
                urlparse(full_url).netloc == urlparse(url).netloc
                and url_count[urlparse(url).netloc] < self.max_urls
            ):
                if full_url not in visited_urls:
                    logging.info(f"Following link: {full_url}")
                    await self.extract_text(
                        session, full_url, visited_urls, url_count, domain_text
                    )

    async def save_to_parquet(self, data):
        df = pd.DataFrame(data)
        df.columns = ["domain", "text"]
        df.to_parquet(self.file_path, index=False)
        logging.info("Data saved to websites_data.parquet")

    async def crawl_website(
        self, url, visited_urls, url_count, domain_text
    ) -> dict[str, str]:
        current_domain = urlparse(url).netloc
        domain_text[current_domain] = []
        url_count[current_domain] = 0

        logging.info(f"Starting extraction for website: {url}")

        async with aiohttp.ClientSession() as session:
            await self.extract_text(session, url, visited_urls, url_count, domain_text)

        # Return the extracted text
        text = " ".join(domain_text[current_domain])
        return {"domain": current_domain, "text": text}

    def crawl(self):
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(executor, self.crawl_website_thread, url)
                for url in self.websites
            ]
            results = loop.run_until_complete(asyncio.gather(*tasks))

        for result in results:
            for key, value in result.items():
                if key == "domain":
                    print(f"results: {value}")

        loop.run_until_complete(self.save_to_parquet(results))

    def crawl_website_thread(self, url) -> dict[str, str]:
        visited_urls = set()
        url_count = {}
        domain_text = {}
        return asyncio.run(
            self.crawl_website(url, visited_urls, url_count, domain_text)
        )

    def pause_here(self):
        if self.pause:
            _ = input("Press Enter to continue: ")
