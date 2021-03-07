from tkinter import *
import random
import time
import tkinter as tk
from PIL import ImageTk, Image


tk = Tk()

canvas = Canvas(tk, width=800,height=600)
canvas.pack()


img1 = ImageTk.PhotoImage(Image.open("img/Sprite0/0-0-0.png"))
obj = canvas.create_image(200,370,anchor=NW,image=img1)  


tk.mainloop()