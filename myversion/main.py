from tkinter import *
import random
import time
import tkinter as tk
from PIL import ImageTk, Image


tk = Tk()

canvas = Canvas(tk, width=800,height=600)
canvas.pack()

backimg = ImageTk.PhotoImage(Image.open("img/scene/map0.jpg"))
obj_back = canvas.create_image(0,0,anchor=NW,image=backimg)  


img1 = ImageTk.PhotoImage(Image.open("img/Sprite0/0-0-0.png"))
img2 = PhotoImage(file = "img/Sprite0/0-0-1.png")
img3 = PhotoImage(file = "img/Sprite0/0-0-2.png")
img4 = PhotoImage(file = "img/Sprite0/0-0-3.png")
imgs =[img1,img2,img3,img4]
obj = canvas.create_image(200,370,anchor=NW,image=imgs[0])  


p =0 

def loop():
    global p

    p = p+1
    if p == 3:
        p = 0

    canvas.itemconfig(obj, image=imgs[p])
    
    canvas.after(250, loop)


loop()
tk.mainloop()