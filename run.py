from fastapi import FastAPI
from core.config import settings
from api.routers import crawl

app = FastAPI()

# Include routers
app.include_router(crawl.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.app_port)
