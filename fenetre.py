from tkinter import *
from logique import *

class Board:
    def __init__(self, n): # n = côté du tableau
        self.WIDTH = 800
        self.HEIGHT = 600
        self.wh = n   # Nombre de boutons sur la largeur et la hauteur
        self.bSizeL = self.WIDTH / self.wh  # Largeur des boutons
        self.bSizeH = self.HEIGHT / self.wh # Hauteur des boutons
        self.board = []
        self.window = Tk()
        self.canvas = Canvas(self.window, width=self.WIDTH, height=self.HEIGHT, background="gray")
        self.canvas.pack()
        self.__drawBoard__()

    def __drawBoard__(self):
        for i in range(self.wh):
            for j in range(self.wh):
                self.canvas.create_rectangle(i * self.bSizeL,  j * self.bSizeH, i * self.bSizeL + self.bSizeL, j * self.bSizeH + self.bSizeH, fill="pink")

if __name__ == "__main__":
    n = 12
    tableau = Board(n)
    logic = logique(n, tableau)

    tableau.canvas.bind("<Button-1>", logic.choix_user)

    tableau.window.mainloop()
