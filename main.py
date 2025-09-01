import json

from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine
from scripts import pinger

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/url", response_model=schemas.Url)
def create_url(user: schemas.UrlCreate, db: Session = Depends(get_db)):
    db_url = models.Url(url=user.url, name=user.name)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

@app.get("/urls", response_model=list[schemas.Url])
def read_url( db: Session = Depends(get_db)):
    users = db.query(models.Url).all()
    return users

from fastapi import HTTPException

@app.delete("/url/{id}", response_model=schemas.Url)
def delete_url(id: int, db: Session = Depends(get_db)):
    url = db.query(models.Url).filter(models.Url.id == id).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    db.delete(url)
    db.commit()
    return url

@app.put("/url/{id}", response_model=schemas.Url)
def update_url(url: schemas.UrlCreate ,id: int, db: Session = Depends(get_db)):
    url_entity = db.query(models.Url).filter(models.Url.id == id).first()

    if not url_entity:
        raise HTTPException(status_code=404, detail="URL not found")

    if url.url != url_entity.url:
        url_entity.url = url.url

    if url.name != url_entity.name:
        url_entity.name = url.name

    db.commit()
    db.refresh(url_entity)

    return url_entity

@app.get("/ping-url/{id}")
def read_url( id: int, db: Session = Depends(get_db)):
    url = db.query(models.Url).filter(models.Url.id == id).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    resp = pinger.main(url.url)
    return resp

@app.post("/ping-url")
async def ping(url: schemas.UrlSimple):

    resp = pinger.main(url.url)

    return resp