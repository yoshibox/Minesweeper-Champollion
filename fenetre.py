from tkinter import *
from logique import *

class Board:
    def __init__(self, n, logique): # n = côté du tableau
        self.logic = logique
        self.play = 1
        self.WIDTH = 800
        self.HEIGHT = 600
        self.wh = n   # Nombre de boutons sur la largeur et la hauteur
        self.tailleBandeau = self.WIDTH / 20 # Taille du bandeau de la zone de jeux
        self.bSizeL = self.WIDTH / self.wh  # Largeur des boutons
        self.bSizeH = (self.HEIGHT - self.tailleBandeau) / self.wh # Hauteur des boutons
        self.board = []
        self.difficulty = 1 # 1 = easy, 2 = intermediate, 3 = hard
        self.state = 0 # 0 = menu, 1 = in-game, 2 = settings, 3 = help
        self.window = Tk()
        self.canvas = Canvas(self.window, width=self.WIDTH, height=self.HEIGHT, background="green")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.__rightclick__)
        self.__menu__()

    def __drawBoard__(self):
        self.canvas.delete("all")
        for i in range(self.wh):
            for j in range(self.wh):
                self.canvas.create_rectangle(i * self.bSizeL, self.tailleBandeau + j * self.bSizeH, i * self.bSizeL + self.bSizeL, self.tailleBandeau + j * self.bSizeH + self.bSizeH, fill="gray", outline="black")
        self.canvas.create_rectangle(0, 0, self.WIDTH, self.tailleBandeau, fill="blue") # Bandeau

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
        if self.state == 0: # Menu
            if self.WIDTH/4 < e.x < self.WIDTH/(800/600): # Click sur la largeur ou il y a les boutons
                if self.HEIGHT/10 < e.y < self.HEIGHT/10*2.5: # Bouton START GAME
                    self.__START_GAME__()
                elif self.HEIGHT/10*3 < e.y < self.HEIGHT/10*4.5: # Bouton SETTINGS
                    self.__SETTINGS__()
                elif self.HEIGHT/10*5 < e.y < self.HEIGHT/10*6.5: # Bouton HELP
                    self.__HELP__()

        elif self.state == 1:
            if e.y < self.tailleBandeau: # Click dans le bandeau
                pass
            else:  # Click dans la zone de jeu
                self.__affichage_jeux__(e)

        elif self.state == 2: # Settings
            if self.WIDTH/4 < e.x < self.WIDTH/(800/600):
                if self.HEIGHT/10 < e.y < self.HEIGHT/10*2.5:
                    if self.difficulty == 3:
                        self.difficulty = 1
                    else:
                        self.difficulty += 1
                    self.canvas.delete("button")
                    self.canvas.create_text(self.WIDTH/2, (self.HEIGHT/10+self.HEIGHT/10*2.5)/2, text="CHANGE DIFFICULTY : " + str(self.difficulty), font="Noto 15", tags="button")
                elif self.HEIGHT/10*3 < e.y < self.HEIGHT/10*4.5:
                    self.__menu__()

        elif self.state == 3: # Help
            if self.WIDTH/4 < e.x < self.WIDTH/(800/600):
                if self.HEIGHT/10*3 < e.y < self.HEIGHT/10*4.5:
                    self.__menu__()

    def __START_GAME__(self):
        self.state = 1
        self.__drawBoard__()

    def __SETTINGS__(self):
        self.state = 2
        self.canvas.delete("all")

        self.canvas.create_rectangle(self.WIDTH/4, self.HEIGHT/10, self.WIDTH/(800/600), self.HEIGHT/10*2.5, fill="pink")
        self.canvas.create_text(self.WIDTH/2, (self.HEIGHT/10+self.HEIGHT/10*2.5)/2, text="CHANGE DIFFICULTY : " + str(self.difficulty), font="Noto 15", tags="button")

        self.canvas.create_rectangle(self.WIDTH/4, self.HEIGHT/10*3, self.WIDTH/(800/600), self.HEIGHT/10*4.5, fill="pink")
        self.canvas.create_text(self.WIDTH/2, (self.HEIGHT/10*3+self.HEIGHT/10*4.5)/2, text="GO BACK", font="Noto 20")

    def __HELP__(self):
        self.state = 3
        self.canvas.delete("all")

        self.canvas.create_rectangle(self.WIDTH/4, self.HEIGHT/10, self.WIDTH/(800/600), self.HEIGHT/10*2.5, fill="pink")
        self.canvas.create_text(self.WIDTH/2, (self.HEIGHT/10+self.HEIGHT/10*2.5)/2, text="METTRE LES REGLES ICI !!!!!!!!", font="Noto 15")

        self.canvas.create_rectangle(self.WIDTH/4, self.HEIGHT/10*3, self.WIDTH/(800/600), self.HEIGHT/10*4.5, fill="pink")
        self.canvas.create_text(self.WIDTH/2, (self.HEIGHT/10*3+self.HEIGHT/10*4.5)/2, text="GO BACK", font="Noto 20")
    
    def __affichage_jeux__(self, e):
        x, y = logic.get_case_from_coordinate(e, self.bSizeL, self.bSizeH, self.tailleBandeau) # Case numéro x, y
        resultats = logic.choix_user(x, y) # Qu'est-ce que y'avait sur cette case ? (renvoie une liste de tuple (x,y))
        for r in resultats:
            if r not in self.board:
                xCenter, yCenter = logic.get_coordinate_from_case(x, y, self.bSizeL, self.bSizeH)
                self.canvas.create_text(xCenter, yCenter, text=str(r), font="Noto 20") 
                # CREER UNE FONCTION POUR GERER L'AFFICHAGE DES NOMBRES/DRAPEAUX
    
    def start(self):
        self.window.mainloop()



    def quit(self):
        self.window.quit()







if __name__ == "__main__":
    n = 12
    logic = logique(n)
    tableau = Board(n, logic)
    tableau.start()
