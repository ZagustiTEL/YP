import sqlite3
from datetime import datetime

class LanguageDatabase:
    def __init__(self, db_name='language_learning.db'):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Таблица языков
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS languages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                level TEXT DEFAULT 'beginner',
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица слов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language_id INTEGER,
                original_word TEXT NOT NULL,
                translation TEXT NOT NULL,
                category TEXT,
                difficulty TEXT DEFAULT 'easy',
                learned BOOLEAN DEFAULT FALSE,
                last_reviewed TIMESTAMP,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (language_id) REFERENCES languages (id)
            )
        ''')
        
        # Таблица прогресса
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                language_id INTEGER,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                words_learned INTEGER DEFAULT 0,
                time_studied INTEGER DEFAULT 0,
                FOREIGN KEY (language_id) REFERENCES languages (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"База данных {self.db_name} инициализирована!")
    
    def add_language(self, name, level='beginner'):
        """Добавление нового языка"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO languages (name, level) VALUES (?, ?)',
            (name, level)
        )
        conn.commit()
        conn.close()
        print(f"Язык '{name}' добавлен!")
    
    def get_languages(self):
        """Получение списка всех языков"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM languages')
        languages = cursor.fetchall()
        conn.close()
        return languages
    
    def add_word(self, language_id, original_word, translation, category='general', difficulty='easy'):
        """Добавление нового слова"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO words (language_id, original_word, translation, category, difficulty) 
               VALUES (?, ?, ?, ?, ?)''',
            (language_id, original_word, translation, category, difficulty)
        )
        conn.commit()
        conn.close()
        print(f"Слово '{original_word}' добавлено!")
    
    def get_words(self, language_id=None):
        """Получение слов (всех или для конкретного языка)"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        if language_id:
            cursor.execute('''
                SELECT w.*, l.name as language_name 
                FROM words w 
                JOIN languages l ON w.language_id = l.id 
                WHERE w.language_id = ?
            ''', (language_id,))
        else:
            cursor.execute('''
                SELECT w.*, l.name as language_name 
                FROM words w 
                JOIN languages l ON w.language_id = l.id
            ''')
        
        words = cursor.fetchall()
        conn.close()
        return words
    
    def mark_word_learned(self, word_id):
        """Отметить слово как выученное"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE words SET learned = TRUE, last_reviewed = ? WHERE id = ?',
            (datetime.now(), word_id)
        )
        conn.commit()
        conn.close()
        print(f"Слово с ID {word_id} отмечено как выученное!")
    
    def add_progress(self, language_id, words_learned=0, time_studied=0):
        """Добавление записи о прогрессе"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO progress (language_id, words_learned, time_studied) VALUES (?, ?, ?)',
            (language_id, words_learned, time_studied)
        )
        conn.commit()
        conn.close()
        print(f"Прогресс для языка ID {language_id} добавлен!")
    
    def get_progress(self, language_id):
        """Получение прогресса по языку"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM progress WHERE language_id = ? ORDER BY date',
            (language_id,)
        )
        progress = cursor.fetchall()
        conn.close()
        return progress

# ДОБАВЬТЕ ЭТОТ КОД ДЛЯ СОЗДАНИЯ БАЗЫ ДАННЫХ
if __name__ == "__main__":
    # Создаем экземпляр класса - это вызовет создание БД
    db = LanguageDatabase()
    
    # Добавляем тестовые данные
    db.add_language("Английский")
    db.add_language("Испанский")
    
    db.add_word(1, "hello", "привет")
    db.add_word(1, "book", "книга")
    db.add_word(2, "hola", "привет")
    
    # Проверяем
    languages = db.get_languages()
    words = db.get_words()
    
