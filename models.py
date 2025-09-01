from sqlalchemy import Column, Integer, String
from database import Base

class Url(Base):
    __tablename__ = "url"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)