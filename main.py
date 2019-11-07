import sqlite3
import random
import string
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

conn = sqlite3.connect('pwsafe.db')


class LoginWindow(Screen):

    # Verifies correct password
    def loginBtn(self):
        if self.admin_password.text == "password":
            sm.current = "menu"
            self.reset()
        else:
            InvalidPassword()
            self.reset()

    def CreateTable(self):
        conn.execute('''CREATE TABLE IF NOT EXISTS PWSAFE
            (SERVICE TEXT NOT NULL,
            PASSWORD TEXT NOT NULL,
            USERNAME TEXT,
            CREATION TEXT NOT NULL,
            PRIMARY KEY(SERVICE, CREATION));''')
        conn.commit()

    # clears out input text space
    def reset(self):
        self.admin_password.text = ""


class MenuWindow(Screen):
    pass


class GPWindow(Screen):

    service_text_input = ObjectProperty()

    def GetPassword(self):
        service_name = self.service_text_input.text
        if service_name != "":
            cursor = conn.execute(
                "SELECT USERNAME, PASSWORD, CREATION FROM PWSAFE WHERE\
                SERVICE ='" + service_name + "' AND CREATION =\
                (SELECT MAX(CREATION) FROM PWSAFE WHERE SERVICE= '"
                + service_name + "')"
                )
            # Automatically copies latest password to clipboard
            for row in cursor:
                os.system("echo '%s' | pbcopy" % row[0])
                conn.commit()
                # Popup
                GetPasswordSuccess(row[0], row[1], row[2])
                self.reset()
        else:
            EmptyService()
            self.reset()

    def reset(self):
        self.service_text_input.text = ""


class APWindow(Screen):

    service_text_input = ObjectProperty(None)
    username_text_input = ObjectProperty(None)
    password_text_input = ObjectProperty(None)

    def GeneratePassword(self):
        service_name = self.service_text_input.text
        password_name = create_password()
        user_name = self.username_text_input.text
        if service_name == "":
            EmptyService()
            self.reset()
        else:
            conn.execute(
                    "INSERT INTO PWSAFE (SERVICE, PASSWORD, USERNAME, CREATION)\
                    VALUES ('" + service_name + "' , '" + password_name +
                    "' , '" + user_name + "', CURRENT_TIMESTAMP)"
                    )
            conn.commit()
            AddPasswordSuccess()
            self.reset()

    def AddPassword(self):
        service_name = self.service_text_input.text
        password_name = self.password_text_input.text
        user_name = self.username_text_input.text
        if service_name == "":
            EmptyService()
            self.reset()
        else:
            conn.execute(
                    "INSERT INTO PWSAFE (SERVICE, PASSWORD, USERNAME, CREATION)\
                    VALUES ('" + service_name + "' , '" + password_name +
                    "' , '" + user_name + "', CURRENT_TIMESTAMP)"
                    )
            conn.commit()
            AddPasswordSuccess()
        self.reset()

    def reset(self):
        self.service_text_input.text = ""
        self.password_text_input.text = ""
        self.username_text_input.text = ""


class CSWindow(Screen):

    service_text_input = ObjectProperty()

    def CleanService(self):
        service_name = self.service_text_input.text
        if service_name == "":
            EmptyService()
        else:
            conn.execute(
                    "DELETE FROM PWSAFE WHERE SERVICE = '" + service_name +
                    "' AND CREATION <> (SELECT MAX(CREATION) FROM PWSAFE WHERE\
                    SERVICE= '" + service_name + "')"
                    )
            conn.commit
            CleanServiceSuccess(service_name)
            self.reset()

    def reset(self):
        self.service_text_input.text = ""


class WindowManager(ScreenManager):
    pass


# Popups for errors
# When I input the incorrect password to gain access
def InvalidPassword():
    popup = Popup(title="ERROR",
                  content=Label(text="Your Password is Incorrect!"),
                  pos_hint={"x": 0.25, "top": .75}, size_hint=(0.5, 0.5),
                  size=(1200, 1200))
    popup.open()


def GetPasswordSuccess(username, password, date):
    popup = Popup(title="SUCCESS",
                  content=Label(text="Username: " + username + "\nPassword: "
                                     + password + "\nCreated on: " + date),
                  pos_hint={"x": 0.25, "top": .75}, size_hint=(0.5, 0.5),
                  size=(1200, 1200))
    popup.open()


def EmptyService():
    popup = Popup(title="ERROR",
                  content=Label(text="Service is empty"),
                  pos_hint={"x": 0.25, "top": .75}, size_hint=(0.5, 0.5),
                  size=(1200, 1200))
    popup.open()


def NoService():
    popup = Popup(title="ERROR",
                  content=Label(text="That Service doesn't exist!"),
                  pos_hint={"x": 0.25, "top": .75}, size_hint=(0.5, 0.5),
                  size=(1200, 1200))
    popup.open()


def AddPasswordSuccess():
    popup = Popup(title="SUCCESS",
                  content=Label(text="Your Password has been added!"),
                  pos_hint={"x": 0.25, "top": .75}, size_hint=(0.5, 0.5),
                  size=(1200, 1200))
    popup.open()


def CleanServiceSuccess(service):
    popup = Popup(title="SUCCESS",
                  content=Label(text="Only your most recent " + service +
                                " password remains!"),
                  pos_hint={"x": 0.25, "top": .75}, size_hint=(0.5, 0.5),
                  size=(1200, 1200))
    popup.open()


# Function that creates a secure password
def create_password():

    stringLength = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(stringLength))


sm = WindowManager()
kv = Builder.load_file("PWStorer.kv")

screens = [LoginWindow(name="login"), MenuWindow(name="menu"),
           GPWindow(name="GP"), APWindow(name="AP"), CSWindow(name="CS")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
