"""Графический интерфейс трекера книг"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List

from models import Book
from storage import Storage
from validators import BookValidator


class BookTrackerApp:
    """Основной класс приложения"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("📚 Book Tracker - Трекер прочитанных книг")
        self.root.geometry("1000x650")
        self.root.resizable(True, True)
        
        # Инициализация хранилища
        self.storage = Storage()
        self.books = self.storage.load()
        
        # Настройка цветов
        self.colors = {
            'bg': '#f5f5f5',
            'primary': '#4A90E2',
            'success': '#27AE60',
            'danger': '#E74C3C',
            'warning': '#F39C12'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Создание интерфейса
        self._create_widgets()
        
        # Обновление списка
        self.refresh_list()
        
        # Обработка закрытия
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def _create_widgets(self):
        """Создание всех виджетов"""
        # Верхняя панель с заголовком
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="📖 Трекер прочитанных книг",
            font=("Arial", 22, "bold"),
            fg="white",
            bg=self.colors['primary']
        )
        title_label.pack(pady=20)
        
        # Основной контейнер
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Левая панель - форма добавления
        self._create_form_panel(main_container)
        
        # Правая панель - список и фильтрация
        self._create_list_panel(main_container)
        
        # Статусная строка
        self.status_label = tk.Label(
            self.root,
            text="Готов к работе",
            bg=self.colors['bg'],
            font=("Arial", 9),
            anchor=tk.W
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=5)
    
    def _create_form_panel(self, parent):
        """Создание панели с формой добавления книги"""
        form_frame = tk.Frame(parent, bg=self.colors['bg'], width=350)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        form_frame.pack_propagate(False)
        
        # Заголовок формы
        tk.Label(
            form_frame,
            text="➕ Добавить новую книгу",
            font=("Arial", 14, "bold"),
            bg=self.colors['bg']
        ).pack(pady=(0, 15))
        
        # Поле названия
        self._create_input_field(form_frame, "Название книги:", "title")
        
        # Поле автора
        self._create_input_field(form_frame, "Автор:", "author")
        
        # Поле жанра (выпадающий список)
        genre_frame = tk.Frame(form_frame, bg=self.colors['bg'])
        genre_frame.pack(fill=tk.X, pady=5)
        tk.Label(genre_frame, text="Жанр:", bg=self.colors['bg'], font=("Arial", 10)).pack(anchor=tk.W)
        self.genre_var = tk.StringVar()
        self.genre_combo = ttk.Combobox(
            genre_frame,
            textvariable=self.genre_var,
            values=BookValidator.GENRES,
            state="readonly",
            font=("Arial", 10)
        )
        self.genre_combo.pack(fill=tk.X, pady=5)
        self.genre_combo.set(BookValidator.GENRES[0])
        
        # Поле страниц
        self._create_input_field(form_frame, "Количество страниц:", "pages")
        
        # Кнопка добавления
        self.add_btn = tk.Button(
            form_frame,
            text="📚 Добавить книгу",
            bg=self.colors['success'],
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            command=self.add_book
        )
        self.add_btn.pack(fill=tk.X, pady=20)
        
        # Информационная панель
        info_frame = tk.Frame(form_frame, bg="white", relief=tk.RAISED, bd=1)
        info_frame.pack(fill=tk.X, pady=10)
        
        self.total_label = tk.Label(
            info_frame,
            text="📊 Всего книг: 0",
            font=("Arial", 11, "bold"),
            bg="white",
            fg=self.colors['primary']
        )
        self.total_label.pack(pady=10)
        
        # Подсказки
        self._add_tooltips()
    
    def _create_input_field(self, parent, label_text, attr_name):
        """Создание поля ввода"""
        frame = tk.Frame(parent, bg=self.colors['bg'])
        frame.pack(fill=tk.X, pady=5)
        
        tk.Label(frame, text=label_text, bg=self.colors['bg'], font=("Arial", 10)).pack(anchor=tk.W)
        
        entry = tk.Entry(frame, font=("Arial", 11), relief=tk.SOLID, bd=1)
        entry.pack(fill=tk.X, pady=5)
        entry.configure(highlightthickness=1, highlightcolor=self.colors['primary'])
        
        setattr(self, f"{attr_name}_entry", entry)
    
    def _create_list_panel(self, parent):
        """Создание панели со списком книг и фильтрацией"""
        right_panel = tk.Frame(parent, bg=self.colors['bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Панель фильтрации
        filter_frame = tk.Frame(right_panel, bg=self.colors['bg'])
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(filter_frame, text="🔍 Фильтр по жанру:", bg=self.colors['bg'], font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        self.filter_genre_var = tk.StringVar(value="Все")
        self.filter_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_genre_var,
            values=["Все"] + BookValidator.GENRES,
            state="readonly",
            width=15
        )
        self.filter_combo.pack(side=tk.LEFT, padx=5)
        self.filter_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_filters())
        
        # Фильтр по страницам
        tk.Label(filter_frame, text="Страниц >", bg=self.colors['bg'], font=("Arial", 10)).pack(side=tk.LEFT, padx=(20, 5))
        
        self.pages_filter_var = tk.StringVar()
        self.pages_filter_entry = tk.Entry(filter_frame, textvariable=self.pages_filter_var, width=8, font=("Arial", 10))
        self.pages_filter_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            filter_frame,
            text="Применить фильтр",
            command=self.apply_filters,
            bg=self.colors['primary'],
            fg="white",
            cursor="hand2",
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            filter_frame,
            text="Сбросить фильтры",
            command=self.reset_filters,
            bg=self.colors['warning'],
            fg="white",
            cursor="hand2",
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=5)
        
        # Таблица книг
        columns = ("ID", "Название", "Автор", "Жанр", "Страницы")
        self.tree = ttk.Treeview(right_panel, columns=columns, show="headings", height=18)
        
        # Настройка колонок
        self.tree.heading("ID", text="№")
        self.tree.heading("Название", text="Название книги")
        self.tree.heading("Автор", text="Автор")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Страницы", text="Страниц")
        
        self.tree.column("ID", width=40)
        self.tree.column("Название", width=250)
        self.tree.column("Автор", width=150)
        self.tree.column("Жанр", width=120)
        self.tree.column("Страницы", width=80)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(right_panel, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопка удаления
        self.delete_btn = tk.Button(
            right_panel,
            text="🗑 Удалить выбранную книгу",
            bg=self.colors['danger'],
            fg="white",
            font=("Arial", 10),
            cursor="hand2",
            command=self.delete_book
        )
        self.delete_btn.pack(pady=10)
    
    def _add_tooltips(self):
        """Добавление подсказок"""
        self._create_tooltip(self.title_entry, "Введите название книги")
        self._create_tooltip(self.author_entry, "Введите ФИО автора")
        self._create_tooltip(self.pages_entry, "Только целое положительное число")
    
    def _create_tooltip(self, widget, text):
        """Создание всплывающей подсказки"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, background="#ffffe0", 
                           relief="solid", borderwidth=1, font=("Arial", 9))
            label.pack()
            widget.tooltip = tooltip
        
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
        
        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)
    
    def add_book(self):
        """Добавление новой книги"""
        # Валидация названия
        title = self.title_entry.get().strip()
        is_valid, error = BookValidator.validate_title(title)
        if not is_valid:
            messagebox.showerror("Ошибка валидации", error)
            return
        
        # Валидация автора
        author = self.author_entry.get().strip()
        is_valid, error = BookValidator.validate_author(author)
        if not is_valid:
            messagebox.showerror("Ошибка валидации", error)
            return
        
        # Валидация жанра
        genre = self.genre_var.get()
        is_valid, error = BookValidator.validate_genre(genre)
        if not is_valid:
            messagebox.showerror("Ошибка валидации", error)
            return
        
        # Валидация страниц
        pages_str = self.pages_entry.get().strip()
        is_valid, error, pages = BookValidator.validate_pages(pages_str)
        if not is_valid:
            messagebox.showerror("Ошибка валидации", error)
            return
        
        # Создание книги
        book = Book(title, author, genre, pages)
        self.books.append(book)
        
        # Сохранение
        if self.storage.save(self.books):
            messagebox.showinfo("Успех", f"✅ Книга '{title}' успешно добавлена!")
            self.clear_form()
            self.refresh_list()
            self.status_label.config(text=f"Добавлена книга: {title}")
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить данные")
    
    def clear_form(self):
        """Очистка формы"""
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_combo.set(BookValidator.GENRES[0])
        self.pages_entry.delete(0, tk.END)
    
    def apply_filters(self):
        """Применение фильтров"""
        self.refresh_list()
    
    def reset_filters(self):
        """Сброс фильтров"""
        self.filter_genre_var.set("Все")
        self.pages_filter_var.set("")
        self.refresh_list()
        self.status_label.config(text="Фильтры сброшены")
    
    def refresh_list(self):
        """Обновление списка книг с применением фильтров"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получение фильтров
        filter_genre = self.filter_genre_var.get()
        pages_filter_str = self.pages_filter_var.get().strip()
        
        # Фильтрация
        filtered_books = self.books.copy()
        
        # Фильтр по жанру
        if filter_genre != "Все":
            filtered_books = [b for b in filtered_books if b.genre == filter_genre]
        
        # Фильтр по страницам
        if pages_filter_str:
            try:
                min_pages = int(pages_filter_str)
                filtered_books = [b for b in filtered_books if b.pages > min_pages]
            except ValueError:
                if pages_filter_str:  # Если не число, показываем предупреждение
                    messagebox.showwarning("Предупреждение", "Количество страниц должно быть числом")
        
        # Заполнение таблицы
        for idx, book in enumerate(filtered_books, 1):
            self.tree.insert("", tk.END, values=(
                idx,
                book.title,
                book.author,
                book.genre,
                book.pages
            ), tags=(book,))
        
        # Обновление счетчика
        self.total_label.config(text=f"📊 Всего книг: {len(filtered_books)}")
        
        # Обновление статуса
        status_text = f"Показано книг: {len(filtered_books)}"
        if filter_genre != "Все":
            status_text += f" | Жанр: {filter_genre}"
        if pages_filter_str:
            status_text += f" | Страниц > {pages_filter_str}"
        
        self.status_label.config(text=status_text)
    
    def delete_book(self):
        """Удаление выбранной книги"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите книгу для удаления")
            return
        
        # Получение названия книги
        item = self.tree.item(selected[0])
        values = item['values']
        if not values:
            return
        
        book_title = values[1]
        
        # Поиск и удаление книги
        for book in self.books:
            if book.title == book_title:
                if messagebox.askyesno("Подтверждение", 
                                     f"Удалить книгу?\n\n{book}"):
                    self.books.remove(book)
                    if self.storage.save(self.books):
                        messagebox.showinfo("Успех", "✅ Книга удалена")
                        self.refresh_list()
                        self.status_label.config(text=f"Удалена книга: {book_title}")
                    else:
                        messagebox.showerror("Ошибка", "Не удалось сохранить изменения")
                break
    
    def on_closing(self):
        """Обработка закрытия окна"""
        if messagebox.askokcancel("Выход", "Сохранить изменения перед выходом?"):
            if self.storage.save(self.books):
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()