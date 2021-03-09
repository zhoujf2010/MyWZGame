from tkinter import *
import random
import time
import tkinter as tk
from PIL import ImageTk, Image
import os
import math


tk = Tk()

canvas = Canvas(tk, width=800, height=600)
canvas.pack()

backimg = ImageTk.PhotoImage(Image.open("img/scene/map0.jpg"))
obj_back = canvas.create_image(0, 0, anchor=NW, image=backimg)

manPos = [151, 318]

spriteImages = {}
for file in os.listdir("./img/Sprite0"):
    if file.endswith(".png"):
        filename = file[:-4]
        spriteImages[filename] = ImageTk.PhotoImage(
            Image.open(os.path.join("./img/Sprite0", file)))

obj = canvas.create_image(
    manPos[0], manPos[1], anchor=NW, image=spriteImages["0-0-0"])

direct = 0  # 0停止(0~3)  1行走(0~4)  2攻击(0~4)  3??(0~2)
action = 0

p = 0


def loop():
    global p

    p = p+1
    if p == 3:
        p = 0

    imgfile = "%s-%s-%s" % (action, direct, p)
    canvas.itemconfig(obj, image=spriteImages[imgfile])
    canvas.after(250, loop)


def getDir(current, target):
    tan = (target[1] - current[1]) / (target[0] - current[0])

    if abs(tan) >= math.tan(math.pi * 3 / 8) and target[1] <= current[1]:
        return 0
    elif (abs(tan) > math.tan(math.pi / 8) and abs(tan) < math.tan(math.pi * 3 / 8) and target[0] > current[0] and target[1] < current[1]):
        return 1
    elif (abs(tan) <= math.tan(math.pi / 8) and target[0] >= current[0]):
        return 2
    elif (abs(tan) > math.tan(math.pi / 8) and abs(tan) < math.tan(math.pi * 3 / 8) and target[0] > current[0] and target[1] > current[1]):
        return 3
    elif (abs(tan) >= math.tan(math.pi * 3 / 8) and target[1] >= current[1]):
        return 4
    elif (abs(tan) > math.tan(math.pi / 8) and abs(tan) < math.tan(math.pi * 3 / 8) and target[0] < current[0] and target[1] > current[1]):
        return 5
    elif (abs(tan) <= math.tan(math.pi / 8) and target[0] <= current[0]):
        return 6
    elif (abs(tan) > math.tan(math.pi / 8) and abs(tan) < math.tan(math.pi * 3 / 8) and target[0] < current[0] and target[1] < current[1]):
        return 7
    else:
        return 0


startrun = False


def goto(target):
    global startrun, manPos, action
    duration = math.sqrt(
        math.pow((manPos[0]-target[0]), 2)+math.pow((manPos[1]-target[1]), 2)) * 30

    step = int(duration / 120)

    dx = (target[0]-manPos[0]) / step
    dy = (target[1]-manPos[1]) / step

    action = 1
    goto2(step, dx, dy)


def goto2(step, dx, dy):
    global action
    if step == 0:
        action = 0
        return
    step = step - 1

    x = manPos[0] + dx
    y = manPos[1] + dy

    canvas.move(obj, dx, dy)
    manPos[0] = x
    manPos[1] = y

    # if startrun:
    canvas.after(120, goto2, step-1, dx, dy)


def mouseDown(evt):
    global p, direct, action, startrun
    newPos = [evt.x, evt.y]
    direct = getDir(manPos, newPos)
    print(1, evt)
    startrun = True
    goto(newPos)
    showClick(newPos, 0, None)


def mouseUp(evt):
    global p, direct, action, startrun
    # action = 0
    print(2, evt)
    startrun = FALSE


canvas.bind("<Button-1>", mouseDown)
canvas.bind("<ButtonRelease-1>", mouseUp)


Animations = []
for file in os.listdir("./img/Animation/3/"):
    if file.endswith(".png"):
        Animations.append(ImageTk.PhotoImage(
            Image.open(os.path.join("./img/Animation/3/", file))))


def showClick(pos, startAindex, obj):
    if startAindex >= len(Animations):
        canvas.delete(obj)
        return
    if obj is None:
        obj = canvas.create_image(
            pos[0]-36, pos[1]-19, anchor=NW, image=Animations[startAindex])

    canvas.itemconfig(obj, image=Animations[startAindex])

    canvas.after(120, showClick, pos, startAindex+1, obj)


x = 0
y = 0
endy = 0
isjump = False


def KeyPress(evt):
    global x, y
    if evt.keysym == 'Right':
        x = 1
    elif evt.keysym == 'Left':
        x = -1
    elif evt.keysym == 'Up':
        y = -1
    elif evt.keysym == 'Down':
        y = 1


def KeyRelease(evt):
    global x, y
    if evt.keysym == 'Right':
        x = 0
    elif evt.keysym == 'Left':
        x = 0
    elif evt.keysym == 'Up':
        y = 0
    elif evt.keysym == 'Down':
        y = 0


canvas.bind_all('<KeyPress>', KeyPress)
canvas.bind_all('<KeyRelease>', KeyRelease)


def loop2():
    canvas.move(obj_back, x, y)
    canvas.after(10, loop2)


# def where(posn):                       #cursor tiop movement and colour change
#     cx=tk.winfo_pointerx() - tk.winfo_rootx()
#     cy=tk.winfo_pointery() - tk.winfo_rooty()
#     tipC.place(x=cx, y=cy)

# canvas.bind("<Motion>",where)        #track mouse movement

loop()
loop2()
tk.mainloop()
