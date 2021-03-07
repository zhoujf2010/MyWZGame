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





x = 0
y = 0
endy= 0
isjump = False

def KeyPress(evt):
#     print(evt)
    global x,y
    if evt.keysym=='Right':
        x = 1
    elif evt.keysym=='Left':
        x = -1
    
def KeyRelease(evt):
#     print(evt)
    global x,y,isjump,endy
    if evt.keysym=='Right':
        x = 0
    elif evt.keysym=='Left':
        x = 0
    elif evt.keysym=='space':
        y = -10
        endy = 10
        isjump = True
    #x = 0

canvas.bind_all('<KeyPress>', KeyPress)
canvas.bind_all('<KeyRelease>', KeyRelease)

def loop2():
    global y,isjump,p,index
#     print('x')
    # print(canvas.coords(obj))
    canvas.move(obj_back,x,y)

    
    canvas.after(10, loop2)


loop()
loop2()
tk.mainloop()