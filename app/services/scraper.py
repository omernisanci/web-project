import requests
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy.orm import Session

from app.schemas.event import EventCreate
from app.crud import event as crud_event

# OTONOM KAZIMA ROBOTU (Web Scraper)
# Ne işe yarıyor?: Web sayfalarındaki HTML etiketlerini tarar, metinleri ayıklar ve DB'ye kaydeder.
# Neden kullanıyoruz?: Veritabanımızı insan eli değmeden, dış dünyadaki verilerle beslemek için.
def scrape_sample_events(db: Session):
    # GERÇEK DÜNYA BAĞLANTISI: 
    # Gerçekte 'requests.get("https://hedef-etkinlik-sitesi.com")' diyerek canlı HTML'i indiririz.
    # Ancak ticari siteler anlık engelleme (Cloudflare/403) yapabildiği için, 
    # mantığı %100 kavramak adına indirilen standart bir HTML iskeletini parçalıyoruz:
    
    ornek_html_sayfasi = """
    <html>
        <body>
            <div class="etkinlik-karti">
                <h2 class="baslik">Büyük Yapay Zeka Zirvesi 2026</h2>
                <span class="kategori">Yapay Zeka</span>
                <span class="lokasyon">Levent, İstanbul</span>
            </div>
            <div class="etkinlik-karti">
                <h2 class="baslik">Açık Hava Senfoni Orkestrası</h2>
                <span class="kategori">Müzik</span>
                <span class="lokasyon">Harbiye, İstanbul</span>
            </div>
        </body>
    </html>
    """
    
    # 1. HTML kodunu BeautifulSoup motoruna veriyoruz (Aşçıya malzemeyi verdik)
    soup = BeautifulSoup(ornek_html_sayfasi, "html.parser")
    
    # 2. Sayfadaki tüm 'etkinlik-karti' sınıflı kutuları buluyoruz
    etkinlik_kutulari = soup.find_all("div", class_="etkinlik-karti")
    
    kaydedilenler = []
    
    # 3. Her bir kutunun içindeki etiketleri cımbızla çekiyoruz
    for kutu in etkinlik_kutulari:
        cekilen_baslik = kutu.find("h2", class_="baslik").text.strip()
        cekilen_kategori = kutu.find("span", class_="kategori").text.strip()
        cekilen_lokasyon = kutu.find("span", class_="lokasyon").text.strip()
        
        # A) Şemamıza döküyoruz (Güvenlik Kapısından Geçiriyoruz)
        yeni_sema = EventCreate(
            baslik=cekilen_baslik,
            kategori=cekilen_kategori,
            tarih=datetime(2026, 10, 29, 14, 0),  # Gelecek bir tarih atadık
            lokasyon=cekilen_lokasyon,
            kapasite=300,
            yas_siniri=12
        )
        
        # B) Hamala verip fiziksel olarak PostgreSQL'e yazdırıyoruz
        db_event = crud_event.create_event(db=db, event_data=yeni_sema)
        kaydedilenler.append(db_event)
        
    return {
        "mesaj": f"{len(kaydedilenler)} yeni etkinlik dışarıdan kazındı ve veritabanına eklendi!",
        "eklenenler": kaydedilenler
    }