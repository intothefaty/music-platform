# -*- coding: utf-8 -*-

import sqlite3
import PySimpleGUI as sg
from datetime import datetime
from login import user_login_screen,user_login_button,u_name,uemail,window
from tracks import list_all_tracks

sg.theme("DarkGrey13")

def window_for_standart(tracks):
    
    layout = [[sg.Text("Tracks Displayed")],
    [sg.Listbox(tracks, size = (50, 10), key = "tracks")],
    [sg.Text("Genre", size = (10,1)),sg.Input(key = "genre",size=(30)),sg.Button("Search")],
    [sg.Text("Artist Name", size = (10,1)),sg.Input(key = "artist",size=(30)),sg.Button("Search")],
    [sg.Text("Album Name", size = (10,1)),sg.Input(key = "album",size=(30)),sg.Button("Search")],
    [sg.Button("List Albums",size=(20))],
    [sg.Button("Play Selected Track",size=(20))],
    [sg.Button("List All Tracks",size=(20))],
    [sg.Button("History",size=(20))],
    [sg.Button("Log Out",size=(20))]]
    return sg.Window("Music Share Platform", layout)
    
    
def window_for_artist(tracks):

    layout = [[sg.Text("Tracks Displayed")],
    [sg.Listbox(tracks, size = (200, 10), key = "tracktosearch")]]

    return sg.Window("Musics for Searching", layout) 
    
    
    

    


    
def played_counter(track_id):
    counter = 0
    con3 = sqlite3.connect("sqlite2.db")
    cursor3 = con3.cursor()
    
    for row in cursor3.execute("SELECT * FROM Listenhistory WHERE tid ='"+str(track_id)+"'"):
        datetime_object = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        datetime_now = datetime.now()
        
        difference = datetime_now - datetime_object
        
        one_month = timedelta(days=30)

        if difference <= one_month:
            counter+=1
    cursor3.close()
    con3.close()
    return counter

    
def display_own(artist_user_name):
    con2 = sqlite3.connect("sqlite2.db")
    cursor2 = con2.cursor()
    cursor3 = con2.cursor()
    
    tracks=[]

    for row in cursor2.execute('select * from Tracks'):
        cursor3.execute("select artistusername from A_includes where tid='"+str(row[0])+"'")
        a_name = cursor3.fetchone()
        row2 = list(row)
        row2.append(a_name[0])
        if row2[5]==artist_user_name:
            counter = played_counter(row2[0])
            row2.pop()
            row2.append(counter)
            tracks.append(row2)
    
    cursor2.close()
    cursor3.close()
    con2.close()
    
    return tracks




    
def list_albums():
    con2 = sqlite3.connect("sqlite2.db")
    cursor2 = con2.cursor()
    cursor3 = con2.cursor()
    tracks = []
    for row in cursor2.execute("select id,name,username from Albums"):
        tracks.append(row)
    cursor2.close()
    cursor3.close()
    con2.close()
    return tracks


def list_album(album_id):
    con2 = sqlite3.connect("sqlite2.db")
    cursor2 = con2.cursor()
    cursor3 = con2.cursor()
    ts = []
    tracks = []
    for row in cursor2.execute("select tid from A_includes where aid='"+str(album_id)+"'"):
        tracks.append(row[0])
    for track in tracks:
        for row in cursor2.execute('select * from Tracks'):
            cursor3.execute("select artistusername from A_includes where tid='"+str(row[0])+"'")
            a_name = cursor3.fetchone()
            row2 = list(row)
            row2.append(a_name[0])
            if row2[0]==track:
                ts.append(row2)
    cursor2.close()
    cursor3.close()
    con2.close()
    return ts
    

def played(track_id):
    con2 = sqlite3.connect("sqlite2.db")
    cursor2 = con2.cursor()
    
    cursor2.execute("SELECT * FROM listenhistory ORDER BY hid DESC LIMIT 1")
    history_id = str(cursor2.fetchone()[0]+1)
    x = str(datetime.now())[0:19]
    
    cursor2.execute("INSERT INTO listenhistory (hid,timestamp,tid,standardusername) VALUES ("+history_id+",'"+x+"',"+str(track_id)+",'"+str(u_name)+"')")
    con2.commit()
    cursor2.close()
    con2.close
    
    
def history():
    con2 = sqlite3.connect("sqlite2.db")
    cursor2 = con2.cursor()
    cursor3 = con2.cursor()
    
    histories = []
    for row in cursor2.execute("select timestamp,tid from listenhistory where standardusername='"+u_name+"'"):
        cursor3.execute("select name from tracks where tid='"+str(row[1])+"'")
        t_name = cursor3.fetchone()
        row = list(row)
        row[1] = t_name[0]
        histories.append(row)
        
    cursor2.close()
    cursor3.close()
    con2.close()
    return histories
    
    
    

global u_name
global uemail
    

window = user_login_screen()
all_tracks = list_all_tracks('All')
Type="all"
while 1:
    event, values = window.read()
    if event == "Login":
        val = user_login_button(values)
        if val is not None:
            u_name = val[0]
            uemail = val[1]
            is_artist = val[2]
    elif event == "Search":
        if values["genre"]=='':
            sg.popup("Empty Input")
        else:
            filtered = search_genre(values["genre"])
            if filtered==[]:
                sg.popup("Genre does not exist")
            else:
                window.close()
                window = window_for_standart(filtered)
    elif event == "Search0":
        if values["artist"]=='':
            sg.popup("Empty Input")
        else:
            artist_name = search_artist(values["artist"])
            if artist_name==[]:
                sg.popup("Artist does not exist")
            else:
                window.close()
                window = window_for_standart(artist_name)
        
    
    elif event == "Search1":
        window.close()
        window = window_for_standart(list_albums())
        
    elif event == "Details":
        if past_event=="List":
            try:
                seltrack= values["tracktosearch"][0][0]
                window.close()
                window = window_for_standart(list_album(seltrack))
            except:
                sg.popup("Please Select An Album")
        else:
            event=past_event
            sg.popup("Please list albums before selecting albums")
    elif event == "Go":
        window.close()
        window = window_for_standart(list_all_tracks())
    elif event == "Play":
        if past_event=="List" or past_event=="History":
            event=past_event
            sg.popup("Tracks cannot be played in this menu")
        else:
            try:
                seltrack= values["tracktosearch"][0][0]
                played(seltrack)
                sg.popup("Played")
            except:
                sg.popup("Please Select A Track")
    
    elif event == "History":
        window.close()
        window = window_for_standart(history())
        
    elif event == sg.WIN_CLOSED:
        break
    past_event = event
    
    
    
    
    