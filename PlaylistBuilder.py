import Tkinter as tk
import tkMessageBox
import os
from Song import Song
from SavePlaylistDialog import SavePlaylistDialog
from LoadPlaylistDialog import LoadPlaylistDialog
import sqlite3

# SQL Table Structure
# CREATE TABLE playlist (
#   id INTEGER PRIMARY KEY AUTOINCREMENT,
#   name VAR_CHAR(255));
# CREATE TABLE playlist_entry (
#   id INTEGER PRIMARY KEY AUTOINCREMENT, 
#   playlist_id INTEGER, 
#   song_reference VAR_CHAR(255));

class PlaylistBuilder(tk.Frame):
    master_songlist = []
    filtered_songlist = []

    def __init__(self, parent, controller):

        self.controller = controller
        self.parent = parent
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Create Your Playlist")

        # Connect to sqlite db
        self.conn = sqlite3.connect(controller.dirname + '/pistand.db')
        self.cursor = self.conn.cursor()

        # Frame to hold the song lists and transfer buttons
        self.songlistFrame = tk.Frame(self)

        # Frame to hold the buttons
        self.buttonFrame = tk.Frame(self)

        # Create the filter box
        filtervalue = tk.StringVar()
        self.filterLabel = tk.Label(self.songlistFrame, text = "Filter:")
        self.filterInput = tk.Entry(self.songlistFrame, textvariable = filtervalue)
        filtervalue.trace("w", lambda name, index, mode, filtervalue=filtervalue: self.filterSonglist(filtervalue.get()))

        # Create the master song list
        self.load_songs()
        self.masterList = tk.Listbox(self.songlistFrame, selectmode=tk.EXTENDED, width=30, height=30)
        for mastersongs in self.master_songlist:
            self.masterList.insert(tk.END, mastersongs)
        # Create button the transfer from master list to playlist
        self.transferButton = tk.Button(self.songlistFrame, text=">>"
                , command = self.transferCallback)
        # Create button to remove from playlist
        self.removeButton = tk.Button(self.songlistFrame, text='<<'
                , command = self.removeFromPlaylist)
        # Create the playlist song list
        self.playlist = tk.Listbox(self.songlistFrame, selectmode=tk.EXTENDED, width=30, height=30)

        # Button to move selected items in the playlist up
        self.moveUpButton = tk.Button(self.songlistFrame, text="/\\", command = self.movePlaylistUp)

        # Button to move selected items in the playlist down
        self.moveDownButton = tk.Button(self.songlistFrame, text="\\/", command = self.movePlaylistDown)

        # Create the button to play the playlsit
        self.playButton = tk.Button(self.buttonFrame, text="PLAY", command = self.launchPlayMode)

        # Display the elements
        self.label.pack(side = tk.TOP, fill="x", pady = 10)

        self.filterLabel.grid(row=1, column=1)
        self.filterInput.grid(row=1, column=2, columnspan=2)
        self.masterList.grid(row=2, column=1, rowspan=2)
        self.transferButton.grid(row=2, column=2)
        self.removeButton.grid(row=3, column=2)
        self.playlist.grid(row=2, column=3, rowspan=2)
        self.moveUpButton.grid(row=2, column=4)
        self.moveDownButton.grid(row=3, column=4)
        self.songlistFrame.pack(side = tk.TOP)
        self.playButton.pack(side = tk.LEFT)
        self.buttonFrame.pack(side = tk.TOP)

    def setup_menu(self):
        self.controller.add_menu_command("Load Playlist", self.loadPlaylistDialog)
        self.controller.add_menu_command("Save Playlist", self.savePlaylistDialog)
        self.controller.add_menu_command("Exit", self.quit)


    def filterSonglist(self, filterValue):
        self.filtered_songlist = []
        self.masterList.delete(0, self.masterList.size() - 1)
        for song in self.master_songlist:
            if(filterValue in song.album or filterValue in song.artist or filterValue in song.title):
                self.filtered_songlist.append(song)
        for song in self.filtered_songlist:
            self.masterList.insert(tk.END, song)

    def launchPlayMode(self):
        self.controller.Playlist = []
        for song in self.playlist.get(0, self.playlist.size() - 1):
            for songObj in self.master_songlist:
                if song == str(songObj):
                    self.controller.Playlist.append(songObj)
                    break
        self.controller.show_frame("MusicStand")


    def transferCallback(self):
        selectedSongs = self.masterList.curselection()
        for selected in selectedSongs:
            self.playlist.insert(tk.END, self.filtered_songlist[selected])

    def removeFromPlaylist(self):
        selectedSongs = self.playlist.curselection()
        for selected in reversed(selectedSongs):
            self.playlist.delete(selected)

    def load_songs(self):
        artists = os.listdir(self.controller.musicFolder)
        for artist in artists:
            artistsAlbums = os.listdir(self.controller.musicFolder + '/' + artist)
            for album in artistsAlbums:
                albumsongs = os.listdir(self.controller.musicFolder + '/' + artist + '/' + album)
                for song in albumsongs:
                    songObj = Song(album, artist, song)
                    song_files = os.listdir(self.controller.musicFolder + '/' + artist + '/' + album + '/' + song)
                    for file in song_files:
                        songObj.add_file(file)
                    self.master_songlist.append(songObj)
        self.filtered_songlist = self.master_songlist

    def movePlaylistDown(self):
        for song in reversed(self.playlist.curselection()):
            if song < self.playlist.size() - 1:
                songText = self.playlist.get(song)
                self.playlist.delete(song)
                self.playlist.insert(song + 1, songText)
                self.playlist.selection_set(song + 1)

    def movePlaylistUp(self):
        for song in self.playlist.curselection():
            if(song > 0):
                songText = self.playlist.get(song)
                self.playlist.delete(song)
                self.playlist.insert(song - 1, songText)
                self.playlist.selection_set(song-1)

    def savePlaylistDialog(self):
        self.popup = SavePlaylistDialog(self.parent, self)
        self.parent.wait_window(self.popup.top)

    def savePlaylist(self, popupObject):
        if self.playlist.size() > 0:
            playlistName = popupObject.value
            self.cursor.execute('INSERT INTO playlist(name) VALUES(?)', (playlistName, ))
            playlistId = self.cursor.lastrowid
            for song in self.playlist.get(0, self.playlist.size() - 1):
                self.cursor.execute('INSERT INTO playlist_entry (playlist_id, song_reference) VALUES(?, ?)', (playlistId, song))
            self.conn.commit()


    def loadPlaylistDialog(self):
        self.cursor.execute('SELECT id, name FROM playlist ORDER BY name ASC')
        res = self.cursor.fetchall()
        playlists = []
        for playlistId, name in res:
            playlists.append(name + " :"+str(playlistId))
        self.popup = LoadPlaylistDialog(self.parent, self, playlists)
        self.parent.wait_window(self.popup.top)

    def loadPlaylist(self, popupWindow):
        playlistId = popupWindow.value
        self.cursor.execute('SELECT song_reference FROM playlist_entry WHERE playlist_id = ? ORDER BY id ASC', (playlistId,))
        songs = self.cursor.fetchall()
        print songs
        for song in songs:
            self.playlist.insert(tk.END, song[0])

    def deletePlaylist(self, popupWindow):
        playlistId = popupWindow.value
        self.cursor.execute('DELETE FROM playlist_entry WHERE playlist_id = ?', (playlistId,))
        self.cursor.execute('DELETE FROM playlist WHERE id = ?', (playlistId,))
        self.conn.commit()


