from colorama import Fore, init
from collections import namedtuple
from components import AddressBook, Record
import pickle

init(autoreset=True)
COLORS_SET={
        'BLUE'        :Fore.BLUE,
        'GREEN'       :Fore.GREEN,
        'YELLOW'      :Fore.YELLOW,
        'RED'         :Fore.RED,
        'MAGENTA'     :Fore.MAGENTA,
        'CYAN'        :Fore.CYAN,
        'LIGHTCYAN_EX':Fore.LIGHTCYAN_EX,
    }


def colorize_message(message, color):
    color=color.upper()
    if color in COLORS_SET.keys():
        return f"{COLORS_SET[color]}{message}{Fore.RESET}"
    else:
        return f"{Fore.WHITE}{message}{Fore.RESET}"


def error_handler(e):
    print(colorize_message(f"{e}", "RED"))


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
    

def add_contact(args, book: AddressBook):
    if len(args)<2:
        raise ValueError("Please give me the contact's name and phone")
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated"
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added"
    if phone:
        record.add_phone(phone)
    return colorize_message(message, "GREEN")


def change_contact(args, book: AddressBook):
    if len(args)<3:
        raise ValueError("Please give me the contact's name, old phone and new phone")
    name, phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise Exception(f"The contact {name} is not found")
    record.edit_phone(phone, new_phone)
    message = "Contact updated"
    return colorize_message(message, "GREEN")


def show_phone(args, book: AddressBook):
    if len(args)<1:
        raise ValueError("Please give me the contact's name")
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise Exception(f"The contact {name} is not found")
    return record.get_phones


def delete_contact(args, book: AddressBook):
    if len(args)<1:
        raise ValueError("Please give me the contact's name")
    name, *_ = args
    book.delete(name)
    message = "Contact deleted"
    return colorize_message(message, "GREEN")


def show_all(book: AddressBook):
    list_of_contacts = []
    Contact_tuple = namedtuple('Contact', ['name', 'phones'])
    for name, record in book.get_all_records.items():
        list_of_contacts.append(Contact_tuple(name, record.get_phones))
    return sorted(list_of_contacts)


def add_birthday(args, book: AddressBook):
    if len(args)<2:
        raise ValueError(f"Please give me the contact's name and birthday date")
    name, birthay, *_ = args
    record = book.find(name)
    if record is None:
        raise Exception(f"The contact {name} is not found")
    record.add_birthday(birthay)
    message = "Contact updated"
    return colorize_message(message, "GREEN")


def show_birthday(args, book: AddressBook):
    if len(args)<1:
        raise ValueError(f"Please give me the contact's name")
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise Exception(f"The contact {name} is not found")
    res = record.get_birthday
    return colorize_message(res, "GREEN")


def birthdays(book: AddressBook):
    list_of_birthdays = []
    Birthday_tuple = namedtuple('Birthday_tuple', ['name', 'birthday'])
    for contact in book.get_upcoming_birthdays():
        list_of_birthdays.append(Birthday_tuple(contact.get('name'), contact.get('congratulation_date')))
    return list_of_birthdays

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
    
if __name__ == "__main__":
    pass
