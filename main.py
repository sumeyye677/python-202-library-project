#!/usr/bin/env python3
"""
Kütüphane Yönetim Sistemi - Terminal Uygulaması
Aşama 1: OOP ile terminal uygulaması
Aşama 2: Harici API entegrasyonu
"""

from models import Book, Library


def display_menu():
    """Ana menüyü gösterir"""
    print("\n" + "="*50)
    print("📚 KÜTÜPHANİ YÖNETİM SİSTEMİ")
    print("="*50)
    print("1. Kitap Ekle (ISBN ile)")
    print("2. Kitap Ekle (Manuel)")
    print("3. Kitap Sil")
    print("4. Kitapları Listele")
    print("5. Kitap Ara")
    print("6. Çıkış")
    print("-"*50)


def add_book_by_isbn(library: Library):
    """ISBN ile kitap ekler (API kullanarak)"""
    isbn = input("📖 Kitap ISBN'ini giriniz: ").strip()
    if not isbn:
        print("❌ ISBN boş olamaz!")
        return
    
    print("🔍 Kitap bilgileri API'den çekiliyor...")
    library.add_book(isbn)


def add_book_manual(library: Library):
    """Manuel kitap ekleme"""
    title = input("📖 Kitap başlığı: ").strip()
    author = input("👤 Yazar: ").strip()
    isbn = input("🔢 ISBN: ").strip()
    
    if not all([title, author, isbn]):
        print("❌ Tüm alanları doldurunuz!")
        return
    
    book = Book(title=title, author=author, isbn=isbn)
    library.add_book_manual(book)


def remove_book(library: Library):
    """Kitap siler"""
    isbn = input("🗑️  Silinecek kitabın ISBN'ini giriniz: ").strip()
    if not isbn:
        print("❌ ISBN boş olamaz!")
        return
    
    library.remove_book(isbn)


def list_books(library: Library):
    """Kitapları listeler"""
    books = library.list_books()
    if not books:
        print("📚 Kütüphanede henüz kitap bulunmuyor.")
        return
    
    print(f"\n📚 KÜTÜPHANEDEKİ KİTAPLAR ({len(books)} adet):")
    print("-"*80)
    for i, book in enumerate(books, 1):
        print(f"{i:2d}. {book}")


def search_book(library: Library):
    """Kitap arar"""
    isbn = input("🔍 Aranacak kitabın ISBN'ini giriniz: ").strip()
    if not isbn:
        print("❌ ISBN boş olamaz!")
        return
    
    book = library.find_book(isbn)
    if book:
        print(f"✅ Kitap bulundu: {book}")
    else:
        print("❌ Kitap bulunamadı!")


def main():
    """Ana uygulama döngüsü"""
    print("🚀 Kütüphane Yönetim Sistemi başlatılıyor...")
    library = Library()
    
    while True:
        try:
            display_menu()
            choice = input("Seçiminizi yapınız (1-6): ").strip()
            
            if choice == "1":
                add_book_by_isbn(library)
            elif choice == "2":
                add_book_manual(library)
            elif choice == "3":
                remove_book(library)
            elif choice == "4":
                list_books(library)
            elif choice == "5":
                search_book(library)
            elif choice == "6":
                print("👋 Güle güle!")
                break
            else:
                print("❌ Geçersiz seçim! Lütfen 1-6 arası bir sayı giriniz.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Program sonlandırıldı. Güle güle!")
            break
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {e}")


if __name__ == "__main__":
    main()