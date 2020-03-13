from tkinter import *
from PIL import Image, ImageTk
from logique import *
from threading import Timer
from random import randrange as rd

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
        self.Emojis = [] # Liste des emojis
        self.board = [] # Coordinate of cases disovered on the board
        self.flag = []  # Coordinate of the flags placed
        self.qMark = [] # Coordinate of the questions mark placed
        self.difficulty = 1 # 1 = easy, 2 = intermediate, 3 = hard
        self.state = 0 # 0 = menu, 1 = in-game, 2 = settings, 3 = help, 4 = game over
        self.timer = 0 # Timer
        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.quit) # Appeler cette fonction quand la fenêtre est fermer
        self.canvas = Canvas(self.window, width=self.WIDTH, height=self.HEIGHT, background="green")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.__rightclick__)
        self.canvas.bind("<Button-3>", self.__leftclick__)
        self.stopwatch = None # timer Threading 
        self.__loadImages__()
        self.__menu__()
    

    def __stopwatch_update__(self):
        self.stopwatch = Timer(1, self.__stopwatch_update__)
        self.stopwatch.start()
        self.timer += 1
        self.canvas.delete("timer")
        self.canvas.create_text(self.WIDTH - self.WIDTH/40, self.tailleBandeau/2, text=str(round(self.timer)), font="Noto 20", tags="timer")

    def __drawBoard__(self):
        self.canvas.delete("all")
        for i in range(self.wh):
            for j in range(self.wh):
                xCenter, yCenter = self.logic.get_coordinate_from_case(i, j, self.bSizeL, self.bSizeH)
                self.canvas.create_image(xCenter, yCenter - 6, image=self.Case)
                #self.canvas.create_rectangle(i * self.bSizeL, self.tailleBandeau + j * self.bSizeH, i * self.bSizeL + self.bSizeL, self.tailleBandeau + j * self.bSizeH + self.bSizeH, fill="gray", outline="black")
        self.canvas.create_rectangle(0, 0, self.WIDTH, self.tailleBandeau, fill="blue") # Bandeau
        self.__mine_counter_update__()
        self.__emoji__()

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
                if self.WIDTH/2 - self.tailleBandeau/2 < e.x < self.WIDTH/2 + self.tailleBandeau/2:
                    self.__emoji__()
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
        
        elif self.state == 4:
            if self.WIDTH*0.2 < e.x < self.WIDTH*0.8 and self.HEIGHT*0.4 < e.y < self.HEIGHT*0.6:
                self.board = []
                self.flag = []
                self.qMark = []
                self.logic.reset()
                self.__menu__()

    def __leftclick__(self, e):
        if self.state == 1:
            x, y = self.logic.get_case_from_coordinate(e, self.bSizeL, self.bSizeH, self.tailleBandeau)
            if (x, y) not in self.board: # Si les points ne sont pas découvert, on peut y placer un drapeau
                if (x, y) not in self.flag: # Si il n'y a pas de drapeau
                    if (x, y) not in self.qMark: # Si il n'y a pas de point d'interrogation
                        self.flag.append((x, y))
                    else:
                        self.qMark.remove((x, y))
                elif (x, y) in self.flag: # Si il y a déjà un drapeau
                    self.flag.remove((x, y)) # Gérer le cas ou le ValueError est lever (même si ça ne doit jamais arriver)
                    self.qMark.append((x, y))
            self.__drawFlag()
            self.__mine_counter_update__()

    def __drawFlag(self):
        self.canvas.delete("flag") # flag sont les drapeau et les points d'interrogation
        for x, y in self.flag:
            xCenter, yCenter = self.logic.get_coordinate_from_case(x, y, self.bSizeL, self.bSizeH)
            self.canvas.create_image(xCenter, yCenter - 6, image=self.Flag, tags="flag")
        for x, y in self.qMark:
            xCenter, yCenter = self.logic.get_coordinate_from_case(x, y, self.bSizeL, self.bSizeH)
            self.canvas.create_image(xCenter, yCenter - 6, image=self.QMark, tags="flag")

    def __START_GAME__(self):
        self.state = 1
        self.timer = 0
        self.__stopwatch_update__()
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
    
    def __GAME_OVER__(self):
        self.state = 4
        self.__stop_thread__()
        self.canvas.create_rectangle(self.WIDTH*0.2, self.HEIGHT*0.4, self.WIDTH*0.8, self.HEIGHT*0.6, fill="pink")
        self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2, text="Retry", font="Noto 40")
    

    def __GAME_WON__(self):
        pass

    
    def __affichage_jeux__(self, e):
        x, y = self.logic.get_case_from_coordinate(e, self.bSizeL, self.bSizeH, self.tailleBandeau) # Case numéro x, y
        resultats = self.logic.choix_user(x, y) # Qu'est-ce que y'avait sur cette case ? (renvoie une liste de tuple (x,y))
        for r, x, y in resultats:
            if (x, y) not in self.board and (x, y) not in self.flag and (x, y) not in self.qMark:
                self.board.append((x, y))
                xCenter, yCenter = self.logic.get_coordinate_from_case(x, y, self.bSizeL, self.bSizeH)
                if r == 42:
                    self.canvas.create_image(xCenter, yCenter - 6, image=self.Bomb) # pk -6 ??????????????
                    self.__GAME_OVER__()
                elif r == 0:
                    self.canvas.create_image(xCenter, yCenter - 6, image=self.Zero)
                elif r == 1:
                    self.canvas.create_image(xCenter, yCenter - 6, image=self.One)
                elif r == 2:
                    self.canvas.create_image(xCenter, yCenter - 6, image=self.Two)
                elif r == 3:
                    self.canvas.create_image(xCenter, yCenter - 6, image=self.Three)
                elif r == 4:
                    self.canvas.create_image(xCenter, yCenter - 6, image=self.Four)
                elif r == 5:
                    self.canvas.create_image(xCenter, yCenter - 6, image=self.Five)
                elif r == 6:
                    self.canvas.create_image(xCenter, yCenter - 6, image=self.Six)
                elif r == 7:
                    self.canvas.create_image(xCenter, yCenter - 6, image=self.Seven)
                elif r == 8:
                    self.canvas.create_image(xCenter, yCenter - 6, image=self.Eight)
                else:
                    self.canvas.create_text(xCenter, yCenter, text=str(r), font="Noto 20")
        if len(self.board) == self.wh ** 2 - self.logic.nb_bombe:
            self.__GAME_WON__()

    def __get_resized_tile__(self, name):
        imgTmp = Image.open("assets/" + name)
        imgTmp = imgTmp.resize((round(self.bSizeL), round(self.bSizeH)))
        return ImageTk.PhotoImage(imgTmp)

    def __loadImages__(self):
        self.Case = self.__get_resized_tile__("minesweeper_00.png")
        self.Bomb = self.__get_resized_tile__("minesweeper_05.png")
        self.Flag = self.__get_resized_tile__("minesweeper_02.png")
        self.QMark = self.__get_resized_tile__("minesweeper_03.png")
        self.Zero = self.__get_resized_tile__("minesweeper_01.png")
        self.One = self.__get_resized_tile__("minesweeper_08.png")
        self.Two = self.__get_resized_tile__("minesweeper_09.png")
        self.Three = self.__get_resized_tile__("minesweeper_10.png")
        self.Four = self.__get_resized_tile__("minesweeper_11.png")
        self.Five = self.__get_resized_tile__("minesweeper_12.png")
        self.Six = self.__get_resized_tile__("minesweeper_13.png")
        self.Seven = self.__get_resized_tile__("minesweeper_14.png")
        self.Eight = self.__get_resized_tile__("minesweeper_15.png")

        imgTmp = Image.open("assets/emojis/emoji_smiling.png")
        imgTmp = imgTmp.resize(((round(self.tailleBandeau)), round(self.tailleBandeau)))
        self.Emojis.append(ImageTk.PhotoImage(imgTmp))
        imgTmp = Image.open("assets/emojis/emoji_tear_of_joy.png")
        imgTmp = imgTmp.resize(((round(self.tailleBandeau)), round(self.tailleBandeau)))
        self.Emojis.append(ImageTk.PhotoImage(imgTmp))




    def __emoji__(self):
        self.canvas.delete("emoji")
        self.canvas.create_image(self.WIDTH/2, self.tailleBandeau/2, image=self.Emojis[rd(0, len(self.Emojis))], tags="emoji")
    

    def __mine_counter_update__(self):
        self.canvas.delete("counter")
        self.canvas.create_text(self.WIDTH/40, self.tailleBandeau/2, text=str(self.logic.nb_bombe - (len(self.flag) + len(self.qMark))), font="Noto 20", tags="counter")


    
    def start(self):
        self.window.mainloop()
    

    def __stop_thread__(self):
        if self.stopwatch != None:
            self.stopwatch.cancel()
    
    def quit(self):
        self.__stop_thread__()
        self.window.quit()







if __name__ == "__main__":
    n = 12
    logic = logique(n)
    tableau = Board(n, logic)
    tableau.start()
