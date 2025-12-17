from tkinter import *
from PIL import Image, ImageTk
import random, os, atexit

####################

main = Tk()
main.title("Minesweeper")
main.geometry("442x442")
main.resizable(False,False)
main.configure(background='#4c545c')

global mouseDown

def load_textures(folder):
        dictTextures = {}
        for filename in os.listdir(folder):
            if filename.endswith(".png"):
                name = os.path.splitext(filename)[0]
                path = os.path.join(folder, filename)
                img = Image.open(path)
                if name in ['face_lose', 'face_pressed', 'face_unpressed']:
                    dictTextures[name + "_small"] = ImageTk.PhotoImage(img.resize( (45, 45), Image.Resampling.LANCZOS ), master=main)
                    img = Image.open(path).resize( (70, 70), Image.Resampling.LANCZOS)
                elif img.size == (94,94):
                    img = img.resize( (38, 38), Image.Resampling.LANCZOS )
                elif img.size == (541, 336):
                    img = img.resize( (146, 91), Image.Resampling.LANCZOS )
                else:
                    img = img.resize( (40, 76), Image.Resampling.LANCZOS )
                dictTextures[name] = ImageTk.PhotoImage(img, master=main)
        return dictTextures
textures = load_textures('images')

current_widget = None
def gameCellPress(event):
    if not(event.widget.cell.revealed) and not(event.widget.cell.flagged) and not(event.widget.cell.jeu.gameIsOver):
        global current_widget
        event.widget.config(image=textures['type0'])
        current_widget = event.widget
def gameCellRelease(event):
    if not(event.widget.cell.revealed) and not(event.widget.cell.flagged) and not(event.widget.cell.jeu.gameIsOver):
        global current_widget
        if (current_widget) and not(current_widget.cell.flagged) and (event.type == '35'):
            current_widget.config(image=textures['closed'])
        current_widget = event.widget.winfo_containing(event.x_root, event.y_root)
        if (event.type == '5') and not(current_widget.cell.flagged):
            current_widget.cell.openArea()
        else:
            event.widget.config(image=textures['closed'])
def gameCellMotion(event):
    if not(event.widget.cell.revealed) and not(event.widget.cell.flagged) and not(event.widget.cell.jeu.gameIsOver):
        global current_widget
        # current_widget = widget under the mouse previously
        widget = event.widget.winfo_containing(event.x_root, event.y_root)
        # widget = widget under the mouse currently
        if (widget) and (widget.cell.cellType == 'gameCell') and (current_widget != widget):
            if current_widget:
                current_widget.event_generate("<<Leave>>")
            current_widget = widget
            # current_widget is updated
            current_widget.event_generate("<<Enter>>")
def gameCellFlag(event):
    if not(event.widget.cell.revealed) and not(event.widget.cell.jeu.gameIsOver):
        if event.widget.cell.flagged:
            event.widget.cell.flagged = False
            event.widget.cell.jeu.mineCount += 1
            event.widget.config(image=textures['closed'])
        else:
            event.widget.cell.flagged = True
            event.widget.cell.jeu.mineCount -= 1
            event.widget.config(image=textures['flag'])
        event.widget.cell.jeu.showMineCount()
def smileyFacePress(event):
    event.widget.config(image=textures['face_pressed_small' if event.widget.cell.jeu.difficulty == 'easy' else 'face_pressed'])
def smileyFaceRelease(event):
    event.widget.config(image=textures['face_unpressed_small' if event.widget.cell.jeu.difficulty == 'easy' else 'face_unpressed'])
    event.widget.cell.jeu.resetWindow()
    Jeu()
    



class Jeu:
    def __init__(self):
        self.askDifficulty()
        self.createBorderCells()
        self.createTopBarCells()
        self.createGameCells()
        self.placeMines()
        self.showMineCount()
        self.timer(-1)

    def askDifficulty(self):
        self.difficulty = None
        self.createBorderCells()
        while not(self.difficulty):
            self.difficulty = input('Which difficulty ? (easy, normal, hard) : ')
            if (self.difficulty != 'easy') and (self.difficulty != 'normal') and (self.difficulty != 'hard'):
                self.difficulty = None
                print('!Invalid answer!')
        self.resetWindow()
        self.gameIsOver = False
                
    def createBorderCells(self):
        textures
        if (self.difficulty == 'easy') or (self.difficulty == None):
            main.title('Minesweeper - Easy Difficulty')
            self.width = 9+2
            self.height = 9+6
        elif self.difficulty == 'normal':
            main.title('Minesweeper - Normal Difficulty')
            self.width = 16+2
            self.height = 11+6
        else:
            main.title('Minesweeper - Hard Difficulty')
            self.width = 30+2
            self.height = 11+6
        main.geometry(f'{38*self.width}x{38*self.height}')
        self.placeWindow()
        self.listeBorderCells = [[Cell('borderCell', x, y, self) for x in range(self.width)] for y in range(self.height)]
        self.listeBorderLabels = []
        borderTemplate = [['corner_up_left',     'border_hor',     'corner_up_right'],
                          ['border_vert',         'blank',             'border_vert'],
                          ['t_left',             'border_hor',             't_right'],
                          ['border_vert',         'blank',             'border_vert'],
                          ['corner_bottom_left', 'border_hor', 'corner_bottom_right']]
        template_y = 0
        for y in range(self.height):
            self.listeBorderLabels.append([])
            if not(y == 0):
                if 0 < y < 4:
                    template_y = 1
                elif y == 4:
                    template_y = 2
                elif 4 < y < self.height-1:
                    template_y = 3
                else:
                    template_y = 4
            for x in range(self.width):
                template_x = 0
                if 0 < x < self.width-1:
                    template_x = 1
                elif x == self.width-1:
                    template_x = 2
                label = Label(main, image=textures[borderTemplate[template_y][template_x]], height=38, width=38, bd=0, highlightthickness=0)
                self.listeBorderLabels[y].append(label)
                self.listeBorderCells[y][x].label = label
                label.cell = self.listeBorderCells[y][x]
                label.place(x=38*x, y=38*y)

    def createTopBarCells(self):
        textures
        self.smileyFaceCell = Cell('smileyFace', 0, 0, self)
        if self.difficulty == 'easy':
                self.smileyFaceLabel = Label(main, image=textures['face_unpressed_small'], height=45, width=45, bd=0, highlightthickness=0)
        else:
                self.smileyFaceLabel = Label(main, image=textures['face_unpressed'], height=70, width=70, bd=0, highlightthickness=0)
        self.smileyFaceLabel.place(relx=0.5, y=95, anchor=CENTER)
        self.smileyFaceCell.label = self.smileyFaceLabel
        self.smileyFaceLabel.cell = self.smileyFaceCell
        self.smileyFaceLabel.bind('<Button-1>', smileyFacePress)
        self.smileyFaceLabel.bind('<ButtonRelease-1>', smileyFaceRelease)
        self.digNumbersList = [[], []]
        self.digLabelsList = [[], []]
        if self.difficulty == 'easy':
                Label(main, image=textures['nums_background'], height=91, width=146, bd=0, highlightthickness=0).place(x=40, y=95, anchor=W)
                Label(main, image=textures['nums_background'], height=91, width=146, bd=0, highlightthickness=0).place(x=233 + (self.width-11)*38, y=95, anchor=W)
        else:
                Label(main, image=textures['nums_background'], height=91, width=146, bd=0, highlightthickness=0).place(x=50, y=95, anchor=W)
                Label(main, image=textures['nums_background'], height=91, width=146, bd=0, highlightthickness=0).place(x=222 + (self.width-11)*38, y=95, anchor=W)
        for i in range(3):
                self.digNumbersList[0].append(Cell('digNumber', i, 0, self))
                self.digLabelsList[0].append(Label(main, image=textures['d0'], height=76, width=40, bd=0, highlightthickness=0))
                if self.difficulty == 'easy':
                        self.digLabelsList[0][i].place(x=47+46*i, y=95, anchor=W)
                else:
                        self.digLabelsList[0][i].place(x=57+46*i, y=95, anchor=W)
                self.digNumbersList[0][i].label = self.digLabelsList[0][i]
                self.digLabelsList[0][i] = self.digNumbersList[0][i]
        for i in range(3):
                self.digNumbersList[1].append(Cell('digNumber', i, 0, self))
                self.digLabelsList[1].append(Label(main, image=textures['d0'], height=76, width=40, bd=0, highlightthickness=0))
                if self.difficulty == 'easy':
                        self.digLabelsList[1][i].place(x=240+46*i, y=95, anchor=W)
                else:
                        self.digLabelsList[1][i].place(x=229 + 46*i + (self.width-11)*38, y=95, anchor=W)
                self.digNumbersList[1][i].label = self.digLabelsList[1][i]
                self.digLabelsList[1][i] = self.digNumbersList[1][i]

    def createGameCells(self):
        textures
        self.listeGameCells = [[Cell('gameCell', x,y, self) for x in range(self.width-2)] for y in range(self.height-6)]
        self.listeGameLabels = []
        for y in range(len(self.listeGameCells)):
            self.listeGameLabels.append([Label(main, image=textures['closed'], height=38, width=38, bd=0, highlightthickness=0) for _ in range(len(self.listeGameCells[0]))])
            for x in range(len(self.listeGameLabels[y])):
                label = self.listeGameLabels[y][x]
                label.bind('<Button-1>', gameCellPress)
                label.bind('<ButtonRelease-1>', gameCellRelease)
                label.bind('<B1-Motion>', gameCellMotion)
                label.bind('<<Enter>>', gameCellPress)
                label.bind('<<Leave>>', gameCellRelease)
                label.bind('<Button-3>', gameCellFlag)
                label.cell = self.listeGameCells[y][x]
                self.listeGameCells[y][x].label = label
                label.place(x=38+x*38, y=38*5+y*38)

    def placeMines(self):
        self.mineCount = 0
        if self.difficulty == 'easy':
            self.mineCount = 10
        elif self.difficulty == 'normal':
            self.mineCount = 40
        else:
            self.mineCount = 80
        for _ in range(self.mineCount):
            randHeight = random.randint(0, self.height-7)
            randWidth = random.randint(0, self.width-3)
            if not(self.listeGameCells[randHeight][randWidth].mine):
                self.listeGameCells[randHeight][randWidth].mine = True

    def showMineCount(self):
        textures
        digNumbers = self.digNumbersList[0]
        mineCount = str(self.mineCount)
        mineCount = "0"*(3-len(mineCount)) + mineCount
        for i in range(3):
            digNumbers[i].label.config(image=textures[f'd{mineCount[i]}'])

    def timer(self, time):
        self.time = time
        if not(time == 999):
            self.time += 1
        digNumbers = self.digNumbersList[1]
        strTime = str(self.time)
        strTime = "0"*(3-len(strTime)) + strTime
        for i in range(3):
            try: digNumbers[i].label.config(image=textures[f'd{strTime[i]}'])
            except: pass
        if not(self.gameIsOver):
            main.after(1000, self.timer, self.time)

    def gameOver(self):
        self.gameIsOver = True
        main.title('Minesweeper - You lost!')
        self.smileyFaceLabel.config(image=textures['face_lose_small' if self.difficulty == 'easy' else 'face_lose'])
        for tab in self.listeGameCells:
            for cell in tab:
                if not(cell.revealed):
                    if (cell.mine) and not(cell.flagged):
                        cell.label.config(image=textures['mine'])
                    elif (cell.flagged) and not(cell.mine):
                        cell.label.config(image=textures['flag_wrong'])
    
    def placeWindow(self):
        main.update_idletasks()  # Let Tk calculate window size
        w = main.winfo_width()
        h = main.winfo_height()
        screen_w = main.winfo_screenwidth()
        screen_h = main.winfo_screenheight() - 85
        x = (screen_w // 2) - (w // 2)
        y = (screen_h // 2) - (h // 2)
        main.geometry(f"{w}x{h}+{x}+{y}")

    def resetWindow(self):
        self.gameIsOver = True
        for widget in main.winfo_children():
            widget.destroy()
        main.title("Minesweeper")
        main.geometry("442x442")

    

    
                
            
class Cell:
    def __init__(self, cellType:['gameCell', 'borderCell', 'smileyFace', 'digNumber'], x,y, jeu):
        self.jeu = jeu
        self.cellType = cellType
        self.x = x
        self.y = y
        # x is the horizontal axis, y is the vertical axis
        self.label = None
        self.flagged = False
        self.mine = False
        self.revealed = False

    def openArea(self):
        textures
        if not(self.flagged) and not(self.revealed):
            self.revealed = True
            if not(self.mine):
                nearbyMines = 0
                for i in range(3):
                    for j in [[-1, 0, 1], [-1, 1], [-1, 0, 1]][i]:
                        try:
                            assert  (0 <= self.y+1-i < self.jeu.height-6) and (0 <= self.x+j < self.jeu.width-2)
                            if self.jeu.listeGameCells[self.y+1-i][self.x+j].mine:
                                nearbyMines += 1
                        except: pass
                self.label.config(image=textures[f'type{nearbyMines}'])
                if nearbyMines == 0:
                    for i in range(3):
                        for j in [[-1, 0, 1], [-1, 1], [-1, 0, 1]][i]:
                            try:
                                assert  (0 <= self.y+1-i < self.jeu.height-6) and (0 <= self.x+j < self.jeu.width-2)
                                self.jeu.listeGameCells[self.y+1-i][self.x+j].openArea()
                            except: pass
            elif self == current_widget.cell:
                self.label.config(image=textures['mine_red'])
                self.jeu.gameOver()
        
    

Jeu()
atexit.register(main.destroy)
