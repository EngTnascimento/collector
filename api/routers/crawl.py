from fastapi import APIRouter, HTTPException
from core.crawler import Crawler
from api.models.url import UrlList

router = APIRouter()

@router.post("/crawl/")
async def crawl_urls_handler(urls: UrlList):
    try:
        crawler = Crawler()
        job_id = await crawler.crawl(urls.urls)
        return {"message": "Crawling initiated successfully", "job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
