"""Модуль валидации данных книги"""
from typing import Tuple, Optional


class BookValidator:
    """Класс для валидации данных книги"""
    
    # Доступные жанры
    GENRES = ['Роман', 'Детектив', 'Фантастика', 'Научная литература', 
              'Поэзия', 'Драма', 'Комедия', 'Приключения', 'Ужасы', 'Другое']
    
    @staticmethod
    def validate_title(title: str) -> Tuple[bool, Optional[str]]:
        """Проверка названия книги"""
        if not title or not title.strip():
            return False, "Название книги не может быть пустым"
        if len(title) > 100:
            return False, "Название не должно превышать 100 символов"
        return True, None
    
    @staticmethod
    def validate_author(author: str) -> Tuple[bool, Optional[str]]:
        """Проверка автора"""
        if not author or not author.strip():
            return False, "Имя автора не может быть пустым"
        if len(author) > 50:
            return False, "Имя автора не должно превышать 50 символов"
        return True, None
    
    @staticmethod
    def validate_genre(genre: str) -> Tuple[bool, Optional[str]]:
        """Проверка жанра"""
        if not genre:
            return False, "Выберите жанр"
        if genre not in BookValidator.GENRES:
            return False, f"Недопустимый жанр. Доступны: {', '.join(BookValidator.GENRES)}"
        return True, None
    
    @staticmethod
    def validate_pages(pages_str: str) -> Tuple[bool, Optional[str], Optional[int]]:
        """Проверка количества страниц"""
        if not pages_str or not pages_str.strip():
            return False, "Количество страниц не может быть пустым", None
        
        try:
            pages = int(pages_str)
            if pages <= 0:
                return False, "Количество страниц должно быть положительным числом", None
            if pages > 10000:
                return False, "Количество страниц не может превышать 10 000", None
            return True, None, pages
        except ValueError:
            return False, "Введите целое число (например: 350)", None