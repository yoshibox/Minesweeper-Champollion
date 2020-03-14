from pygame import mixer


class audio:

    def __init__(self, default):
        mixer.init()
        mixer.music.load(default)

    def stop(self):
        mixer.music.stop()

    def play(self):
        mixer.music.play()
