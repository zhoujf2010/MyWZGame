import tkinter
import time
from tkinter import *

tk = Tk()


window = Frame(tk)
width = 800
height = 600
left = (tk.winfo_screenwidth() - width) / 2
top = (tk.winfo_screenheight() - height) / 2
tk.geometry("%dx%d+%d+%d" % (width, height, left, top)) 




canvas = Canvas(tk, width=300, height=200,bg='white')
canvas.pack()
obj = canvas.create_image(0,0)

canvas = Canvas(tk, width=300, height=200,bg='red')
canvas.pack()

window.mainloop()

