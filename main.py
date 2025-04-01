from utility import *
from colorama import Fore, init
import difflib

init(autoreset=True)
commands = ["hello","add","change","delete","phone","all","add-birthday","show-birthday","birthdays"]

def suggest_command(user_command):
    matches = difflib.get_close_matches(user_command, commands, n=1, cutoff=0.6)
    return matches[0] if matches else None

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
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
