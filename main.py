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

    description = input("🔍 Describe your Pokémon or Animal Crossing expense: ")

    categories = get_categories(cur)
    print("🌈 Choose a category by number:")
    for idx, category in enumerate(categories):
        print(f"{idx + 1}. {category[0]}")
    print(f"{len(categories) + 1}. ✨ Create a new category")

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
        category = input("🆕 Enter the new category name: ")
    else:
        category = categories[category_choice - 1][0]

    card_name = None
    card_rarity = None
    plush_name = None
    plush_size = None
    game_platform = None
    subscription_name = None
    subscription_duration = None

    if category.lower() == "pokémon card":
        card_name = input("🃏 Enter the Pokémon card name: ")
        card_rarity = input("⭐ Enter the rarity of the Pokémon card: ")
    elif category.lower() == "pokémon plush":
        plush_name = input("🧸 Enter the Pokémon plush name: ")
        plush_size = input("📏 Enter the size of the Pokémon plush: ")
    elif category.lower() == "video game":
        print("🎮 Choose the game platform by number:")
        platforms = ["PC", "PS4", "Nintendo Switch", "Nintendo DS", "Nintendo 3DS"]
        for idx, platform in enumerate(platforms):
            print(f"{idx + 1}. {platform}")
        while True:
            try:
                platform_choice = int(input("🔢 Enter your choice: "))
                if 1 <= platform_choice <= len(platforms):
                    game_platform = platforms[platform_choice - 1]
                    break
                else:
                    print("⚠️ Invalid choice. Please select a valid number.")
            except ValueError:
                print("⚠️ Invalid input. Please enter a number.")
    elif category.lower() == "subscription service":
        subscription_name = input("🔔 Enter the subscription service name: ")
        subscription_duration = input("⏳ Enter the duration of the subscription (e.g., monthly, yearly): ")

    while True:
        currency = input("💱 Enter the currency (PokéCoins or Bells): ").strip().lower()
        if currency in ["pokécoins", "bells"]:
            break
        else:
            print("⚠️ Invalid currency. Please enter 'PokéCoins' or 'Bells'.")

    while True:
        price = input(f"💸 How many {currency.capitalize()} did it cost? ")
        try:
            price = float(price)
            break
        except ValueError:
            print(f"⚠️ Oops! That's not a valid number of {currency.capitalize()}.")

    try:
        cur.execute("""INSERT INTO expenses (Date, description, category, price, currency, card_name, card_rarity, plush_name, plush_size, game_platform, subscription_name, subscription_duration)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (date, description, category, price, currency, card_name, card_rarity, plush_name, plush_size, game_platform, subscription_name, subscription_duration))
        conn.commit()
        print("✅ Your expense has been added successfully.")
    except sqlite3.Error as e:
        print(f"⚠️ Oh no! An error occurred: {e}")

def view_all_expenses(cur):
    try:
        cur.execute("SELECT * FROM expenses")
        expenses = cur.fetchall()
        print("📜 All Expenses:")
        for expense in expenses:
            print(f"📅 Date: {expense[0]}, Description: {expense[1]}, Category: {expense[2]}, Cost: {expense[3]} {expense[4].capitalize()}")
            if expense[5]:
                print(f"🃏 Pokémon Card: {expense[5]}, ⭐ Rarity: {expense[6]}")
            if expense[7]:
                print(f"🧸 Pokémon Plush: {expense[7]}, 📏 Size: {expense[8]}")
            if expense[9]:
                print(f"🎮 Game Platform: {expense[9]}")
            if expense[10]:
                print(f"🔔 Subscription Service: {expense[10]}, ⏳ Duration: {expense[11]}")
    except sqlite3.Error as e:
        print(f"⚠️ Oh no! An error occurred: {e}")

def view_monthly_expenses(cur):
    month = input("🌟 Enter the month (MM): ")
    year = input("🌟 Enter the year (YYYY): ")
    try:
        cur.execute("""SELECT category, SUM(price), currency FROM expenses
                       WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
                       GROUP BY category, currency""", (month, year))
        expenses = cur.fetchall()
        print(f"🌟 Monthly Expenses for {month}/{year}:")
        for expense in expenses:
            print(f"🏷️ Category: {expense[0]}, 💰 Total: {expense[1]} {expense[2].capitalize()}")
    except sqlite3.Error as e:
        print(f"⚠️ Oh no! An error occurred: {e}")

def view_expenses_summary(cur):
    print("📊 Select an option:")
    print("1. 📜 View all expenses")
    print("2. 🌟 View monthly expenses by category")
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

    # Ensure the expenses table includes columns for card, plush, game, subscription, and currency details
    cur.execute("""CREATE TABLE IF NOT EXISTS expenses (
                    Date TEXT,
                    description TEXT,
                    category TEXT,
                    price REAL,
                    currency TEXT,
                    card_name TEXT,
                    card_rarity TEXT,
                    plush_name TEXT,
                    plush_size TEXT,
                    game_platform TEXT,
                    subscription_name TEXT,
                    subscription_duration TEXT)""")
    conn.commit()

    while True:
        print("📊 Select an option:")
        print("1. ➕ Enter a new expense")
        print("2. 📊 View expenses summary")
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
            print("🚪 Exiting the expense tracker.")
            break
        else:
            print("⚠️ Invalid choice. Please select a valid option.")

        repeat = input("🔄 Would you like to do something else (y/n)? ").lower()
        if repeat != "y":
            break

    close_db(conn)

if __name__ == "__main__":
    main()
