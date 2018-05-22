class Song:
    files = []

    def __init__(self, album, artist, song):
        self.title = song
        self.album = album
        self.artist = artist
        self.files = []

    def __str__(self):
        return self.title + ' | ' + self.artist + ' | ' + self.album

    def add_file(self, filename):
        self.files.append(filename)
