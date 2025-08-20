# Python 202 Library Project
## Global AI Hub Python 202 Bootcamp Final Project

Bu proje, Python 202 Bootcamp'inde öğrenilen OOP, Harici API kullanımı ve FastAPI ile web servis oluşturma konularını birleştiren kapsamlı bir kütüphane yönetim sistemidir.

## 🚀 Özellikler

- **Aşama 1**: OOP prensiplerine uygun terminal tabanlı kütüphane yönetimi
- **Aşama 2**: Open Library API ile otomatik kitap bilgisi çekme
- **Aşama 3**: FastAPI ile RESTful web servisi

## 📁 Proje Yapısı

```
python-202-library-project/
├── main.py                 # Terminal uygulaması
├── api.py                  # FastAPI web servisi
├── book.py                 # Book sınıfı
├── library.py              # Library sınıfı
├── requirements.txt        # Gerekli paketler
├── library.json           # Veri depolama dosyası
├── test_library.py        # Library testleri
├── test_api.py            # API testleri
└── README.md              # Bu dosya
```

## 🛠 Kurulum

### 1. Projeyi klonlayın:
```bash
git clone https://github.com/KULLANICI_ADINIZ/python-202-library-project.git
cd python-202-library-project
```

### 2. Sanal ortam oluşturun (opsiyonel ama önerilen):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows
```

### 3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## 💻 Kullanım

### Terminal Uygulaması (Aşama 1-2):
```bash
python main.py
```

Menü seçenekleri:
1. Kitap Ekle (sadece ISBN girin, diğer bilgiler API'den çekilir)
2. Kitap Sil
3. Kitapları Listele
4. Kitap Ara
5. Çıkış

### FastAPI Web Servisi (Aşama 3):
```bash
uvicorn api:app --reload
```

API endpoints:
- `GET /books` - Tüm kitapları listele
- `POST /books` - Yeni kitap ekle (Body: `{"isbn": "9780140328721"}`)
- `DELETE /books/{isbn}` - Kitap sil

### Interaktif API Dokümantasyonu:
Sunucu çalışırken: http://localhost:8000/docs

## 🧪 Testler

Tüm testleri çalıştırmak için:
```bash
pytest -v
```

Belirli test dosyasını çalıştırmak için:
```bash
pytest test_library.py -v
pytest test_api.py -v
```

## 📚 Kullanılan Teknolojiler

- **Python 3.8+**
- **FastAPI** - Modern web framework
- **httpx** - HTTP client
- **pytest** - Test framework
- **uvicorn** - ASGI server
- **pydantic** - Data validation
- **Open Library API** - Kitap bilgileri

## 📋 API Endpoint'leri Detayı

### GET /books
Kütüphanedeki tüm kitapları döndürür.

**Response:**
```json
[
  {
    "title": "Ulysses",
    "author": "James Joyce",
    "isbn": "9780140328721"
  }
]
```

### POST /books
Yeni kitap ekler. Open Library API'sinden bilgileri otomatik çeker.

**Request Body:**
```json
{
  "isbn": "9780140328721"
}
```

**Response:**
```json
{
  "message": "Kitap başarıyla eklendi",
  "book": {
    "title": "Ulysses",
    "author": "James Joyce", 
    "isbn": "9780140328721"
  }
}
```

### DELETE /books/{isbn}
Belirtilen ISBN'e sahip kitabı siler.

**Response:**
```json
{
  "message": "Kitap başarıyla silindi"
}
```

## 🎯 Test Senaryoları

### Başarılı Test İçin Deneyebileceğiniz ISBN'ler:
- `9780140328721` - Ulysses by James Joyce
- `9780486280619` - Pride and Prejudice by Jane Austen
- `9780140449136` - 1984 by George Orwell

### Hata Testleri:
- `1234567890` - Geçersiz ISBN
- Boş ISBN değeri

## 🚀 Gelecekteki Geliştirmeler

- [ ] SQLite veritabanı entegrasyonu
- [ ] PUT endpoint ile kitap güncelleme
- [ ] Web frontend arayüzü
- [ ] Docker container desteği
- [ ] Kullanıcı authentication sistemi

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👤 Geliştirici

**[Adınız Soyadınız]**
- GitHub: [@kullanici_adiniz](https://github.com/kullanici_adiniz)
- Email: email@example.com

---
*Global AI Hub Python 202 Bootcamp Final Project - 2025*
