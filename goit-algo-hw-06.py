# address_book.py
from collections import UserDict
from typing import Optional, List
# Базовий клас для полів запису, включаючи ім'я та телефон
class Field:
    """Базовий клас для всіх полів запису."""
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other) -> bool:
        if isinstance(other, Field):
            return self.value == other.value
        return False
# Клас для зберігання імені контакту (обов'язкове поле)
class Name(Field):
    """Клас для зберігання імені контакту (обов'язкове поле)."""
    pass  # тут можна додати валідацію, якщо потрібно

# Клас для зберігання номера телефону з валідацією (10 цифр)
class Phone(Field):
    """Клас для зберігання номера телефону з валідацією (10 цифр)."""
    def __init__(self, value: str):
        if not self._is_valid_phone(value):
            raise ValueError("Номер телефону має містити рівно 10 цифр")
        super().__init__(value)
# Валідація номера телефону: дозволяє лише цифри та перевіряє довжину
    @staticmethod
    def _is_valid_phone(value: str) -> bool:
        """Перевіряє, що номер телефону складається рівно з 10 цифр."""
        cleaned = ''.join(filter(str.isdigit, value))
        return len(cleaned) == 10 and cleaned == value
# Клас для зберігання інформації про один контакт, включаючи ім'я та список телефонів
class Record:
    """Клас для зберігання інформації про один контакт."""
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: List[Phone] = []

    def add_phone(self, phone: str) -> None:
        """Додає новий номер телефону до запису."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Видаляє номер телефону з запису."""
        target = Phone(phone)
        if target in self.phones:
            self.phones.remove(target)
        else:
            raise ValueError(f"Номер {phone} не знайдено в записі {self.name}")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """
        Замінює старий номер телефону на новий.
        Кидає ValueError, якщо старий номер не знайдено.
        """
        target = Phone(old_phone)
        if target not in self.phones:
            raise ValueError(f"Старий номер {old_phone} не знайдено")

        # видаляємо старий
        self.phones.remove(target)
        # додаємо новий
        self.add_phone(new_phone)

    def find_phone(self, phone: str) -> Optional[Phone]:
        """Шукає об'єкт Phone за значенням або повертає None."""
        target = Phone(phone)
        try:
            return next(p for p in self.phones if p == target)
        except StopIteration:
            return None

    def __str__(self) -> str:
        phones_str = '; '.join(str(p) for p in self.phones) if self.phones else "немає телефонів"
        return f"Контакт: {self.name.value}, телефони: {phones_str}"
# Клас для зберігання та управління всіма записами (адресна книга)
class AddressBook(UserDict):
    """Клас для зберігання та управління всіма записами (адресна книга)."""

    def add_record(self, record: Record) -> None:
        """Додає запис до адресної книги (ключ — ім'я контакту)."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """Знаходить запис за ім'ям або повертає None."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Видаляє запис за ім'ям."""
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Контакт '{name}' не знайдено")

    def __str__(self) -> str:
        """Красивий вивід усіх контактів у книзі."""
        if not self.data:
            return "Адресна книга порожня."

        lines = ["Адресна книга містить такі контакти:"]
        for record in sorted(self.data.values(), key=lambda r: r.name.value.lower()):
            lines.append(f"  {record}")
        return "\n".join(lines)

if __name__ == "__main__":
    # Створюємо нову адресну книгу
    book = AddressBook()

    # Створюємо запис для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додаємо запис у книгу
    book.add_record(john_record)

    # Додаємо ще один контакт
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виводимо всю книгу
    print(book)

    # Знаходимо та редагуємо телефон
    john = book.find("John")
    if john:
        john.edit_phone("1234567890", "1112223333")
        print("\nПісля редагування:")
        print(john)
        # Контакт: John, телефони: 1112223333; 5555555555
        # Шукаємо конкретний телефон
        found = john.find_phone("5555555555")
        print(f"Знайдено: {found}")   # 5555555555

    # Видаляємо контакт
    book.delete("Jane")
    print("\nПісля видалення Jane:")
    print(book)