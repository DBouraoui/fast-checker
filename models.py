from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Url(Base):
    __tablename__ = "url"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)

    # Ajoute une relation pour accéder aux entrées du Scheduler depuis Url
    schedulers = relationship("Scheduler", back_populates="url")

class Ping(Base):
    __tablename__ = "ping"
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    result = Column(String(1000), nullable=False)
    date = Column(DateTime, nullable=False)

class Scheduler(Base):
    __tablename__ = "scheduler"
    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey("url.id"), nullable=False)
    date = Column(DateTime, nullable=False)

    url = relationship("Url", back_populates="schedulers")
