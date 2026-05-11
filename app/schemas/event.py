from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# 1. ETKİNLİK YARATMA ŞEMASI (Gelen Veri)
# Ne işe yarıyor?: İnternetten yeni etkinlik eklenirken gönderilmesi zorunlu verileri belirler.
# Neden kullanıyoruz?: Biri sisteme kafasına göre id veya yanlış formatta tarih atamasın diye.
class EventCreate(BaseModel):
    baslik: str = Field(..., min_length=3, json_schema_extra={"example": "Açık Hava Rock Konseri"})
    kategori: str = Field(..., json_schema_extra={"example": "Rock Müzik"})
    tarih: datetime = Field(..., json_schema_extra={"example": "2026-06-15T20:00:00"})
    lokasyon: str = Field(..., json_schema_extra={"example": "Kadıköy, İstanbul"})
    kapasite: Optional[int] = Field(100, ge=1, json_schema_extra={"example": 500})
    yas_siniri: Optional[int] = Field(0, ge=0, json_schema_extra={"example": 18})

# 2. ETKİNLİK CEVAP ŞEMASI (Giden Veri)
# Ne işe yarıyor?: Veritabanına kaydolan etkinliği internete (Swagger'a) temizce geri basar.
# Neden kullanıyoruz?: SQLAlchemy nesnesini, tarayıcının anlayacağı JSON diline çevirmek için.
class EventResponse(BaseModel):
    id: int
    baslik: str
    kategori: str
    tarih: datetime
    lokasyon: str
    kapasite: int
    yas_siniri: int

    # Dönüşüm Motoru: Veritabanı dilini JSON diline otomatik çevirir.
    model_config = ConfigDict(from_attributes=True)