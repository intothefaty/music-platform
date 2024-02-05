# -*- coding: utf-8 -*-
import sqlite3
import PySimpleGUI as sg
import re

def user_login_screen():
    layout = [[sg.Text("Welcome to Music Sharing System!")],
    [sg.Text("Enter your credentials:")],
    [sg.Text("Enter E-mail: ", size = (22,1)), sg.Input(size = (15,1), key = 'email')],
    [sg.Text("Password: ", size = (22,1)), sg.Input(size = (15,1), key = 'password')],
    [sg.Button("Login")]]

    return sg.Window("Login Window", layout)

def user_login_button(values):
    con2 = sqlite3.connect("sqlite2.db")
    cursor2 = con2.cursor()

    email = values["email"]
    password = values["password"]

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    
    if (re.fullmatch(regex, email)):
        sg.popup("Enter a valid E-mail.")
    else:
        cursor2.execute("select email, username, is_artist from User where email = '"+email+"' and Password='"+password+"'")
        row = cursor2.fetchone()

        if row is None:
            sg.popup("Incorrect Credentials.")
        else:
            sg.popup("Hi, %s" %  row[1])
            cursor2.close()
            con2.close()
            return row
    cursor2.close()
    con2.close()
    