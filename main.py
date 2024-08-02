import sqlite3
import datetime

def connect_db():
    print("🔮 Connecting to the PokéDex database...")
    return sqlite3.connect("expenses.db")

def close_db(conn):
    conn.close()
    print("🔮 The PokéDex database connection has been closed.")

def get_categories(cur):
    cur.execute("SELECT DISTINCT category FROM expenses")
    return cur.fetchall()

def add_expense(cur, conn):
    while True:
        date = input("🌟 Enter the date of the expense (YYYY-MM-DD): ")
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("⚠️ Oops! That's not the right date format. Please use YYYY-MM-DD.")

    description = input("🔍 Describe your Pokémon expense: ")

    categories = get_categories(cur)
    print("🌈 Choose a category by number:")
    for idx, category in enumerate(categories):
        print(f"{idx + 1}. {category[0]}")
    print(f"{len(categories) + 1}. ✨ Create a new Pokémon category")

    while True:
        try:
            category_choice = int(input("🔢 Enter your choice: "))
            if 1 <= category_choice <= len(categories) + 1:
                break
            else:
                print("⚠️ Invalid choice. Please select a valid number.")
        except ValueError:
            print("⚠️ Invalid input. Please enter a number.")

    if category_choice == len(categories) + 1:
        category = input("🆕 Enter the new Pokémon category name: ")
    else:
        category = categories[category_choice - 1][0]

    while True:
        price = input("💸 How many PokéCoins did it cost? ")
        try:
            price = float(price)
            break
        except ValueError:
            print("⚠️ Oops! That's not a valid number of PokéCoins.")

    try:
        cur.execute("INSERT INTO expenses (Date, description, category, price) VALUES (?, ?, ?, ?)",
                    (date, description, category, price))
        conn.commit()
        print("✅ Your Pokémon expense has been added successfully.")
    except sqlite3.Error as e:
        print(f"⚠️ Oh no! An error occurred: {e}")

def view_all_expenses(cur):
    try:
        cur.execute("SELECT * FROM expenses")
        expenses = cur.fetchall()
        print("📜 All Pokémon Expenses:")
        for expense in expenses:
            print(f"📅 Date: {expense[0]}, Description: {expense[1]}, Category: {expense[2]}, Cost: {expense[3]} PokéCoins")
    except sqlite3.Error as e:
        print(f"⚠️ Oh no! An error occurred: {e}")

def view_monthly_expenses(cur):
    month = input("🌟 Enter the month (MM): ")
    year = input("🌟 Enter the year (YYYY): ")
    try:
        cur.execute("""SELECT category, SUM(price) FROM expenses
                       WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
                       GROUP BY category""", (month, year))
        expenses = cur.fetchall()
        print(f"🌟 Monthly Pokémon Expenses for {month}/{year}:")
        for expense in expenses:
            print(f"🏷️ Category: {expense[0]}, 💰 Total: {expense[1]} PokéCoins")
    except sqlite3.Error as e:
        print(f"⚠️ Oh no! An error occurred: {e}")

def view_expenses_summary(cur):
    print("📊 Select an option:")
    print("1. 📜 View all Pokémon expenses")
    print("2. 🌟 View monthly Pokémon expenses by category")
    try:
        view_choice = int(input("🔢 Enter your choice: "))
        if view_choice == 1:
            view_all_expenses(cur)
        elif view_choice == 2:
            view_monthly_expenses(cur)
        else:
            print("⚠️ Invalid choice.")
    except ValueError:
        print("⚠️ Invalid input. Please enter a number.")

def main():
    conn = connect_db()
    cur = conn.cursor()

    while True:
        print("📊 Select an option:")
        print("1. ➕ Enter a new Pokémon expense")
        print("2. 📊 View Pokémon expenses summary")
        print("3. 🚪 Exit")

        try:
            choice = int(input("🔢 Enter your choice: "))
        except ValueError:
            print("⚠️ Invalid input. Please enter a number.")
            continue

        if choice == 1:
            add_expense(cur, conn)
        elif choice == 2:
            view_expenses_summary(cur)
        elif choice == 3:
            print("🚪 Exiting the Pokémon expense tracker.")
            break
        else:
            print("⚠️ Invalid choice. Please select a valid option.")

        repeat = input("🔄 Would you like to do something else (y/n)? ").lower()
        if repeat != "y":
            break

    close_db(conn)

if __name__ == "__main__":
    main()
