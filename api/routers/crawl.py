from fastapi import APIRouter, HTTPException

from api.models.url import CrawlerRequest
from core.config.logging import basic_logger
from core.crawler import Crawler

router = APIRouter()
crawler = Crawler()

logger = basic_logger(__name__)


@router.post("/crawl")
async def crawl_urls_handler(request: CrawlerRequest):
    try:
        logger.info(f"Handling crawler for {request.urls}")
        await crawler.crawl(request)
        return {"message": "Crawling initiated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
