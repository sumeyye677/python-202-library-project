import pytest
import sys
import os

# Test için modülleri import etmek için path ayarı
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.book import Book


class TestBook:
    """Book sınıfı test senaryoları"""
    
    def test_book_creation(self):
        """Kitap nesnesi oluşturma testi"""
        book = Book("1984", "George Orwell", "978-0451524935")
        
        assert book.title == "1984"
        assert book.author == "George Orwell"
        assert book.isbn == "978-0451524935"
    
    def test_book_str_representation(self):
        """Kitap string temsili testi"""
        book = Book("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565")
        expected = "The Great Gatsby by F. Scott Fitzgerald (ISBN: 978-0743273565)"
        
        assert str(book) == expected
    
    def test_book_to_dict(self):
        """Kitap nesnesinin sözlüğe çevrilmesi testi"""
        book = Book("To Kill a Mockingbird", "Harper Lee", "978-0061120084")
        book_dict = book.to_dict()
        
        expected_dict = {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "isbn": "978-0061120084"
        }
        
        assert book_dict == expected_dict
    
    def test_book_from_dict(self):
        """Sözlükten kitap nesnesi oluşturma testi"""
        book_data = {
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "isbn": "978-0141439518"
        }
        
        book = Book.from_dict(book_data)
        
        assert book.title == "Pride and Prejudice"
        assert book.author == "Jane Austen"
        assert book.isbn == "978-0141439518"
    
    def test_book_roundtrip_serialization(self):
        """Kitap nesnesi serileştirme döngü testi"""
        original_book = Book("Dune", "Frank Herbert", "978-0441172719")
        book_dict = original_book.to_dict()
        reconstructed_book = Book.from_dict(book_dict)
        
        assert str(original_book) == str(reconstructed_book)
        assert original_book.title == reconstructed_book.title
        assert original_book.author == reconstructed_book.author
        assert original_book.isbn == reconstructed_book.isbn
    
    def test_book_with_special_characters(self):
        """Özel karakter içeren kitap testi"""
        book = Book("Çelik Taht", "Ahmet Ümit", "978-9750738777")
        
        assert "Çelik Taht" in str(book)
        assert "Ahmet Ümit" in str(book)
    
    def test_book_empty_values(self):
        """Boş değerlerle kitap oluşturma testi"""
        book = Book("", "", "")
        
        assert book.title == ""
        assert book.author == ""
        assert book.isbn == ""
        assert str(book) == " by  (ISBN: )"