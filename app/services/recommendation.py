from sqlalchemy.orm import Session
from app.models.user import User
from app.models.event import Event
from fastapi import HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ANLAMSAL (SEMANTİK) YAPAY ZEKA ÖNERİ SERVİSİ
# Ne işe yarıyor?: Kelimeleri vektörlere (sayılara) çevirip, metinler arasındaki benzerlik açısını hesaplar.
# Neden kullanıyoruz?: Birebir aynı kelime olmasa bile, kavramsal olarak benzer etkinlikleri yakalamak için.
def get_recommendations_for_user(db: Session, user_id: int):
    # 1. Kullanıcıyı bul
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı!")

    # 2. Veritabanındaki tüm etkinlikleri çek
    all_events = db.query(Event).all()
    if not all_events:
        return []

    # Kullanıcının ilgi alanı metni (Örn: "Yazılım, Yapay Zeka, Teknoloji")
    kullanici_metni = user.ilgi_alanlari if user.ilgi_alanlari else ""
    onerilen_etkinlikler = []

    # 3. AI Vektör Motorunu Devreye Sokuyoruz
    if kullanici_metni:
        # Etkinliklerin başlığını ve kategorisini birleştirip bir metin havuzu yapıyoruz
        etkinlik_metinleri = [f"{e.baslik} {e.kategori}" for e in all_events]
        
        # Kıyaslama yapabilmek için havuzun en başına kullanıcının ilgi alanını ekliyoruz
        tum_metinler = [kullanici_metni] + etkinlik_metinleri
        
        # TF-IDF: Kelimelerin önem derecesine göre matematiksel harita çıkarır
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(tum_metinler)
        
        # Kosinüs Benzerliği: Kullanıcı metni (0. indeks) ile diğer etkinlikler arasındaki yakınlığı ölçer
        benzerlik_skorlari = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        
        # 4. Skorları Filtreliyoruz
        for indeks, skor in enumerate(benzerlik_skorlari):
            event = all_events[indeks]
            
            # Yaş sınırı kontrolü (Güvenlik her zaman önce gelir)
            if user.yas and event.yas_siniri and user.yas < event.yas_siniri:
                continue
                
            # Eğer anlamsal benzerlik skoru %10'dan (0.1) büyükse, konseptler uyuşuyor demektir!
            if skor > 0.1:
                onerilen_etkinlikler.append(event)
    else:
        # Kullanıcının ilgi alanı boşsa sadece yaş kriterine uyanları getir
        for event in all_events:
            if user.yas and event.yas_siniri and user.yas < event.yas_siniri:
                continue
            onerilen_etkinlikler.append(event)

    return onerilen_etkinlikler