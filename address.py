from utility import *
from colorama import Fore, init
import difflib

class EmailValidator:
    @staticmethod
    def is_valid(email):
        import re
        # Проста перевірка на валідність email
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return re.match(pattern, email) is not None

class AddEmail:
    def __init__(self, book):
        self.book = book # Книга контактів (словник з об'єктами Record)

    def add(self, *args):
         # Перевіряємо, чи передано хоча б два аргументи: ім’я і email
        if len(args) < 2:
            return "Usage: add-email <name> <email>"
        name, email = args[0], args[1]
        contact = self.book.get(name)
         # Якщо контакту з таким ім’ям не знайдено
        if not contact:
            return f"Contact '{name}' not found."
            # Використовуємо клас EmailValidator для перевірки email
        if not EmailValidator.is_valid(email):
            return f"Invalid email format: {email}"
             # Додаємо email до контакту
        contact.email = email
        return f"Email '{email}' added to contact '{name}'."

class AddAddress:
    def __init__(self, book):
        self.book = book

    def add(self, *args):
        # Перевірка: чи вказані ім’я та адреса
        if len(args) < 2:
            return "Usage: add-address <name> <address>"
        name, address = args[0], ' '.join(args[1:]) # Дозволяємо адресу з декількох слів
        contact = self.book.get(name)
        if not contact:
            return f"Contact '{name}' not found."
         # Додаємо адресу до контакту
        contact.address = address
        return f"Address '{address}' added to contact '{name}'."

class EmailEditor:
    def __init__(self, book):
        # Зберігаємо посилання на адресну книгу
        self.book = book

    def edit(self, name, new_email):
        # Шукаємо контакт за іменем
        contact = self.book.get(name)
        # Якщо контакт не знайдено
        if not contact:
            return f"Contact '{name}' not found."
         # Перевірка правильності формату email
        if not EmailValidator.is_valid(new_email):
            return f"Invalid email format: {new_email}"
         # Зберігаємо старий email
        old_email = contact.email
         # Оновлюємо email на новий
        contact.email = new_email
        # Повертаємо повідомлення про успішне редагування
        return f"Email for '{name}' updated from '{old_email}' to '{new_email}'."


class AddressEditor:
    def __init__(self, book):
        # Зберігаємо посилання на адресну книгу (словник об'єктів Record)
        self.book = book

    def edit(self, name, new_address):
        # Шукаємо контакт у книзі за ім'ям
        contact = self.book.get(name)
        # Якщо контакт не знайдено — повертаємо повідомлення
        if not contact:
            return f"Contact '{name}' not found."
        # Зберігаємо стару адресу для повідомлення
        old_address = contact.address
        # Оновлюємо адресу
        contact.address = new_address
        # Повертаємо підтвердження змін
        return f"Address for '{name}' updated from '{old_address}' to '{new_address}'."



init(autoreset=True)
commands = ["hello","add","change","delete","phone","all","add-birthday","show-birthday","birthdays", "hello", "add-email", "add-address", "show-email", "show-address", "edit-email", "edit-address"]

def suggest_command(user_command):
    matches = difflib.get_close_matches(user_command, commands, n=1, cutoff=0.6)
    return matches[0] if matches else None

def main():
    email_adder = AddEmail(book)
    address_adder = AddAddress(book)    

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    
    # Створення об'єктів ОДИН раз
    email_adder = AddEmail(book)
    address_adder = AddAddress(book)
    email_editor = EmailEditor(book)
    address_editor = AddressEditor(book)

    while True:
        try:
            user_input = input(f"Enter a command: {Fore.LIGHTCYAN_EX}")
            print(Fore.RESET, end="")
            command, *args = parse_input(user_input)
            if command in ["close", "exit"]:
                save_data(book)
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "add-email":
                print(email_adder.add(*args))
            elif command == "add-address":
                print(address_adder.add(*args))
            elif command == "edit-email":
                print(email_editor.edit(*args))
            elif command == "edit-address":
                print(address_editor.edit(args[0], ' '.join(args[1:])))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "delete":
                print(delete_contact(args, book))
            elif command == "phone":
                print(', '.join(show_phone(args, book)))
            elif command == "all":
                print(colorize_message(f"{"Name":<20}{"Phone":<15}", "MAGENTA"))
                for i, contact in enumerate(show_all(book)):
                    print(colorize_message(f"{contact.name:<20}{'\n                    '.join(contact.phones)}", f"{"CYAN" if i%2==0 else "BLUE"}"))
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(colorize_message(f"{"Name":<20}{"Birthday":<15}", "MAGENTA"))
                for i, contact in enumerate(birthdays(book)):
                    print(colorize_message(f"{contact.name:<20}{contact.birthday}", f"{"CYAN" if i%2==0 else "BLUE"}"))
            else:
                suggestion = suggest_command(command)
                if suggestion:
                    print(colorize_message(f"Unknown command: '{command}'. Did you mean '{suggestion}'?", "YELLOW"))

                else:
                    print(colorize_message(f"Invalid command: '{command}'.", "YELLOW"))  
        except Exception as e:
        # Обробка будь-якого винятку
            error_handler(e)
            

if __name__ == "__main__":
    main()
