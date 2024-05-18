import json
from datetime import datetime

class Note:
    def __init__(self, note_id, title, body, timestamp=None):
        self.note_id = note_id
        self.title = title
        self.body = body
        self.timestamp = timestamp if timestamp else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "note_id": self.note_id,
            "title": self.title,
            "body": self.body,
            "timestamp": self.timestamp
        }

class NotesManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.notes = []
        self.load_notes()

    def load_notes(self):
        try:
            with open(self.file_path, 'r') as file:
                self.notes = json.load(file)
        except FileNotFoundError:
            pass

    def save_notes(self):
        with open(self.file_path, 'w') as file:
            json.dump([note.to_dict() for note in self.notes], file, indent=4)

    def add_note(self, title, body):
        note_id = len(self.notes) + 1
        self.notes.append(Note(note_id, title, body))
        self.save_notes()

    def edit_note(self, note_id, title, body):
        for note in self.notes:
            if note.note_id == note_id:
                note.title = title
                note.body = body
                note.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_notes()
                return True
        return False

    def delete_note(self, note_id):
        self.notes = [note for note in self.notes if note.note_id != note_id]
        self.save_notes()

    def get_notes(self, date=None):
        if date:
            filtered_notes = [note for note in self.notes if note.timestamp.startswith(date)]
            return filtered_notes
        return self.notes

if __name__ == "__main__":
    notes_manager = NotesManager("notes.json")

    while True:
        command = input("Введите команду (add/edit/delete/show/exit): ").strip().lower()

        if command == "add":
            title = input("Введите заголовок заметки: ")
            body = input("Введите тело заметки: ")
            notes_manager.add_note(title, body)
            print("Заметка успешно сохранена")
        elif command == "edit":
            note_id = int(input("Введите ID заметки для редактирования: "))
            title = input("Введите новый заголовок заметки: ")
            body = input("Введите новое тело заметки: ")
            if notes_manager.edit_note(note_id, title, body):
                print("Заметка успешно отредактирована")
            else:
                print("Заметка с таким ID не найдена")
        elif command == "delete":
            note_id = int(input("Введите ID заметки для удаления: "))
            notes_manager.delete_note(note_id)
            print("Заметка успешно удалена")
        elif command == "show":
            date = input("Введите дату для фильтрации (гггг-мм-дд): ")
            notes = notes_manager.get_notes(date)
            for note in notes:
                print(f"ID: {note.note_id}, Заголовок: {note.title}, Тело: {note.body}, Время создания: {note.timestamp}")
        elif command == "exit":
            break
        else:
            print("Неверная команда. Пожалуйста, попробуйте ещё раз.")