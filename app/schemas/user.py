from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

# 1. KULLANICI KAYIT OLURKEN İSTEYECEĞİMİZ VERİLER (Gelen Veri)
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Şifre en az 6 karakter olmalı")
    ad_soyad: str = Field(
        ..., 
        min_length=2, 
        json_schema_extra={"example": "Ahmet Yılmaz"}
    )
    yas: Optional[int] = Field(
        None, 
        ge=18, 
        description="Kullanıcı 18 yaşından küçük olamaz"
    )
    ilgi_alanlari: Optional[str] = Field(
        None, 
        json_schema_extra={"example": "Konser, Tiyatro, Rock Müzik"}
    )
    lokasyon: Optional[str] = Field(
        None, 
        json_schema_extra={"example": "Kadıköy, İstanbul"}
    )

# 2. İNTERNETE CEVAP OLARAK DÖNECEĞİMİZ VERİLER (Giden Veri - ŞİFRE YOK!)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    ad_soyad: str
    yas: Optional[int]
    ilgi_alanlari: Optional[str]
    lokasyon: Optional[str]

    # Pydantic v2'nin SQLAlchemy nesnelerini JSON'a çevirebilmesi için şarttır:
    model_config = ConfigDict(from_attributes=True)
    # GİRİŞ YAPMA ŞEMASI (Gelen Veri)
# Ne işe yarıyor?: Kullanıcı giriş yaparken sadece email ve şifre göndersin, başka veri atamasın.
class UserLogin(BaseModel):
    email: EmailStr
    password: str