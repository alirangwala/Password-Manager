import sqlite3
import random
import string
import time
import os
# import getpass
# connect = getpass.getpass('What is your password?\n')

# Password to access program

PASSWORD = 'password'

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
            (SERVICE TEXT NOT NULL,
            PASSWORD TEXT NOT NULL,
            USERNAME TEXT,
            CREATION TEXT NOT NULL,
            PRIMARY KEY(SERVICE, CREATION));''')
        conn.commit()
        print("Your safe has been created!\nWhat would you like to store?")
    except Exception:
        print("What would you like to do today?")

while True:
    print('*' * 20)
    print('COMMANDS')
    print('gp(h) = get password (hidden)')
    print('sp = store password')
    print('mp = make password')
    print('cs = clean service')
    print('q = quit program')
    print('*' * 20)
    input_ = input(':')

    if input_ == 'q':
        break
    if input_ == 'gp':
        service = input('Which serivce do you want the password for?\n')

        cursor = conn.execute(
            "SELECT PASSWORD, CREATION FROM SAFE WHERE SERVICE =\
            '" + service + "'"
            )
        for row in cursor:
            print("Password: " + row[0] + "   Created on: " + row[1])
# Automatically copies latest password to clipboard
            os.system("echo '%s' | pbcopy" % row[0])
        conn.commit()
        time.sleep(3)
# Option to copy latest password to clipboard and hide password in terminal
    if input_ == 'gph':
        service = input('Which serivce do you want the password for?\n')

        cursor = conn.execute(
            "SELECT PASSWORD, CREATION FROM SAFE WHERE SERVICE =\
            '" + service + "'"
            )
        for row in cursor:
            # Automatically copies latest password to clipboard
            os.system("echo '%s' | pbcopy" % row[0])
            print("Password has been copied")
        conn.commit()
        time.sleep(1)

    if input_ == 'sp':
        service_name = input('What is the name of the service?\n')
        user_name = input('What is the username of the service?\n')
        password_name = input('What is the password?\n')

        conn.execute(
                "INSERT INTO SAFE (SERVICE, PASSWORD, USERNAME, CREATION)\
                VALUES ('" + service_name + "' , '" + password_name + "' , '"
                + user_name + "', CURRENT_TIMESTAMP)"
                )
        print('Your password has been added sucessfully.')
        conn.commit()
        time.sleep(2)

    if input_ == 'mp':
        service_name = input('What is the name of the service?\n')
        user_name = input('What is the username of the service?\n')
        password_name = create_password()
        conn.execute(
                "INSERT INTO SAFE (SERVICE, PASSWORD, USERNAME, CREATION)\
                VALUES('" + service_name + "' , '" + password_name + "' , '"
                + user_name + "', CURRENT_TIMESTAMP)"
                )
        print('Your password has been created sucessfully.')
        conn.commit()
        time.sleep(2)
        # Clear all the passwords but the most recent
    if input_ == 'cs':

        service_name = input('What is the name of the service?\n')
        conn.execute(
                "DELETE FROM SAFE WHERE SERVICE = '" + service_name +
                "' AND CREATION <> (SELECT MAX(CREATION) FROM SAFE WHERE\
                SERVICE= '" + service_name + "')"
                )
        print('Only your most recent ' + service_name + ' password remains!')
        conn.commit()
        time.sleep(1)
        # Hidden capability: print out full database
    if input_ == 'pf':
        cursor = conn.execute(
            "SELECT * FROM SAFE"
            )
        for row in cursor:
            print(row[0], row[1], row[2], row[3])
    conn.commit()
    time.sleep(5)
conn.close()
