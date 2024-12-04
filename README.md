# Python Kamera İzleme Sistemi - Kurulum Kılavuzu

## Önkoşullar
- Python
- pip
- Frontend üstünden veritabanı migration edilmiş olmalı

## Kurulum
```bash
# Gerekli paketleri yükle
pip3 install -r requirements.txt
```

## Kullanım
- `.env` dosyasını düzenleyerek MySQL veritabanı ayarlarını yapın.

```bash
# Api başlatmak için

python3 api.py
```

```bash
# Kamera izleme uygulamasını başlatmak için:

python3 run.py
```
```bash
# Video üstünden nesne tanıma yapmak için:

python videorun.py IMG_5274.MOV

# Video işlenirken canlı görüntüleme ve kayıt yapmak istemiyorsanız:
# --no-preview
# --no-output
```
