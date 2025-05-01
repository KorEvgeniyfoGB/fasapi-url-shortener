from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
)
from starlette import status

from api.api_v1.short_urls.crud import storage
from api.api_v1.short_urls.dependencies import save_storage_state, api_token_required
from shemas.shorter_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlOutput,
)

router = APIRouter(
    prefix="/short-urls",
    tags=["Short URLs"],
    dependencies=[Depends(save_storage_state), Depends(api_token_required)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthenticated. Only for unsafe methods.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token",
                    },
                },
            },
        },
    },
)


@router.get("/", response_model=list[ShortUrlOutput])
def read_short_urls_list():
    return storage.get()


@router.post(
    "/",
    response_model=ShortUrlOutput,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    short_url_create: ShortUrlCreate,
):
    return storage.create(short_url_in=short_url_create)
