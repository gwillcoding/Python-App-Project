import pytest
from pathlib import Path  # Path is use to get the path or directory of a file
import csv  # To import,write, and save csv file
from datetime import datetime  # To add date and time to app method


class FinanceApp:   # The class for the personal finance manager app

    # This method (the constructor) is used to initialized object.

    def __init__(self, csv_file="appData.csv"):
        self.balance = 0.0  # Balance is zero until the user provides input.
        self.record_history = []  # No records exist until the user adds an emtry
        self.csv_file = Path(csv_file)
        self.load_file()

    # This method is used to read the saved file

    def load_file(self):
        try:     # Try  and except block is used for exception handling while working with files
            path = self.csv_file
            with path.open("r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                headers = next(reader)
                for row in reader:
                    if len(row) >= 3:
                        date, category, amount = row[0], row[1], float(row[2])
                        self.record_history.append((date, category, amount))
                        self.balance += amount
        except FileNotFoundError:  # the except keywword will create the file if it doesn't exist
            with self.csv_file.open("w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Category", "Amount"])
                print(
                    f"File not found. A new file was created: {self.csv_file}")

            # This method is used to saved data from the user input
    def save_entries(self, date, category, amount):

        try:
            with self.csv_file.open("a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([date, category, amount])
        except Exception as e:
            print(f"Error saving file: {e}")

    # This method is used to reset or clear all entries from the app
    def app_reset(self):
        try:
            with self.csv_file.open("w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Category", "Amount"])
            self.balance = 0.0
            self.record_history = []
            print(f"All entriess cleared (file kept).")
        except Exception as e:
            print(f"Error clearing previous entries: {e}")

    # This method is used to record or add funds(money) received by the user

    def add_funds(self, amount, source_of_funds, date=None):
        try:
            date = datetime.now().strftime("%Y-%m-%d %H:%M")  # Timestamp each entry
            self.balance += amount  # this is the as self.balance = self.balance + amount
            self.record_history.append((date, source_of_funds, amount))
            self.save_entries(date, source_of_funds, amount)
            print(f"Funds added: €{amount:.2f}")
        except ValueError as e:
            print(f"Invalid input: {e}")

    # This method is used to record or add the user's expenses

    def add_expenses(self, amount, category, date=None):
        try:
            if amount > self.balance:
                print(f"Insufficient balance. Please try again.")
                return
            date = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.balance -= amount  # this is the as self.balance = self.balance - amount
            self.record_history.append((date, category, -amount))
            self.save_entries(date, category, -amount)
            print(f"Expense recorded: €{amount:.2f} for {category}")
        except ValueError as e:
            print(f"Invalid input: {e}")

    # This method is used to display the current balance

    def app_balance(self):
        print(f"Current balance: €{self.balance:.2f}")

    # This method is used to prints and track all the financial record.

    def app_summary(self):
        print(f"\nSummary:")
        print(f"{'Date':<20} {'Category':<30} {'Amount':>10}")
        print("-" * 65)
        for date, category, amount in self.record_history:
            print(f"{date:<20} {category:<30} €{amount:.2f}")
        self.app_balance()

    # This method is used to runs the interactive menu of the app.
    def start(self):
        print(f"Welcome to Personal Finance Manager!")

        while True:
            print(f"\nMenu:")
            print(f"1. Add Funds")
            print(f"2. Record Expense")
            print(f"3. Check Balance")
            print(f"4. View Summary")
            print(f"5. Reset App")
            print(f"6. Exit")

            choice = input(f"Choose an option (1-6): ")

            if choice == '1':  # To add funds (e.g, salary, savings and gift)
                try:
                    amount = float(
                        input(f"Enter the amount of funds: €").strip())
                    source_of_funds = input(
                        "Enter source of funds (Salary, Savings, Gift, etc.): ").strip()
                    self.add_funds(amount, source_of_funds)
                except ValueError:
                    print("Invalid amount. Please try again.")

            elif choice == '2':  # To add expenses
                try:
                    amount = float(
                        input(f"Enter the amount of expense: €").strip())
                    category = input(
                        "Enter expense category (Rent, Groceries, Transport, Utility, etc.): ").strip()
                    self.add_expenses(amount, category)
                except ValueError:
                    print("Invalid amount. Please try again.")

            elif choice == '3':
                self.app_balance()  # To view current balance

            elif choice == '4':
                # To check the summary or history of the finances.
                self.app_summary()

            elif choice == '5':
                self.app_reset()  # Call the clear function

            elif choice == '6':
                print(f"Exiting... Thank you for using the app!")
                break

            else:
                print(f"Invalid option. Please try again.")


# This conditional statement ensures that the code runs only when executed directly from the main file
if __name__ == "__main__":
    app = FinanceApp()
    app.start()
