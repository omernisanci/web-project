from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    baslik = Column(String, index=True, nullable=False)         # Örn: "Açık Hava Rock Konseri"
    kategori = Column(String, index=True, nullable=False)       # Örn: "Rock Müzik", "Tiyatro", "Yazılım"
    tarih = Column(DateTime, default=datetime.utcnow, nullable=False)
    lokasyon = Column(String, nullable=False)                   # Örn: "Kadıköy, İstanbul"
    kapasite = Column(Integer, default=100)                     # Katılımcı limiti
    yas_siniri = Column(Integer, default=0)                     # 18+ gibi kontroller için

    def __repr__(self):
        return f"<Event(baslik='{self.baslik}', kategori='{self.kategori}')>"