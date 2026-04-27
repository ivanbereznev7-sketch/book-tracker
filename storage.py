"""Модуль для работы с JSON-хранилищем"""
import json
import os
from typing import List
from models import Book


class Storage:
    """Класс для сохранения и загрузки данных"""
    
    def __init__(self, filename: str = "books.json"):
        self.filename = filename
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Создание файла если не существует"""
        if not os.path.exists(self.filename):
            self.save([])
    
    def load(self) -> List[Book]:
        """Загрузка книг из файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Book.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save(self, books: List[Book]) -> bool:
        """Сохранение книг в файл"""
        try:
            data = [book.to_dict() for book in books]
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False