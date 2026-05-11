from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.event import EventCreate, EventResponse
from app.services import event as event_service

# Garsonumuzu tanımlıyoruz (URL başına '/events' ekler)
router = APIRouter(prefix="/events", tags=["Events"])

# 1. ETKİNLİK EKLEME KAPISI (POST)
# Ne işe yarıyor?: İnternetten (veya ileride yazacağımız robotlardan) gelen veriyi sisteme kaydeder.
@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event_endpoint(event_data: EventCreate, db: Session = Depends(get_db)):
    return event_service.create_new_event(db=db, event_data=event_data)

# 2. ETKİNLİKLERİ LİSTELEME KAPISI (GET)
# Ne işe yarıyor?: Sistemdeki etkinlikleri liste halinde dışarı basar.
@router.get("/", response_model=List[EventResponse])
def get_events_endpoint(db: Session = Depends(get_db)):
    return event_service.list_all_events(db=db)
# KAZIMA ROBOTUNU TETİKLEME KAPISI (POST)
# Ne işe yarıyor?: Dışarıdan butona basıldığında kazıma robotunu harekete geçirir.
@router.post("/scrape")
def trigger_scraper_endpoint(db: Session = Depends(get_db)):
    from app.services import scraper as scraper_service
    return scraper_service.scrape_sample_events(db=db)