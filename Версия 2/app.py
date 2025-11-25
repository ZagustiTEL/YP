import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from database import LanguageDatabase
from datetime import datetime

class LanguageLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Приложение для изучения языков")
        self.root.geometry("1000x800")
        self.root.configure(bg='lightblue')
        
        # Инициализация базы данных
        self.db = LanguageDatabase()
        
        # Создание вкладок
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Создание вкладок
        self.create_languages_tab()
        self.create_words_tab()
        self.create_study_tab()
        self.create_progress_tab()
        
        # Загрузка данных
        self.refresh_languages()
        self.refresh_words()
    
    def create_languages_tab(self):
        """Вкладка для управления языками"""
        self.languages_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.languages_frame, text="Языки")
        
        # Панель добавления языка
        add_frame = ttk.LabelFrame(self.languages_frame, text="Добавить язык", padding=10)
        add_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(add_frame, text="Название языка:").grid(row=0, column=0, sticky='w')
        self.language_name_entry = ttk.Entry(add_frame, width=20)
        self.language_name_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(add_frame, text="Уровень:").grid(row=0, column=2, padx=(20,0))
        self.level_combo = ttk.Combobox(add_frame, values=['beginner', 'intermediate', 'advanced'], width=15)
        self.level_combo.set('beginner')
        self.level_combo.grid(row=0, column=3, padx=5)
        
        ttk.Button(add_frame, text="Добавить язык", command=self.add_language).grid(row=0, column=4, padx=10)
        
        # Список языков
        list_frame = ttk.LabelFrame(self.languages_frame, text="Мои языки", padding=10)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Таблица языков
        columns = ('ID', 'Название', 'Уровень', 'Дата добавления')
        self.languages_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.languages_tree.heading(col, text=col)
            self.languages_tree.column(col, width=100)
        
        self.languages_tree.pack(fill='both', expand=True)
        
        # Кнопки управления
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="Удалить язык", command=self.delete_language).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Обновить", command=self.refresh_languages).pack(side='left', padx=5)
    
    def create_words_tab(self):
        """Вкладка для управления словарем"""
        self.words_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.words_frame, text="Словарь")
        
        # Панель добавления слов
        add_frame = ttk.LabelFrame(self.words_frame, text="Добавить слово", padding=10)
        add_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(add_frame, text="Язык:").grid(row=0, column=0, sticky='w')
        self.language_combo = ttk.Combobox(add_frame, width=20)
        self.language_combo.grid(row=0, column=1, padx=5)
        
        ttk.Label(add_frame, text="Слово:").grid(row=0, column=2, padx=(20,0))
        self.word_entry = ttk.Entry(add_frame, width=20)
        self.word_entry.grid(row=0, column=3, padx=5)
        
        ttk.Label(add_frame, text="Перевод:").grid(row=0, column=4, padx=(20,0))
        self.translation_entry = ttk.Entry(add_frame, width=20)
        self.translation_entry.grid(row=0, column=5, padx=5)
        
        ttk.Label(add_frame, text="Категория:").grid(row=1, column=0, sticky='w', pady=(10,0))
        self.category_entry = ttk.Entry(add_frame, width=20)
        self.category_entry.grid(row=1, column=1, padx=5, pady=(10,0))
        
        ttk.Label(add_frame, text="Сложность:").grid(row=1, column=2, padx=(20,0), pady=(10,0))
        self.difficulty_combo = ttk.Combobox(add_frame, values=['easy', 'medium', 'hard'], width=15)
        self.difficulty_combo.set('easy')
        self.difficulty_combo.grid(row=1, column=3, padx=5, pady=(10,0))
        
        ttk.Button(add_frame, text="Добавить слово", command=self.add_word).grid(row=1, column=4, columnspan=2, padx=10, pady=(10,0))
        
        # Список слов
        list_frame = ttk.LabelFrame(self.words_frame, text="Мои слова", padding=10)
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Таблица слов
        columns = ('ID', 'Язык', 'Слово', 'Перевод', 'Категория', 'Сложность', 'Выучено')
        self.words_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col in columns:
            self.words_tree.heading(col, text=col)
        
        self.words_tree.column('ID', width=50)
        self.words_tree.column('Язык', width=100)
        self.words_tree.column('Слово', width=150)
        self.words_tree.column('Перевод', width=150)
        self.words_tree.column('Категория', width=100)
        self.words_tree.column('Сложность', width=80)
        self.words_tree.column('Выучено', width=80)
        
        self.words_tree.pack(fill='both', expand=True)
        
        # Кнопки управления
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="Отметить выученным", command=self.mark_word_learned).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Удалить слово", command=self.delete_word).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Обновить", command=self.refresh_words).pack(side='left', padx=5)
    
    def create_study_tab(self):
        """Вкладка для изучения слов"""
        self.study_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.study_frame, text="Изучение")
        
        # Выбор языка для изучения
        study_top_frame = ttk.Frame(self.study_frame)
        study_top_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(study_top_frame, text="Выберите язык для изучения:").pack(side='left')
        self.study_language_combo = ttk.Combobox(study_top_frame, width=20)
        self.study_language_combo.pack(side='left', padx=10)
        ttk.Button(study_top_frame, text="Начать изучение", command=self.start_study_session).pack(side='left')
        
        # Область для изучения
        self.study_area = ttk.LabelFrame(self.study_frame, text="Изучение слов", padding=20)
        self.study_area.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.current_word_label = ttk.Label(self.study_area, text="Выберите язык и нажмите 'Начать изучение'", 
                                           font=('Arial', 14))
        self.current_word_label.pack(pady=20)
        
        self.translation_label = ttk.Label(self.study_area, text="", font=('Arial', 12))
        self.translation_label.pack(pady=10)
        
        button_frame = ttk.Frame(self.study_area)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Показать перевод", command=self.show_translation).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Следующее слово", command=self.next_word).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Выучено", command=self.mark_current_learned).pack(side='left', padx=5)
        
        # Переменные для текущей сессии
        self.current_study_words = []
        self.current_word_index = -1
        self.current_word_id = None
    
    def create_progress_tab(self):
        """Вкладка для отслеживания прогресса"""
        self.progress_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.progress_frame, text="Прогресс")
        
        # Статистика
        stats_frame = ttk.LabelFrame(self.progress_frame, text="Статистика", padding=10)
        stats_frame.pack(fill='x', padx=10, pady=10)
        
        self.stats_text = tk.Text(stats_frame, height=10, width=80)
        self.stats_text.pack(fill='both', expand=True)
        
        ttk.Button(stats_frame, text="Обновить статистику", command=self.update_stats).pack(pady=5)
    
    def refresh_languages(self):
        """Обновление списка языков"""
        # Очистка дерева
        for item in self.languages_tree.get_children():
            self.languages_tree.delete(item)
        
        # Загрузка языков
        languages = self.db.get_languages()
        for lang in languages:
            self.languages_tree.insert('', 'end', values=lang)
        
        # Обновление комбобоксов
        language_names = [lang[1] for lang in languages]
        self.language_combo['values'] = language_names
        self.study_language_combo['values'] = language_names
        
        if language_names:
            self.language_combo.set(language_names[0])
            self.study_language_combo.set(language_names[0])
    
    def refresh_words(self):
        """Обновление списка слов"""
        # Очистка дерева
        for item in self.words_tree.get_children():
            self.words_tree.delete(item)
        
        # Загрузка слов
        words = self.db.get_words()
        for word in words:
            learned_text = "Да" if word[6] else "Нет"
            self.words_tree.insert('', 'end', values=(
                word[0], word[9], word[2], word[3], word[4], word[5], learned_text
            ))
    
    def add_language(self):
        """Добавление нового языка"""
        name = self.language_name_entry.get().strip()
        level = self.level_combo.get()
        
        if not name:
            messagebox.showerror("Ошибка", "Введите название языка")
            return
        
        try:
            self.db.add_language(name, level)
            self.language_name_entry.delete(0, 'end')
            self.refresh_languages()
            messagebox.showinfo("Успех", f"Язык '{name}' добавлен")
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Такой язык уже существует")
    
    def delete_language(self):
        """Удаление выбранного языка"""
        selected = self.languages_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите язык для удаления")
            return
        
        language_id = self.languages_tree.item(selected[0])['values'][0]
        language_name = self.languages_tree.item(selected[0])['values'][1]
        
        if messagebox.askyesno("Подтверждение", f"Удалить язык '{language_name}'?"):
            conn = sqlite3.connect(self.db.db_name)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM languages WHERE id = ?', (language_id,))
            conn.commit()
            conn.close()
            
            self.refresh_languages()
            self.refresh_words()
    
    def add_word(self):
        """Добавление нового слова"""
        language_name = self.language_combo.get()
        original_word = self.word_entry.get().strip()
        translation = self.translation_entry.get().strip()
        category = self.category_entry.get().strip() or 'general'
        difficulty = self.difficulty_combo.get()
        
        if not all([language_name, original_word, translation]):
            messagebox.showerror("Ошибка", "Заполните все обязательные поля")
            return
        
        # Получаем ID языка
        languages = self.db.get_languages()
        language_id = None
        for lang in languages:
            if lang[1] == language_name:
                language_id = lang[0]
                break
        
        if not language_id:
            messagebox.showerror("Ошибка", "Язык не найден")
            return
        
        try:
            self.db.add_word(language_id, original_word, translation, category, difficulty)
            self.word_entry.delete(0, 'end')
            self.translation_entry.delete(0, 'end')
            self.category_entry.delete(0, 'end')
            self.refresh_words()
            messagebox.showinfo("Успех", "Слово добавлено")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при добавлении слова: {str(e)}")
    
    def mark_word_learned(self):
        """Отметка слова как выученного"""
        selected = self.words_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите слово")
            return
        
        word_id = self.words_tree.item(selected[0])['values'][0]
        self.db.mark_word_learned(word_id)
        self.refresh_words()
        messagebox.showinfo("Успех", "Слово отмечено как выученное")
    
    def delete_word(self):
        """Удаление выбранного слова"""
        selected = self.words_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите слово для удаления")
            return
        
        word_id = self.words_tree.item(selected[0])['values'][0]
        word_text = self.words_tree.item(selected[0])['values'][2]
        
        if messagebox.askyesno("Подтверждение", f"Удалить слово '{word_text}'?"):
            conn = sqlite3.connect(self.db.db_name)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM words WHERE id = ?', (word_id,))
            conn.commit()
            conn.close()
            
            self.refresh_words()
    
    def start_study_session(self):
        """Начало сессии изучения"""
        language_name = self.study_language_combo.get()
        if not language_name:
            messagebox.showwarning("Предупреждение", "Выберите язык")
            return
        
        # Получаем ID языка
        languages = self.db.get_languages()
        language_id = None
        for lang in languages:
            if lang[1] == language_name:
                language_id = lang[0]
                break
        
        if not language_id:
            messagebox.showerror("Ошибка", "Язык не найден")
            return
        
        # Получаем слова для изучения
        words = self.db.get_words(language_id)
        if not words:
            messagebox.showinfo("Информация", "Нет слов для изучения")
            return
        
        self.current_study_words = [word for word in words if not word[6]]  # Только не выученные
        if not self.current_study_words:
            messagebox.showinfo("Поздравляем!", "Все слова выучены!")
            return
        
        self.current_word_index = -1
        self.next_word()
    
    def next_word(self):
        """Переход к следующему слову"""
        if not self.current_study_words:
            self.current_word_label.config(text="Нет слов для изучения")
            self.translation_label.config(text="")
            return
        
        self.current_word_index = (self.current_word_index + 1) % len(self.current_study_words)
        current_word = self.current_study_words[self.current_word_index]
        
        self.current_word_id = current_word[0]
        self.current_word_label.config(text=f"Слово: {current_word[2]}")
        self.translation_label.config(text="")
    
    def show_translation(self):
        """Показать перевод текущего слова"""
        if self.current_word_index >= 0 and self.current_study_words:
            current_word = self.current_study_words[self.current_word_index]
            self.translation_label.config(text=f"Перевод: {current_word[3]}")
    
    def mark_current_learned(self):
        """Отметить текущее слово как выученное"""
        if self.current_word_id:
            self.db.mark_word_learned(self.current_word_id)
            # Удаляем слово из текущего списка
            self.current_study_words = [word for word in self.current_study_words if word[0] != self.current_word_id]
            self.next_word()
            self.refresh_words()
    
    def update_stats(self):
        """Обновление статистики"""
        self.stats_text.delete(1.0, tk.END)
        
        languages = self.db.get_languages()
        total_words = 0
        learned_words = 0
        
        stats_text = "=== СТАТИСТИКА ИЗУЧЕНИЯ ===\n\n"
        
        for lang in languages:
            lang_id, lang_name, level, created_date = lang
            words = self.db.get_words(lang_id)
            
            lang_total = len(words)
            lang_learned = len([word for word in words if word[6]])
            
            total_words += lang_total
            learned_words += lang_learned
            
            stats_text += f"Язык: {lang_name}\n"
            stats_text += f"Уровень: {level}\n"
            stats_text += f"Всего слов: {lang_total}\n"
            stats_text += f"Выучено слов: {lang_learned}\n"
            stats_text += f"Прогресс: {lang_learned}/{lang_total} ({lang_learned/lang_total*100:.1f}%)\n"
            stats_text += "-" * 40 + "\n\n"
        
        if total_words > 0:
            overall_progress = learned_words / total_words * 100
            stats_text += f"ОБЩИЙ ПРОГРЕСС: {learned_words}/{total_words} ({overall_progress:.1f}%)"
        
        self.stats_text.insert(1.0, stats_text)

def main():
    root = tk.Tk()
    app = LanguageLearningApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()