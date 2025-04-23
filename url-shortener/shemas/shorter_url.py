from typing import Annotated

from annotated_types import Len, MaxLen
from pydantic import BaseModel, AnyHttpUrl

DescriptionString = Annotated[
    str,
    MaxLen(200),
]


class ShortUrlBase(BaseModel):
    target_url: AnyHttpUrl
    description: DescriptionString = ""


class ShortUrlCreate(ShortUrlBase):
    """
    Модель для создания короткой ссылки
    """

    slug: Annotated[
        str,
        Len(min_length=3, max_length=10),
    ]


class ShortUrlUpdate(ShortUrlBase):
    """
    Модель для обновления короткой ссылки
    """

    description: DescriptionString


class ShortUrlUpdatePartial(ShortUrlBase):
    """
    Модель для частичного обновления короткой ссылки
    """

    target_url: AnyHttpUrl | None = None
    description: DescriptionString | None = None


class ShortUrlOutput(ShortUrlBase):
    slug: str


class ShortUrl(ShortUrlBase):
    """
    Модель сокращенной ссылки
    """

    slug: str
    visits: int = 42
