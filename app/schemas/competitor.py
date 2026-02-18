from pydantic import BaseModel, HttpUrl

class CompetitorCreate(BaseModel):
    name: str
    url: HttpUrl
    tag: str | None = None

class CompetitorOut(BaseModel):
    id: int
    name: str
    url: str
    tag: str | None

    class Config:
        from_attributes = True
