# -*- coding: utf-8 -*-

import sqlite3

def find_tracks(track_ids):
    print(track_ids)
    con2 = sqlite3.connect("sqlite2.db")
    cursor = con2.cursor()
    cursor2 = con2.cursor()
    cursor3 = con2.cursor()
    tracks=[]
    
    if track_ids=="All":
        for row in cursor2.execute('select * from Tracks'):
            row2 = list(row)
            cursor3.execute("select artistusername from A_includes where tid='"+str(row[0])+"'")
            artist_name = cursor3.fetchone()
            cursor3.execute("select aid from A_includes where tid='"+str(row[0])+"'")
            album_id = cursor3.fetchone()
            cursor.execute("select name from Albums where id='"+str(album_id[0])+"'")
            album_name = cursor.fetchone()
            row2.append(artist_name[0])
            row2.append(album_id[0])
            row2.append(album_name[0])
            tracks.append(row2)
    else:
        
        for track_id in track_ids:
            cursor2.execute("select * from Tracks where tid='"+str(track_id)+"'")
            row = cursor2.fetchone()
            row2 = list(row)
            cursor3.execute("select artistusername from A_includes where tid='"+str(row[0])+"'")
            artist_name = cursor3.fetchone()
            cursor3.execute("select aid from A_includes where tid='"+str(row[0])+"'")
            album_id = cursor3.fetchone()
            cursor.execute("select name from Albums where id='"+str(album_id[0])+"'")
            album_name = cursor.fetchone()
            row2.append(artist_name[0])
            row2.append(album_id[0])
            row2.append(album_name[0])
            tracks.append(row2)
        
    cursor.close()
    cursor2.close()
    cursor3.close()
    con2.close()
    
    return tracks