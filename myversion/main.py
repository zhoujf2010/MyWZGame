from tkinter import *
import random
import time
import tkinter as tk
from PIL import ImageTk, Image
import os
import math


tk = Tk()

canvas = Canvas(tk, width=800,height=600)
canvas.pack()

backimg = ImageTk.PhotoImage(Image.open("img/scene/map0.jpg"))
obj_back = canvas.create_image(0,0,anchor=NW,image=backimg)  


manPos =[151,318]

spriteImages = {}
for file in os.listdir("./img/Sprite0"):
    if file.endswith(".png"):
        filename = file[:-4]
        spriteImages[filename] = ImageTk.PhotoImage(
            Image.open(os.path.join("./img/Sprite0", file)))

obj = canvas.create_image(manPos[0], manPos[1], anchor=NW, image=spriteImages["0-0-0"])

direct = 0  #0停止(0~3)  1行走(0~4)  2攻击(0~4)  3??(0~2)
action = 0 

p = 0

def loop():
    global p

    p = p+1
    if p == 3:
        p = 0

    imgfile = "%s-%s-%s" % (action,direct,p)
    canvas.itemconfig(obj, image=spriteImages[imgfile])
    canvas.after(250, loop)


def getDir(current,target):
    tan = (target[1] - current[1]) / (target[0] - current[0])

    if abs(tan) >= math.tan(math.pi * 3 / 8) and target[1] <= current[1]:
        return 0
    elif (abs(tan) > math.tan(math.pi / 8) and abs(tan) < math.tan(math.pi * 3 / 8) and target[0] > current[0] and target[1] < current[1]):
        return 1
    elif (abs(tan) <= math.tan(math.pi / 8) and target[0] >= current[0]):
        return 2
    elif (abs(tan) > math.tan(math.pi / 8) and abs(tan) < math.tan(math.pi * 3 / 8) and target[0] > current[0] and target[1] > current[1]) :
        return 3
    elif (abs(tan) >= math.tan(math.pi * 3 / 8) and target[1] >= current[1]) :
        return 4
    elif (abs(tan) > math.tan(math.pi / 8) and abs(tan) < math.tan(math.pi * 3 / 8) and target[0] < current[0] and target[1] > current[1]) :
        return 5
    elif (abs(tan) <= math.tan(math.pi / 8) and target[0] <= current[0]):
        return 6
    elif (abs(tan) > math.tan(math.pi / 8) and abs(tan) < math.tan(math.pi * 3 / 8) and target[0] < current[0] and target[1] < current[1]) :
        return 7
    else:
        return 0


startrun = False

def goto(target):
    global startrun,manPos
    if target[0] > manPos[0]:
        dx = 5
    elif target[0] < manPos[0]:
        dx = -5
    else:
        dx = 0
    if target[1] > manPos[1]:
        dy = 5
    elif target[0] < manPos[0]:
        dy = -5
    else:
        dy = 0

    x = manPos[0] + dx
    y = manPos[1] + dy
    
    canvas.move(obj, dx,dy)
    manPos[0] = x
    manPos[1] = y
    print("----",manPos)


    if startrun:
        canvas.after(120,goto,target)
    #threading.Timer(0.1,myfunction).start()#第一个参数为执行间隔,单位秒




def mouseDown(evt):
    global p, direct,action,startrun
    newPos = [evt.x,evt.y]
    direct = getDir(manPos,newPos)
    action = 1
    print(1,evt)
    startrun = True
    goto(newPos)


def mouseUp(evt):
    global p, direct,action,startrun
    action = 0
    print(2,evt)
    startrun = FALSE

canvas.bind("<Button-1>", mouseDown)
canvas.bind("<ButtonRelease-1>", mouseUp)



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