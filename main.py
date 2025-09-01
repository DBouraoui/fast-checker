from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine
from scripts import pinger

models.Base.metadata.create_all(bind=engine)

app = FastAPI( title="Pinger API",)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/url", response_model=schemas.Url, tags=["URL Management"])
def create_url(user: schemas.UrlCreate, db: Session = Depends(get_db)):
    """Créer une nouvelle URL."""
    db_url = models.Url(url=user.url, name=user.name)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

@app.get("/urls", response_model=list[schemas.Url], tags=["URL Management"])
def read_url(db: Session = Depends(get_db)):
    """Lister toutes les URLs."""
    users = db.query(models.Url).all()
    return users

@app.delete("/url/{id}", response_model=schemas.Url, tags=["URL Management"])
def delete_url(id: int, db: Session = Depends(get_db)):
    """Supprimer une URL par son ID."""
    url = db.query(models.Url).filter(models.Url.id == id).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    db.delete(url)
    db.commit()
    return url

@app.put("/url/{id}", response_model=schemas.Url, tags=["URL Management"])
def update_url(url: schemas.UrlCreate, id: int, db: Session = Depends(get_db)):
    """Mettre à jour une URL par son ID."""
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

# Endpoints pour le ping des URLs
@app.get("/ping-url/{id}", tags=["URL Ping"])
def read_url(id: int, db: Session = Depends(get_db)):
    """Pinger une URL par son ID."""
    url = db.query(models.Url).filter(models.Url.id == id).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    resp = pinger.main(url.url)
    return resp

@app.post("/ping-url", tags=["URL Ping"])
async def ping(url: schemas.UrlSimple):
    """Pinger une URL donnée."""
    resp = pinger.main(url.url)
    return resp


@app.get("/pings", tags=["Ping Management"])
def read_pings(db: Session = Depends(get_db)):
    """Lister tout les Pings."""
    pings = db.query(models.Ping).all()
    return pings

@app.post("/schedule", response_model=schemas.Scheduler, tags=["Schedule Management"])
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    """Créer une nouvelle entrée de planification pour une URL à ping."""

    url = db.query(models.Url).filter(models.Url.id == schedule.id).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    schedule_model = models.Scheduler(
        url_id=schedule.id,
        date=datetime.now()
    )

    db.add(schedule_model)
    db.commit()
    db.refresh(schedule_model)
    return schedule_model