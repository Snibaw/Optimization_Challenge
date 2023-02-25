from calendar import c
import random as rd
from typing import List
from handle_files import *


def main():
    data = readFile("./instances/cs1.txt")
    Meilleur_Instertion(data.vehicles, data.options)
    return


def PlusGrandRatio(k, Options):
    x = 0
    for i in range(len(Options)):
        if(k.options[i] and Options[i].ratio_p > x):
            x = Options[i].ratio_p
    return x


def Meilleur_Instertion(Liste, Options):
    New_Liste = [-1]*len(Liste)
    ListeAjoute = [0]*len(Liste)
    for i in range(len(Liste)):
        bestVeh = -1
        bestVal = 100000
        for k in range(len(Liste)):
            if(ListeAjoute[k] == 0):
                TempoListe = New_Liste
                TempoListe[i] = Liste[k]
                val = CalculCout(TempoListe, Options, i-97, i+1)
                if(val < bestVal):
                    bestVeh = Liste[k]
                    bestVal = val
        New_Liste[i] = bestVeh
        ListeAjoute[bestVeh.index] = 1
    print(CalculCout(New_Liste, Options, 0, len(New_Liste)))
    exportFile(12, New_Liste)
    return


def random(Liste, Options):
    min = 100000000
    MinListe = []
    for i in range(10000):
        rd.shuffle(Liste)
        val = CalculCout(Liste, Options)
        if(val < min):
            min = val
            MinListe = Liste
    print(val)
    return


def CalculCout(Liste, Option, debut, fin):
    somme = 0
    for i in range(len(Option)):
        for j in range(debut, fin):
            valeur = 0
            for k in range(j, j+Option[i].ratio_p):
                if(k >= fin or Liste[k] == -1):
                    delta = 0
                else:
                    delta = int(Liste[k].options[i])
                valeur += delta
            valeur = valeur - Option[i].ratio_n
            somme += Option[i].weight*max(0, valeur)
    return somme

if __name__ == '__main__':
    main()