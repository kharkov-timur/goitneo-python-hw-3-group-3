from bot import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)

    return inner


@input_error
def add_contact(book, name, phone):
    record = Record(name, phone=phone)
    book.add_record(record)
    return f"Contact {name} added."


@input_error
def change_contact(book, name, new_phone):
    record = book.data.get(name)
    if record:
        record.edit_phone(record.phones[0].value, new_phone)
        return f"Contact {name}'s phone changed."
    else:
        raise ValueError("Contact not found.")


@input_error
def show_phone(book, name):
    record = book.data.get(name)
    if record:
        return ", ".join([phone.value for phone in record.phones])
    else:
        raise ValueError("Contact not found.")


@input_error
def show_all(book):
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(book, name, birthday):
    record = book.data.get(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}"
    else:
        raise ValueError("Contact not found.")


@input_error
def show_birthday(book, name):
    record = book.data.get(name)
    if record and record.birthday:
        return record.birthday.value
    else:
        raise ValueError("Contact or birthday not found.")


@input_error
def show_birthdays(book):
    birthdays = book.get_birthdays_per_week()
    if birthdays:
        return ", ".join(birthdays)
    else:
        return "No birthdays next week."


def hello():
    return "How can I help you?"


def close():
    return "Good bye!"


def show_info():
    info_message = (
        "Available commands:\n"
        "- add [name] [phone] - Add a new contact with a name and phone number.\n"
        "- change [name] [new phone] - Change a contact's phone number.\n"
        "- phone [name] - Show a contact's phone number.\n"
        "- all - Show all saved contacts.\n"
        "- add-birthday [name] [birthday] - Add a birthday to a contact (format DD.MM.YYYY).\n"
        "- show-birthday [name] - Show a contact's birthday.\n"
        "- birthdays - Show birthdays that occur within the next week.\n"
        "- hello - Greeting from the assistant.\n"
        "- close or exit - Close the program.\n"
        "- info - Show available commands."
    )
    return info_message


COMMANDS = {
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "all": show_all,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": show_birthdays,
    "hello": hello,
    "close": close,
    "exit": close,
    "info": show_info,
}


def main():
    book = AddressBook()
    while True:
        command_line = input("Enter a command: ").strip().lower()
        if len(command_line) == 0:
            continue
        parts = command_line.split()
        cmd, args = parts[0], parts[1:]

        if cmd in COMMANDS:
            if cmd == "info":
                result = COMMANDS[cmd]()
            else:
                result = COMMANDS[cmd](book, *args)

            if result == "Good bye!":
                print(result)
                break
            print(result)
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
