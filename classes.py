import re
import datetime
from collections import UserDict

class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        validated_name = self.validate_name(value)
        self._value = validated_name

    def validate_name(self, name):
        if not isinstance(name, str):
            raise ValueError
        return name

    def __str__(self):
        return str(self.value)

class Phone(Field):
    def __init__(self, value):
        self._value = None
        self.set_value(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.set_value(new_value)

    def set_value(self, value):
        if self.is_valid_phone(value):
            self._value = value
        else:
            raise ValueError("Invalid phone number")

    def is_valid_phone(self, value):
        pattern = r'^0[0-9]{9}$'
        return bool(re.match(pattern, value))

class Email:
    pass

class Birthday(Field):
    def __init__(self, value):
        self._value = datetime.datetime.strptime(value, "%d.%m.%Y").date()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = datetime.datetime.strptime(new_value, "%d.%m.%Y").date()

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name, phone=None, birthday=None, email=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        if phone:
            self.add_phone(phone)
        if birthday:
            self.add_birthday(birthday)
        if email:
            self.add_email(email)

    def add_email(self, email):
        self.email = email

    def add_birthday(self, birthday):
        if self.birthday:
            self.birthday.value = birthday
        else:
            self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.date.today()
            next_birthday = datetime.date(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > next_birthday:
                next_birthday = datetime.date(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_left = (next_birthday - today).days
            return days_left
        else:
            return "No birthday set"

    def add_phone(self, phone):
        if isinstance(phone, str):
            phone = Phone(phone)
        if phone not in self.phones:
            self.phones.append(phone)

    def edit_phone(self, index, phone):
        self.phones[index].value = phone

    def delete_phone(self, index):
        del self.phones[index]

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def search(self, name=None, phone=None, email=None):
        results = []
        for contact in self.data.values():
            if (name and name.lower() in contact.name.value.lower()) or \
               (phone and phone in [phone.value for phone in contact.phones]) or \
               (email and contact.email and email.lower() in contact.email.lower()):
                results.append(contact)
        return results