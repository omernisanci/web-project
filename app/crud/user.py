from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

# 1. EMAİLE GÖRE ARAMA: Sisteme yeni biri geldiğinde "Bu email zaten kayıtlı mı?" 
# sorusunun cevabını veritabanında arayan fonksiyon.
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# 2. YENİ KULLANICI YARATMA: Pydantic şemasından gelen o dinamik verileri alıp,
# veritabanındaki fiziksel tablomuza (Model) kesin olarak yazan fonksiyon.
def create_user(db: Session, user_data: UserCreate, hashed_password: str):
    # Şemadan gelen güvenli verileri SQLAlchemy modeline dönüştürüyoruz
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,  # Şifrenin kriptolanmış halini yazıyoruz!
        ad_soyad=user_data.ad_soyad,
        yas=user_data.yas,
        ilgi_alanlari=user_data.ilgi_alanlari,
        lokasyon=user_data.lokasyon
    )
    
    db.add(db_user)      # Bekleme odasına (Session) al
    db.commit()          # Veritabanına kesin olarak yaz
    db.refresh(db_user)  # Veritabanının atadığı o dinamik ID'yi nesneye geri yükle
    
    return db_user