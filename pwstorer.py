import sqlite3
import random
import string
import time
import os
# Password to access program
PASSWORD = 'phoolsakhiji'

connect = input('What is your password?\n')

while connect != PASSWORD:
    connect = input('What is your password?\n')
    if connect == 'q':
        break

conn = sqlite3.connect('safe.db')


# Function that creates a secure password
def create_password():

    stringLength = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(stringLength))


if connect == PASSWORD:
    try:
        conn.execute('''CREATE TABLE SAFE
            (SERVICE TEXT PRIMARY KEY NOT NULL,
            PASSWORD TEXT NOT NULL,
            USERNAME TEXT);''')
        conn.commit()
        print("Your safe has been created!\nWhat would you like to store?")
    except Exception:
        print("What would you like to do today?")

while True:
    print('*' * 20)
    print('COMMANDS')
    print('gp = get password')
    print('sp = store password')
    print('mp = make password')
    print('q = quit program')
    print('*' * 20)
    input_ = input(':')

    if input_ == 'q':
        break
    if input_ == 'gp':
        service = input('Which serivce do you want the password for?\n')

        cursor = conn.execute(
            "SELECT PASSWORD FROM SAFE WHERE SERVICE = '" + service + "'"
            )
        for row in cursor:
            print("Password: ", row[0])
# Automatically copies password to clipboard
            os.system("echo '%s' | pbcopy" % row[0])
        conn.commit()
        time.sleep(3)

    if input_ == 'sp':
        service_name = input('What is the name of the service?\n')
        user_name = input('What is the username of the service?\n')
        password_name = input('What is the password?\n')

        conn.execute(
                "INSERT INTO SAFE (SERVICE, PASSWORD, USERNAME) VALUES ('"
                + service_name + "' , '" + password_name + "' , '"
                + user_name + "')"
                )
        print('Your password has been added sucessfully.')
        conn.commit()

    if input_ == 'mp':
        service_name = input('What is the name of the service?\n')
        user_name = input('What is the username of the service?\n')
        password_name = create_password()
        conn.execute(
                "INSERT INTO SAFE (SERVICE, PASSWORD, USERNAME) VALUES ('"
                + service_name + "' , '" + password_name + "' , '"
                + user_name + "')"
                )
        cursor = conn.execute(
            "SELECT PASSWORD FROM SAFE WHERE SERVICE = '" + service_name + "'"
            )
        for row in cursor:
            print("Password: ", row[0])
        conn.commit()

conn.close()
