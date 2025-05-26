from pathlib import Path  # Path is use to get the path or directory of a file
import csv  # To import,write, and save csv file
from datetime import datetime  # To add date and time to app method


class FinanceApp:   # The class for the personal finance manager app

    # This method (the constructor) is used to initialized object.
    def __init__(self):
        self.balance = 0.0
        self.transaction_history = []
        self.csv_file = Path("appData.csv")
        self.load_transactions()  # Load existing transactions when starting.

    # This method is used to load saved data
    def load_transactions(self):
        try:    # Try  and except block is used for exception handling while working with files
            path = Path(self.csv_file)
            with path.open("r", newline="", encoding="utf-8") as file:
                print(f"The '{path.name}' is now open")
                reader = csv.reader(file)
                headers = next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 3:
                        date, category, amount = row[0], row[1], float(
                            row[2])
                        self.transaction_history.append(
                            (date, category, amount))
                        self.balance += amount

        except FileNotFoundError:
            # the except keywword will create the file if it doesn't exist
            with path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Category", "Amount"])

    # This method is used to saved data from the user input
    def save_file(self, date, category, amount):
        try:
            path = Path(self.csv_file)
            with path.open("a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([date, category, amount])

        except Exception as e:
            print(f"Error saving file: {e}")

    def clear_all_enteries(self):
        try:
            path = Path(self.csv_file)
            with path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Category", "Amount"])
            self.balance = 0.0
            self.transaction_history = []
            print(f"All transactions cleared (file kept).")

        except Exception as e:
            print(f"Error clearing previous entries: {e}")

    # This method is used to record or add funds(money) received by the user
    def add_funds(self):
        try:
            amount = float(input(f"Enter the amount of funds: €").strip())
            source_of_funds = input(
                f"Enter source of funds(Salary, Saving, Gift): ").strip()
            date = datetime.now().strftime("%Y-%m-%d %H:%M")  # Adding data and time
            self.balance += amount  # this is the as self.balance = self.balance + amount
            self.transaction_history.append((date, source_of_funds, amount))
            self.save_file(date, source_of_funds, amount)
            print(f"Funds added: €{amount:.2f}")

        except ValueError:
            print(f"Invalid amount. Please enter a number.")

    # This method is used to record or add the user's expenses
    def add_expenses(self):
        try:
            amount = float(input(f"Enter the amount of expense: €").strip())
            if amount > self.balance:
                print(f"Insufficient balance. Please try again")

            else:
                expense_category = input(
                    f"Enter expense category (Rent, Groceries, Transport, Utility, Miscellaneous): ").strip()
            date = datetime.now().strftime("%Y-%m-%d %H:%M")    # To add date and time
            self.save_file(date, expense_category, -amount)
            self.balance -= amount  # this is the as self.balance = self.balance - amount
            self.transaction_history.append((date, expense_category, -amount))
            print(f"Expense recorded: €{amount:.2f} for {expense_category}")

        except ValueError:
            print(f"Invalid amount. Please enter a number.")

    # This method is used to display the current balance
    def app_balance(self):
        print(f"Current balance: €{self.balance:.2f}")

    # This method is used to prints and track all the financial record.
    def app_summary(self):
        print(f"\nSummary:")
        print(f"{'Date':<20} {'Category':<30} {'Amount':>10}")
        print("-" * 65)
        for date, category, amount in self.transaction_history:
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
            print(f"4. View Transaction History")
            print(f"5. Clear All Previous Entries")
            print(f"6. Exit")

            choice = input(f"Choose an option (1-6): ")

            if choice == '1':
                self.add_funds()

            elif choice == '2':
                self.add_expenses()

            elif choice == '3':
                self.app_balance()

            elif choice == '4':
                self.app_summary()

            elif choice == '5':
                self.clear_all_enteries()  # Call the clear function

            elif choice == '6':
                print(f"Exiting... Thank you for using the app!")
                break

            else:
                print(f"Invalid option. Please try again.")


# This onditional statement ensures that the code runs only when executed directly from the main file
if __name__ == "__main__":
    app = FinanceApp()
    app.start()
