from sqlalchemy.orm import Session
from app.crud import event as crud_event
from app.schemas.event import EventCreate

# 1. ETKİNLİK YARATMA SERVİSİ
# Ne işe yarıyor?: CRUD hamalına emri iletmeden önce iş kurallarını yönetir.
# Neden kullanıyoruz?: İleride "aynı saatte başka etkinlik var mı?" gibi zekice kontrolleri buraya yazmak için.
def create_new_event(db: Session, event_data: EventCreate):
    return crud_event.create_event(db=db, event_data=event_data)

# 2. TÜM ETKİNLİKLERİ GETİRME SERVİSİ
# Ne işe yarıyor?: Veritabanındaki tüm etkinlikleri getirir.
def list_all_events(db: Session):
    return crud_event.get_all_events(db=db)