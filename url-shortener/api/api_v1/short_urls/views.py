from typing import Annotated

from annotated_types import Len

from fastapi import (
    Depends,
    APIRouter,
    Form,
)
from starlette import status
from pydantic import AnyHttpUrl

from api.api_v1.short_urls.dependencies import prefetch_short_url
from api.api_v1.short_urls.crud import storage
from shemas.shorter_url import ShortUrl, ShortUrlCreate

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
)


@router.get("/", response_model=list[ShortUrl])
def read_short_urls_list():
    return storage.get()


@router.post(
    "/",
    response_model=ShortUrl,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(short_url_create: ShortUrlCreate):
    return storage.create(short_url_in=short_url_create)


@router.get("/{slug}/", response_model=ShortUrl)
def read_short_url_detail(
    slug: Annotated[
        ShortUrl,
        Depends(prefetch_short_url),
    ],
) -> ShortUrl:
    return slug


@router.delete(
    "/{slug}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Short URL not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "URL slug not found",
                    },
                },
            },
        },
    },
)
def delete_short_url(
    url: Annotated[
        ShortUrl,
        Depends(prefetch_short_url),
    ],
) -> None:
    storage.delete(short_url=url)
