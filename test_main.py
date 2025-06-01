import pytest
from pathlib import Path
from main import FinanceApp  # Make sure this matches your file name

# Helper function to create a temporary CSV file with only headers


def create_temp_file():
    temp_file = Path("temp_test_data.csv")
    temp_file.write_text("Date,Category,Amount\n")  # Write CSV headers
    return temp_file

# Test if FinanceApp starts with correct initial balance and empty history


def test_initial_balance_and_history():
    temp_file = create_temp_file()
    app = FinanceApp(csv_file=str(temp_file))
    assert app.balance == 0.0  # Initial balance should be 0
    assert app.record_history == []  # No records yet
    temp_file.unlink()  # Delete the temporary file

# Test if adding funds updates the balance and history correctly


def test_add_funds():
    temp_file = create_temp_file()
    app = FinanceApp(csv_file=str(temp_file))
    app.add_funds(150, "Salary")  # Add income
    assert app.balance == 150  # The funds added should reflect in balance
    assert len(app.record_history) == 1  # One transaction should be recorded
    _, category, amount = app.record_history[0]
    assert category == "Salary"
    assert amount == 150  # The amount should match the added funds
    temp_file.unlink()

# Test if expenses are subtracted correctly and recorded properly


def test_add_expenses():
    temp_file = create_temp_file()
    app = FinanceApp(csv_file=str(temp_file))
    app.add_funds(200, "Gift")  # Add initial funds
    app.add_expenses(50, "Groceries")  # Spend part of the funds
    assert app.balance == 150  # Balance should decrease
    assert len(app.record_history) == 2  # Two transactions in total
    _, category, amount = app.record_history[-1]  # Check last transaction
    assert category == "Groceries"
    assert amount == -50  # Expenses are stored as negative amounts
    temp_file.unlink()

# To test if resetting the app clears all recorded data


def test_app_reset():
    temp_file = create_temp_file()
    app = FinanceApp(csv_file=str(temp_file))
    app.add_funds(100, "Salary")
    app.add_expenses(20, "Transport")
    app.app_reset()  # To reset balance and record history
    assert app.balance == 0.0  # Balance is reset to 0
    assert app.record_history == []  # Record history is cleared
    temp_file.unlink()


# To test if entered entries are saved correctly in the CSV file
def test_save_file():
    temp_file = create_temp_file()
    app = FinanceApp(csv_file=str(temp_file))
    app.add_funds(120, "Bonus")  # To add funds
    contents = temp_file.read_text()  # for reading saved file contents
    assert "Bonus" in contents  # To check if category exists in file
    assert "120" in contents  # To check if amount exists in file
    temp_file.unlink()

# To test if record entries are loaded correctly from the file


def test_load_transactions():
    temp_file = Path("temp_test_data.csv")
    content = (
        "Date,Category,Amount\n"
        "2025-05-29 10:00,Salary,300\n"
        "2025-05-30 15:00,Groceries,-50\n"
    )
    temp_file.write_text(content)  # Write sample transactions to file
    app = FinanceApp(csv_file=str(temp_file))
    assert app.balance == 250  # 300 income - 50 expense
    assert len(app.record_history) == 2  # Two record history are loaded
    assert app.record_history[0][1] == "Salary"
    assert app.record_history[1][1] == "Groceries"
    temp_file.unlink()

# def test_initial_state():
#     app = FinanceApp()
#     assert app.balance == 0.0
#     assert app.record_history == []

# # Test if adding funds updates the balance and history correctly


# def test_add_funds():
#     app = FinanceApp()
#     app.add_funds(100, "Salary")
#     assert app.balance == 100
#     assert len(app.record_history) == 1
#     assert app.record_history[0][1] == "Salary"
#     assert app.record_history[0][2] == 100

# # Test if expenses are subtracted correctly and recorded properly


# def test_add_expenses():
#     app = FinanceApp()
#     app.add_funds(200, "Gift")
#     app.add_expenses(50, "Groceries")
#     assert app.balance == 150
#     assert len(app.record_history) == 2
#     assert app.record_history[-1][1] == "Groceries"
#     assert app.record_history[-1][2] == -50

# # To test if resetting the app clears all recorded data


# def test_app_reset():
#     app = FinanceApp()
#     app.add_funds(100, "Salary")
#     app.add_expenses(20, "Transport")
#     app.app_reset()
#     assert app.balance == 0.0
#     assert app.record_history == []

# # To test if entered entries are saved correctly in the CSV file


# def test_save_enteries(tmp_path):
#     test_file = tmp_path / "test_data.csv"
#     test_file.write_text("Date,Category,Amount\n")
#     app = FinanceApp(csv_file=str(test_file))
#     app.add_funds(120, "Bonus")
#     contents = test_file.read_text()
#     assert "Bonus" in contents
#     assert "120" in contents

# # To test if record entries are loaded correctly from the file


# def test_load_file():
#     temp_file = Path("test_appData.csv")
#     if temp_file.exists():
#         contents = temp_file.read_text()
#         assert "Bonus" in contents
#         assert "100" in contents
#     new_app = FinanceApp(csv_file=str(temp_file))
#     assert new_app.balance == 120
#     assert len(new_app.record_history) == 1
#     assert new_app.record_history[0][1] == "Bonus"
#     if temp_file.exists():
#         temp_file()
