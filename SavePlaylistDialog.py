from Tkinter import *

class SavePlaylistDialog(object):
    def __init__(self, master, playlistObj):
        top = self.top = Toplevel(master)
        self.playlistObj = playlistObj
        self.saveLabel = Label(top, text="Playlist Name:")
        self.saveLabel.pack()
        self.playlistName = Entry(top)
        self.playlistName.pack()
        self.saveButton = Button(top, text="Save", command=self.cleanup)
        self.saveButton.pack()

    def cleanup(self):
        self.value = self.playlistName.get()
        self.playlistObj.savePlaylist(self)
        self.top.destroy()

