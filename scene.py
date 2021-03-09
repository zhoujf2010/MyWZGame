
from PIL import ImageTk, Image
import tkinter as tk

class Scene:
    def __init__(self,canvas,map):
        backimg = ImageTk.PhotoImage(Image.open("img/scene/%s.jpg" %map))
        self.backimg = backimg
        obj_back = canvas.create_image(0, 0, anchor=tk.NW, image=backimg)
        self.obj_back= obj_back

        self.x = 0
        self.y = 0
        self.canvas = canvas
        self.loop()

    def setX(self,x):
        self.x = x

    def setY(self,y):
        self.y = y

    def setMoveDir(self,move):
        if move == 'Right':
            self.setX(1)
        elif move == 'Left':
            self.setX(-1)
        elif move == 'Up':
            self.setY(-1)
        elif move == 'Down':
            self.setY(1)
    
    def stop(self):
        self.x = 0
        self.y = 0
    
    def loop(self):
        self.canvas.move(self.obj_back, self.x, self.y)
        self.canvas.after(10, self.loop)

