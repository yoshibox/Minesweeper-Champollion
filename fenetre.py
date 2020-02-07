from tkinter import *

class Board: 
    def __init__(self, n): # n = côté du tableau
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.buttonSizeL = self.WIDTH / n  # Largeur des boutons
        self.buttonSizeH = self.HEIGHT / n # Hauteur des boutons
        Tk()




if __name__ == "__main__":
    Board(42)