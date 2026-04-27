"""Модуль тестирования трекера книг"""
import unittest
import tempfile
import os
from models import Book
from validators import BookValidator
from storage import Storage


class TestBookValidator(unittest.TestCase):
    """Тесты валидатора книг"""
    
    def test_validate_title_positive(self):
        """Позитивный тест: корректные названия"""
        valid_titles = ["Война и мир", "Преступление и наказание", "А"]
        for title in valid_titles:
            is_valid, error = BookValidator.validate_title(title)
            self.assertTrue(is_valid)
            self.assertIsNone(error)
    
    def test_validate_title_negative(self):
        """Негативный тест: некорректные названия"""
        invalid_titles = ["", "   ", "A" * 101]
        for title in invalid_titles:
            is_valid, error = BookValidator.validate_title(title)
            self.assertFalse(is_valid)
            self.assertIsNotNone(error)
    
    def test_validate_author_positive(self):
        """Позитивный тест: корректные авторы"""
        valid_authors = ["Лев Толстой", "Ф.М. Достоевский", "Джоан Роулинг"]
        for author in valid_authors:
            is_valid, error = BookValidator.validate_author(author)
            self.assertTrue(is_valid)
    
    def test_validate_author_negative(self):
        """Негативный тест: некорректные авторы"""
        invalid_authors = ["", "   ", "A" * 51]
        for author in invalid_authors:
            is_valid, error = BookValidator.validate_author(author)
            self.assertFalse(is_valid)
    
    def test_validate_pages_positive(self):
        """Позитивный тест: корректное количество страниц"""
        valid_pages = ["100", "500", "1", "10000"]
        for pages in valid_pages:
            is_valid, error, value = BookValidator.validate_pages(pages)
            self.assertTrue(is_valid)
            self.assertGreater(value, 0)
    
    def test_validate_pages_negative(self):
        """Негативный тест: некорректное количество страниц"""
        invalid_pages = ["0", "-50", "abc", "", "10001"]
        for pages in invalid_pages:
            is_valid, error, value = BookValidator.validate_pages(pages)
            self.assertFalse(is_valid)
    
    def test_validate_genre(self):
        """Тест валидации жанров"""
        # Позитивные
        for genre in BookValidator.GENRES:
            is_valid, error = BookValidator.validate_genre(genre)
            self.assertTrue(is_valid)
        
        # Негативные
        is_valid, error = BookValidator.validate_genre("Несуществующий жанр")
        self.assertFalse(is_valid)
        
        is_valid, error = BookValidator.validate_genre("")
        self.assertFalse(is_valid)


class TestStorage(unittest.TestCase):
    """Тесты хранилища"""
    
    def setUp(self):
        """Подготовка тестового окружения"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.storage = Storage(self.temp_file.name)
    
    def tearDown(self):
        """Очистка после тестов"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_save_and_load(self):
        """Тест сохранения и загрузки"""
        books = [
            Book("Война и мир", "Лев Толстой", "Роман", 1300),
            Book("Преступление и наказание", "Достоевский", "Роман", 600)
        ]
        
        # Сохранение
        result = self.storage.save(books)
        self.assertTrue(result)
        
        # Загрузка
        loaded = self.storage.load()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].title, "Война и мир")
        self.assertEqual(loaded[0].pages, 1300)
    
    def test_load_empty_file(self):
        """Тест загрузки из пустого файла"""
        books = self.storage.load()
        self.assertEqual(books, [])
    
    def test_save_empty_list(self):
        """Тест сохранения пустого списка"""
        result = self.storage.save([])
        self.assertTrue(result)
        
        loaded = self.storage.load()
        self.assertEqual(loaded, [])


class TestBookModel(unittest.TestCase):
    """Тесты модели книги"""
    
    def test_to_dict(self):
        """Тест преобразования в словарь"""
        book = Book("Мастер и Маргарита", "Булгаков", "Роман", 400)
        data = book.to_dict()
        
        self.assertEqual(data['title'], "Мастер и Маргарита")
        self.assertEqual(data['author'], "Булгаков")
        self.assertEqual(data['genre'], "Роман")
        self.assertEqual(data['pages'], 400)
    
    def test_from_dict(self):
        """Тест создания из словаря"""
        data = {
            'title': "1984",
            'author': "Джордж Оруэлл",
            'genre': "Фантастика",
            'pages': 328
        }
        book = Book.from_dict(data)
        
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "Джордж Оруэлл")
        self.assertEqual(book.genre, "Фантастика")
        self.assertEqual(book.pages, 328)
    
    def test_string_representation(self):
        """Тест строкового представления"""
        book = Book("Тест", "Автор", "Жанр", 100)
        str_repr = str(book)
        
        self.assertIn("Тест", str_repr)
        self.assertIn("Автор", str_repr)
        self.assertIn("100", str_repr)


def run_all_tests():
    """Запуск всех тестов"""
    print("\n" + "="*60)
    print("🧪 ЗАПУСК ТЕСТИРОВАНИЯ BOOK TRACKER")
    print("="*60)
    
    # Создание загрузчика тестов
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Добавление всех тестов
    suite.addTests(loader.loadTestsFromTestCase(TestBookValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestStorage))
    suite.addTests(loader.loadTestsFromTestCase(TestBookModel))
    
    # Запуск тестов
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Вывод результатов
    print("\n" + "="*60)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("="*60)
    print(f"✅ Успешно пройдено: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Ошибок: {len(result.errors)}")
    print(f"⚠️  Падений: {len(result.failures)}")
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)