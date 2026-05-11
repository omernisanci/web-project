from app.schemas.user import UserCreate, UserResponse, UserLogin # UserLogin eklendi
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

# İhtiyacımız olan araçları ve yazdığımız diğer katmanları çağırıyoruz
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services import user as user_service

# Garsonumuzu (Router) tanımlıyoruz. 
# URL'lerin başına otomatik olarak '/users' ekleyecek ve Swagger'da 'Users' başlığına koyacak.
router = APIRouter(prefix="/users", tags=["Users"])

# YENİ KULLANICI KAYIT ROTALAMASI (POST İSTEĞİ)
# Başarılı olursa internete otomatik olarak '201 Created' (Başarıyla Oluşturuldu) kodu dönecek.
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user_endpoint(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Sisteme yeni bir kullanıcı kaydeder. Email kontrolü ve şifreleme işlemleri otomatik yapılır.
    """
    # Garson aklını kullanmaz, siparişi ve veritabanı bağlantısını doğrudan Şefe (Service) iletir:
    yeni_kullanici = user_service.register_new_user(db=db, user_data=user_data)
    
    # Şefin hazırladığı ve veritabanına yazdığı nesneyi müşteriye (internete) servis et:
    return yeni_kullanici
# GİRİŞ YAPMA KAPISI (POST)
# Ne işe yarıyor?: İnternetten gelen giriş taleplerini karşılar ve doğrulama servisine iletir.
@router.post("/login")
def login_user_endpoint(login_data: UserLogin, db: Session = Depends(get_db)):
    return user_service.authenticate_user(db=db, login_data=login_data)