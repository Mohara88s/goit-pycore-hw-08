from collections import UserDict
from datetime import datetime, timedelta
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        self.value = name.capitalize()


class Phone(Field):    
    def __init__(self, phone):
        self.value = self.phone_validation(phone)
    
    def phone_validation(self, phone):
        if len(phone) != 10 | (not phone.isdigit()):
            raise Exception("The phone number has to contain 10 digits")
        return phone


class Birthday(Field):
    def __init__(self, value):
        if isinstance(value, str) and re.fullmatch(r'(\d{1}|\d{2}).(\d{1}|\d{2}).\d{4}', value) is not None: 
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        else: raise ValueError("Invalid date format. Use DD.MM.YYYY")

    
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    @property
    def get_phones(self):
        list_of_phones = []
        for phone in self.phones:
            list_of_phones.append(phone.value)
        return list_of_phones
    
    def add_phone(self, phone):
        if self.find_phone(phone):
            raise Exception(f"The phone number {phone} has already been added to contact {self.name}")
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        if not self.find_phone(phone):
            raise Exception(f"The phone number:{phone} is not found")
        self.phones = [ph for ph in self.phones if ph.value != phone]   

    def edit_phone(self, phone, new_phone):
        if not self.find_phone(phone):
            raise Exception(f"The phone number:{phone} is not found")
        self.phones = [Phone(new_phone) if ph.value == phone else ph for ph in self.phones]
        
    def find_phone(self, phone):
        result = [ph for ph in self.phones if ph.value == phone]
        return result[0] if len(result) > 0 else None
    
    @property
    def get_birthday(self):
        if self.birthday:   
            birthday_date = datetime.strptime(str(self.birthday), "%Y-%m-%d").strftime("%d.%m.%Y")
        else:
            raise Exception(f"The birthday is not found")
        return birthday_date
    
    def add_birthday(self, birthday_str):
        self.birthday=Birthday(birthday_str)

    def __str__(self):
        return f"Contact name: {self.name.value}, contact birthday:{self.birthday}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def __getitem__(self, key):
        return self.data.get(key, "Key not found")
    
    def add_record(self, record):
        self.data[record.name.value] = record
            
    def find(self, name):
        result = self.data.get(name.capitalize(), None)
        return result

    def delete(self, name):
        if not name.capitalize() in self.data:
            raise Exception(f"The contact with name:{name.capitalize()} is not found")
        del self.data[name.capitalize()]

    @property
    def get_all_records(self):
        return self.data
    
    def get_upcoming_birthdays(self):
        records_to_congr = []
        today = datetime.today().date()
        for name, record in self.data.items():
            date_of_birth = datetime.strptime(f"{record.birthday}", "%Y-%m-%d").date()
            if today < date_of_birth: continue
            birthday_this_year = date_of_birth.replace(year=today.year)
            next_bd = date_of_birth.replace(year=today.year + 1) if birthday_this_year < today else birthday_this_year  
            if next_bd.toordinal() - today.toordinal() <= 7:    
                bday_of_week = next_bd.weekday()
                if bday_of_week == 5:
                    next_bd = next_bd + timedelta(days = 2)
                if bday_of_week == 6:
                    next_bd = next_bd + timedelta(days = 1)
                congratulation_date = next_bd.strftime("%d.%m.%Y")
                records_to_congr.append({"name":name, "congratulation_date":congratulation_date})
        return records_to_congr
    


if __name__ == "__main__":
    try:
        # Створення нової адресної книги
        book = AddressBook()

        # Створення запису для John
        john_record = Record("John")
        john_record.add_phone("1234567890")
        john_record.add_phone("5555555555")

        # Додавання запису John до адресної книги
        book.add_record(john_record)

        # Створення та додавання нового запису для Jane
        jane_record = Record("Jane")
        jane_record.add_phone("9876543210")
        book.add_record(jane_record)

        # Виведення всіх записів у книзі
        for name, record in book.data.items():
            print(record)

        # Знаходження та редагування телефону для John
        john = book.find("John")
        john.edit_phone("1234567890", "1112223333")

        print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

        # Пошук конкретного телефону у записі John
        found_phone = john.find_phone("5555555555")
        print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

        # Видалення запису Jane
        book.delete("Jane")


        # Мої додаткові перевірки
        # Додавання та видалення телефону для John
        john_record.add_phone("1231231231")
        # Додавання дня народження для John
        john_record.add_birthday("25.03.2000")
        print(john_record.get_birthday) # Виведення: 2000.03.25
        print(john) # Виведення: Contact name: John, contact birthday:2000-03-25, phones: 1112223333; 5555555555; 1231231231
        john_record.remove_phone("1231231231")
        print(john) # Виведення: Contact name: John, contact birthday:2000-03-25, phones: 1112223333; 5555555555
        # Дні народження що в межах 7 наступних днів
        print(book.get_upcoming_birthdays()) #Виведення: [{'name': 'John', 'congratulation_date': '2025.03.25'}]

            
    except Exception as e:
    # Обробка будь-якого винятку
        print(f"An error occurred: {e}")
