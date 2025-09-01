from pydantic import BaseModel

class UrlCreate(BaseModel):
    name: str
    url: str

class Url(BaseModel):
    id: int
    name: str
    url: str

    class Config:
        orm_mode = True

class PingUrl(BaseModel):
        id: int

class UrlSimple(BaseModel):
    url: str