# -*- coding: utf-8 -*-

import PySimpleGUI as sg


def window_for_artist(tracks):
    layout = [[sg.Text("Tracks Displayed")],
              [sg.Listbox(tracks, size=(70, 10), key="tracks")],
              [sg.Text("Number of plays for the past month : "),
               sg.Button("Search", key="lastmonth")],
              [sg.Button("New Track", size=(20))],
              [sg.Button("Update Track Info", size=(20))],
              [sg.Button("Set Co-Artist", size=(20))],
              [sg.Button("Log Out", size=(20))]]

    return sg.Window("Musics for Searching", layout)


def window_for_standart(tracks):

    layout = [[sg.Text("Tracks Displayed")],
              [sg.Listbox(tracks, size=(60, 10), key="tracks")],
              [sg.Text("Genre", size=(10, 1)), sg.Input(
                  key="genre", size=(30)), sg.Button("Search", key="GenreSearch")],
              [sg.Text("Artist Name", size=(10, 1)), sg.Input(
                  key="artist", size=(30)), sg.Button("Search", key="ArtistSearch")],
              [sg.Text("Album Name", size=(10, 1)), sg.Input(
                  key="album", size=(30)), sg.Button("Search", key="AlbumSearch")],
              [sg.Button("List Albums", size=(20))],
              [sg.Button("Play Selected Track", size=(20))],
              [sg.Button("List All Tracks", size=(20))],
              [sg.Button("List Playlists", size=(20))],
              [sg.Button("List Users", size=(20))],
              [sg.Button("History", size=(20))],
              [sg.Button("Log Out", size=(20))]]

    return sg.Window("Music Share Platform", layout)


def albums_window(albums):
    layout = [[sg.Text("Albums Displayed")],
              [sg.Listbox(albums, size=(60, 10), key="albums")],
              [sg.Button("Selected Album Details", size=(20))],
              [sg.Button("Back", size=(20))]]

    return sg.Window("Albums", layout)


def history_window(histories):
    layout = [[sg.Text("History Displayed")],
              [sg.Listbox(histories, size=(60, 30), key="history")],
              [sg.Button("Back", size=(20))]]

    return sg.Window("History", layout)


def play_window(track, duration):
    layout = [[sg.Text("Playing "+track)],
              [sg.Text("Time: "), sg.Text("0", key="t"),
               sg.Text(" / "+str(duration))],
              [sg.Button("Back")]]

    return sg.Window("Play", layout)


def track_update_page(track_id, track_name, track_release, track_lenght, track_genre):
    layout = [[sg.Text("Track ID: "+str(track_id), size=20)],
              [sg.Text("Track Name: ", size=20), sg.Input(
                  track_name, key="trackname_update", size=(30))],
              [sg.Text("Release Date: ", size=20), sg.Input(
                  track_release, key="releasedate_update", size=(30))],
              [sg.Text("Lenght: ", size=20), sg.Input(
                  track_lenght, key="lenght_update", size=(30))],
              [sg.Text("Genre: ", size=20), sg.Input(
                  track_genre, key="genre_update", size=(30))],
              [sg.Button("Update", size=(20)), sg.Button("Cancel", size=(20), key="update_cancel")]]

    return sg.Window("Update Track Info", layout)


def albums_artist_window(albums):
    layout = [[sg.Text("Albums Displayed")],
              [sg.Listbox(albums, size=(60, 10), key="albums")],
              [sg.Button("New Album", size=(20))],
              [sg.Button("Select Album", size=(20))],
              [sg.Button("Cancel", size=(20))]]

    return sg.Window("Albums", layout)


def new_album():
    layout = [[sg.Text("Album Name"), sg.Input(key="newalbumname", size=(30))],
              [sg.Button("Create", key="createalbum")],
              [sg.Button("Cancel", key="cancelnewalbum")]]

    return sg.Window("Albums", layout)


def new_track(album_id):
    layout = [[sg.Text("Album ID: "+str(album_id), size=20)],
              [sg.Text("Track Name: ", size=20), sg.Input(
                  key="trackname_create", size=(30))],
              [sg.Text("Release Date: ", size=20), sg.Input(
                  key="releasedate_create", size=(30))],
              [sg.Text("Lenght: ", size=20), sg.Input(
                  key="lenght_create", size=(30))],
              [sg.Text("Genre: ", size=20), sg.Input(
                  key="genre_create", size=(30))],
              [sg.Button("Create", key="createtrack", size=(20)), sg.Button("Cancel", size=(20), key="create_cancel")]]

    return sg.Window("Create Track Info", layout)


def set_coartist_window(track_id):
    layout = [[sg.Text("Track ID: "+str(track_id))],
              [sg.Text("Co-Artist Username", size=(20)),
               sg.Input(key="coartist", size=(30))],
              [sg.Button("Add Co-Artist")],
              [sg.Button("Cancel")]]

    return sg.Window("Add Co-Artist", layout)


def playlists_window(playlists):
    layout = [[sg.Text("Playlists")],
              [sg.Listbox(playlists,size=(60, 10), key="playlists")],
              [sg.Button("Open Selected Playlist")],
              [sg.Button("Add Playlist")],
              [sg.Button("Cancel",key="cancelplaylists")]]

    return sg.Window("Playlists", layout)

def playlist_window(playlist_name,is_liked,username,tracks):
    layout = [[sg.Text(playlist_name)],
              [sg.Listbox(tracks,size=(60,10),key="tracksplaylist")],
              [sg.Button("Play Selected Track",key="playplaylist")]
        ]
    if is_liked == "Liked":
        layout.append([sg.Button("Unlike")])
    elif is_liked == "Unliked":
        layout.append([sg.Button("Like")])
    elif is_liked == "Mine":
        layout.append([sg.Button("Add Track")])
        
    layout.append([sg.Button("Cancel",key="cancelplaylist")])
    
    return sg.Window("Playlist", layout)

def add_track_playlist_window(tracks):
    layout = [[sg.Listbox(tracks,size=(60,10),key="tracksplaylist")],
              [sg.Button("Add Selected Track")],
              [sg.Button("Cancel",key="cancelplaylist")]
        ]
    
    return sg.Window("Add Track", layout)



def add_playlist_window():
    layout = [[sg.Text("Playlist Name", size=(20)),
               sg.Input(key="pl_name", size=(30))],
              [sg.Button("Create Public Playlist",key="Create Playlist")],
              [sg.Button("Create Private Playlist",key="Create Private Playlist")],
              [sg.Button("Cancel",key="cr_pl_cancel")]
        ]
    
    return sg.Window("Create Playlist", layout)


def list_users_window(users):
    layout = [[sg.Listbox(users,size=(60,10),key="users")],
              [sg.Button("Follow Selected")],
              [sg.Button("Unfollow Selected")],
              [sg.Button("Cancel",key="canceluser")],
        ]

    return sg.Window("Users", layout)






