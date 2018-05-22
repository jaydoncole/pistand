from Tkinter import *
from PlaylistBuilder import PlaylistBuilder
from MusicStand import MusicStand
import os

class PiStand:
    Playlist = []
    musicFolder = 'music'
    dirname = ''

    def __init__(self, master):
        self.dirname = os.path.dirname(os.path.realpath(__file__))
        self.musicFolder = self.dirname + "/" + self.musicFolder
        container = Frame(master)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        # Set up the menu
        self.menu = Menu(master, tearoff=0)
        master.config(menu=self.menu)
        self.reset_menu()

        self.set_window_size(master)
        self.setup_window_frames(container)

    def show_frame(self, page_name):
        self.reset_menu()
        frame = self.frames[page_name]
        frame.tkraise()
        frame.focus_set()
        frame.setup_menu()
        if page_name == "MusicStand":
            frame.pagefiles = []
            frame.loadplaylist()

    def set_window_size(self, master):
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth(), master.winfo_screenheight()
        ))

    def setup_window_frames(self, container):
        self.frames = {}
        for Screen in(PlaylistBuilder, MusicStand):
            page_name = Screen.__name__
            frame = Screen(parent = container, controller = self)
            self.frames[page_name] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
        self.show_frame("PlaylistBuilder")

    def add_menu_command(self, label, action):
        self.fileCascade.add_command(label=label, command=action)

    def reset_menu(self):
        try :
            self.menu.delete("File")
        except:
            pass
        self.fileCascade = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.fileCascade)


root = Tk()
root.wm_title("PiStand")
app = PiStand(root)
root.mainloop()
root.destroy()
