import tkinter as tk
import os
from PIL import ImageTk, Image
import math
from timer import Timer


class Sprite:
    def __init__(self,tkx, canvas, spritename):
        self.canvas = canvas
        manPos = [100, 100]
        self.action = 0     # 0停止(0~3)  1行走(0~4)  2攻击(0~4)  3??(0~2)
        self.direct = 0  # 方向
        self.spriteImages = {}
        self.offset=[54,41]
        for file in os.listdir("./img/%s" % spritename):
            if file.endswith(".png"):
                filename = file[:-4]
                self.spriteImages[filename] = ImageTk.PhotoImage(
                    Image.open(os.path.join("./img/%s" % spritename, file)))

        # canvas = tk.Canvas(tkx, width=50, height=50,bg='red')
        # canvas.pack()

        self.obj = canvas.create_image(
            manPos[0]-self.offset[0], manPos[1]-self.offset[1], anchor=tk.NW, image=self.spriteImages["0-0-0"])

        canvas.create_text(100,100,text='aa')
        self.manPos = manPos
        self.runtimer = None

        self.frame = 0
        frametimer = Timer(self.canvas, 300, self.changeFrame)
        frametimer.start()

    def changeFrame(self):
        self.frame = self.frame+1
        if self.frame == 3:
            self.frame = 0

        imgfile = "%s-%s-%s" % (self.action, self.direct, self.frame)
        self.canvas.itemconfig(self.obj, image=self.spriteImages[imgfile])




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

    def calcdist(self,point1,point2):
        return math.sqrt(
            math.pow((point1[0]-point2[0]), 2)+math.pow((point1[1]-point2[1]), 2))

    def goto(self,target):
        self.direct = self.getDir(self.manPos, target)
        # duration = math.sqrt(
        #     math.pow((self.manPos[0]-target[0]), 2)+math.pow((self.manPos[1]-target[1]), 2)) * 1
        duration = self.calcdist(self.manPos-self.offset,target)
        self.canvas.create_line(self.manPos[0]-self.offset[0],self.manPos[1]-self.offset[1],target[0],target[1])

        if self.runtimer is not None:
            self.runtimer.stop()

        self.runtimer = Timer(self.canvas,10,self.go)
        self.target = target
        self.dx = (target[0]-self.manPos[0]) / duration
        self.dy = (target[1]-self.manPos[1]) / duration
        self.runtimer.start()

    def go(self):
        duration = math.sqrt(
            math.pow((self.manPos[0]-self.target[0]), 2)+math.pow((self.manPos[1]-self.target[1]), 2))
        if duration <= 1:
            self.runtimer.stop()
            self.runtimer = None

        self.canvas.move(self.obj, self.dx, self.dy)
        x = self.manPos[0] + self.dx
        y = self.manPos[1] + self.dy
        self.manPos[0] = x
        self.manPos[1] = y







    # def goto(self, target):
    #     self.direct = self.getDir(self.manPos, target)
    #     duration = math.sqrt(
    #         math.pow((self.manPos[0]-target[0]), 2)+math.pow((self.manPos[1]-target[1]), 2)) * 30

    #     step = int(duration / 120)

    #     dx = (target[0]-self.manPos[0]) / step
    #     dy = (target[1]-self.manPos[1]) / step

    #     self.action = 1
    #     self.goto2(step, dx, dy)

    # def goto2(self, step, dx, dy):
    #     if step == 0:
    #         self.action = 0
    #         return
    #     step = step - 1

    #     x = self.manPos[0] + dx
    #     y = self.manPos[1] + dy

    #     self.canvas.move(self.obj, dx, dy)
    #     self.manPos[0] = x
    #     self.manPos[1] = y

    #     # if startrun:
    #     self.canvas.after(120, self.goto2, step-1, dx, dy)
