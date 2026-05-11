from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Veritabanı Motoru
engine = create_engine(settings.DATABASE_URL, echo=True)

# Oturum Fabrikası
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tabloların miras alacağı temel sınıf
Base = declarative_base()

# FastAPI için DB Asansörü
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()