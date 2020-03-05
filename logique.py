"""
@author: BOTTI Joakim
"""

from random import sample, randrange
from os import system
import sys
from time import sleep

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

    def __init__(self, n):
        self.n = n
        self.state = self.random_platform(self.n, self.nb_bombe)
        self.affiche()

    def affiche(self):
        print('\n'.join(' '.join(map(str, L)) for L in self.state))
        print()

    def voisins(self, n, i, j):
        return [(a,b) for (a, b) in [(i, j+1),(i, j-1),(i-1, j),(i+1,j),(i+1,j+1),(i-1,j-1),(i-1,j+1),(i+1,j-1)] if a in range(n) and b in range(n)]

    def voisins_vertical_horisontal(self, n, i, j):
            return [(a,b) for (a, b) in [(i, j+1),(i, j-1),(i-1, j),(i+1,j)] if a in range(n) and b in range(n)]

    def random_platform(self, n, nb_bombe):
        units=[(line,col) for col in range(n) for line in range(n)]
        bombe=sample(units, nb_bombe)
        state=[[0x0]*n for _ in range(n)]
        for (i,j) in bombe:
            state[i][j]=0x2a
            voisin = self.voisins(n, i, j)
            for x, y in voisin:
                if state[x][y] != 0x2a: state[x][y] += 1
        return state

    def detect_zero(self, x, y):
        result=[]
        voisin = self.voisins_vertical_horisontal(self.n, x, y)
        for i in voisin:
            if self.state[i[0]][i[1]] == 0 and i not in self.locate_0:
                self.locate_0.append((i[0], i[1]))
                result.append((i[0],i[1]))
        return result

    def choix_user(self, x, y):
        result = []
        if (x, y) not in self.locate_0:
            self.locate_0.append((x, y))

            callback = self.detect_zero(x, y)
            for i in callback: result.append((self.state[i[0]][i[1]], i[0], i[1]))
            for z in result:
                callback = self.detect_zero(z[1], z[2])
                for i in callback: result.append((self.state[i[0]][i[1]], i[0], i[1]))

            result.append((self.state[x][y], x, y))
        return result

    def get_case_from_coordinate(self, e, block_width, block_height, taille_bandeau):
        for i in range(self.n):
            if block_width * i < e.x < block_width * (i+1):
                x = i
                break
        for i in range(self.n):
            if taille_bandeau + block_height * i < e.y < taille_bandeau + block_height * (i+1):
                y = i
                break
        return (x, y)

    def get_coordinate_from_case(self, x, y, block_width, block_height):
        xCenter = block_width * x + block_width / 2
        yCenter = block_height * (y+1) + block_height / 2
        return [xCenter, yCenter]



if __name__ == "__main__":
    logic = logique(0xc)
    logic.affiche()
