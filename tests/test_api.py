import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# Test için modülleri import etmek için path ayarı
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from api import app
from models.book import Book


class TestAPI:
    """FastAPI endpoint testleri"""
    
    @pytest.fixture
    def client(self):
        """Test client'ı"""
        return TestClient(app)
    
    def test_root_endpoint(self, client):
        """Ana endpoint testi"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"
    
    def test_health_endpoint(self, client):
        """Sağlık kontrolü endpoint testi"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "total_books" in data
    
    def test_get_books_empty(self, client):
        """Boş kütüphane listeleme testi"""
        # Önce kütüphaneyi temizle
        app.state.library = None
        from models.library import Library
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.close()
        
        # Yeni boş kütüphane oluştur
        from api import library
        library.books = []
        
        response = client.get("/books")
        
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    @patch('models.library.Library.add_book')
    def test_add_book_success(self, mock_add_book, client):
        """Başarılı kitap ekleme testi"""
        mock_add_book.return_value = True
        
        # Mock library.find_book to return the added book
        with patch('models.library.Library.find_book') as mock_find:
            mock_book = Book("Test Book", "Test Author", "978-0441172719")
            mock_find.return_value = mock_book
            
            response = client.post("/books", json={"isbn": "978-0441172719"})
            
            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "Test Book"
            assert data["author"] == "Test Author"
            assert data["isbn"] == "978-0441172719"
    
    def test_add_book_empty_isbn(self, client):
        """Boş ISBN ile kitap ekleme testi"""
        response = client.post("/books", json={"isbn": ""})
        
        assert response.status_code == 400
        data = response.json()
        assert "ISBN boş olamaz" in data["detail"]
    
    @patch('models.library.Library.find_book')
    def test_add_book_duplicate(self, mock_find_book, client):
        """Duplicate kitap ekleme testi"""
        mock_book = Book("Existing Book", "Existing Author", "978-0441172719")
        mock_find_book.return_value = mock_book
        
        response = client.post("/books", json={"isbn": "978-0441172719"})
        
        assert response.status_code == 409
        data = response.json()
        assert "zaten mevcut" in data["detail"]
    
    @patch('models.library.Library.add_book')
    @patch('models.library.Library.find_book')
    def test_add_book_api_failure(self, mock_find_book, mock_add_book, client):
        """API hatası ile kitap ekleme testi"""
        mock_find_book.side_effect = [None, None]  # İlk check'te yok, ekledikten sonra da yok
        mock_add_book.return_value = False
        
        response = client.post("/books", json={"isbn": "978-0441172719"})
        
        assert response.status_code == 404
        data = response.json()
        assert "bulunamadı" in data["detail"] or "API hatası" in data["detail"]
    
    @patch('models.library.Library.find_book')
    def test_get_book_success(self, mock_find_book, client):
        """Başarılı kitap bulma testi"""
        mock_book = Book("Found Book", "Found Author", "978-0441172719")
        mock_find_book.return_value = mock_book
        
        response = client.get("/books/978-0441172719")
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Found Book"
        assert data["author"] == "Found Author"
        assert data["isbn"] == "978-0441172719"
    
    @patch('models.library.Library.find_book')
    def test_get_book_not_found(self, mock_find_book, client):
        """Bulunamayan kitap testi"""
        mock_find_book.return_value = None
        
        response = client.get("/books/nonexistent")
        
        assert response.status_code == 404
        data = response.json()
        assert "bulunamadı" in data["detail"]
    
    def test_get_book_empty_isbn(self, client):
        """Boş ISBN ile kitap arama testi"""
        response = client.get("/books/")
        
        # Bu durumda endpoint bulunamaz
        assert response.status_code == 404
    
    @patch('models.library.Library.find_book')
    @patch('models.library.Library.remove_book')
    def test_delete_book_success(self, mock_remove_book, mock_find_book, client):
        """Başarılı kitap silme testi"""
        mock_book = Book("Book to Delete", "Author", "978-0441172719")
        mock_find_book.return_value = mock_book
        mock_remove_book.return_value = True
        
        response = client.delete("/books/978-0441172719")
        
        assert response.status_code == 200
        data = response.json()
        assert "başarıyla silindi" in data["message"]
        assert "Book to Delete" in data["message"]
    
    @patch('models.library.Library.find_book')
    def test_delete_book_not_found(self, mock_find_book, client):
        """Olmayan kitap silme testi"""
        mock_find_book.return_value = None
        
        response = client.delete("/books/nonexistent")
        
        assert response.status_code == 404
        data = response.json()
        assert "bulunamadı" in data["detail"]
    
    @patch('models.library.Library.find_book')
    @patch('models.library.Library.remove_book')
    def test_delete_book_failure(self, mock_remove_book, mock_find_book, client):
        """Kitap silme hatası testi"""
        mock_book = Book("Book to Delete", "Author", "978-0441172719")
        mock_find_book.return_value = mock_book
        mock_remove_book.return_value = False
        
        response = client.delete("/books/978-0441172719")
        
        assert response.status_code == 500
        data = response.json()
        assert "hata oluştu" in data["detail"]
    
    def test_delete_book_empty_isbn(self, client):
        """Boş ISBN ile kitap silme testi"""
        response = client.delete("/books/")
        
        # Bu durumda endpoint bulunamaz
        assert response.status_code == 404
    
    @patch('models.library.Library.list_books')
    def test_get_books_with_data(self, mock_list_books, client):
        """Kitap listesi dolu testi"""
        mock_books = [
            Book("Book 1", "Author 1", "111"),
            Book("Book 2", "Author 2", "222")
        ]
        mock_list_books.return_value = mock_books
        
        response = client.get("/books")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Book 1"
        assert data[1]["title"] == "Book 2"
    
    def test_invalid_json_request(self, client):
        """Geçersiz JSON isteği testi"""
        response = client.post("/books", data="invalid json")
        
        assert response.status_code == 422  # Unprocessable Entity