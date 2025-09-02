from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import SessionLocal, engine
from scripts import pinger, pingScheduler, fixture

# Création des tables et chargement des fixtures au démarrage
models.Base.metadata.create_all(bind=engine)
fixture.load_fixtures()

app = FastAPI(title="Pinger API")


# --- Dépendance DB ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- URL Management ---
@app.post("/url", response_model=schemas.Url, tags=["URL Management"], status_code=status.HTTP_201_CREATED)
def create_url(user: schemas.UrlCreate, db: Session = Depends(get_db)):
    """Créer une nouvelle URL."""
    db_url = models.Url(url=user.url, name=user.name)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


@app.get("/urls", response_model=List[schemas.Url], tags=["URL Management"])
def list_urls(db: Session = Depends(get_db)):
    """Lister toutes les URLs."""
    return db.query(models.Url).all()


@app.put("/url/{id}", response_model=schemas.Url, tags=["URL Management"])
def update_url(id: int, url: schemas.UrlCreate, db: Session = Depends(get_db)):
    """Mettre à jour une URL par son ID."""
    url_entity = db.query(models.Url).filter(models.Url.id == id).first()
    if not url_entity:
        raise HTTPException(status_code=404, detail="URL not found")

    url_entity.url = url.url
    url_entity.name = url.name

    db.commit()
    db.refresh(url_entity)
    return url_entity


@app.delete("/url/{id}", response_model=schemas.Url, tags=["URL Management"], status_code=status.HTTP_200_OK)
def delete_url(id: int, db: Session = Depends(get_db)):
    """Supprimer une URL par son ID."""
    url = db.query(models.Url).filter(models.Url.id == id).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    db.delete(url)
    db.commit()
    return url


# --- URL Ping ---
@app.get("/ping-url/{id}", tags=["URL Ping"])
def ping_url_by_id(id: int, db: Session = Depends(get_db)):
    """Pinger une URL par son ID."""
    url = db.query(models.Url).filter(models.Url.id == id).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return pinger.main(url.url)


@app.post("/ping-url", tags=["URL Ping"])
async def ping_url(url: schemas.UrlSimple):
    """Pinger une URL donnée."""
    return pinger.main(url.url)


# --- Ping Management ---
@app.get("/pings", tags=["Ping Management"])
def list_pings(db: Session = Depends(get_db)):
    """Lister tous les Pings."""
    return db.query(models.Ping).all()


# --- Schedule Management ---
@app.post("/schedule", response_model=schemas.Scheduler, tags=["Schedule Management"], status_code=status.HTTP_201_CREATED)
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


@app.get("/schedule/urls", response_model=List[schemas.UrlWithSchedules], tags=["Schedule Management"])
def list_schedule_urls(db: Session = Depends(get_db)):
    """Lister toutes les URLs avec leurs schedules."""
    return db.query(models.Url).all()


@app.patch("/auto-schedule", tags=["Schedule Management"])
def switch_scheduler(db: Session = Depends(get_db)):
    """Activer ou désactiver l'auto ping des URL enregistrées dans le scheduler."""
    scheduler = db.query(models.Config).first()
    if not scheduler or scheduler.key != "scheduler":
        raise HTTPException(status_code=404, detail="No scheduler found")

    scheduler.value = "1" if scheduler.value == "0" else "0"
    db.commit()
    db.refresh(scheduler)
    return scheduler


@app.delete("/schedule/{id}", tags=["Schedule Management"], status_code=status.HTTP_200_OK)
def delete_schedule(id: int, db: Session = Depends(get_db)):
    """Supprimer une tâche de schedule par son ID."""
    scheduler = db.query(models.Scheduler).filter(models.Scheduler.id == id).first()
    if not scheduler:
        raise HTTPException(status_code=404, detail="Schedule not found")

    db.delete(scheduler)
    db.commit()
    return True
