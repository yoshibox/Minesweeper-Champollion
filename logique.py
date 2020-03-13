"""
@author: BOTTI Joakim
"""

from random import sample, randrange
from os import system
import sys
from time import sleep
import json

"""
dans la matrice:
    bombe: representer par le nombre 42
    autre: nombre de bombe a proximiter
information du plateau:
    width: 800px
    height: 600px
"""


class logique:
    nb_bombe = 24
    show_case = []
    locate_0 = []
    locate_0x2a = []
    data=None
    user="nom_random"
    state=None

    def __init__(self, n):
        self.n = n

        try:
            with open("assets/data.json") as new_json:
                self.data = json.load(new_json)
        except:
            self.data = {
                "nom_random": {
                    "musique": "dc_rock_bust.mp3",
                    "current_difficulty": 1,
                    "1": [],
                    "2": [],
                    "3": []
                }
            }
            json.dumps(self.data)
            with open("assets/data.json","w") as new_json: new_json.write(json.dumps(self.data))

    def affiche(self):
        print('\n'.join(' '.join(map(str, L)) for L in self.state))
        print()

    def voisins(self, n, i, j):
        return [(a,b) for (a, b) in [(i, j+1),(i, j-1),(i-1, j),(i+1,j),(i+1,j+1),(i-1,j-1),(i-1,j+1),(i+1,j-1)] if a in range(n) and b in range(n)]

    def random_platform(self, n, nb_bombe):
        #a faire: si l'user click sur une bombe on refais la platfome
        units=[(line,col) for col in range(n) for line in range(n)]
        bombe=sample(units, nb_bombe)
        state=[[0x0]*n for _ in range(n)]
        for (i,z) in bombe:
            state[i][z]=0x2a
            self.locate_0x2a.append((0x2a, i, z))
            voisin = self.voisins(n, i, z)
            for x, y in voisin:
                if state[x][y] != 0x2a: state[x][y] += 1
        return state

    def detect_zero(self, x, y):
        result=[]
        autre=[]
        voisin = self.voisins(self.n, x, y)
        for i in voisin:
            if self.state[i[0]][i[1]] == 0 and i not in self.locate_0:
                self.locate_0.append(i)
                result.append(i)
            elif i not in self.locate_0: autre.append(i)
        return [result, autre]

    def choix_user(self, x, y):
        result = []
        autres = []

        if not self.state:
            while True:
                self.state = self.random_platform(self.n, self.nb_bombe)
                if self.state[x][y] != 0x2a: break

        if self.state[x][y] == 0x2a:
            return self.locate_0x2a
        elif (x, y) not in self.locate_0 and self.state[x][y] == 0:
            self.locate_0.append((x, y))

            callback, autre = self.detect_zero(x, y)
            for i in callback: result.append((self.state[i[0]][i[1]], i[0], i[1]))
            for i in autre: autres.append((self.state[i[0]][i[1]], i[0], i[1]))
            for z in result:
                callback, autre = self.detect_zero(z[1], z[2])
                for i in autre: autres.append((self.state[i[0]][i[1]], i[0], i[1]))
                for i in callback: result.append((self.state[i[0]][i[1]], i[0], i[1]))

            result.append((self.state[x][y], x, y))
        else: result.append((self.state[x][y], x, y))
        result.extend(autres)

        return result

    def get_case_from_coordinate(self, e, block_width, block_height, taille_bandeau):
        for i in range(self.n):
            if block_width * i < e.x < block_width * (i+1): x = i
            if taille_bandeau + block_height * i < e.y < taille_bandeau + block_height * (i+1): y = i
        return (x, y)

    def get_coordinate_from_case(self, x, y, block_width, block_height):
        xCenter = block_width * x + block_width / 2
        yCenter = block_height * (y+1) + block_height / 2
        return [xCenter, yCenter]

    def get_difficulty(self):
        return self.data[self.user]["current_difficulty"]

    def reset():
        locate_0 = []
        locate_0x2a = []

    def current_user(self, str):
        """
            str: str
        """
        self.user = str
        if self.user not in self.data.keys():
            print("un truc")
            self.data[str] = {
                "musique": "dc_rock_bust.mp3",
                "current_difficulty": 1,
                "1": [],
                "2": [],
                "3": []
            }
            self.save_data()


    def get_leader_board(self):
        return sorted(self.data[self.user][ str(self.data[self.user]["current_difficulty"]) ])

    def save_data(self, score=None, difficulty=None, music=None):
        """
        input:
            score: [float, str]
            difficulty: int
            music: str
        """

        with open("assets/data.json","w") as data_json:
            if difficulty: self.data[self.user]["current_difficulty"] = difficulty
            if music: self.data[self.user]["musique"] = music
            if score:
                self.data[self.user][ str(self.data[self.user]["current_difficulty"]) ].append([score[0], score[1]])
            data_json.write(json.dumps(self.data))




if __name__ == "__main__":
    logic = logique(0xc)
    logic.affiche()
    logic.current_user("nocturio")
    logic.save_data(score=[12, "escrime"], difficulty=2)
    print(logic.get_difficulty(),"\n", logic.get_leader_board())
