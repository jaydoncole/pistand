from Tkinter import *

class LoadProgressDialog(object):
    def __init__(self, master, labelText, amountToLoad):
        top = self.top = Toplevel(master)
        self.loadingLabel = Label(top, text=labelText)
        self.loadingLabel.pack()
        progressText = "0 of " + str(amountToLoad)
        print progressText
        self.progressLabel = Label(top, text=progressText)
        self.progressLabel.pack()

    def updateProgress(self, progressNumber):
        self.progressLabel = Label(top, "0 of " + progressNumber)


