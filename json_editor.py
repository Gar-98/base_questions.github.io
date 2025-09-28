import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QPushButton, QLineEdit, QTextEdit, QComboBox, 
                            QLabel, QMessageBox, QTreeWidget, QTreeWidgetItem,
                            QTabWidget, QFormLayout, QGroupBox)
from PyQt5.QtCore import Qt

class JsonEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.json_file = 'data/questions.json'
        self.data = {}
        self.load_data()
        self.init_ui()
        
    def load_data(self):
        """Загружает данные из JSON файла"""
        try:
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            else:
                self.data = {}
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл: {e}")
            self.data = {}
    
    def save_data(self):
        """Сохраняет данные в JSON файл"""
        try:
            os.makedirs(os.path.dirname(self.json_file), exist_ok=True)
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            QMessageBox.information(self, "Успех", "Данные сохранены!")
            self.update_tree()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {e}")
    
    def init_ui(self):
        """Инициализация интерфейса"""
        self.setWindowTitle('Редактор базы вопросов')
        self.setGeometry(100, 100, 900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Левая панель - дерево структуры
        left_panel = QVBoxLayout()
        
        # Дерево
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Структура базы")
        left_panel.addWidget(QLabel("Текущая структура:"))
        left_panel.addWidget(self.tree)
        
        # Кнопка сохранения
        save_btn = QPushButton("Сохранить в файл")
        save_btn.clicked.connect(self.save_data)
        left_panel.addWidget(save_btn)
        
        # Правая панель - вкладки с функциями
        tabs = QTabWidget()
        
        # Вкладка создания
        create_tab = QWidget()
        create_layout = QVBoxLayout()
        
        # Группа создания главы
        chapter_group = QGroupBox("Создать главу")
        chapter_layout = QFormLayout()
        self.chapter_name = QLineEdit()
        chapter_layout.addRow("Название главы:", self.chapter_name)
        create_chapter_btn = QPushButton("Создать главу")
        create_chapter_btn.clicked.connect(self.create_chapter)
        chapter_layout.addRow(create_chapter_btn)
        chapter_group.setLayout(chapter_layout)
        
        # Группа создания модуля
        module_group = QGroupBox("Создать модуль")
        module_layout = QFormLayout()
        self.module_chapter = QComboBox()
        self.module_name = QLineEdit()
        module_layout.addRow("Выберите главу:", self.module_chapter)
        module_layout.addRow("Название модуля:", self.module_name)
        create_module_btn = QPushButton("Создать модуль")
        create_module_btn.clicked.connect(self.create_module)
        module_layout.addRow(create_module_btn)
        module_group.setLayout(module_layout)
        
        # Группа создания вопроса
        question_group = QGroupBox("Создать вопрос")
        question_layout = QFormLayout()
        self.question_chapter = QComboBox()
        self.question_module = QComboBox()
        self.question_text = QLineEdit()
        self.answer_text = QTextEdit()
        self.answer_text.setMaximumHeight(100)
        question_layout.addRow("Выберите главу:", self.question_chapter)
        question_layout.addRow("Выберите модуль:", self.question_module)
        question_layout.addRow("Вопрос:", self.question_text)
        question_layout.addRow("Ответ:", self.answer_text)
        create_question_btn = QPushButton("Создать вопрос")
        create_question_btn.clicked.connect(self.create_question)
        question_layout.addRow(create_question_btn)
        question_group.setLayout(question_layout)
        
        create_layout.addWidget(chapter_group)
        create_layout.addWidget(module_group)
        create_layout.addWidget(question_group)
        create_layout.addStretch()
        create_tab.setLayout(create_layout)
        
        # Вкладка удаления
        delete_tab = QWidget()
        delete_layout = QVBoxLayout()
        
        # Группа удаления главы
        del_chapter_group = QGroupBox("Удалить главу")
        del_chapter_layout = QFormLayout()
        self.del_chapter = QComboBox()
        del_chapter_layout.addRow("Выберите главу:", self.del_chapter)
        delete_chapter_btn = QPushButton("Удалить главу")
        delete_chapter_btn.clicked.connect(self.delete_chapter)
        del_chapter_layout.addRow(delete_chapter_btn)
        del_chapter_group.setLayout(del_chapter_layout)
        
        # Группа удаления модуля
        del_module_group = QGroupBox("Удалить модуль")
        del_module_layout = QFormLayout()
        self.del_module_chapter = QComboBox()
        self.del_module = QComboBox()
        del_module_layout.addRow("Выберите главу:", self.del_module_chapter)
        del_module_layout.addRow("Выберите модуль:", self.del_module)
        delete_module_btn = QPushButton("Удалить модуль")
        delete_module_btn.clicked.connect(self.delete_module)
        del_module_layout.addRow(delete_module_btn)
        del_module_group.setLayout(del_module_layout)
        
        # Группа удаления вопроса
        del_question_group = QGroupBox("Удалить вопрос")
        del_question_layout = QFormLayout()
        self.del_question_chapter = QComboBox()
        self.del_question_module = QComboBox()
        self.del_question = QComboBox()
        del_question_layout.addRow("Выберите главу:", self.del_question_chapter)
        del_question_layout.addRow("Выберите модуль:", self.del_question_module)
        del_question_layout.addRow("Выберите вопрос:", self.del_question)
        delete_question_btn = QPushButton("Удалить вопрос")
        delete_question_btn.clicked.connect(self.delete_question)
        del_question_layout.addRow(delete_question_btn)
        del_question_group.setLayout(del_question_layout)
        
        delete_layout.addWidget(del_chapter_group)
        delete_layout.addWidget(del_module_group)
        delete_layout.addWidget(del_question_group)
        delete_layout.addStretch()
        delete_tab.setLayout(delete_layout)
        
        # Добавляем вкладки
        tabs.addTab(create_tab, "Создание")
        tabs.addTab(delete_tab, "Удаление")
        
        # Компоновка
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        
        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(tabs, 2)
        
        # Настройка связей комбобоксов
        self.question_chapter.currentTextChanged.connect(self.update_question_modules)
        self.del_module_chapter.currentTextChanged.connect(self.update_del_modules)
        self.del_question_chapter.currentTextChanged.connect(self.update_del_question_modules)
        self.del_question_module.currentTextChanged.connect(self.update_del_questions)
        
        # Обновляем интерфейс
        self.update_all()
    
    def update_all(self):
        """Обновляет все элементы интерфейса"""
        self.update_tree()
        self.update_comboboxes()
    
    def update_tree(self):
        """Обновляет дерево структуры"""
        self.tree.clear()
        for chapter_name, modules in self.data.items():
            chapter_item = QTreeWidgetItem(self.tree, [chapter_name])
            for module_name, questions in modules.items():
                module_item = QTreeWidgetItem(chapter_item, [module_name])
                for i, question in enumerate(questions):
                    question_item = QTreeWidgetItem(module_item, [f"Вопрос {i+1}: {question['question'][:50]}..."])
        self.tree.expandAll()
    
    def update_comboboxes(self):
        """Обновляет все комбобоксы"""
        chapters = list(self.data.keys())
        
        # Обновляем комбобоксы выбора глав
        for combo in [self.module_chapter, self.question_chapter, self.del_chapter, 
                     self.del_module_chapter, self.del_question_chapter]:
            combo.clear()
            combo.addItems(chapters)
        
        # Обновляем зависимые комбобоксы
        self.update_question_modules()
        self.update_del_modules()
        self.update_del_question_modules()
    
    def update_question_modules(self):
        """Обновляет модули для создания вопроса"""
        self.question_module.clear()
        chapter = self.question_chapter.currentText()
        if chapter in self.data:
            self.question_module.addItems(list(self.data[chapter].keys()))
    
    def update_del_modules(self):
        """Обновляет модули для удаления"""
        self.del_module.clear()
        chapter = self.del_module_chapter.currentText()
        if chapter in self.data:
            self.del_module.addItems(list(self.data[chapter].keys()))
    
    def update_del_question_modules(self):
        """Обновляет модули для удаления вопроса"""
        self.del_question_module.clear()
        chapter = self.del_question_chapter.currentText()
        if chapter in self.data:
            self.del_question_module.addItems(list(self.data[chapter].keys()))
        self.update_del_questions()
    
    def update_del_questions(self):
        """Обновляет вопросы для удаления"""
        self.del_question.clear()
        chapter = self.del_question_chapter.currentText()
        module = self.del_question_module.currentText()
        if chapter in self.data and module in self.data[chapter]:
            questions = [f"{i+1}. {q['question'][:50]}..." for i, q in enumerate(self.data[chapter][module])]
            self.del_question.addItems(questions)
    
    def create_chapter(self):
        """Создает новую главу"""
        name = self.chapter_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название главы")
            return
        
        if name in self.data:
            QMessageBox.warning(self, "Ошибка", "Глава с таким названием уже существует")
            return
        
        self.data[name] = {}
        self.chapter_name.clear()
        self.update_all()
        QMessageBox.information(self, "Успех", f"Глава '{name}' создана")
    
    def create_module(self):
        """Создает новый модуль"""
        chapter = self.module_chapter.currentText()
        name = self.module_name.text().strip()
        
        if not chapter:
            QMessageBox.warning(self, "Ошибка", "Выберите главу")
            return
        
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название модуля")
            return
        
        if name in self.data[chapter]:
            QMessageBox.warning(self, "Ошибка", "Модуль с таким названием уже существует в этой главе")
            return
        
        self.data[chapter][name] = []
        self.module_name.clear()
        self.update_all()
        QMessageBox.information(self, "Успех", f"Модуль '{name}' создан в главе '{chapter}'")
    
    def create_question(self):
        """Создает новый вопрос"""
        chapter = self.question_chapter.currentText()
        module = self.question_module.currentText()
        question = self.question_text.text().strip()
        answer = self.answer_text.toPlainText().strip()
        
        if not chapter or not module:
            QMessageBox.warning(self, "Ошибка", "Выберите главу и модуль")
            return
        
        if not question or not answer:
            QMessageBox.warning(self, "Ошибка", "Введите вопрос и ответ")
            return
        
        self.data[chapter][module].append({
            "question": question,
            "answer": answer
        })
        
        self.question_text.clear()
        self.answer_text.clear()
        self.update_all()
        QMessageBox.information(self, "Успех", "Вопрос добавлен")
    
    def delete_chapter(self):
        """Удаляет главу"""
        chapter = self.del_chapter.currentText()
        if not chapter:
            QMessageBox.warning(self, "Ошибка", "Выберите главу для удаления")
            return
        
        reply = QMessageBox.question(self, "Подтверждение", 
                                   f"Удалить главу '{chapter}' со всем содержимым?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            del self.data[chapter]
            self.update_all()
            QMessageBox.information(self, "Успех", f"Глава '{chapter}' удалена")
    
    def delete_module(self):
        """Удаляет модуль"""
        chapter = self.del_module_chapter.currentText()
        module = self.del_module.currentText()
        
        if not chapter or not module:
            QMessageBox.warning(self, "Ошибка", "Выберите главу и модуль для удаления")
            return
        
        reply = QMessageBox.question(self, "Подтверждение", 
                                   f"Удалить модуль '{module}' из главы '{chapter}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            del self.data[chapter][module]
            self.update_all()
            QMessageBox.information(self, "Успех", f"Модуль '{module}' удален")
    
    def delete_question(self):
        """Удаляет вопрос"""
        chapter = self.del_question_chapter.currentText()
        module = self.del_question_module.currentText()
        question_index = self.del_question.currentIndex()
        
        if not chapter or not module or question_index == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите главу, модуль и вопрос для удаления")
            return
        
        question_text = self.data[chapter][module][question_index]['question']
        reply = QMessageBox.question(self, "Подтверждение", 
                                   f"Удалить вопрос: '{question_text[:50]}...'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            del self.data[chapter][module][question_index]
            self.update_all()
            QMessageBox.information(self, "Успех", "Вопрос удален")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = JsonEditor()
    editor.show()
    sys.exit(app.exec_())