"""Модель данных для книги"""
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class Book:
    """Класс representing книгу"""
    title: str       # Название книги
    author: str      # Автор
    genre: str       # Жанр
    pages: int       # Количество страниц
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь для JSON"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Book':
        """Создание книги из словаря"""
        return cls(
            title=data['title'],
            author=data['author'],
            genre=data['genre'],
            pages=int(data['pages'])
        )
    
    def __str__(self) -> str:
        return f"'{self.title}' - {self.author} ({self.pages} стр., {self.genre})"