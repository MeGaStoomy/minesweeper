from tkinter import *
import random

main = Tk()
main.title("Minesweeper")
main.geometry("423x423")
main.resizable(False,False)
main.configure(background='#4c545c')


class Jeu:
    def __init__(self):
        self.listeCases = [[Case() for _ in range(9)] for _ in range(9)]
        self.preparation()

    def preparation(self):
        text = Label(main, anchor=CENTER, text='Difficultés : ', bg='#4c545c')
        text.pack()

class Case:
    def __init__(self):
        self.mine = False
        self.flag = False
        self.etat = 'closed'

Jeu()
