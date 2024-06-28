from fastapi import FastAPI

from api.routers import crawl
from core.config import main_settings

app = FastAPI()


app.include_router(crawl.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=main_settings.app_port)
