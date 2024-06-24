from fastapi import APIRouter, HTTPException

from api.models.url import CrawlerRequest
from core.crawler import Crawler

router = APIRouter()
crawler = Crawler()

@router.post("/crawl")
async def crawl_urls_handler(request: CrawlerRequest):
    try:
        print(f"Handling crawler for {request.urls}")
        
        items = await crawler.crawl(request)
        return {"message": "Crawling initiated successfully", "items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
