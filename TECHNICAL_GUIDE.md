# Kamera İzleme ve Nesne Tespiti Sistemi

## 1. Genel Bakış
Bu sistem, kamera üzerinden gerçek zamanlı görüntü alarak nesne tespiti yapan, tespitleri kaydeden ve web arayüzü üzerinden canlı izleme imkanı sunan bir uygulamadır.

## 2. Kullanılan Teknolojiler
### 2.1 Ana Bileşenler
- Python 3.9
- OpenCV (cv2)
- YOLOv5 (Nesne Tespiti)
- Torch (YOLOv5)
- WebSocket (Canlı Yayın)
- FastAPI (Web API)
- Uvicorn (Web API)

### 2.2 Veritabanı
- Mysql (Tespit Kayıtları)


## 3. Sistem Mimarisi

### 3.1 Ana Modüller
1. **Camera Module**
   - Kamera bağlantısı yönetimi
   - Frame okuma ve önizleme

2. **Detection Manager**
   - YOLOv5 modeli entegrasyonu
   - Tespit işlemleri
   - Yoğunluk analizi
   - Görüntü kayıt

3. **Video Analyzer**
   - YOLOv5 modeli entegrasyonu
   - Tespit işlemleri
   - Görüntü preview
   - Yoğunluk analizi 
   - İşlenmiş video kaydı
   - Görüntü kayıt

4. **WebSocket Streamer**
   - Canlı görüntü yayını
   - Bağlantı yönetimi
   - Frame sıkıştırma
   - İzleyici yönetimi

5. **Database Manager**
   - Veritabanı işlemleri

6. **Web API**
   - Kayıt edilen tespitlerin görüntü paylaşımı

### 3.2 Veri Akışı
1. Kamera modülü frame yakalar
2. Detection Manager nesneleri tespit eder
3. Tespit sonuçları veritabanına kaydedilir
4. İşlenmiş görüntü WebSocket üzerinden yayınlanır

## 4. Önemli Özellikler

### 4.1 Nesne Tespiti
- YOLOv5 modeli kullanımı
- Çoklu nesne tespiti
- Güven skorları
- Sınıflandırma

### 4.2 Görüntü Yönetimi
- Otomatik kayıt sistemi
- Tarih/saat bazlı klasörleme
- Tespit edilen nesnelerin ayrı kaydı

### 4.4 Canlı İzleme
- WebSocket üzerinden düşük gecikmeli yayın
- Base64 görüntü kodlama
- Çoklu istemci desteği
- Bağlantı durum yönetimi
