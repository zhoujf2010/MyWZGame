from tkinter import *
import random
import time
import tkinter as tk
from PIL import ImageTk, Image
import os
import math
from sprite import Sprite
from animation import Animation
from scene import Scene
from mysocket import mySocket
import json
import sys

#https://www.cnblogs.com/alamiye010/tag/Silverlight%20MMORPG%E7%BD%91%E7%BB%9C%E6%B8%B8%E6%88%8F%E8%AF%BE%E7%A8%8B/

who ="Sprite1"
if len(sys.argv) > 1:
    who = sys.argv[1]

tk = Tk()

canvas = Canvas(tk, width=800, height=600)
canvas.pack()
scene = Scene(canvas,"map0")
sprite = Sprite(tk,canvas,who)
otherlst ={}

def sendginal(x,y):
    dt ={"who":who,"x":x,"y":y}
    mysocket.sendMsg(json.dumps(dt))

def mouseDown(evt):
    newPos = [evt.x, evt.y]
    Animation(canvas,3,newPos)
    sprite.goto(newPos)
    sendginal(evt.x,evt.y)

def mouseUp(evt):
    pass

def KeyPress(evt):
    scene.setMoveDir(evt.keysym)

def KeyRelease(evt):
    scene.stop()

def receiveMsg(msg):
    print(msg)
    dt = json.loads(msg)
    if dt["who"] == who:
        return  #heself

    other = dt["who"]
    x = dt["x"]
    y = dt["y"]
    
    if other not in otherlst:
        sprite = Sprite(tk,canvas,other)
        otherlst[other] = sprite
    otherlst[other].goto((x,y))

canvas.bind("<Button-1>", mouseDown)
canvas.bind("<ButtonRelease-1>", mouseUp)
canvas.bind_all('<KeyPress>', KeyPress)
canvas.bind_all('<KeyRelease>', KeyRelease)


mysocket = mySocket(receiveMsg)
mysocket.connect("127.0.0.1",82)
time.sleep(1)
sendginal(100,210)
# mysocket.sendMsg("我上线了")

tk.mainloop()
mysocket.close()
print(1)
