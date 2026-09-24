from pydantic import BaseModel, HttpUrl

class Link(BaseModel):
    original_url: HttpUrl
    short_alias: str | None = None