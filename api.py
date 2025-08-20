#!/usr/bin/env python3
"""
Kütüphane Yönetim Sistemi - FastAPI Web Servisi
Aşama 3: API endpoint'leri
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from models import Book, Library
import uvicorn


# Pydantic modelleri
class BookResponse(BaseModel):
    title: str
    author: str
    isbn: str
    
    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    isbn: str


class ErrorResponse(BaseModel):
    error: str
    message: str


# FastAPI uygulaması
app = FastAPI(
    title="📚 Kütüphane Yönetim Sistemi API",
    description="Kitaplarınızı yönetmek için RESTful API",
    version="1.0.0"
)

# Library instance'ı - Global olarak tanımla
library = None

@app.on_event("startup")
async def startup_event():
    """Uygulama başlangıcında library'yi initialize et"""
    global library
    library = Library()
    print(f"📚 Kütüphane başlatıldı. Mevcut kitap sayısı: {len(library.books)}")

def get_library():
    """Library instance'ını döndür"""
    global library
    if library is None:
        library = Library()
    return library


@app.get("/", summary="Ana Sayfa")
async def root():
    """API ana sayfası"""
    return {
        "message": "📚 Kütüphane Yönetim Sistemi API'sine hoş geldiniz!",
        "version": "1.0.0",
        "endpoints": {
            "GET /books": "Tüm kitapları listele",
            "POST /books": "Yeni kitap ekle (ISBN ile)",
            "DELETE /books/{isbn}": "Kitap sil",
            "GET /docs": "API dokümantasyonu"
        }
    }


@app.get("/books", response_model=List[BookResponse], summary="Tüm Kitapları Listele")
async def get_books():
    """Kütüphanedeki tüm kitapların listesini döndürür"""
    current_library = get_library()
    books = current_library.list_books()
    print(f"📖 API: {len(books)} kitap listeleniyor")  # Debug için
    return [BookResponse(title=book.title, author=book.author, isbn=book.isbn) for book in books]


@app.post("/books", response_model=BookResponse, summary="Kitap Ekle")
async def add_book(book_data: BookCreate):
    """
    ISBN numarası ile Open Library API'sinden kitap bilgilerini çekerek
    kütüphaneye yeni kitap ekler
    """
    current_library = get_library()
    isbn = book_data.isbn.strip()
    
    if not isbn:
        raise HTTPException(status_code=400, detail="ISBN boş olamaz!")
    
    # Kitap zaten var mı kontrol et
    existing_book = current_library.find_book(isbn)
    if existing_book:
        raise HTTPException(
            status_code=409, 
            detail=f"ISBN {isbn} ile bir kitap zaten mevcut!"
        )
    
    # Kitap eklemeye çalış
    print(f"🔍 API: ISBN {isbn} ile kitap ekleme deneniyor...")  # Debug için
    success = current_library.add_book(isbn)
    
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Kitap bulunamadı veya API hatası oluştu"
        )
    
    # Eklenen kitabı döndür
    added_book = current_library.find_book(isbn)
    if added_book:
        print(f"✅ API: Kitap başarıyla eklendi: {added_book}")  # Debug için
        return BookResponse(
            title=added_book.title, 
            author=added_book.author, 
            isbn=added_book.isbn
        )
    else:
        raise HTTPException(status_code=500, detail="Kitap eklenirken beklenmeyen hata oluştu")


@app.delete("/books/{isbn}", summary="Kitap Sil")
async def delete_book(isbn: str):
    """Belirtilen ISBN'e sahip kitabı kütüphaneden siler"""
    current_library = get_library()
    isbn = isbn.strip()
    
    if not isbn:
        raise HTTPException(status_code=400, detail="ISBN boş olamaz!")
    
    # Kitap var mı kontrol et
    book = current_library.find_book(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı!")
    
    # Kitabı sil
    success = current_library.remove_book(isbn)
    
    if success:
        return {"message": f"Kitap başarıyla silindi: {book.title}"}
    else:
        raise HTTPException(status_code=500, detail="Kitap silinirken hata oluştu")


@app.get("/books/{isbn}", response_model=BookResponse, summary="Kitap Ara")
async def get_book(isbn: str):
    """Belirtilen ISBN'e sahip kitabı bulur ve döndürür"""
    current_library = get_library()
    isbn = isbn.strip()
    
    if not isbn:
        raise HTTPException(status_code=400, detail="ISBN boş olamaz!")
    
    book = current_library.find_book(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı!")
    
    return BookResponse(title=book.title, author=book.author, isbn=book.isbn)


@app.get("/health", summary="Sağlık Kontrolü")
async def health_check():
    """API sağlık durumunu kontrol eder"""
    current_library = get_library()
    return {
        "status": "healthy",
        "total_books": len(current_library.list_books()),
        "message": "API çalışıyor"
    }


if __name__ == "__main__":
    print("🚀 Kütüphane API'si başlatılıyor...")
    print("📖 Dokümantasyon: http://localhost:8000/docs")
    print("🔄 API Test: http://localhost:8000/health")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )