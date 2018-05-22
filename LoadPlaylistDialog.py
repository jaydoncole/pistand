from Tkinter import *
import re

class LoadPlaylistDialog(object):
    def __init__(self, master, playlistObj, playlists):
        top = self.top = Toplevel(master)
        self.playlistObj = playlistObj
        self.loadLabel = Label(top, text="Select Playlist")
        self.loadLabel.pack()
        self.selectedPlaylist = StringVar(master)
        self.playlistMenu = apply(OptionMenu, (top, self.selectedPlaylist) + tuple(playlists))
        self.playlistMenu.pack()
        self.deleteButton = Button(top, text="DELETE", command=self.deletePlaylist)
        self.deleteButton.pack()
        self.loadButton = Button(top, text="LOAD", command=self.loadPlaylist)
        self.loadButton.pack()

    def deletePlaylist(self):
        self.cleanup(self.playlistObj.deletePlaylist)

    def loadPlaylist(self):
        self.cleanup(self.playlistObj.loadPlaylist)

    def cleanup(self, callback):
        playlistId = re.search(r':(\d+)', self.selectedPlaylist.get())
        self.value = playlistId.group(0)[1:]
        callback(self)
        self.top.destroy()

