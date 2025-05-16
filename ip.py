import os
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# file to store username and password
USERS_FILE = "users.txt"


# Utility Functions

def clear_screen():
    """
    Clear the console screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

# Category Selection Function

def select_category():
    """
    Display a predefined list of categories and return the selected one.
    """
    categories = ["Food", "Transportation", "Housing", "Entertainment", "Others"]
    print("Select a category from the list:")
    for idx, cat in enumerate(categories, start=1):
        print(f"{idx}. {cat}")
    choice = input("Enter your choice (1-5): ").strip()
    try:
        index = int(choice)
        if 1 <= index <= len(categories):
            return categories[index - 1]
        else:
            print("Invalid choice, defaulting to 'Others'")
            return "Others"
    except ValueError:
        print("Invalid input, defaulting to 'Others'")
        return "Others"


# Password Validation Function 
# -------------------------------------------------------------
def is_valid_password(password):
    
    if len(password) <= 7:
        return False
    has_alpha = False
    has_digit = False
    has_special = False
    for char in password:
        if char.isalpha():
            has_alpha = True
        elif char.isdigit():
            has_digit = True
        elif not char.isalnum():
            has_special = True
    return has_alpha and has_digit and has_special

# -------------------------------------------------------------
# User Management Functions
# -------------------------------------------------------------
def load_users():
   
    users = {}
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as file:
                for line in file:
                    line = line.strip()
                    if line == "":
                        continue
                    if ":" in line:
                        parts = line.split(":")
                        if len(parts) >= 2:
                            username = parts[0]
                            password = parts[1]
                            users[username] = password
        except Exception as e:
            print("Error reading users file:", e)
    return users

def save_user(username, password):
    
    try:
        with open(USERS_FILE, "a") as file:
            file.write(f"{username}:{password}\n")
    except Exception as e:
        print("Error writing to users file:", e)

def register():
   
    clear_screen()
    print("===== User Registration =====")
    users = load_users()
    
    # Username validation
    while True:
        username = input("Enter a username: ").strip()
        if not username:
            print("Username cannot be empty. Please enter a valid username.")
        elif username in users:
            print("Username already exists. Please try a different username.")
        else:
            break

    # Password validation
    while True:
        password = input("Enter a password: ").strip()
        confirm_password = input("Confirm your password: ").strip()
        if password != confirm_password:
            print("Passwords do not match. Please try again.")
        elif not is_valid_password(password):
            print("Password must be more than 7 characters long, contain at least one alphabet, one number, and one special character.")
        else:
            break
    
    save_user(username, password)
    print("Registration successful! You can now login.")
    input("Press Enter to continue...")

def login():
   
    clear_screen()
    print("===== User Login =====")
    users = load_users()
    
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    
    if username in users:
        if users[username] == password:
            print("Login successful!")
            input("Press Enter to continue...")
            return username
        else:
            print("Incorrect password.")
    else:
        print("Username not found.")
    
    input("Press Enter to continue...")
    return None

# -------------------------------------------------------------
# Expense Management Functions
# -------------------------------------------------------------
def get_expense_file(username):
 
    return f"expenses_{username}.txt"

def load_expenses(username):

    expenses = []
    filename = get_expense_file(username)
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()
                    if line == "":
                        continue
                    parts = line.split(",")
                    if len(parts) >= 4:
                        expense = {
                            "date": parts[0],
                            "amount": parts[1],
                            "description": parts[2],
                            "category": parts[3]
                        }
                        expenses.append(expense)
                    elif len(parts) == 3:
                        expense = {
                            "date": parts[0],
                            "amount": parts[1],
                            "description": parts[2],
                            "category": "Others"
                        }
                        expenses.append(expense)
        except Exception as e:
            print("Error reading expenses file:", e)
    return expenses

def save_expenses(username, expenses):
   
    filename = get_expense_file(username)
    try:
        with open(filename, "w") as file:
            for expense in expenses:
                description = expense["description"].replace("\n", " ")
                file.write(f"{expense['date']},{expense['amount']},{description},{expense['category']}\n")
    except Exception as e:
        print("Error writing to expenses file:", e)

def add_expense(username):
    
    clear_screen()
    print("===== Add New Expense =====")
    date = input("Enter date (YYYY-MM-DD): ").strip()
    amount = input("Enter amount (in Rupees): ").strip()
    description = input("Enter description: ").strip()
    
    # Use the predefined category selection
    category = select_category()
    
    try:
        float(amount)
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
        input("Press Enter to continue...")
        return
    
    expense = {
        "date": date,
        "amount": amount,
        "description": description,
        "category": category
    }
    
    expenses = load_expenses(username)
    expenses.append(expense)
    save_expenses(username, expenses)
    
    print("Expense added successfully!")
    input("Press Enter to continue...")

def view_expenses(username):
   
    clear_screen()
    print("===== View Expenses =====")
    expenses = load_expenses(username)
    
    if not expenses:
        print("No expenses found.")
    else:
        print("{:<5} {:<12} {:<10} {:<20} {}".format("ID", "Date", "Amount", "Category", "Description"))
        print("-" * 80)
        for idx, expense in enumerate(expenses, start=1):
            print("{:<5} {:<12} {:<10} {:<20} {}".format(idx, expense['date'], expense['amount'], expense['category'], expense['description']))
    
    input("\nPress Enter to continue...")

def delete_expense(username):
   
    clear_screen()
    print("===== Delete Expense =====")
    expenses = load_expenses(username)
    
    if not expenses:
        print("No expenses to delete.")
        input("Press Enter to continue...")
        return
    
    print("{:<5} {:<12} {:<10} {:<20} {}".format("ID", "Date", "Amount", "Category", "Description"))
    print("-" * 80)
    for idx, expense in enumerate(expenses, start=1):
        print("{:<5} {:<12} {:<10} {:<20} {}".format(idx, expense['date'], expense['amount'], expense['category'], expense['description']))
    
    try:
        choice = int(input("Enter the ID of the expense to delete: ").strip())
        if 1 <= choice <= len(expenses):
            del expenses[choice - 1]
            save_expenses(username, expenses)
            print("Expense deleted successfully!")
        else:
            print("Invalid ID. No expense deleted.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    
    input("Press Enter to continue...")

def update_expense(username):
   
    clear_screen()
    print("===== Update Expense =====")
    expenses = load_expenses(username)
    
    if not expenses:
        print("No expenses found to update.")
        input("Press Enter to continue...")
        return
    
    print("{:<5} {:<12} {:<10} {:<20} {}".format("ID", "Date", "Amount", "Category", "Description"))
    print("-" * 80)
    for idx, expense in enumerate(expenses, start=1):
        print("{:<5} {:<12} {:<10} {:<20} {}".format(idx, expense['date'], expense['amount'], expense['category'], expense['description']))
    
    try:
        choice = int(input("Enter the ID of the expense to update: ").strip())
        if 1 <= choice <= len(expenses):
            expense = expenses[choice - 1]
            print("Leave blank to keep the current value.")
            new_date = input(f"Enter new date (current: {expense['date']}): ").strip()
            new_amount = input(f"Enter new amount (current: {expense['amount']}): ").strip()
            new_description = input(f"Enter new description (current: {expense['description']}): ").strip()
            update_cat = input("Do you want to update the category? (y/n): ").strip().lower()
            if update_cat == "y":
                new_category = select_category()
            else:
                new_category = ""
            
            if new_date:
                expense['date'] = new_date
            if new_amount:
                try:
                    float(new_amount)
                    expense['amount'] = new_amount
                except ValueError:
                    print("Invalid amount. Keeping the previous value.")
            if new_description:
                expense['description'] = new_description
            if new_category:
                expense['category'] = new_category
            
            expenses[choice - 1] = expense
            save_expenses(username, expenses)
            print("Expense updated successfully!")
        else:
            print("Invalid ID. No expense updated.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    
    input("Press Enter to continue...")

def analyze_expenses(username):
    """
    Analyze expenses by category and display a pie chart using matplotlib.
    """
    clear_screen()
    print("===== Expense Analysis by Category =====")
    expenses = load_expenses(username)
    
    if not expenses:
        print("No expenses found to analyze.")
        input("Press Enter to continue...")
        return
    
    # Calculate total amount for each category
    category_totals = {}
    for expense in expenses:
        try:
            amt = float(expense['amount'])
        except ValueError:
            amt = 0
        category = expense['category'] if expense['category'] else "Others"
        category_totals[category] = category_totals.get(category, 0) + amt
    
    labels = list(category_totals.keys())
    sizes = list(category_totals.values())
    
    if sum(sizes) == 0:
        print("No valid expense amounts to analyze.")
        input("Press Enter to continue...")
        return
    
    # Plotting the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Expenses by Category")
    plt.axis('equal')
    plt.show()
    
    input("Press Enter to continue...")

def summarize_expenses_by_category(username):
    """
    Summarize expenses by category.
    """
    clear_screen()
    print("===== Expense Summary by Category =====")
    expenses = load_expenses(username)
    
    if not expenses:
        print("No expenses found to summarize.")
        input("Press Enter to continue...")
        return
    
    category_summary = defaultdict(float)
    
    for expense in expenses:
        try:
            amount = float(expense['amount'])
        except ValueError:
            continue
        category = expense['category'] if expense['category'] else "Others"
        category_summary[category] += amount
    
    # Display Category Summary
    print("{:<20} {:<10}".format("Category", "Total"))
    print("-" * 30)
    for category, total in sorted(category_summary.items()):
        print("{:<20} {:<10.2f}".format(category, total))
    
    input("Press Enter to continue...")

def expense_tracker_menu(username):
   
    while True:
        clear_screen()
        print("===== Expense Tracker System =====")
        print(f"Logged in as: {username}")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Analyze Expenses (Pie Chart)")
        print("6. View Expense Summary by Category")
        print("7. Logout")
        print("----------------------------------")
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            add_expense(username)
        elif choice == "2":
            view_expenses(username)
        elif choice == "3":
            update_expense(username)
        elif choice == "4":
            delete_expense(username)
        elif choice == "5":
            analyze_expenses(username)
        elif choice == "6":
            summarize_expenses_by_category(username)
        elif choice == "7":
            print("Logging out...")
            input("Press Enter to continue...")
            break
        else:
            print("Invalid choice. Please select a valid option.")
            input("Press Enter to continue...")

def main():
    """
    Main function for the Expense Tracker System.
    """
    while True:
        clear_screen()
        print("===== Expense Tracker System =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print("----------------------------------")
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                expense_tracker_menu(user)
        elif choice == "3":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
