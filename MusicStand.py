import Tkinter as tk
import os
from Song import Song
from PIL import Image, ImageTk
import importlib
from LoadProgressDialog import LoadProgressDialog
from ttk import Progressbar
import threading


class MusicStand(tk.Frame):
    pagefiles = []
    pagepointer = 0

    def __init__(self, parent, controller):
        self.controller = controller
        self.parent = parent
        tk.Frame.__init__(self, parent)

        #Frame to hold the music pages
        self.musicframe = tk.Frame(self)

        self.bind("<Right>", self.nextpage)
        self.bind("<Left>", self.prevpage)

        self.leftPage = tk.Label(self.musicframe)
        self.rightPage = tk.Label(self.musicframe)

        self.leftPage.pack(side = tk.LEFT)
        self.rightPage.pack(side = tk.LEFT)

        self.musicframe.pack(side = tk.TOP)

        # Hardcoding Rapberry Pi inputs... should probably pull this out somewhere
        try: 
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            GPIO.add_event_detect(14, GPIO.RISING, callback=self.nextpage, bouncetime=300)
            GPIO.add_event_detect(18, GPIO.RISING, callback=self.prevpage, bouncetime=300)
        except ImportError:
            pass

    def setup_menu(self):
        self.controller.add_menu_command("Build Playlist", lambda:self.controller.show_frame("PlaylistBuilder"))
        self.controller.add_menu_command("Exit", self.quit)


    def loadplaylist(self):
        progress_dialog = tk.Toplevel()
        progress_dialog.title("Loading Playlist")
        bar = Progressbar(progress_dialog, orient="horizontal", length=500, value=0, mode="determinate")
        bar.grid(row=4, columnspan=2)
        thread = threading.Thread(target=self.threadedPlaylistLoad, args=(bar, progress_dialog))
        thread.start()

    def threadedPlaylistLoad(self, progressBar, progressDialogBox):
        filelist = self.getListOfFilesToLoad()
        progressBar['maximum'] = len(filelist)
        progressBar['value'] = 0
        self.pagepointer = 0
        for filename in filelist:
            progressBar['value'] += 1
            print "Loading file: " + filename
            self.pagefiles.append(self.loadimage(filename))
            self.updatepage()
        progressDialogBox.destroy()


    def getListOfFilesToLoad(self):
        filelist = []
        for song in self.controller.Playlist:
            songdir = self.controller.musicFolder + "/" + song.artist + "/" + song.album + "/" + song.title
            files = os.listdir(songdir)
            files.sort()
            for filename in files:
                filelist.append(songdir + "/" + filename)
        return filelist



    def updatepage(self):
        leftimage = self.pagefiles[self.pagepointer]
        if self.pagepointer + 1 <= len(self.pagefiles) - 1:
            rightimage = self.pagefiles[self.pagepointer + 1]
        else:
            rightimage = self.loadimage(self.controller.dirname + "/Invisible.png")
        self.leftPage.configure(image = leftimage)
        self.leftPage.image = leftimage
        self.rightPage.configure(image = rightimage)
        self.rightPage.image = rightimage


    def loadimage(self, imagefile):
        screenHeight = self.winfo_height() - 20
        image = Image.open(imagefile)
        xsize, ysize = image.size
        if ysize != screenHeight:
            imageRatio = xsize / float(ysize)
            image = image.resize((int(imageRatio * screenHeight), screenHeight), Image.ANTIALIAS)
        photoImage = ImageTk.PhotoImage(image)
        return photoImage


    def prevpage(self, e):
        if self.pagepointer - 2 >= 0:
            self.pagepointer -= 2
            self.updatepage()


    def nextpage(self, e):
        if self.pagepointer + 2 <= len(self.pagefiles) - 1:
            self.pagepointer += 2
            self.updatepage()

