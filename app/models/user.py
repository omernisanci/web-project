from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Etkinlik Öneri Algoritması için kullanacağımız kritik sütunlar:
    ad_soyad = Column(String, nullable=False)
    yas = Column(Integer)
    ilgi_alanlari = Column(String)  # Örn: "Müzik, Tiyatro, Yazılım"
    lokasyon = Column(String)       # Örn: "Kadıköy, İstanbul"

    def __repr__(self):
        return f"<User(email='{self.email}', ad_soyad='{self.ad_soyad}')>"