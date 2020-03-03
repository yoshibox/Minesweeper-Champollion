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

    def __init__(self, n):
        self.n = n
        self.state = self.random_platform(self.n, self.nb_bombe)

    def affiche(self):
        print('\n'.join(' '.join(map(str, L)) for L in self.state))

    def voisins(self, n, i, j):
        return [(a,b) for (a, b) in [(i, j+1),(i, j-1),(i-1, j),(i+1,j),(i+1,j+1),(i-1,j-1),(i-1,j+1),(i+1,j-1)] if a in range(n) and b in range(n)]

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

    def choix_user(self, x, y):
        return self.state[x - 1][y - 1]

    def get_case_from_coordinate(self, e, block_width, block_height, taille_bandeau): # Avoir l'emplacement de la case grâce à ses coordonnées
        for i in range(self.n):
            if block_width * i < e.x < block_width * (i+1):
                x = i + 1
                break
        for i in range(self.n):
            if taille_bandeau + block_height * i < e.y < taille_bandeau + block_height * (i+1):
                y = i + 1
                break
        return (x, y)

    def get_coordinate_from_case(self, x, y, block_width, block_height):
        xCenter = block_width * (x - 1) + block_width / 2
        yCenter = block_height * y + block_height / 2
        return [xCenter, yCenter]



if __name__ == "__main__":
    logic = logique(0xc)
    logic.affiche()
