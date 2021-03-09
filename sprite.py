import tkinter as tk
import os
from PIL import ImageTk, Image
import math


class Sprite:
    def __init__(self, canvas, spritename):

        self.canvas = canvas
        manPos = [151, 318]
        self.action = 0     # 0停止(0~3)  1行走(0~4)  2攻击(0~4)  3??(0~2)
        self.direct = 0  # 方向
        self.spriteImages = {}
        for file in os.listdir("./img/%s" % spritename):
            if file.endswith(".png"):
                filename = file[:-4]
                self.spriteImages[filename] = ImageTk.PhotoImage(
                    Image.open(os.path.join("./img/%s" % spritename, file)))

        self.obj = canvas.create_image(
            manPos[0], manPos[1], anchor=tk.NW, image=self.spriteImages["0-0-0"])
        self.manPos = manPos
        self.p = 0
        self.loop()

    def loop(self):

        self.p = self.p+1
        if self.p == 3:
            self.p = 0

        imgfile = "%s-%s-%s" % (self.action, self.direct, self.p)
        self.canvas.itemconfig(self.obj, image=self.spriteImages[imgfile])
        self.canvas.after(250, self.loop)

    def getDir(self, current, target):
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

    def goto(self, target):
        self.direct = self.getDir(self.manPos, target)
        duration = math.sqrt(
            math.pow((self.manPos[0]-target[0]), 2)+math.pow((self.manPos[1]-target[1]), 2)) * 30

        step = int(duration / 120)

        dx = (target[0]-self.manPos[0]) / step
        dy = (target[1]-self.manPos[1]) / step

        self.action = 1
        self.goto2(step, dx, dy)

    def goto2(self, step, dx, dy):
        if step == 0:
            self.action = 0
            return
        step = step - 1

        x = self.manPos[0] + dx
        y = self.manPos[1] + dy

        self.canvas.move(self.obj, dx, dy)
        self.manPos[0] = x
        self.manPos[1] = y

        # if startrun:
        self.canvas.after(120, self.goto2, step-1, dx, dy)
