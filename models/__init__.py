import json
import os
import httpx
from typing import List, Optional
from .book import Book


class Library:
    """Kütüphane sınıfı - Tüm kütüphane operasyonlarını yönetir"""
    
    def __init__(self, filename: str = "library.json"):
        self.filename = filename
        self.books: List[Book] = []
        self.load_books()
    
    def add_book_manual(self, book: Book) -> bool:
        """Manuel olarak Book nesnesi ekler"""
        # ISBN benzersizliği kontrolü
        if self.find_book(book.isbn):
            print(f"ISBN {book.isbn} ile bir kitap zaten mevcut!")
            return False
        
        self.books.append(book)
        self.save_books()
        print(f"Kitap başarıyla eklendi: {book}")
        return True
    
    def add_book(self, isbn: str) -> bool:
        """ISBN ile API'den kitap bilgilerini çekerek ekler (Aşama 2)"""
        # ISBN benzersizliği kontrolü
        if self.find_book(isbn):
            print(f"ISBN {isbn} ile bir kitap zaten mevcut!")
            return False
        
        try:
            # Open Library API'sine istek gönder
            with httpx.Client() as client:
                response = client.get(f"https://openlibrary.org/isbn/{isbn}.json", timeout=10)
                
                if response.status_code == 404:
                    print("Kitap bulunamadı. Lütfen geçerli bir ISBN giriniz.")
                    return False
                
                response.raise_for_status()
                data = response.json()
                
                # Kitap bilgilerini çıkar
                title = data.get("title", "Bilinmeyen Başlık")
                
                # Yazar bilgisini çıkar (karmaşık yapı olabilir)
                authors = []
                if "authors" in data:
                    for author_ref in data["authors"]:
                        author_key = author_ref["key"]
                        # Yazar detaylarını çek
                        author_response = client.get(f"https://openlibrary.org{author_key}.json", timeout=10)
                        if author_response.status_code == 200:
                            author_data = author_response.json()
                            authors.append(author_data.get("name", "Bilinmeyen Yazar"))
                
                author = ", ".join(authors) if authors else "Bilinmeyen Yazar"
                
                # Kitap nesnesini oluştur ve ekle
                book = Book(title=title, author=author, isbn=isbn)
                self.books.append(book)
                self.save_books()
                print(f"Kitap başarıyla eklendi: {book}")
                return True
                
        except httpx.RequestError:
            print("İnternet bağlantısı hatası. Lütfen bağlantınızı kontrol edin.")
            return False
        except httpx.HTTPStatusError:
            print("API'den veri çekilirken hata oluştu.")
            return False
        except Exception as e:
            print(f"Beklenmeyen hata: {str(e)}")
            return False
    
    def remove_book(self, isbn: str) -> bool:
        """ISBN numarasına göre kitap siler"""
        book = self.find_book(isbn)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Kitap başarıyla silindi: {book}")
            return True
        else:
            print("Kitap bulunamadı!")
            return False
    
    def list_books(self) -> List[Book]:
        """Kütüphanedeki tüm kitapları listeler"""
        return self.books
    
    def find_book(self, isbn: str) -> Optional[Book]:
        """ISBN ile kitap arar"""
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def load_books(self) -> None:
        """JSON dosyasından kitapları yükler"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.books = [Book.from_dict(book_data) for book_data in data]
                print(f"{len(self.books)} kitap yüklendi.")
            except (json.JSONDecodeError, KeyError) as e:
                print(f"JSON dosyası okunamadı: {e}")
                self.books = []
        else:
            print("Veri dosyası bulunamadı, yeni kütüphane oluşturuluyor.")
            self.books = []
    
    def save_books(self) -> None:
        """Kitapları JSON dosyasına kaydeder"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump([book.to_dict() for book in self.books], file, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Kitaplar kaydedilirken hata oluştu: {e}")