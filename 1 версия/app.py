import random
import json
import os

class LanguageLearner:
    def __init__(self):
        self.vocabulary_file = "vocabulary.json"
        self.load_vocabulary()
    
    def load_vocabulary(self):
        """Загрузка словаря из файла или создание базового"""
        if os.path.exists(self.vocabulary_file):
            with open(self.vocabulary_file, 'r', encoding='utf-8') as f:
                self.vocabulary = json.load(f)
        else:
            # Базовый словарь
            self.vocabulary = {
                "english": {
                    "hello": "привет",
                    "goodbye": "до свидания",
                    "thank you": "спасибо",
                    "please": "пожалуйста",
                    "yes": "да",
                    "no": "нет",
                    "water": "вода",
                    "food": "еда",
                    "house": "дом",
                    "friend": "друг"
                },
                "spanish": {
                    "hola": "привет",
                    "adiós": "до свидания",
                    "gracias": "спасибо",
                    "por favor": "пожалуйста",
                    "sí": "да",
                    "no": "нет",
                    "agua": "вода",
                    "comida": "еда",
                    "casa": "дом",
                    "amigo": "друг"
                }
            }
            self.save_vocabulary()
    
    def save_vocabulary(self):
        """Сохранение словаря в файл"""
        with open(self.vocabulary_file, 'w', encoding='utf-8') as f:
            json.dump(self.vocabulary, f, ensure_ascii=False, indent=2)
    
    def add_word(self, language, word, translation):
        """Добавление нового слова"""
        if language in self.vocabulary:
            self.vocabulary[language][word] = translation
            self.save_vocabulary()
            print(f"Слово '{word}' добавлено в словарь {language}")
        else:
            print("Неверный язык. Используйте 'english' или 'spanish'")
    
    def practice_translation(self, language):
        """Тренировка перевода"""
        if language not in self.vocabulary:
            print("Неверный язык. Используйте 'english' или 'spanish'")
            return
        
        words = list(self.vocabulary[language].keys())
        if not words:
            print("Словарь пуст!")
            return
        
        score = 0
        total_questions = min(5, len(words))  # Максимум 5 вопросов
        
        print(f"\n--- Тренировка {language} ---")
        for i in range(total_questions):
            word = random.choice(words)
            correct_translation = self.vocabulary[language][word]
            
            print(f"\nСлово: {word}")
            user_answer = input("Перевод: ").strip().lower()
            
            if user_answer == correct_translation.lower():
                print("✓ Правильно!")
                score += 1
            else:
                print(f"✗ Неправильно. Правильный ответ: {correct_translation}")
        
        print(f"\nРезультат: {score}/{total_questions}")
    
    def practice_typing(self, language):
        """Тренировка написания слов"""
        if language not in self.vocabulary:
            print("Неверный язык. Используйте 'english' или 'spanish'")
            return
        
        words = list(self.vocabulary[language].items())
        if not words:
            print("Словарь пуст!")
            return
        
        score = 0
        total_questions = min(5, len(words))
        
        print(f"\n--- Тренировка написания {language} ---")
        for i in range(total_questions):
            word, translation = random.choice(words)
            
            print(f"\nПеревод: {translation}")
            user_answer = input(f"Напишите слово на {language}: ").strip().lower()
            
            if user_answer == word.lower():
                print("✓ Правильно!")
                score += 1
            else:
                print(f"✗ Неправильно. Правильный ответ: {word}")
        
        print(f"\nРезультат: {score}/{total_questions}")
    
    def show_vocabulary(self, language):
        """Показать словарь"""
        if language in self.vocabulary:
            print(f"\n--- Словарь {language} ---")
            for word, translation in self.vocabulary[language].items():
                print(f"{word} - {translation}")
        else:
            print("Неверный язык. Используйте 'english' или 'spanish'")
    
    def run(self):
        """Основной цикл программы"""
        while True:
            print("\n" + "="*50)
            print("        ПРОГРАММА ДЛЯ ИЗУЧЕНИЯ ЯЗЫКОВ")
            print("="*50)
            print("1. Тренировка перевода (английский)")
            print("2. Тренировка перевода (испанский)")
            print("3. Тренировка написания (английский)")
            print("4. Тренировка написания (испанский)")
            print("5. Показать словарь (английский)")
            print("6. Показать словарь (испанский)")
            print("7. Добавить новое слово")
            print("8. Выход")
            print("="*50)
            
            choice = input("Выберите действие (1-8): ").strip()
            
            if choice == "1":
                self.practice_translation("english")
            elif choice == "2":
                self.practice_translation("spanish")
            elif choice == "3":
                self.practice_typing("english")
            elif choice == "4":
                self.practice_typing("spanish")
            elif choice == "5":
                self.show_vocabulary("english")
            elif choice == "6":
                self.show_vocabulary("spanish")
            elif choice == "7":
                self.add_new_word()
            elif choice == "8":
                print("До свидания! Удачи в изучении языков!")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
    
    def add_new_word(self):
        """Добавление нового слова через интерфейс"""
        print("\n--- Добавление нового слова ---")
        language = input("Язык (english/spanish): ").strip().lower()
        word = input("Слово на иностранном языке: ").strip()
        translation = input("Перевод на русский: ").strip()
        
        self.add_word(language, word, translation)

if __name__ == "__main__":
    app = LanguageLearner()
    app.run()