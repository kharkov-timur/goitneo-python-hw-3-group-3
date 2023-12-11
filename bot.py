from collections import UserDict
import re
from datetime import datetime, timedelta
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError(f"Phone number {value} is invalid")
        super().__init__(value)

    def validate(self, phone):
        return re.fullmatch(r"\d{10}", phone) is not None


class Birthday(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError(f"Birthday {value} is invalid")
        super().__init__(value)

    def validate(self, birthday):
        try:
            datetime.strptime(birthday, "%d.%m.%Y")
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones.remove(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError(f"Phone number {old_phone} not found in contact")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday:
            now = datetime.now()
            bday = datetime.strptime(self.birthday.value, "%d.%m.%Y").replace(
                year=now.year
            )
            if bday < now:
                bday = bday.replace(year=now.year + 1)
            return (bday - now).days
        return None

    def __str__(self):
        contact_str = f"Name: {self.name.value}"
        if self.phones:
            contact_str += f", Phones: {'; '.join(str(p) for p in self.phones)}"
        if self.birthday:
            contact_str += f", Birthday: {self.birthday.value}"
        return contact_str


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def get_birthdays_per_week(self):
        today = datetime.now()
        one_week_ahead = today + timedelta(days=7)
        birthdays_this_week = []
        for record in self.data.values():
            if record.birthday:
                birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y")
                if today <= birthday.replace(year=today.year) <= one_week_ahead:
                    birthdays_this_week.append(record.name.value)
        return birthdays_this_week

    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        with open(filename, "rb") as file:
            self.data = pickle.load(file)
