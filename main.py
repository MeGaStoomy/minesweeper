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
                    img = img.resize( (62, 62), Image.Resampling.LANCZOS )
                elif img.size == (94,94):
                    img = img.resize( (38, 38), Image.Resampling.LANCZOS )
                else:
                    img = img.resize( (26, 50), Image.Resampling.LANCZOS )
                dictTextures[name] = ImageTk.PhotoImage(img, master=main)
        return dictTextures
textures = load_textures('images')

current_widget = None
def gameCellPress(event):
    global current_widget
    event.widget.config(image=textures['type0'])
    current_widget = event.widget
def gameCellUnpressed(event):
    global current_widget
    event.widget.config(image=textures['closed'])
    if current_widget:
        current_widget.config(image=textures['closed'])
    if event.type == '5':
        print((event.widget.cell.x, event.widget.cell.y))
    print(event.type)
def gameCellMotion(event):
    global current_widget
    widget = event.widget.winfo_containing(event.x_root, event.y_root)
    if (widget) and (widget.cell.cellType == 'gameCell') and (current_widget != widget):
        if current_widget:
            current_widget.event_generate("<<Leave>>")
        current_widget = widget
        current_widget.event_generate("<<Enter>>")





class Jeu:
    def __init__(self):
        self.createBorderCells(input('Quelle difficulté ? (easy, normal, hard) : '))
        self.createGameCells()

    def createGameCells(self):
        textures
        self.listeGameCells = [[Cell('gameCell', x,y) for x in range(self.width-2)] for y in range(self.height-6)]
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
                label.place(x=38+x*38, y=38*5+y*38)
                
    def createBorderCells(self, mode):
        textures
        if mode == 'easy':
            self.width = 9+2
            self.height = 9+6
        elif mode == 'normal':
            self.width = 16+2
            self.height = 11+6
        else:
            self.width = 30+2
            self.height = 11+6
        main.geometry(f'{38*self.width}x{38*self.height}')
        self.placeWindow()
        self.listeBorderCells = [[Cell('borderCell', x, y) for x in range(self.width)] for y in range(self.height)]
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

    def placeWindow(self):
        main.update_idletasks()  # Let Tk calculate window size
        w = main.winfo_width()
        h = main.winfo_height()
        screen_w = main.winfo_screenwidth()
        screen_h = main.winfo_screenheight() - 85
        x = (screen_w // 2) - (w // 2)
        y = (screen_h // 2) - (h // 2)
        main.geometry(f"{w}x{h}+{x}+{y}")

    
                
            
class Cell:
    def __init__(self, cellType:['gameCell', 'borderCell', 'smileyFace', 'digNumber'], x,y):
        self.cellType = cellType
        self.x = x
        self.y = y
        self.label = None

jeuActuel = Jeu()
atexit.register(main.destroy)
