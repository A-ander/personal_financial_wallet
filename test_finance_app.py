import os
import tempfile
import unittest
from unittest.mock import patch
from io import StringIO

from finance_app import FinanceApp, Record


class TestFinanceApp(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        self.app = FinanceApp(self.temp_file.name)
        # Clear the file before each test
        self.temp_file.seek(0)
        self.temp_file.truncate()

    def test_load_data(self):
        """ Test that load_data loads data from the file correctly """
        self.app.load_data()
        self.assertEqual(len(self.app.data), 0)  # Initially, there should be no data

        # Add some test data to the file
        with open(self.temp_file.name, "w") as f:  # Use self.temp_file.name here
            f.write("Дата: 2022-01-01\n")
            f.write("Категория: Доход\n")
            f.write("Сумма: 1000\n")
            f.write("Описание: Test load\n\n")
            f.write("Дата: 2022-01-02\n")
            f.write("Категория: Расход\n")
            f.write("Сумма: 500\n")
            f.write("Описание: Test load\n\n")

        self.app.load_data()
        self.assertEqual(len(self.app.data), 2)  # Now there should be 2 records

    def test_save_data(self):
        """ Test that save_data saves data to the file correctly """
        record1 = Record("2022-01-01", "Доход", 1000, "Test save method")
        record2 = Record("2022-01-02", "Расход", 500, "Test save method")
        self.app.data = [record1, record2]
        self.app.save_data()

        with open(self.temp_file.name, "r") as f:  # Use self.temp_file.name here
            lines = f.readlines()
            self.assertEqual(lines[0].strip(), "Дата: 2022-01-01")
            self.assertEqual(lines[1].strip(), "Категория: Доход")
            self.assertEqual(lines[2].strip(), "Сумма: 1000")
            self.assertEqual(lines[3].strip(), "Описание: Test save method")
            self.assertEqual(lines[4].strip(), "")
            self.assertEqual(lines[5].strip(), "Дата: 2022-01-02")
            self.assertEqual(lines[6].strip(), "Категория: Расход")
            self.assertEqual(lines[7].strip(), "Сумма: 500")
            self.assertEqual(lines[8].strip(), "Описание: Test save method")

    @patch('builtins.input', side_effect=['2022-01-03', 'Доход', '1500', 'Test add method'])
    def test_add_record(self, mock_input):
        """ Test that add_record adds a new record correctly """
        self.app.add_record()
        self.assertEqual(len(self.app.data), 1)
        record = self.app.data[0]
        self.assertEqual(record.date, '2022-01-03')
        self.assertEqual(record.category, 'Доход')
        self.assertEqual(record.amount, 1500)
        self.assertEqual(record.description, 'Test add method')

        with open(self.temp_file.name, "r") as f:
            lines = f.readlines()

            self.assertEqual(lines[0].strip(), "Дата: 2022-01-03")
            self.assertEqual(lines[1].strip(), "Категория: Доход")
            self.assertEqual(lines[2].strip(), "Сумма: 1500")
            self.assertEqual(lines[3].strip(), "Описание: Test add method")

    @patch('builtins.input', side_effect=['1', '2022-01-04', 'Расход', '2000', 'Test edit method'])
    def test_edit_record(self, mock_input):
        """ Test that edit_record edits an existing record correctly """
        self.app.data.append(Record("2022-01-01", "Доход", 1000, "Test income"))
        self.app.edit_record()
        self.assertEqual(self.app.data[0].date, "2022-01-04")
        self.assertEqual(self.app.data[0].category, "Расход")
        self.assertEqual(self.app.data[0].amount, 2000)
        self.assertEqual(self.app.data[0].description, "Test edit method")

    @patch('builtins.input', return_value="1")
    def test_delete_record(self, mock_input):
        """ Test method delete_record."""
        self.app.data.append(Record("2022-01-01", "Доход", 1000, "Test income"))
        self.app.delete_record()
        self.assertEqual(len(self.app.data), 0)

    @patch('builtins.input', return_value="Test save method")
    @patch('sys.stdout', new_callable=StringIO)
    def test_search(self, mock_stdout, mock_input):
        """ Test search method """
        self.app.data.append(Record("2022-01-01", "Доход", 1000, "Test save method"))
        self.app.data.append(Record("2022-01-02", "Расход", 500, "Test save method"))
        self.app.search()
        output = mock_stdout.getvalue()
        self.assertIn("1. Дата: 2022-01-01\nКатегория: Доход\nСумма: 1000\nОписание: Test save method\n", output)
        self.assertIn("2. Дата: 2022-01-02\nКатегория: Расход\nСумма: 500\nОписание: Test save method\n", output)

    def test_count_balance(self):
        """ Test that count_balance calculates the balance correctly """
        record1 = Record("2022-01-01", "Доход", 1000, "Test income")
        record2 = Record("2022-01-02", "Расход", 500, "Test expense")
        self.app.data = [record1, record2]
        incomes, expenses, balance = self.app.count_balance()
        self.assertEqual(incomes, 1000)
        self.assertEqual(expenses, 500)
        self.assertEqual(balance, 500)


if __name__ == '__main__':
    unittest.main()
