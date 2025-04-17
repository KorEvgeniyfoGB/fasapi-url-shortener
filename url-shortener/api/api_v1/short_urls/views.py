from typing import Annotated

from fastapi import Depends, APIRouter

from api.api_v1.short_urls.dependencies import prefetch_short_url
from api.api_v1.short_urls.crud import SHORT_URLS
from shemas.shorter_url import ShortUrl

router = APIRouter(
    prefix="/short_urls",
    tags=["Short URLs"],
)


@router.get("/short-urls/", response_model=list[ShortUrl])
def read_short_urls_list():
    return SHORT_URLS


@router.get("/{slug}/", response_model=ShortUrl)
def read_short_url_detail(
    slug: Annotated[
        ShortUrl,
        Depends(prefetch_short_url),
    ],
) -> ShortUrl:
    return slug
