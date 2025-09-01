from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Url(Base):
    __tablename__ = "url"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)

class Ping(Base):
    __tablename__ = "ping"
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    result = Column(String(1000), nullable=False)
    date = Column(DateTime, nullable=False)