from pydantic import (
    BaseModel,
    ValidationError,
)

from shemas.shorter_url import (
    ShortUrl,
    ShortUrlCreate,
    ShortUrlUpdate,
    ShortUrlUpdatePartial,
)

from core.config import URL_SHORT_STORAGE_FILE

# SHORT_URLS = [
#     ShortUrl(
#         target_url=AnyHttpUrl("https://www.example.com"),
#         slug="example",
#     ),
#     ShortUrl(
#         target_url=AnyHttpUrl("https://www.google.com"),
#         slug="search",
#     ),
# ]


class ShortUrlStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    def safe_state(self) -> None:
        URL_SHORT_STORAGE_FILE.write_text(self.model_dump_json(indent=2))

    @classmethod
    def from_state(cls) -> "ShortUrlStorage":
        if not URL_SHORT_STORAGE_FILE.exists():
            return ShortUrlStorage()
        return cls.model_validate_json(URL_SHORT_STORAGE_FILE.read_text())

    def get(self) -> list[ShortUrl]:
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug: str) -> ShortUrl | None:
        return self.slug_to_short_url.get(slug)

    def create(self, short_url_in: ShortUrlCreate) -> ShortUrl:
        short_url = ShortUrl(**short_url_in.model_dump())
        self.slug_to_short_url[short_url.slug] = short_url
        self.safe_state()
        return short_url

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_short_url.pop(slug, None)
        self.safe_state()

    def delete(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

    def update(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdate,
    ) -> ShortUrl:
        for field_name, value in short_url_in:
            setattr(short_url, field_name, value)
        self.safe_state()
        return short_url

    def update_partial(
        self,
        short_url: ShortUrl,
        short_url_in: ShortUrlUpdatePartial,
    ) -> ShortUrl:
        for field_name, values in short_url_in.model_dump(exclude_unset=True).items():
            setattr(short_url, field_name, values)
        self.safe_state()
        return short_url


try:
    storage = ShortUrlStorage.from_state()
except ValidationError:
    storage = ShortUrlStorage()
    storage.safe_state()


# storage.create(
#     ShortUrlCreate(
#         target_url=AnyHttpUrl("https://www.example.com"),
#         slug="example",
#     )
# )
#
# storage.create(
#     ShortUrlCreate(
#         target_url=AnyHttpUrl("https://www.google.com"),
#         slug="search",
#     )
# )
