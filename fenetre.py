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
        self.difficulty = 1 # 1 = easy, 2 = intermediate, 3 = hard
        self.state = 0 # 0 = menu, 1 = in-game, 2 = settings
        self.window = Tk()
        self.canvas = Canvas(self.window, width=self.WIDTH, height=self.HEIGHT, background="green")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.__rightclick__)
        self.__menu__()

    def __drawBoard__(self):
        for i in range(self.wh):
            for j in range(self.wh):
                self.canvas.create_rectangle(i * self.bSizeL,  j * self.bSizeH, i * self.bSizeL + self.bSizeL, j * self.bSizeH + self.bSizeH, fill="gray", outline="black")
    
    def __menu__(self):
        self.state = 0
        self.canvas.delete("all")

        self.canvas.create_rectangle(self.WIDTH/4, self.HEIGHT/10, self.WIDTH/(800/600), self.HEIGHT/10*2.5, fill="pink")
        self.canvas.create_text(self.WIDTH/2, (self.HEIGHT/10+self.HEIGHT/10*2.5)/2, text="START GAME", font="Noto 35")

        self.canvas.create_rectangle(self.WIDTH/4, self.HEIGHT/10*3, self.WIDTH/(800/600), self.HEIGHT/10*4.5, fill="pink")
        self.canvas.create_text(self.WIDTH/2, (self.HEIGHT/10*3 + self.HEIGHT/10*4.5)/2, text="SETTINGS", font="Noto 35")

        self.canvas.create_rectangle(self.WIDTH/4, self.HEIGHT/10*5, self.WIDTH/(800/600), self.HEIGHT/10*6.5, fill="pink")
        self.canvas.create_text(self.WIDTH/2, (self.HEIGHT/10*5 + self.HEIGHT/10*6.5)/2, text="HELP", font="Noto 35")
    
    def __rightclick__(self, e):
        if self.state == 0:
            if self.WIDTH/4 < e.x < self.WIDTH/(800/600): # Click sur la largeur ou il y a les boutons
                if self.HEIGHT/10 < e.y < self.HEIGHT/10*2.5: # Bouton START GAME
                    pass
                elif self.HEIGHT/10*3 < e.y < self.HEIGHT/10*4.5: # Bouton SETTINGS
                    self.__SETTINGS__()
                elif self.HEIGHT/10*5 < e.y < self.HEIGHT/10*6.5: # Bouton HELP
                    pass

        elif self.state == 2:
            if self.WIDTH/4 < e.x < self.WIDTH/(800/600):
                if self.HEIGHT/10 < e.y < self.HEIGHT/10*2.5:
                    if self.difficulty == 3:
                        self.difficulty = 1
                    else:
                        self.difficulty += 1
                    self.canvas.delete("button")
                    self.canvas.create_text(self.WIDTH/2, (self.HEIGHT/10+self.HEIGHT/10*2.5)/2, text="CHANGE DIFFICULTY " + str(self.difficulty), font="Noto 15", tags="button")
                elif self.HEIGHT/10*3 < e.y < self.HEIGHT/10*4.5:
                    self.__menu__()
    
    def __SETTINGS__(self):
        self.state = 2
        self.canvas.delete("all")

        self.canvas.create_rectangle(self.WIDTH/4, self.HEIGHT/10, self.WIDTH/(800/600), self.HEIGHT/10*2.5, fill="pink")
        self.canvas.create_text(self.WIDTH/2, (self.HEIGHT/10+self.HEIGHT/10*2.5)/2, text="CHANGE DIFFICULTY " + str(self.difficulty), font="Noto 15", tags="button")

        self.canvas.create_rectangle(self.WIDTH/4, self.HEIGHT/10*3, self.WIDTH/(800/600), self.HEIGHT/10*4.5, fill="pink")
        self.canvas.create_text(self.WIDTH/2, (self.HEIGHT/10*3+self.HEIGHT/10*4.5)/2, text="QUIT", font="Noto 20")










if __name__ == "__main__":
    n = 12
    tableau = Board(n)
    logic = logique(n, tableau)

    #tableau.canvas.bind("<Button-1>", logic.choix_user)

    tableau.window.mainloop()
