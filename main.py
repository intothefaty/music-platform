# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import login
import search_functions
from tracks import find_tracks
import windows

username = ""
sg.theme("DarkGrey13")

run_cond = True
val = None

while run_cond:

    window = login.user_login_screen()

    login_cond = True

    while login_cond:
        event, values = window.read()
        print(event)
        if event == "Login":
            val = login.user_login_button(values)
            if val is not None:
                username = val[1]
                email = val[0]
                is_artist = val[2]
                window.close()
        elif (event == None or event == "Cancel") and val != None:
            if is_artist == 0:
                window = windows.window_for_standart(find_tracks('All'))
            elif is_artist == 1:
                window.close()
                tracks = search_functions.search_artist(
                    username) + search_functions.search_cotracks(username)
                window = windows.window_for_artist(find_tracks(tracks))
        elif event == "lastmonth":
            try:
                selected_track = values["tracks"][0][0]
                count = search_functions.played_counter(selected_track)
                sg.popup("this song has been played " +
                         str(count)+" times in the last 1 month")
            except:
                sg.popup("Please Select A Track")
        elif event == "update_cancel":
            window.close()
            tracks = search_functions.search_artist(
                username) + search_functions.search_cotracks(username)
            window = windows.window_for_artist(find_tracks(tracks))
        elif event == "Update Track Info":
            window.close()
            try:
                selected_track = values["tracks"][0][0]
                track_infos = search_functions.get_track_info(selected_track)
                window.close()
                window = windows.track_update_page(
                    track_infos[0], track_infos[1], track_infos[2], track_infos[3], track_infos[4])
            except:
                sg.popup("Please Select A Track")
        elif event == "Update":
            try:
                search_functions.update_track(selected_track, values)
                sg.popup("Updated")
                tracks = search_functions.search_artist(
                    username) + search_functions.search_cotracks(username)
                window.close()
                window = windows.window_for_artist(find_tracks(tracks))
            except:
                sg.popup("Update Failed")
        elif event == "New Track" or event == "cancelnewalbum" or event == "create_cancel":
            albums = search_functions.list_artist_albums(username)
            window.close()
            window = windows.albums_artist_window(albums)
        elif event == "New Album":
            window.close()
            window = windows.new_album()
        elif event == "createalbum":
            album_name = values["newalbumname"]
            if album_name == "":
                sg.popup("Empty Input")
            else:
                search_functions.create_new_album(album_name, username)
                albums = search_functions.list_artist_albums(username)
                window.close()
                window = windows.albums_artist_window(albums)
        elif event == "Select Album":
            try:
                selected_album = values["albums"][0][0]
                window.close()
                window = windows.new_track(selected_album)
            except:
                sg.popup("Please Select an Album")
        elif event == "createtrack":
            try:
                search_functions.create_track(selected_album, values, username)
                sg.popup("Success")
                albums = search_functions.list_artist_albums(username)
                window.close()
                window = windows.albums_artist_window(albums)
            except:
                sg.popup("Failed")
        elif event == "Set Co-Artist":
            if values["tracks"][0][5] == username:
                try:
                    selected_track = values["tracks"][0][0]
                    window.close()
                    window = windows.set_coartist_window(selected_track)
                except:
                    sg.popup("Please Select a Track")
            else:
                sg.popup(
                    "You are co-artist for this song. You cannot set a co-artist.")
        elif event == "Add Co-Artist":
            try:
                check_artist = search_functions.check_artist(
                    values["coartist"], username)
                print(check_artist)
                if check_artist == "same":
                    sg.popup("Artist cannot be selected as a co-artist ")
                elif check_artist == "absent":
                    sg.popup("There is no user with this username")
                elif check_artist == "notartist":
                    sg.popup("This user is not an Artist")
                elif check_artist == "coartist":
                    search_functions.set_coartist(
                        selected_track, values["coartist"])
                    sg.popup("Success")
                    window.close()
                    tracks = search_functions.search_artist(
                        username) + search_functions.search_cotracks(username)
                    window = windows.window_for_artist(find_tracks(tracks))
            except:
                sg.popup("Failed")

        elif event == "Log Out" or event == sg.WIN_CLOSED:
            val = None
            login_cond = False
            window.close()
        elif event == "GenreSearch":
            if values["genre"] == '':
                sg.popup("Empty Input")
            else:
                track_ids = search_functions.search_genre(
                    values["genre"].capitalize())
                if track_ids == []:
                    sg.popup("Genre does not exist")
                else:
                    window.close()
                    window = windows.window_for_standart(
                        find_tracks(track_ids))
        elif event == "ArtistSearch":
            if values["artist"] == '':
                sg.popup("Empty Input")
            else:
                track_ids = search_functions.search_artist(
                    values["artist"].capitalize())
                if track_ids == []:
                    sg.popup("Artist does not exist")
                else:
                    window.close()
                    window = windows.window_for_standart(
                        find_tracks(track_ids))
        elif event == "AlbumSearch":
            if values["album"] == '':
                sg.popup("Empty Input")
            else:
                try:
                    track_ids = search_functions.search_album(
                        values["album"].capitalize())
                    window.close()
                    window = windows.window_for_standart(
                        find_tracks(track_ids))
                except:
                    sg.popup("Album does not exist")
        elif event == "Play Selected Track":
            try:
                seltrack = values["tracks"][0][0]
                search_functions.played(seltrack, username)
                track_info = search_functions.playing(seltrack)
                window.close()
                window = windows.play_window(track_info[0], track_info[1])
                for i in range(int(track_info[1])):
                    if event == "Back":
                        break
                    event, values = window.read(timeout=1000)
                    window["t"].Update(str(i))
                window.close()
                window = windows.window_for_standart(find_tracks('All'))
            except:
                sg.popup("Please Select A Track")
        elif event == "List Albums":
            window.close()
            window = windows.albums_window(search_functions.list_albums())
        elif event == "List All Tracks":
            window.close()
            window = windows.window_for_standart(find_tracks('All'))
        elif event == "Selected Album Details":
            try:
                selected_album = values["albums"][0][0]
                track_ids = search_functions.search_album(selected_album)
                window.close()
                window = windows.window_for_standart(find_tracks(track_ids))
            except:
                sg.popup("Please Select An Album")
        elif event == "History":
            window.close()
            history = search_functions.history(username)
            window = windows.history_window(history)
        elif event == "Back" or event == "Back0" or event == "Back1" or event == "cancelplaylists":
            window.close()
            window = windows.window_for_standart(find_tracks('All'))
        elif event == "List Playlists":
            window.close()
            window = windows.playlists_window(search_functions.list_playlists(username))
        elif event == "Open Selected Playlist":
            try:
                selected_playlist_info = values["playlists"][0]
                tracks = find_tracks(search_functions.open_playlist(selected_playlist_info[0]))
                window.close()
                window = windows.playlist_window(selected_playlist_info[1], selected_playlist_info[2], username, tracks)
            except:
                sg.popup("Please Select A Track")
        elif event == "cancelplaylists":
            tracks = find_tracks(search_functions.open_playlist(selected_playlist_info[0]))
            window.close()
            window = windows.playlist_window(selected_playlist_info[1], selected_playlist_info[2], username, tracks)
        elif event == "cancelplaylist" or event == "cr_pl_cancel":
            window.close()
            window = windows.playlists_window(search_functions.list_playlists(username))
        elif event == "Like":
            search_functions.like_playlist(selected_playlist_info[0],username)
            sg.popup("This Playlist Liked")
            window.close()
            window = windows.playlists_window(search_functions.list_playlists(username))
        elif event == "Unlike":
            search_functions.unlike_playlist(selected_playlist_info[0],username)
            sg.popup("This Playlist Unliked")
            window.close()
            window = windows.playlists_window(search_functions.list_playlists(username))
        elif event == "Add Track":
            window.close()
            window = windows.add_track_playlist_window(find_tracks('All'))
        elif event == "Add Selected Track":
            try:
                seltrack = values["tracksplaylist"][0][0]
                search_functions.add_track_into_playlist(selected_playlist_info[0],seltrack)
                sg.popup("Track Added")
                tracks = find_tracks(search_functions.open_playlist(selected_playlist_info[0]))
                window.close()
                window = windows.playlist_window(selected_playlist_info[1], selected_playlist_info[2], username, tracks)
            except:
                sg.popup("Please select a Track")
        elif event == "Add Playlist":
            window.close()
            window = windows.add_playlist_window()
        elif event == "Create Playlist":
            try:
                pl_name = values["pl_name"]
                search_functions.create_pl(pl_name, username,"1")
                window.close()
                window = windows.playlists_window(search_functions.list_playlists(username))
                sg.popup("Created")
            except:
                sg.popup("Failed")
        elif event == "Create Private Playlist":
            try:
                pl_name = values["pl_name"]
                search_functions.create_pl(pl_name, username,"0")
                window.close()
                window = windows.playlists_window(search_functions.list_playlists(username))
                sg.popup("Created")
            except:
                sg.popup("Failed")
        elif event == "List Users":
            window.close()
            window = windows.list_users_window(search_functions.list_users(username))
        elif event == "Follow Selected":
            other_username = values["users"][0][0]
            text = search_functions.follow_user(username, other_username)
            sg.popup(text)
            window.close()
            window = windows.list_users_window(search_functions.list_users(username))
        elif event == "Unfollow Selected":
            other_username = values["users"][0][0]
            text = search_functions.unfollow_user(username, other_username)
            sg.popup(text)
            window.close()
            window = windows.list_users_window(search_functions.list_users(username))
        elif event == "playplaylist":
            try:
                seltrack = values["tracksplaylist"][0][0]
                search_functions.played(seltrack, username)
                track_info = search_functions.playing(seltrack)
                window.close()
                window = windows.play_window(track_info[0], track_info[1])
                for i in range(int(track_info[1])):
                    if event == "Back":
                        break
                    event, values = window.read(timeout=1000)
                    window["t"].Update(str(i))
                tracks = find_tracks(search_functions.open_playlist(selected_playlist_info[0]))
                window.close()
                window = windows.playlist_window(selected_playlist_info[1], selected_playlist_info[2], username, tracks)
            except:
                sg.popup("Please Select A Track")
        elif event == "canceluser":
            window.close()
            window = windows.window_for_standart(find_tracks('All'))
            
            
            
            
            
    if event == sg.WIN_CLOSED:
        run_cond = False
