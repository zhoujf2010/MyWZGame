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

tk = Tk()

canvas = Canvas(tk, width=800, height=600)
canvas.pack()
scene = Scene(canvas,"map0")
sprite = Sprite(canvas,"Sprite0")


def mouseDown(evt):
    newPos = [evt.x, evt.y]
    Animation(canvas,3,newPos)
    sprite.goto(newPos)

def mouseUp(evt):
    pass

def KeyPress(evt):
    scene.setMoveDir(evt.keysym)

def KeyRelease(evt):
    scene.stop()


canvas.bind("<Button-1>", mouseDown)
canvas.bind("<ButtonRelease-1>", mouseUp)
canvas.bind_all('<KeyPress>', KeyPress)
canvas.bind_all('<KeyRelease>', KeyRelease)

tk.mainloop()
