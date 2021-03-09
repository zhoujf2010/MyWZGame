
import os
from PIL import ImageTk, Image
import tkinter as tk


class Animation:
    def __init__(self, canvas, num, pos):
        Animations = []
        for file in os.listdir("./img/Animation/%d/" % num):
            if file.endswith(".png"):
                Animations.append(ImageTk.PhotoImage(
                    Image.open(os.path.join("./img/Animation/%d/" % num, file))))
        self.Animations = Animations
        self.canvas = canvas
        self.showClick(pos, 0, None)

    def showClick(self, pos, startAindex, obj):
        if startAindex >= len(self.Animations):
            self.canvas.delete(obj)
            return
        if obj is None:
            obj = self.canvas.create_image(
                pos[0]-36, pos[1]-19, anchor=tk.NW, image=self.Animations[startAindex])

        self.canvas.itemconfig(obj, image=self.Animations[startAindex])

        self.canvas.after(120, self.showClick, pos, startAindex+1, obj)
