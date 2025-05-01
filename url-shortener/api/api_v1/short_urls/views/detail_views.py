from typing import Annotated

from fastapi import Depends, APIRouter, BackgroundTasks
from starlette import status

from api.api_v1.short_urls.crud import storage
from api.api_v1.short_urls.dependencies import prefetch_short_url
from shemas.shorter_url import (
    ShortUrl,
    ShortUrlUpdate,
    ShortUrlUpdatePartial,
    ShortUrlOutput,
)


router = APIRouter(
    prefix="/{slug}",
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

ShortUrlBySlug = Annotated[
    ShortUrl,
    Depends(prefetch_short_url),
]


@router.get("/", response_model=ShortUrlOutput)
def read_short_url_detail(slug: ShortUrlBySlug) -> ShortUrl:
    return slug


@router.put(
    "/",
    response_model=ShortUrlOutput,
)
def update_short_url_details(
    url: ShortUrlBySlug,
    short_url_in: ShortUrlUpdate,
) -> ShortUrl:
    return storage.update(
        short_url=url,
        short_url_in=short_url_in,
    )


@router.patch(
    "/",
    response_model=ShortUrlOutput,
)
def update_short_url_details_partial(
    url: ShortUrlBySlug,
    short_url_in: ShortUrlUpdatePartial,
) -> ShortUrl:
    return storage.update_partial(
        short_url=url,
        short_url_in=short_url_in,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_short_url(
    url: ShortUrlBySlug,
) -> None:
    storage.delete(short_url=url)
