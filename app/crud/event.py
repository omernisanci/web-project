from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate

# 1. YENİ ETKİNLİK KAYDETME (Hamal Yazma İşlemi)
# Ne işe yarıyor?: Şemadan gelen temiz veriyi PostgreSQL'e yeni bir satır olarak ekler.
# Neden kullanıyoruz?: İnternetten gönderilen konseri/tiyatroyu kalıcı olarak diske yazmak için.
def create_event(db: Session, event_data: EventCreate):
    db_event = Event(
        baslik=event_data.baslik,
        kategori=event_data.kategori,
        tarih=event_data.tarih,
        lokasyon=event_data.lokasyon,
        kapasite=event_data.kapasite,
        yas_siniri=event_data.yas_siniri
    )
    db.add(db_event)      # Bekleme odasına al
    db.commit()           # Veritabanına kesin olarak yaz
    db.refresh(db_event)  # Oluşan dinamik ID'yi nesneye yükle
    return db_event

# 2. ETKİNLİKLERİ GETİRME (Hamal Okuma İşlemi)
# Ne işe yarıyor?: Veritabanındaki etkinlikleri liste halinde çekip getirir.
# Neden kullanıyoruz?: İleride "Öneri Algoritması"nın eşleştirme yapacağı havuzu oluşturmak için.
def get_all_events(db: Session, skip: int = 0, limit: int = 100):
    # offset(skip): Baştan şu kadar kaydı atla, limit(limit): En fazla şu kadar kayıt getir.
    return db.query(Event).offset(skip).limit(limit).all()