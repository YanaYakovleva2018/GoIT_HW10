from collections import UserDict
from typing import List


class Field: #батьківський клас для всіх полів
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f'{self.value}'


class Name(Field): 
    pass


class Phone(Field):
    pass


class Record: # реалізує методи для створення, видаляння та зміни номеру 
    def __init__(self, name: Name, phones: List[Phone]) -> None:
        self.name = name
        self.phones = phones

    def add_phone(self, phone: Phone) -> Phone | None:
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return phone

    def delete_phone(self, phone: Phone) -> Phone | None:
        for p in self.phones:
            if p.value == phone.value:
                self.phones.remove(p)
                return p

    def change_phone(self, phone, new_phone) -> tuple[Phone, Phone] | None:
        if self.delete_phone(phone):
            self.add_phone(new_phone)
            return phone, new_phone

    def __str__(self) -> str:
        return f'Phone {", ".join([p.value for p in self.phones])}'


class AddressBook(UserDict):

    def add_record(self, record: Record) -> Record | None:
        if not self.data.get(record.name.value):
            self.data[record.name.value] = record
            return record

    def delete_record(self, key: str) -> Record | None:
        rcd = self.data.get(key)
        if rcd:
            self.data.pop(key)
            return rcd


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Please, enter the contact like this: \nName number"
        except KeyError:
            return "This contact doesn't exist!"
        except ValueError:
            return "Invalid command entered"

    return inner

def welcome(*args):
    return "How can i help you?"

def to_exit(*args):
    return "Good bye!"

address_book = AddressBook()

@input_error
def add_contact(*args):
    rec = Record(Name(args[0]), [Phone(args[1])])
    if address_book.add_record(rec):
        return f"Contact {rec.name.value} has added."
    else:
        return f"{rec.name.value} contact in notebook."

@input_error
def change_number(*args):
    rec = address_book.get(args[0])
    if rec:
        rec.change_phone(Phone(args[1]), Phone(args[2]))
        return f"Contact {rec.name.value} has changed."
    return f"Contact {args[0]} not in notebook."

@input_error
def print_phone(*args):
    return address_book[args[0]]

@input_error
def delete_number(*args):
    rec = address_book.get(args[0])
    if rec:
        rec.delete_phone(Phone(args[1]))
        return f"Number {args[1]} has deleted."
    else:
        return f"Contact {args[0]} not in notebook."

def show_all(*args):
    if len(address_book) > 0:
        return "\n".join([f"{k.title()} : {v}" for k, v in address_book.items()])
    else:
        return "Contacts is empty"

        
all_comands = {
    welcome: ["hello", "hi"],
    add_contact: ["add", "new"],
    change_number: ["change"],
    print_phone: ["phone", "number"],
    show_all: ["show", "show all"],
    to_exit: [".", "bye", "close", "good bye", "exit"],
    delete_number: ["del", "delete"]
}

def command(user_input: str):
    for key, value in all_comands.items():
        for v in value:
            if user_input.lower().startswith(v.lower()):
                return key, user_input[len(v):].strip().split()

def main():
    while True:
        user_input = input("Enter the command: ")
        cmd, parser_data = command(user_input)
        print(cmd(*parser_data))
        if cmd is to_exit:
            break

if __name__ == "__main__":
    main()
        

    
