from pydantic import BaseModel

class UrlList(BaseModel):
    urls: list[str]