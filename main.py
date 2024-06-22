import sqlite3
import datetime

def connect_db():
    return sqlite3.connect("expenses.db")

def close_db(conn):
    conn.close()

def get_categories(cur):
    cur.execute("SELECT DISTINCT category FROM expenses")
    return cur.fetchall()

def add_expense(cur, conn):
    while True:
        date = input("Enter the date of the expense (YYYY-MM-DD): ")
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    description = input("Enter the description of the expense: ")

    categories = get_categories(cur)
    print("Select a category by number:")
    for idx, category in enumerate(categories):
        print(f"{idx + 1}. {category[0]}")
    print(f"{len(categories) + 1}. Create a new category")

    while True:
        try:
            category_choice = int(input("Enter your choice: "))
            if 1 <= category_choice <= len(categories) + 1:
                break
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    if category_choice == len(categories) + 1:
        category = input("Enter the new category name: ")
    else:
        category = categories[category_choice - 1][0]

    while True:
        price = input("Enter the price of the expense: ")
        try:
            price = float(price)
            break
        except ValueError:
            print("Invalid price format. Please enter a number.")

    try:
        cur.execute("INSERT INTO expenses (Date, description, category, price) VALUES (?, ?, ?, ?)",
                    (date, description, category, price))
        conn.commit()
        print("Expense added successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def view_all_expenses(cur):
    try:
        cur.execute("SELECT * FROM expenses")
        expenses = cur.fetchall()
        for expense in expenses:
            print(expense)
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def view_monthly_expenses(cur):
    month = input("Enter the month (MM): ")
    year = input("Enter the year (YYYY): ")
    try:
        cur.execute("""SELECT category, SUM(price) FROM expenses
                       WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
                       GROUP BY category""", (month, year))
        expenses = cur.fetchall()
        for expense in expenses:
            print(f"Category: {expense[0]}, Total: {expense[1]}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def view_expenses_summary(cur):
    print("Select an option:")
    print("1. View all expenses")
    print("2. View monthly expenses by category")
    try:
        view_choice = int(input("Enter your choice: "))
        if view_choice == 1:
            view_all_expenses(cur)
        elif view_choice == 2:
            view_monthly_expenses(cur)
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main():
    conn = connect_db()
    cur = conn.cursor()

    while True:
        print("Select an option:")
        print("1. Enter a new expense")
        print("2. View expenses summary")
        print("3. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            add_expense(cur, conn)
        elif choice == 2:
            view_expenses_summary(cur)
        elif choice == 3:
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

        repeat = input("Would you like to do something else (y/n)? ").lower()
        if repeat != "y":
            break

    close_db(conn)

if __name__ == "__main__":
    main()
