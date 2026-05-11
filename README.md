# 🚀 Akıllı Etkinlik Öneri Sistemi (AI-Driven Event API)

Bu proje, kullanıcıların ilgi alanlarına göre **Yapay Zeka (NLP)** desteğiyle kişiselleştirilmiş etkinlik önerileri sunan, otonom veri toplama yeteneğine sahip bir **FastAPI** backend projesidir.

## 🧠 Proje Özellikleri
* **Otonom Veri Kazıma (Web Scraping):** İnternet üzerindeki etkinlikleri otomatik olarak tarar ve veritabanına kaydeder.
* **AI Tabanlı Öneri Motoru:** `Scikit-learn` ve `Cosine Similarity` kullanarak kullanıcı hobileri ile etkinlikler arasında anlamsal eşleşme yapar.
* **Güvenli Giriş:** Kullanıcı şifreleri `SHA-256` ile kriptolanarak saklanır.
* **Dockerize Edilmiş Yapı:** Proje her ortamda tek tıkla çalışmaya hazır hale getirilmiştir.

---

## 🛠️ Teknik Yol Haritası (Arkadaşlarım İçin)

Projeye katkı sağlamak isteyen arkadaşlarımız şu adımları izleyebilir:

1.  **Depoyu Klonlayın:**
    `git clone https://github.com/omernisanci/web-project.git`
2.  **Sanal Ortam Kurun:**
    `python -m venv venv`
    `venv\Scripts\activate`
3.  **Gerekli Paketleri Yükleyin:**
    `pip install -r requirements.txt`
4.  **Sunucuyu Başlatın:**
    `uvicorn app.main:app --reload`
5.  **API Dökümantasyonunu İnceleyin:**
    Tarayıcıda `http://127.0.0.1:8000/docs` adresine giderek tüm uç noktaları test edebilirsiniz.

---

## 📅 Gelecek Planları (Roadmap)
- [ ] **Frontend Entegrasyonu:** React kullanılarak kullanıcı arayüzünün tamamlanması.
- [ ] **Mobil Bildirim:** Önerilen etkinlikler için anlık bildirim sistemi.
- [ ] **Gerçek Zamanlı Veri:** Canlı etkinlik sitelerinden (Biletix, Eventbrite vb.) veri çekme.
