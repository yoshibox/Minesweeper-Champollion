from pygame import mixer


class audio:

    def __init__(self, default):
        mixer.init()
        mixer.music.load(default)

    def stop(self):
        mixer.music.stop()

    def play(self):
        mixer.music.play()

    def game_over(self):
        mixer.music.load("assets/lost.mp3")
        mixer.music.play()

    def win(self):
        mixer.music.load("assets/win.mp3")
        mixer.music.play()
