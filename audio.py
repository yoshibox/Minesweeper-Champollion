pygameInstalled = True

try:
    from pygame import mixer
except ModuleNotFoundError:
    print("Il semble que pygame n'est pas installé, vous pouvez l'installer avec \"pip install --user pygame\"\n\
Vous pouvez continuer à jouer, mais vous n'aurez pas de son")
    pygameInstalled = False

class audio:

    def __init__(self, default):
        if not pygameInstalled: return
        mixer.init()
        mixer.music.load(default)

    def stop(self):
        if not pygameInstalled: return
        mixer.music.stop()

    def play(self):
        if not pygameInstalled: return
        mixer.music.play()

    def game_over(self):
        if not pygameInstalled: return
        mixer.music.load("assets/lost.mp3")
        mixer.music.play()

    def win(self):
        if not pygameInstalled: return
        mixer.music.load("assets/win.mp3")
        mixer.music.play()
