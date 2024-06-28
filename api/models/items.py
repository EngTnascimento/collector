from pydantic import BaseModel


class FullContentMessage(BaseModel):
    url: str
    root_domain: str
    content: list[str]


class TextContentMessage(BaseModel):
    url: str
    root_domain: str
    content: list[str]
