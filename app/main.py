from fastapi import FastAPI
from app.database import engine, Base

# 1. Tüm garsonlarımızı (router) içeri aktarıyoruz
from app.routers import user_router, event_router, rec_router

# Veritabanı tablolarını güvenceye alıyoruz
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Etkinlik Öneri API")

# 2. İŞTE EKSİK OLAN KISIM: Garsonları ana uygulamaya bağlıyoruz!
app.include_router(user_router)
app.include_router(event_router)
app.include_router(rec_router)

# Ana sayfa kök adresi (Şu an ekranda gördüğün tek yer)
@app.get("/")
def root():
    return {"mesaj": "Tüm sistemler aktif, Etkinlik Öneri API hazır!"}