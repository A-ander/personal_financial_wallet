import os

from dataclasses import dataclass

from tabulate import tabulate


@dataclass
class Record:
    """Represents a financial record with date, category, amount and description."""
    date: str
    category: str
    amount: int
    description: str

    def __str__(self):
        return f"Дата: {self.date}\nКатегория: {self.category}\nСумма: {self.amount}\nОписание: {self.description}\n"


class FinanceApp:
    def __init__(self, filename="finance.txt"):
        """Manages financial records, allowing adding, editing, deleting, searching and displaying balance."""
        self.data = []
        self.filename = filename
        self.load_data()
        self.balance = 0

    def load_data(self):
        """Loads records from the data file if it exists."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
                self.data = []
                for i in range(0, len(lines), 4):
                    parts = [part.split(':')[1].strip() for part in lines[i:i + 4]]
                    date, category, amount, description = parts
                    amount = int(amount)  # Преобразование суммы в целое число
                    self.data.append(Record(date, category, amount, description))

    def save_data(self):
        """Saves records to the data file."""
        with open(self.filename, "w") as f:
            for record in self.data:
                f.write(f"Дата: {record.date}\n")
                f.write(f"Категория: {record.category}\n")
                f.write(f"Сумма: {record.amount}\n")
                f.write(f"Описание: {record.description}\n\n")

    @staticmethod
    def get_record_input():
        """Gets user input for a new record."""
        date = input("Введите новую дату (YYYY-MM-DD): ")
        category = input("Введите новую категорию (Доход/Расход): ")
        amount = int(input("Введите новую сумму: "))
        description = input("Введите новое описание: ")
        return date, category, amount, description

    def add_record(self):
        """Adds a new record to the data."""
        date, category, amount, description = FinanceApp.get_record_input()
        self.data.append(Record(date, category, amount, description))
        self.save_data()

    def edit_record(self):
        """Edits an existing record with given index and updated fields."""
        index = int(input("Введите номер записи для исправления: "))
        if index >= len(self.data) + 1:
            print("Неверный номер записи!")
            return
        date, category, amount, description = FinanceApp.get_record_input()
        self.data[index-1] = Record(date, category, amount, description)
        self.save_data()

    def delete_record(self):
        """Deletes a record with the given index."""
        index = int(input("Номер записи для удаления: "))
        if index >= len(self.data)+1:
            print("Неверный номер записи!")
            return
        self.data.pop(index-1)
        self.save_data()

    def search(self):
        """Searches for records containing the query string."""
        query = input("Введите запрос для поиска: ")
        results = [(i, record) for i, record in enumerate(self.data) if query.lower() in str(record).lower()]
        if results:
            print("Результаты поиска:")
            for index, record in results:
                print(f"{index + 1}. {record}")
        else:
            print("Не найдено записей!")

    def count_balance(self):
        """Calculates the total income and expenses."""
        incomes = sum(record.amount for record in self.data if record.category == "Доход")
        expenses = sum(record.amount for record in self.data if record.category == "Расход")
        self.balance = incomes - expenses
        return incomes, expenses, self.balance

    def display(self):
        """Displays all records and the current balance."""
        headers = ["Дата", "Категория", "Сумма", "Описание"]
        table_data = [[record.date, record.category, record.amount, record.description] for record in self.data]
        print(tabulate(table_data, headers, tablefmt="grid"))

        incomes, expenses, self.balance = self.count_balance()
        print(f"\nБаланс: {self.balance}")
        print(f"Доход: {incomes}")
        print(f"Расход: {expenses}")

        print("\nRecords:")
        for i, record in enumerate(self.data):
            category_color = "\033[92m" if record.category == "Доход" else "\033[91m"
            print(f"{i + 1}. {category_color}{record}\033[0m", end='')

    def run(self):
        """Runs the main application loop with user menu."""
        actions = {
            '1': self.display,
            '2': self.add_record,
            '3': self.edit_record,
            '4': self.delete_record,
            '5': self.search,
            '0': exit
        }

        while True:
            print("\nFinance App Menu:")
            print("1. Вывести записи и баланс")
            print("2. Добавить запись")
            print("3. Исправить запись")
            print("4. Удалить запись")
            print("5. Искать запись")
            print("0. Выход")
            choice = input("Ваш выбор: ")
            action = actions.get(choice)
            if action:
                action()
            else:
                print("Неверный выбор, попробуйте ещё.")


if __name__ == '__main__':
    app = FinanceApp()
    app.run()
