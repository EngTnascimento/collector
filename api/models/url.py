from pydantic import BaseModel


class CrawlerRequest(BaseModel):
    urls: list[str]
