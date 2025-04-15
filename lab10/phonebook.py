'''import psycopg2
import csv
import pandas as pd
from tabulate import tabulate 

conn = psycopg2.connect(host="localhost", dbname = "postgres", user = "postgres",
                        password = "Almaty250505", port = 5432,options='-c client_encoding=UTF8')
conn.set_client_encoding('UTF8')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS phonebook (
      user_id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      surname VARCHAR(255) NOT NULL, 
      phone VARCHAR(255) NOT NULL

)
""")
filepath = "Users\dasta\work\PP2_2024\lab10\student.csv"  
with open(filepath, 'r',encoding='utf-8') as f:
   
    next(f)
    reader = csv.reader(f)
    for row in reader:
        cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (row[0], row[1], row[2]))

conn.commit()


check = True
command = ''
temp = ''

name_var = ''
surname_var = ''
phone_var = ''
id_var = ''

start = True
back = False

back_com = ''
name_upd = ''
surname_upd = ''
phone_upd = ''

filepath = ''

while check:
    if start == True or back == True:
        start = False
        print("""
        List of the commands:
        1. Type "i" or "I" in order to INSERT data to the table.
        2. Type "u" or "U" in order to UPDATE data in the table.
        3. Type "q" or "Q" in order to make specidific QUERY in the table.
        4. Type "d" or "D" in order to DELETE data from the table.
        5. Type "f" or "F" in order to close the program.
        6. Type "s" or "S" in order to see the values in the table.
        """)
        command = str(input())
        
        #insert
        if command == "i" or command == "I":
            print('Type "csv" or "con" to choose option between uploading csv file or typing from console: ')
            command = ''
            temp = str(input())
            if temp == "con":
                name_var = str(input("Name: "))
                surname_var = str(input("Surname: "))
                phone_var = str(input("Phone: "))
                cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (name_var, surname_var, phone_var))
                conn.commit()
                back_com = str(input('Type "back" in order to return to the list of the commands: '))
                if back_com == "back":
                    back = True
            if temp == "csv":
                filepath = input("Enter a file path with proper extension: ")
                with open(str(filepath), 'r',encoding='utf-8') as f:
                # Skip the header row.
                    reader = csv.reader(f)
                    next(reader)
                    for row in reader:
                        cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (row[0], row[1], row[2]))
                conn.commit()

                    
                back_com = str(input('Type "back" in order to return to the list of the commands: '))
                if back_com == "back":
                    back = True

        #delete
        if command == "d" or command == "D":
            back = False
            command = ''
            phone_var = str(input('Type phone number which you want to delete: '))
            cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone_var,))
            conn.commit()
            back_com = str(input('Type "back" in order to return to the list of the commands: '))
            if back_com == "back":
                back = True
        
        #update
        if command == 'u' or command == 'U':
            back = False
            command = ''
            temp = str(input('Type the name of the column that you want to change: '))
            if temp == "name":
                name_var = str(input("Enter name that you want to change: "))
                name_upd = str(input("Enter the new name: "))
                cur.execute("UPDATE phonebook SET name = %s WHERE name = %s", (name_upd, name_var))
                conn.commit()
                back_com = str(input('Type "back" in order to return to the list of the commands: '))
                if back_com == "back":
                    back = True

            if temp == "surname":
                surname_var = str(input("Enter surname that you want to change: "))
                surname_upd = str(input("Enter the new surname: "))
                cur.execute("UPDATE phonebook SET surname = %s WHERE surname = %s", (surname_upd, surname_var))
                back_com = str(input('Type "back" in order to return to the list of the commands: '))
                if back_com == "back":
                    back = True

            if temp == "phone":
                name_var = str(input("Enter phone number that you want to change: "))
                name_upd = str(input("Enter the new phone number: "))
                cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s", (phone_upd, phone_var))
                back_com = str(input('Type "back" in order to return to the list of the commands: '))
                if back_com == "back":
                    back = True
        
        #query
        if command == "q" or command == "Q":
            back = False
            command = ''
            temp = str(input("Type the name of the column which will be used for searching data: "))
            if temp == "id":
                id_var = str(input("Type id of the user: "))
                cur.execute("SELECT * FROM phonebook WHERE user_id = %s", (id_var, ))
                rows = cur.fetchall()
                print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"]))
                back_com = str(input('Type "back" in order to return to the list of the commands: '))
                if back_com == "back":
                    back = True
            
            if temp == "name":
                name_var = str(input("Type name of the user: "))
                cur.execute("SELECT * FROM phonebook WHERE name = %s", (name_var, ))
                rows = cur.fetchall()
                print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"]))
                back_com = str(input('Type "back" in order to return to the list of the commands: '))
                if back_com == "back":
                    back = True
            
            if temp == "surname":
                surname_var = str(input("Type surname of the user: "))
                cur.execute("SELECT * FROM phonebook WHERE surname = %s", (surname_var, ))
                rows = cur.fetchall()
                print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"]))
                back_com = str(input('Type "back" in order to return to the list of the commands: '))
                if back_com == "back":
                    back = True
                
            if temp == "phone":
                phone_var = str(input("Type phone number of the user: "))
                cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone_var, ))
                rows = cur.fetchall()
                print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"]))
                back_com = str(input('Type "back" in order to return to the list of the commands: '))
                if back_com == "back":
                    back = True

        
        #display
        if command == "s" or command == "S":
            back = False
            command = ''
            cur.execute("SELECT * from phonebook;")
            rows = cur.fetchall()
            print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))
            back_com = str(input('Type "back" in order to return to the list of the commands: '))
            if back_com == "back":
                back = True
        #finish
        if command == "f" or command == "F":
            command = ''
            check = False
        

conn.commit()
cur.close()
conn.close()'''
import psycopg2
import csv

# === CONNECT TO DB ===
def connect():
    return psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="Almaty2500505"  # change this
    )

# === INSERT FROM CONSOLE ===
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    print("Added!")

# === INSERT FROM CSV ===
def insert_from_csv(path):
    with connect() as conn:
        with conn.cursor() as cur:
            with open(path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
    print("CSV imported!")

# === UPDATE ===
def update_user(name, new_phone):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, name))
    print("Updated!")

# === QUERY ===
def query_all():
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook")
            for row in cur.fetchall():
                print(row)

def query_by_name(name):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook WHERE name = %s", (name,))
            print(cur.fetchall())

# === DELETE ===
def delete_user(name):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
    print("Deleted!")

# === MAIN MENU ===
def menu():
    while True:
        print("\n1. Insert (console)")
        print("2. Insert (CSV)")
        print("3. Update user")
        print("4. View all")
        print("5. Search by name")
        print("6. Delete user")
        print("7. Exit")

        choice = input("Choose: ")

        if choice == '1':
            insert_from_console()
        elif choice == '2':
            insert_from_csv(input("Enter CSV path: "))
        elif choice == '3':
            update_user(input("Name to update: "), input("New phone: "))
        elif choice == '4':
            query_all()
        elif choice == '5':
            query_by_name(input("Name: "))
        elif choice == '6':
            delete_user(input("Name to delete: "))
        elif choice == '7':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()