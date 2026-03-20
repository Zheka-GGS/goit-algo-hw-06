from collections import UserDict
from typing import Optional, List

# Базовий клас для полів (ім'я, телефон) з атрибутом value та методом __str__ для зручного виводу.
class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

# Обов'язкове поле — ім'я контакту. Може бути будь-яким рядком, але не може бути порожнім. Якщо ім'я порожнє — кидає ValueError.
class Name(Field):
    """Обов'язкове поле — ім'я контакту."""
    pass

# Поле для номера телефону з валідацією (точно 10 цифр). Якщо номер не відповідає вимогам, кидає ValueError.
class Phone(Field):
    """Поле для номера телефону з валідацією (точно 10 цифр)."""

    def __init__(self, value: str):
        if not self._is_valid_phone(value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

    @staticmethod
    def _is_valid_phone(value: str) -> bool:
        # Не чистимо рядок, не видаляємо символи — має бути рівно 10 цифр
        return value.isdigit() and len(value) == 10

# Запис контакту: ім'я + список телефонів. Може мати кілька номерів. 
class Record:
    """Запис контакту: ім'я + список телефонів."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: List[Phone] = []

    def add_phone(self, phone_number: str) -> None:
        """Додає новий номер телефону."""
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        """Видаляє номер телефону за значенням."""
        for i, phone in enumerate(self.phones):
            if phone.value == phone_number:
                self.phones.pop(i)
                return
        raise ValueError(f"Phone number {phone_number} not found.")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """
        Замінює старий номер на новий.
        Спочатку перевіряє валідність нового номера.
        Якщо новий невалідний — кидає ValueError без змін.
        """
        # Спочатку перевіряємо, чи новий номер валідний
        if not Phone._is_valid_phone(new_phone):
            raise ValueError("New phone number must contain exactly 10 digits.")

        # Перевіряємо, чи старий номер існує
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                # Видаляємо старий і додаємо новий
                self.phones.pop(i)
                self.phones.insert(i, Phone(new_phone))
                return

        raise ValueError(f"Old phone number {old_phone} not found.")

    def find_phone(self, phone_number: str) -> Optional[Phone]:
        """Шукає об'єкт Phone за значенням номера."""
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "no phones"
        return f"Contact name: {self.name.value}, phones: {phones_str}"

# Адресна книга — словник з іменами як ключами та Record як значеннями.
class AddressBook(UserDict):
    """Адресна книга — словник з іменами як ключами та Record як значеннями."""

    def add_record(self, record: Record) -> None:
        """Додає запис до книги."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """Шукає запис за ім'ям."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Видаляє запис за ім'ям."""
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Record with name {name} not found.")

    def __str__(self) -> str:
        if not self.data:
            return "Address book is empty."
        lines = [str(record) for record in self.data.values()]
        return "\n".join(lines)

# Приклад використання
if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    print(book)

    john = book.find("John")
    try:
        john.edit_phone("1234567890", "1112223333")          # успішно
        john.edit_phone("9999999999", "0000000000")          # помилка — старого немає
    except ValueError as e:
        print("Помилка:", e)

    print(john)

    found = john.find_phone("1112223333")
    print(f"{john.name}: {found}")   # John: 1112223333

    try:
        john.edit_phone("1112223333", "123abc4567")
    except ValueError as e:
        print("Очікувана помилка:", e)   # New phone number must contain exactly 10 digits.

    book.delete("Jane")
    print("\nПісля видалення Jane:\n", book)