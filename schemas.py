from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

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

class Scheduler(BaseModel):
    id: int
    url_id: int
    date: datetime

    class Config:
        orm_mode = True

class ScheduleCreate(BaseModel):
    id: int

class SchedulerBase(BaseModel):
    id: int
    date: datetime

    class Config:
        orm_mode = True

class UrlWithSchedules(BaseModel):
    id: int
    name: str
    url: str
    schedulers: List[SchedulerBase] = []

    class Config:
        orm_mode = True
