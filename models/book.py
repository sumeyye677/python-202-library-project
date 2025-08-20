class Book:
    """Kitap sınıfı - Her bir kitabı temsil eder"""
    
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
    
    def __str__(self) -> str:
        """Kitap bilgilerini okunaklı şekilde döndürür"""
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
    
    def to_dict(self) -> dict:
        """Kitap nesnesini sözlüğe çevirir (JSON kayıt için)"""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Sözlükten kitap nesnesi oluşturur (JSON yükleme için)"""
        return cls(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"]
        )