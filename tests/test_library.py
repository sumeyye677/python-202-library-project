import pytest
import os
import json
import sys
from unittest.mock import patch, MagicMock

# Test için modülleri import etmek için path ayarı
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.book import Book
from models.library import Library


class TestLibrary:
    """Library sınıfı test senaryoları"""
    
    @pytest.fixture
    def temp_library_file(self, tmp_path):
        """Geçici test dosyası oluşturur"""
        return str(tmp_path / "test_library.json")
    
    @pytest.fixture
    def library(self, temp_library_file):
        """Test kütüphanesi örneği"""
        return Library(temp_library_file)
    
    @pytest.fixture
    def sample_book(self):
        """Örnek kitap nesnesi"""
        return Book("Test Book", "Test Author", "123456789")
    
    def test_library_creation(self, library):
        """Kütüphane oluşturma testi"""
        assert isinstance(library.books, list)
        assert len(library.books) == 0
    
    def test_add_book_manual(self, library, sample_book):
        """Manuel kitap ekleme testi"""
        result = library.add_book_manual(sample_book)
        
        assert result is True
        assert len(library.books) == 1
        assert library.books[0] == sample_book
    
    def test_add_duplicate_book(self, library, sample_book):
        """Aynı ISBN ile kitap ekleme testi"""
        library.add_book_manual(sample_book)
        result = library.add_book_manual(sample_book)
        
        assert result is False
        assert len(library.books) == 1
    
    def test_find_book_existing(self, library, sample_book):
        """Mevcut kitap arama testi"""
        library.add_book_manual(sample_book)
        found_book = library.find_book("123456789")
        
        assert found_book == sample_book
    
    def test_find_book_non_existing(self, library):
        """Olmayan kitap arama testi"""
        found_book = library.find_book("nonexistent")
        
        assert found_book is None
    
    def test_remove_book_existing(self, library, sample_book):
        """Mevcut kitap silme testi"""
        library.add_book_manual(sample_book)
        result = library.remove_book("123456789")
        
        assert result is True
        assert len(library.books) == 0
    
    def test_remove_book_non_existing(self, library):
        """Olmayan kitap silme testi"""
        result = library.remove_book("nonexistent")
        
        assert result is False
    
    def test_list_books_empty(self, library):
        """Boş kütüphane listeleme testi"""
        books = library.list_books()
        
        assert books == []
    
    def test_list_books_with_content(self, library, sample_book):
        """Dolu kütüphane listeleme testi"""
        library.add_book_manual(sample_book)
        books = library.list_books()
        
        assert len(books) == 1
        assert books[0] == sample_book
    
    def test_save_and_load_books(self, temp_library_file):
        """Kitap kaydetme ve yükleme testi"""
        # İlk kütüphane oluştur ve kitap ekle
        library1 = Library(temp_library_file)
        book = Book("Save Test", "Test Author", "987654321")
        library1.add_book_manual(book)
        
        # Yeni kütüphane oluştur ve kitapları yükle
        library2 = Library(temp_library_file)
        
        assert len(library2.books) == 1
        assert library2.books[0].title == "Save Test"
        assert library2.books[0].author == "Test Author"
        assert library2.books[0].isbn == "987654321"
    
    @patch('httpx.Client')
    def test_add_book_api_success(self, mock_client, library):
        """API ile başarılı kitap ekleme testi"""
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "title": "Test API Book",
            "authors": [{"key": "/authors/OL1A"}]
        }
        
        mock_author_response = MagicMock()
        mock_author_response.status_code = 200
        mock_author_response.json.return_value = {"name": "Test API Author"}
        
        mock_client_instance = MagicMock()
        mock_client_instance.get.side_effect = [mock_response, mock_author_response]
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        result = library.add_book("978-0441172719")
        
        assert result is True
        assert len(library.books) == 1
        assert library.books[0].title == "Test API Book"
        assert library.books[0].author == "Test API Author"
        assert library.books[0].isbn == "978-0441172719"
    
    @patch('httpx.Client')
    def test_add_book_api_not_found(self, mock_client, library):
        """API ile bulunamayan kitap testi"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        
        mock_client_instance = MagicMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        result = library.add_book("invalid-isbn")
        
        assert result is False
        assert len(library.books) == 0
    
    @patch('httpx.Client')
    def test_add_book_api_connection_error(self, mock_client, library):
        """API bağlantı hatası testi"""
        from httpx import RequestError
        
        mock_client_instance = MagicMock()
        mock_client_instance.get.side_effect = RequestError("Connection failed")
        mock_client.return_value.__enter__.return_value = mock_client_instance
        
        result = library.add_book("978-0441172719")
        
        assert result is False
        assert len(library.books) == 0
    
    def test_save_books_error_handling(self, library, sample_book):
        """Kayıt hatası yönetimi testi"""
        library.add_book_manual(sample_book)
        
        # Geçersiz dosya yolu ile kaydetmeye çalış
        library.filename = "/invalid/path/library.json"
        
        # Hata fırlatmamalı, sadece hata mesajı yazdırmalı
        try:
            library.save_books()
        except Exception:
            pytest.fail("save_books should handle errors gracefully")
    
    def test_load_books_invalid_json(self, temp_library_file):
        """Geçersiz JSON dosyası yükleme testi"""
        # Geçersiz JSON dosyası oluştur
        with open(temp_library_file, 'w') as f:
            f.write("invalid json content")
        
        library = Library(temp_library_file)
        
        # Boş liste ile başlamalı
        assert library.books == []