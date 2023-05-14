from classes import Record, AddressBook

phonebook = AddressBook()

def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            return "There is no such name"
        except ValueError:
            return "Give me name, phone, email or birthday please"
        except IndexError:
            return "Enter user name"
        except TypeError:
            return "Incorrect values"
    return inner

@input_error
def greeting():
    return "How can I help you?"

def unknown_command():
    return "Unknown command"

@input_error
def exit():
    return None

@input_error
def add_user(name, contact_details=None):
    record = phonebook.get(name, None)
    if record:
        if contact_details:
            if '@' in contact_details:
                record.add_email(contact_details)
            elif '.' in contact_details:
                record.add_birthday(contact_details)
            else:
                record.add_phone(contact_details)
            return "Contact successfully updated"
        else:
            return "Contact already exists"
    else:
        if contact_details:
            if '@' in contact_details:
                record = Record(name, email=contact_details)
            elif '.' in contact_details:
                record = Record(name, birthday=contact_details)
            else:
                record = Record(name, phone=contact_details)
        else:
            return "Give me name and phone please"

        phonebook.add_record(record)
        return "Contact added successfully"

@input_error
def change_phone(name, phone):
    record = phonebook.get(name, None)
    if record:
        record.edit_phone(index=0, phone=phone)
        return "Phone number updated successfully"
    else:
        return "There is no such name"

def show_all():
    if not phonebook:
        return "The phonebook is empty"
    result = ''
    for record in phonebook.values():
        result += record.name.value
        if record.phones:
            phones = ', '.join([phone.value for phone in record.phones])
            result += f": {phones}"
        if record.email:
            result += f", Email: {record.email}"
        if record.birthday:
            result += f", Birthday: {str(record.birthday)}"
            days_left = record.days_to_birthday()
            result += f", Days to birthday: {days_left}"
        result += '\n'
    return result.rstrip()

@input_error
def get_birthday(name):
    result = phonebook.search(name=name)
    if result:
        result_strings = [f"{contact.name.value}: {contact.birthday}, Days to birthday: {contact.days_to_birthday()}" for contact in result if contact.birthday]
        if result_strings:
            return ", ".join(result_strings)
        else:
            return "No birthday found for that name"
    else:
        return "There is no such name"

@input_error
def get_phone_number(name):
    result = phonebook.search(name=name)
    if result:
        result_strings = []
        for contact in result:
            if contact.phones:
                phone_numbers = ', '.join([phone.value for phone in contact.phones])
                result_strings.append(f"{contact.name.value}: {phone_numbers}")
            else:
                result_strings.append(f"{contact.name.value}: No phone number")
        return ", ".join(result_strings)
    else:
        return "There is no such name"

@input_error
def get_email(name):
    result = phonebook.search(name=name)
    if result:
        result_strings = [f"{contact.name.value}: {contact.email}" for contact in result if contact.email]
        if result_strings:
            return ", ".join(result_strings)
        else:
            return "No email found for that name"
    else:
        return "There is no such name"

def search_by_criteria(criteria):
    if criteria:
        result = phonebook.search(name=criteria) or phonebook.search(email=criteria) or phonebook.search(phone=criteria)
        if result:
            result_strings = []
            for contact in result:
                contact_info = f"{contact.name.value}"
                if contact.phones:
                    phones = ', '.join([phone.value for phone in contact.phones])
                    contact_info += f": {phones}"
                if contact.email:
                    contact_info += f", Email: {contact.email}"
                if contact.birthday:
                    contact_info += f", Birthday: {str(contact.birthday)}"
                    days_left = contact.days_to_birthday()
                    contact_info += f", Days to birthday: {days_left}"
                result_strings.append(contact_info)
            return "\n".join(result_strings)
    return "No records found for that criteria"

commands = {
    'hello': greeting,
    'add': add_user,
    'change': change_phone,
    'show all': show_all,
    "phone": get_phone_number,
    'exit': exit,
    'good bye': exit,
    'close': exit,
    "email": get_email,
    "birthday": get_birthday,
    'search': search_by_criteria,
}

def main():
    while True:
        command, *args = input(">>> ").strip().split(' ', 1)
        if commands.get(command):
            handler = commands.get(command)
            if args:
                args = args[0].split()
                result = handler(*args)
            else:
                result = handler(*args)
        elif args and commands.get(command + ' ' + args[0]):
            command = command + ' ' + args[0]
            args = args[1:]
            handler = commands.get(command)
            result = handler(*args)
        else:
            result = unknown_command()

        if not result:
            print('Good bye!')
            break

        print(result)

if __name__ == "__main__":
    main()