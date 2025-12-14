from tkinter import *
from PIL import Image, ImageTk
import random, os

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
                    img = img.resize( (62, 62), Image.Resampling.LANCZOS )
                elif img.size == (94,94):
                    img = img.resize( (38, 38), Image.Resampling.LANCZOS )
                else:
                    img = img.resize( (26, 50), Image.Resampling.LANCZOS )
                dictTextures[name] = ImageTk.PhotoImage(img, master=main)
        return dictTextures
textures = load_textures('images')


def mousePress(event):
    global mouseDown
    mouseDown = True
def mouseRelease(event):
    global mouseDown
    mouseDown = False

current_widget = None
def gameCellPress(event):
    mousePress(event)
    event.widget.config(image=textures['type0'])
def gameCellUnpressed(event):
    global current_widget
    mouseRelease(event)
    event.widget.config(image=textures['closed'])
    if current_widget:
        current_widget.config(image=textures['closed'])
def gameCellMotion(event):
    global current_widget
    widget = event.widget.winfo_containing(event.x_root, event.y_root)
    if current_widget != widget:
        if current_widget:
            current_widget.event_generate("<<Leave>>")
        current_widget = widget
        current_widget.event_generate("<<Enter>>")




class Jeu:
    def __init__(self):
        self.createBorderCells('normal')
        #self.createGameCells()

    def createGameCells(self):
        textures
        self.listeGameCells = [[Cell('gameCell', x,y) for x in range(9)] for y in range(9)]
        self.listeGameLabels = []
        for y in range(len(self.listeGameCells)):
            self.listeGameLabels.append([Label(main, image=textures['closed'], height=38, width=38, bd=0, highlightthickness=0) for _ in range(len(self.listeGameCells[0]))])
            for x in range(len(self.listeGameLabels[y])):
                label = self.listeGameLabels[y][x]
                label.bind('<Button-1>', gameCellPress)
                label.bind('<ButtonRelease-1>', gameCellUnpressed)
                label.bind('<B1-Motion>', gameCellMotion)
                label.bind('<<Enter>>', gameCellPress)
                label.bind('<<Leave>>', gameCellUnpressed)
                label.cell = self.listeGameCells[y][x]
                self.listeGameCells[y][x].label = label
                label.place(x=x*38, y=y*38)
                
    def createBorderCells(self, mode):
        textures
        if mode == 'easy':
            width = 9+2
            height = 9+6
        elif mode == 'normal':
            width = 16+2
            height = 16+6
        else:
            width = 30+2
            height = 16+6
        main.geometry(f'{38*width}x{38*height}')
        self.listeBorderCells = [[Cell('borderCell', x, y) for x in range(width)] for y in range(height)]
        self.listeBorderLabels = []
        borderTemplate = [['corner_up_left',     'border_hor',     'corner_up_right'],
                          ['border_vert',         'blank',             'border_vert'],
                          ['t_left',             'border_hor',             't_right'],
                          ['border_vert',         'blank',             'border_vert'],
                          ['corner_bottom_left', 'border_hor', 'corner_bottom_right']]
        template_y = 0
        for y in range(height):
            self.listeBorderLabels.append([])
            if not(y == 0):
                if 0 < y < 4:
                    template_y = 1
                elif y == 4:
                    template_y = 2
                elif 4 < y < height-1:
                    template_y = 3
                else:
                    template_y = 4
            for x in range(width):
                template_x = 0
                if 0 < x < width-1:
                    template_x = 1
                elif x == width-1:
                    template_x = 2
                label = Label(main, image=textures[borderTemplate[template_y][template_x]], height=38, width=38, bd=0, highlightthickness=0)
                self.listeBorderLabels[y].append(label)
                self.listeBorderCells[y][x].label = label
                label.cell = self.listeBorderCells[y][x]
                label.place(x=38*x, y=38*y)
                
                
            
class Cell:
    def __init__(self, cellType:['gameCell', 'borderCell', 'smileyFace', 'digNumber'], x,y):
        self.cellType = cellType
        self.x = x
        self.y = y
        self.label = None

jeuActuel = Jeu()
