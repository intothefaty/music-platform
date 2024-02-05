# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime, timedelta


def search_genre(types):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()

    track_ids = []

    for row in cursor.execute("Select tid From Tracks Where Genre = "+"'"+types+"'"):
        track_ids.append(row[0])

    cursor.close()
    con.close()

    return track_ids


def search_artist(artist_name):

    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()

    track_ids = []

    for row in cursor.execute("select tid from A_includes Where artistusername='"+artist_name+"'"):
        track_ids.append(row[0])

    cursor.close()
    con.close()
    return track_ids


def search_album(album_name):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()
    cursor2 = con.cursor()

    cursor2.execute("select id from albums where name='"+album_name+"'")
    album_id = cursor2.fetchone()

    track_ids = []

    for row in cursor.execute("select tid from A_includes Where aid='"+str(album_id[0])+"'"):
        track_ids.append(row[0])

    cursor.close()
    cursor2.close()
    con.close()
    return track_ids


def list_albums():
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()
    cursor2 = con.cursor()

    albums = []

    for row in cursor2.execute("select name from albums"):
        albums.append(row)

    cursor.close()
    cursor2.close()
    con.close()

    return albums


def history(username):
    con2 = sqlite3.connect("sqlite2.db")
    cursor2 = con2.cursor()
    cursor3 = con2.cursor()

    histories = []
    for row in cursor2.execute("select timestamp,tid from listenhistory where standardusername='"+username+"'"):

        cursor3.execute("select name from tracks where tid='"+str(row[1])+"'")
        t_name = cursor3.fetchone()
        row = list(row)
        print(row)
        row[1] = t_name[0]
        histories.append(row)

    cursor2.close()
    cursor3.close()
    con2.close()
    return histories


def played(track_id, username):
    con2 = sqlite3.connect("sqlite2.db")
    cursor2 = con2.cursor()

    cursor2.execute("SELECT * FROM listenhistory ORDER BY hid DESC LIMIT 1")
    history_id = str(cursor2.fetchone()[0]+1)
    x = str(datetime.now())[0:19]

    cursor2.execute("INSERT INTO listenhistory (hid,timestamp,tid,standardusername) VALUES (" +
                    history_id+",'"+x+"',"+str(track_id)+",'"+str(username)+"')")
    con2.commit()
    cursor2.close()
    con2.close


def playing(track_id):
    con2 = sqlite3.connect("sqlite2.db")
    cursor2 = con2.cursor()

    cursor2.execute("select name,lenght from tracks where tid="+str(track_id))
    info_arr = cursor2.fetchone()

    cursor2.close()
    con2.close

    return info_arr


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
            counter += 1
    cursor3.close()
    con3.close()
    return counter


def get_track_info(track_id):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()

    cursor.execute("select * from tracks where tid="+str(track_id))
    track_infos = cursor.fetchone()

    cursor.close()
    con.close()

    return track_infos


def update_track(track_id, track_info):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()

    track_info_t = (track_info["trackname_update"].capitalize(
    ), track_info["releasedate_update"], track_info["lenght_update"], track_info["genre_update"].capitalize())

    query = "update tracks set name=?,release_date=?,lenght=?,genre=? where tid=?"
    cursor.execute(query, track_info_t + (track_id,))

    con.commit()

    cursor.close()
    con.close()


def list_artist_albums(username):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()
    cursor2 = con.cursor()

    albums = []

    for row in cursor2.execute("select id,name from albums where username='"+username+"'"):
        albums.append(row)

    cursor.close()
    cursor2.close()
    con.close()

    return albums


def create_new_album(album_name, username):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()
    cursor2 = con.cursor()
    cursor3 = con.cursor()
    cursor.execute("SELECT * FROM albums ORDER BY id DESC LIMIT 1")
    album_id = str(cursor.fetchone()[0]+1)
    release_date = str(datetime.now())[0:10]
    cursor2.execute("insert into albums (id,name,release_date,username) values (" +
                    album_id+",'"+album_name.capitalize()+"','"+release_date+"','"+username+"')")
    cursor3.execute(
        "insert into create_a (aid,cusername) values ("+album_id+",'"+username+"')")
    con.commit()

    cursor.close()
    cursor2.close()
    cursor3.close()
    con.close()


def create_track(album_id, track_info, username):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()
    cursor2 = con.cursor()
    cursor3 = con.cursor()
    cursor4 = con.cursor()
    cursor2.execute("SELECT tid FROM tracks ORDER BY tid DESC LIMIT 1")
    track_id = str(cursor2.fetchone()[0]+1)
    cursor.execute("insert into tracks (tid,name,release_date,lenght,genre) values ("+track_id+",'"+track_info["trackname_create"].capitalize(
    )+"','"+track_info["releasedate_create"]+"','"+track_info["lenght_create"]+"','"+track_info["genre_create"].capitalize()+"')")
    cursor3.execute(
        "insert into create_t (tid,tusername) values ("+track_id+",'"+username+"')")
    cursor4.execute("insert into a_includes (tid,aid,artistusername) values (" +
                    track_id+","+str(album_id)+",'"+username+"')")
    con.commit()
    cursor.close()
    cursor2.close()
    cursor3.close()
    con.close()


def check_artist(coartist_username, username):
    if username == coartist_username:
        return "same"
    else:
        try:
            con = sqlite3.connect("sqlite2.db")
            cursor = con.cursor()
            cursor.execute(
                "select is_artist from user where username='"+coartist_username+"'")
            is_artist = cursor.fetchone()[0]
            cursor.close()
            con.close()
            if is_artist == 0:
                return "notartist"
            elif is_artist == 1:
                return "coartist"
        except:
            cursor.close()
            con.close()
            return "absent"


def set_coartist(track_id, coop_username):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()

    cursor.execute("insert into coop_track (tid,coop_username) values (" +
                   str(track_id)+",'"+coop_username+"')")
    con.commit()

    cursor.close()
    con.close()


def search_cotracks(username):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()

    track_ids = []

    for row in cursor.execute("select tid from coop_track where coop_username='"+username+"'"):
        track_ids.append(row[0])

    cursor.close()
    con.close()

    return track_ids


def myFunc(e):
  return len(e[2])

def myFunc2(e):
  return len(e[1])

def list_playlists(username):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()
    cursor2 = con.cursor()
    cursor3 = con.cursor()
    
    playlists = []
    
    for row in cursor.execute("select * from playlist"):
        addition = "Unliked"
        playlist_id = row[0]
        cursor2.execute("select standardusername from standardcreateplaylist where pid="+str(playlist_id))
        playlist_owner = cursor2.fetchone()[0]
        if playlist_owner == username:
            addition = "Mine"
            row2 = list(row)
            row2.pop()
            row2.append(addition)
            playlists.append(row2)
        else:
            if row[2] == 1:
                cursor3.execute("select * from standardlikesplaylist where pid="+str(playlist_id)+" and standardusername='"+username+"'")
                if cursor3.fetchone() is not None:
                    addition = "Liked"
                row2 = list(row)
                row2.pop()
                row2.append(addition)
                playlists.append(row2)
                
    cursor.close()
    cursor2.close()
    cursor3.close()
    con.close()
    
    playlists.sort(key=myFunc)
    
    return playlists
    
    
def open_playlist(playlist_id):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()
    
    tracks_ids = []
    
    for row in cursor.execute("select tid from p_includes where pid="+str(playlist_id)):
        tracks_ids.append(row[0])
    
    
    
    cursor.close()
    con.close()
    
    return tracks_ids
    
    
def like_playlist(playlist_id,username):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()
    
    cursor.execute("INSERT INTO standardlikesplaylist (pid,standardusername) VALUES (" +
                    str(playlist_id)+",'"+username+"')")

    con.commit()
    cursor.close()
    con.close()
    
def unlike_playlist(playlist_id,username):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()
    
    cursor.execute("delete from standardlikesplaylist where pid="+str(playlist_id)+" and standardusername='"+username+"'")

    con.commit()
    cursor.close()
    con.close()


def add_track_into_playlist(pid,tid):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()
    
    cursor.execute("insert into p_includes (pid,tid) values ("+str(pid)+","+str(tid)+")")
    
    con.commit()
    cursor.close()
    con.close()
    
    
def create_pl(pl_name,username,visibility):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()
    cursor2 = con.cursor()
    cursor3 = con.cursor()
    
    cursor3.execute("SELECT * FROM playlist ORDER BY pid DESC LIMIT 1")
    pid = str(cursor3.fetchone()[0]+1)
    
    cursor.execute("insert into playlist (pid,name,visibility) values ("+pid+",'"+pl_name+"',"+visibility+")")
    cursor2.execute("insert into standardcreateplaylist (pid,standardusername) values ("+pid+",'"+username+"')")
    
    con.commit()
    cursor.close()
    cursor2.close()
    cursor3.close()
    con.close()
    
    
    
def list_users(username):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()
    cursor2 = con.cursor()
    
    users = []
    
    for row in cursor.execute("select username from user where username!='"+username+"' and is_artist=0"):
        cursor2.execute("select * from follow where followername='"+row[0]+"' and followeername='"+username+"'")
        gg = cursor2.fetchone()
        if gg == None:
            is_follower = "Not Follower"
        else:
            is_follower = "Follower"
        
        cursor2.execute("select * from follow where followername='"+username+"' and followeername='"+row[0]+"'")
        wp = cursor2.fetchone()
        
        if wp == None:
            is_following = "Not Following"
        else:
            is_following = "Following"
        
        row2 = list(row)
        row2.append(is_follower)
        row2.append(is_following)
        users.append(row2)
    
    cursor.close()
    cursor2.close()
    con.close()
    users.sort(key=lambda i: ( myFunc(i), myFunc2(i) ))
    
    return users
    
    
def unfollow_user(username,other_username):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()
    cursor2 = con.cursor()
    
    cursor2.execute("select * from follow where followername='"+username+"' and followeername='"+other_username+"'")
    gg = cursor2.fetchone()
    if gg == None:
        cursor.close()
        cursor2.close()
        con.close()
        return "Not Already Followed"
    
    cursor.execute("delete from follow where followername='"+username+"' and followeername='"+other_username+"'")
    
    con.commit()
    cursor.close()
    cursor2.close()
    con.close()
    
    return "Successfully Unfollowed"
    
    
def follow_user(username,other_username):
    con = sqlite3.connect("sqlite2.db")
    cursor = con.cursor()
    cursor2 = con.cursor()
    
    cursor2.execute("select * from follow where followername='"+username+"' and followeername='"+other_username+"'")
    gg = cursor2.fetchone()
    if gg is not None:
        cursor.close()
        cursor2.close()
        con.close()
        return "Already Followed"
    
    
    cursor.execute("insert into follow (followername,followeername) values('"+username+"','"+other_username+"')")
    
    con.commit()
    cursor.close()
    con.close()
    
    return "Successfully Followed"
    
    






