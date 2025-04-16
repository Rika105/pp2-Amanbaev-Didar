import psycopg2

# === CONNECT TO DB ===
def connect():
    return psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="Almaty2500505"  # измени на свой пароль, если надо
    )

# === 1. Insert or update user ===
def insert_or_update_user():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL insert_or_update_user(%s::TEXT, %s::TEXT)", (name, phone))
    print("Done!")


# === 2. Insert many users ===
def insert_many_users():
    names = input("Enter names (comma separated): ").split(",")
    phones = input("Enter phones (comma separated): ").split(",")

    if len(names) != len(phones):
        print("Number of names and phones must match!")
        return

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL insert_many_users(%s, %s)", (names, phones))
            try:
                cur.execute("FETCH ALL IN \"<unnamed portal 1>\";")  # если OUT возвращает курсор
                result = cur.fetchall()
                if result:
                    print("Invalid entries:")
                    for row in result:
                        print(row)
                else:
                    print("All inserted!")
            except:
                print("All inserted!")

# === 3. Search by pattern ===
def search_pattern():
    pattern = input("Enter search pattern: ")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_by_pattern(%s)", (pattern,))
            results = cur.fetchall()
            for row in results:
                print(row)

# === 4. Paginated query ===
def paginated_query():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_paginated_users(%s, %s)", (limit, offset))
            for row in cur.fetchall():
                print(row)

# === 5. Delete by name or phone ===
def delete_by_key():
    key = input("Enter name or phone to delete: ")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL delete_by_name_or_phone(%s)", (key,))
    print("Deleted.")

# === MAIN MENU ===
def menu():
    while True:
        print("\n==== PHONEBOOK MENU ====")
        print("1. Insert or update user")
        print("2. Insert many users")
        print("3. Search by pattern")
        print("4. Paginated query")
        print("5. Delete by name or phone")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            insert_or_update_user()
        elif choice == '2':
            insert_many_users()
        elif choice == '3':
            search_pattern()
        elif choice == '4':
            paginated_query()
        elif choice == '5':
            delete_by_key()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()