import logging

from fastapi import (
    FastAPI,
    Request,
)
from api import router as api_router
from api.redirect_views import router as redirect_router
from core import config
from app_lifespan import lifespan


logging.basicConfig(
    level=config.LOG_LEVEL,
    format=config.LOG_FORMAT,
)
app = FastAPI(title="URL Shortener", lifespan=lifespan)
app.include_router(redirect_router)
app.include_router(api_router)


@app.get("/")
def read_root(request: Request, name: str = "World"):
    docs_url = request.url.replace(path="/docs", query="")
    return {
        "message": f"Hello {name}",
        "docs": str(docs_url),
    }


# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
