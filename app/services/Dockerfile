# 1. Hafif ve hızlı bir Python işletim sistemi indir
FROM python:3.11-slim

# 2. Konteyner içinde çalışma klasörü oluştur
WORKDIR /app

# 3. Kütüphane listesini kopyala ve kurulumları yap
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Projemizdeki tüm kodları konteynerin içine kopyala
COPY . .

# 5. Dış dünyaya açılacağımız portu belirle
EXPOSE 8000

# 6. Konteyner çalıştığı an garsonu (Uvicorn) otomatik olarak yayına al
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]