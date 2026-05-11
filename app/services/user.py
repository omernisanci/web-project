import hashlib
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud import user as crud_user
from app.schemas.user import UserCreate

# 1. ŞİFRE KRİPTOLAMA FONKSİYONU
# Gelen düz metin şifreyi (örn: "benimsifrem123") SHA-256 algoritmasıyla 
# kimsenin çözemeyeceği 64 karakterlik rastgele bir metne dönüştürür.
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# 2. ANA İŞ MANTIĞI: YENİ KULLANICI KAYIT OPERASYONU
def register_new_user(db: Session, user_data: UserCreate):
    # A) KONTROL: Bu email sistemde zaten var mı? CRUD'a soralım.
    mevcut_kullanici = crud_user.get_user_by_email(db, email=user_data.email)
    if mevcut_kullanici:
        # Varsa işlemi anında durdur ve internete hata fırlat!
        raise HTTPException(
            status_code=400, 
            detail="Bu email adresi zaten sistemde kayıtlı!"
        )
    
    # B) GÜVENLİK: Şifreyi güvenli hale getir
    kriptolu_sifre = hash_password(user_data.password)
    
    # C) KAYIT: Her şey kurallara uygun. CRUD hamalına emri ver, veritabanına yazsın.
    yeni_kullanici = crud_user.create_user(
        db=db, 
        user_data=user_data, 
        hashed_password=kriptolu_sifre
    )
    
    return yeni_kullanici

# KULLANICI GİRİŞ (LOGIN) KONTROL SERVİSİ
# Ne işe yarıyor?: Email veritabanında var mı bakar, varsa gelen şifreyi hash'leyip DB'dekiyle kıyaslar.
def authenticate_user(db: Session, login_data: UserLogin):
    # A) Kullanıcıyı email ile bul
    user = crud_user.get_user_by_email(db, email=login_data.email)
    if not user:
        raise HTTPException(status_code=404, detail="Bu email adresi sistemde kayıtlı değil.")
    
    # B) Şifre kontrolü (Gelen şifreyi kriptola ve DB'deki hash ile karşılaştır)
    kriptolu_sifre = hash_password(login_data.password)
    if user.hashed_password != kriptolu_sifre:
        raise HTTPException(status_code=401, detail="Şifre hatalı, lütfen tekrar deneyin.")
    
    # C) Başarılıysa güvenli bilgileri dön
    return {
        "mesaj": "Giriş başarılı!", 
        "user_id": user.id, 
        "ad_soyad": user.ad_soyad
    }