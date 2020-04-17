from tkinter import *
from PIL import Image, ImageTk
from logique import *
from threading import Timer
from random import randrange as rd
from glob import glob

class Board: # écran de chargement Champollion
    def __init__(self, n, logique): # n = côté du tableau
        self.logic = logique
        self.play = 1
        self.WIDTH = 800
        self.HEIGHT = 600
        self.tailleBandeau = self.WIDTH / 20 # Taille du bandeau de la zone de jeux
        self.Emojis = [] # Liste des emojis
        self.board = [] # Coordinate of cases disovered on the board
        self.flag = []  # Coordinate of the flags placed
        self.qMark = [] # Coordinate of the questions mark placed
        self.state = 0 # 0 = menu, 1 = in-game, 2 = settings, 3 = help, 4 = game over
        self.timer = 0 # Timer
        self.window = Tk()
        self.window.title("Minesweeper")
        self.window.protocol("WM_DELETE_WINDOW", self.quit) # Appeler cette fonction quand la fenêtre est fermer
        self.canvas = Canvas(self.window, width=self.WIDTH, height=self.HEIGHT, background="green")
        self.canvas.pack()
        self.themes = self.__get_theme_list() # Folder names of themes
        self.selectedTheme = self.__startup_theme__()
        self.__update_sizes__()
        self.canvas.bind("<Button-1>", self.__rightclick__)
        self.canvas.bind("<Button-3>", self.__leftclick__)
        self.stopwatch = None # timer Threading
        self.__menu__()


    def __ask_pseudo__(self):
        self.__new_window__()
        self.second.title("Choose your pseudo")
        self.pseudo = StringVar()
        self.pseudo.set("pseudo")
        textZone = Entry(self.second, textvariable=self.pseudo, width=30)
        self.second.bind("<Return>", self.__second_window_destruction__)
        textZone.pack()

    def __new_window__(self):
        self.second = Toplevel(master=self.window)
        self.second.geometry("170x23+500+200")
        self.second.protocol("WM_DELETE_WINDOW", self.__second_window_destruction__)
        self.second.grab_set()

    def __second_window_destruction__(self, *args):
        logic.current_user(self.pseudo.get())
        self.second.destroy()
        self.__menu__()


    def __update_sizes__(self):
        self.bSizeL = self.WIDTH / self.logic.n  # Largeur des boutons
        self.bSizeH = (self.HEIGHT - self.tailleBandeau) / self.logic.n # Hauteur des boutons
        self.__loadImages__()


    def __stopwatch_update__(self):
        self.stopwatch = Timer(1, self.__stopwatch_update__)
        self.stopwatch.start()
        self.timer += 1
        self.canvas.delete("timer")
        self.canvas.create_text(self.WIDTH - self.WIDTH/40, self.tailleBandeau/2, text=str(round(self.timer)), font="Noto 20", tags="timer")

    def __drawBoard__(self):
        self.canvas.delete("all")
        for i in range(self.logic.n):
            for j in range(self.logic.n):
                xCenter, yCenter = self.logic.get_coordinate_from_case(i, j, self.bSizeL, self.bSizeH, self.tailleBandeau)
                self.canvas.create_image(xCenter, yCenter, image=self.Case, anchor=CENTER)
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

        self.canvas.create_rectangle(self.WIDTH - self.WIDTH/15, 2, self.WIDTH, self.HEIGHT/15, fill="pink")
        self.canvas.create_text(self.WIDTH - 70, 50, text=logic.user, font="Noto 15")

    def __rightclick__(self, e):
        if self.state == 0: # Menu
            if self.WIDTH/4 < e.x < self.WIDTH/(800/600): # Click sur la largeur ou il y a les boutons
                if self.HEIGHT/10 < e.y < self.HEIGHT/10*2.5: # Bouton START GAME
                    self.__START_GAME__()
                elif self.HEIGHT/10*3 < e.y < self.HEIGHT/10*4.5: # Bouton SETTINGS
                    self.__SETTINGS__()
                elif self.HEIGHT/10*5 < e.y < self.HEIGHT/10*6.5: # Bouton HELP
                    self.__HELP__()
            elif self.WIDTH - self.WIDTH/15 < e.x < self.WIDTH:
                if 2 < e.y < self.HEIGHT/15:
                    self.__ask_pseudo__()

        elif self.state == 1:
            if e.y < self.tailleBandeau: # Click dans le bandeau
                if self.WIDTH/2 - self.tailleBandeau/2 < e.x < self.WIDTH/2 + self.tailleBandeau/2:
                    self.__emoji__()
            else:  # Click dans la zone de jeu
                self.__affichage_jeux__(e)

        elif self.state == 2: # Settings
            if self.WIDTH/4 < e.x < self.WIDTH/(800/600):
                if self.HEIGHT/10 < e.y < self.HEIGHT/10*2.5:
                    if self.logic.get_difficulty() == 3:
                        self.logic.save_data(difficulty=1)
                    else:
                        self.logic.save_data(difficulty=self.logic.get_difficulty()+1)
                    self.canvas.delete("button")
                    self.canvas.create_text(self.WIDTH/2, (self.HEIGHT/10+self.HEIGHT/10*2.5)/2, text="CHANGE DIFFICULTY : " + str(self.logic.get_difficulty()), font="Noto 15", tags="button")
                    self.__update_sizes__()
                elif self.HEIGHT/10*3 < e.y < self.HEIGHT/10*4.5:
                    self.selectedTheme = (self.selectedTheme + 1)%len(self.themes)
                    self.canvas.delete("theme")
                    self.canvas.create_text(self.WIDTH/2, (self.HEIGHT/10*3+self.HEIGHT/10*4.5)/2, text="CHANGE THEME : " + self.themes[self.selectedTheme], font="Noto 20", tags="theme")
                    self.__loadImages__()
                elif self.HEIGHT/10*5 < e.y < self.HEIGHT/10*6.5:
                    self.__menu__()

        elif self.state == 3: # Help
            if self.WIDTH/4 < e.x < self.WIDTH/(800/600):
                if self.HEIGHT/10*3 < e.y < self.HEIGHT/10*4.5:
                    self.__menu__()

        elif self.state == 4: # GAME OVER
            if self.WIDTH*0.2 < e.x < self.WIDTH*0.8 and self.HEIGHT*0.2 < e.y < self.HEIGHT*0.4:
                self.board = []
                self.flag = []
                self.qMark = []
                self.logic.reset()
                self.logic.audio.stop()
                self.__menu__()
            elif self.WIDTH*0.2 < e.x < self.WIDTH*0.8 and self.HEIGHT*0.55 < e.y < self.HEIGHT*0.75:
                self.board = self.board[0: -(self.logic.nb_bombe - len(self.flag) - len(self.qMark))]
                self.canvas.delete("bombs")
                self.canvas.delete("gameOver")
                self.__stopwatch_update__()
                self.logic.start_audio()
                self.state = 1

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
            xCenter, yCenter = self.logic.get_coordinate_from_case(x, y, self.bSizeL, self.bSizeH, self.tailleBandeau)
            self.canvas.create_image(xCenter, yCenter, image=self.Flag, tags="flag")
        for x, y in self.qMark:
            xCenter, yCenter = self.logic.get_coordinate_from_case(x, y, self.bSizeL, self.bSizeH, self.tailleBandeau)
            self.canvas.create_image(xCenter, yCenter, image=self.QMark, tags="flag")

    def __START_GAME__(self):
        self.state = 1
        self.timer = 0
        self.__stopwatch_update__()
        self.__drawBoard__()

    def __SETTINGS__(self):
        self.state = 2
        self.canvas.delete("all")

        self.canvas.create_rectangle(self.WIDTH/4, self.HEIGHT/10, self.WIDTH/(800/600), self.HEIGHT/10*2.5, fill="pink")
        self.canvas.create_text(self.WIDTH/2, (self.HEIGHT/10+self.HEIGHT/10*2.5)/2, text="CHANGE DIFFICULTY : " + str(self.logic.get_difficulty()), font="Noto 15", tags="button")

        self.canvas.create_rectangle(self.WIDTH/4, self.HEIGHT/10*3, self.WIDTH/(800/600), self.HEIGHT/10*4.5, fill="pink")
        self.canvas.create_text(self.WIDTH/2, (self.HEIGHT/10*3+self.HEIGHT/10*4.5)/2, text="CHANGE THEME : " + self.themes[self.selectedTheme], font="Noto 20", tags="theme")

        self.canvas.create_rectangle(self.WIDTH/4, self.HEIGHT/10*5, self.WIDTH/(800/600), self.HEIGHT/10*6.5, fill="pink")
        self.canvas.create_text(self.WIDTH/2, (self.HEIGHT/10*5+self.HEIGHT/10*6.5)/2, text="GO BACK", font="Noto 20")

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
        self.canvas.create_rectangle(self.WIDTH*0.2, self.HEIGHT*0.2, self.WIDTH*0.8, self.HEIGHT*0.4, fill="pink", tags="gameOver")
        self.canvas.create_text(self.WIDTH/2, self.HEIGHT*0.3, text="Retry", font="Noto 40", tags="gameOver")

        self.canvas.create_rectangle(self.WIDTH*0.2, self.HEIGHT*0.55, self.WIDTH*0.8, self.HEIGHT*0.75, fill="pink", tags="gameOver")
        self.canvas.create_text(self.WIDTH/2, self.HEIGHT*0.65, text="Cancel last move", font="Noto 40", tags="gameOver")


    def __GAME_WON__(self):
        self.__stop_thread__() # Stopper le timer
        self.logic.save_data(score=self.timer)
        self.board = []
        self.flag = []
        self.qMark = []
        # Affichage d'un message "vous avez gagné en XXX.XX secondes avant le retour au menu"
        self.__menu__()


    def __affichage_jeux__(self, e):
        x, y = self.logic.get_case_from_coordinate(e, self.bSizeL, self.bSizeH, self.tailleBandeau) # Case numéro x, y
        resultats = self.logic.choix_user(x, y) # Qu'est-ce que y'avait sur cette case ? (renvoie une liste de tuple (x,y))
        for r, x, y in resultats:
            if (x, y) not in self.board and (x, y) not in self.flag and (x, y) not in self.qMark:
                self.board.append((x, y))
                xCenter, yCenter = self.logic.get_coordinate_from_case(x, y, self.bSizeL, self.bSizeH, self.tailleBandeau)
                if r == 42:
                    self.canvas.create_image(xCenter, yCenter, image=self.Bomb, tags="bombs")
                    self.__GAME_OVER__()
                elif r == 0:
                    self.canvas.create_image(xCenter, yCenter, image=self.Zero)
                elif r == 1:
                    self.canvas.create_image(xCenter, yCenter, image=self.One)
                elif r == 2:
                    self.canvas.create_image(xCenter, yCenter, image=self.Two)
                elif r == 3:
                    self.canvas.create_image(xCenter, yCenter, image=self.Three)
                elif r == 4:
                    self.canvas.create_image(xCenter, yCenter, image=self.Four)
                elif r == 5:
                    self.canvas.create_image(xCenter, yCenter, image=self.Five)
                elif r == 6:
                    self.canvas.create_image(xCenter, yCenter, image=self.Six)
                elif r == 7:
                    self.canvas.create_image(xCenter, yCenter, image=self.Seven)
                elif r == 8:
                    self.canvas.create_image(xCenter, yCenter, image=self.Eight)
                else:
                    self.canvas.create_text(xCenter, yCenter, text=str(r), font="Noto 20")
        if len(self.board) == self.logic.n ** 2 - self.logic.nb_bombe:
            self.__GAME_WON__()

    def __startup_theme__(self):
        if logic.get_current_theme() != None:
            return logic.get_current_theme
        if "darkened" in self.themes:
            return self.themes.index("darkened")
        return 0


    def __get_theme_list(self): # Return folders in assets/themes
        L = []
        for path in glob("assets/themes/*/"):
            if path[13] == "\\": # Windows path
                endOfPath = path[14:].index("\\") + 14
            else: # Unix path
                endOfPath = path[14:].index("/") + 14
            L.append(path[14:endOfPath])
        return L

    def __get_resized_tile__(self, name):
        imgTmp = Image.open("assets/themes/" + self.themes[self.selectedTheme] + "/" + name)
        imgTmp = imgTmp.resize((round(self.bSizeL), round(self.bSizeH)))
        return ImageTk.PhotoImage(imgTmp)

    def __loadImages__(self):
        self.Case = self.__get_resized_tile__("base.png")
        self.Bomb = self.__get_resized_tile__("bomb.png")
        self.Flag = self.__get_resized_tile__("flag.png")
        self.QMark = self.__get_resized_tile__("questionmark.png")
        self.Zero = self.__get_resized_tile__("0.png")
        self.One = self.__get_resized_tile__("1.png")
        self.Two = self.__get_resized_tile__("2.png")
        self.Three = self.__get_resized_tile__("3.png")
        self.Four = self.__get_resized_tile__("4.png")
        self.Five = self.__get_resized_tile__("5.png")
        self.Six = self.__get_resized_tile__("6.png")
        self.Seven = self.__get_resized_tile__("7.png")
        self.Eight = self.__get_resized_tile__("8.png")

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
