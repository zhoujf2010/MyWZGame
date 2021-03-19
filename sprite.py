import tkinter as tk
import os
from PIL import ImageTk, Image, ImageDraw
import math
from timer import Timer
from xml.dom import minidom


class Sprite:
    def __init__(self, tkx, canvas, spritename):
        self.canvas = canvas
        self.action = 0     # 0停止(0~3)  1行走(0~4)  2攻击(0~4)  3??(0~2)
        self.direct = 0  # 方向

        mydoc = minidom.parse('img/%s.xml' % spritename[-1:])
        sprite = mydoc.getElementsByTagName("Sprite")[0]
        items = mydoc.getElementsByTagName('Frame')
        speed =  int(sprite.getAttribute("Speed"))

        offesetlst = {}
        for item in items:
            offesetlst[str(item.getAttribute("ID"))] = [int(item.getAttribute("OffsetX")), int(item.getAttribute("OffsetY"))]
        self.offesetlst = offesetlst
        self.centerX = int(sprite.getAttribute("CenterX"))
        self.centerY = int(sprite.getAttribute("CenterY"))

        self.spriteImages = {}
        for file in os.listdir("./img/%s" % spritename):
            if file.endswith(".png"):
                filename = file[:-4]

                imgsrc = Image.open(os.path.join("./img/%s" % spritename, file))
                size = imgsrc.size
                offset = self.offesetlst[filename]

                img = Image.new('RGBA', (size[0]+offset[0], size[1]+offset[1]), color=(255, 0, 0, 0))
                img.paste(imgsrc, (offset[0], offset[1]))

                self.spriteImages[filename] = ImageTk.PhotoImage(img)

        self.manPos = [0, 0]
        self.obj = canvas.create_image(0, 0, anchor=tk.NW)
        self.gotoPos(200, 200)

        # self.centobj = canvas.create_arc(self.manPos[0]-2, self.manPos[1]-2, self.manPos[0]+2, self.manPos[1]+2,fill='red', outline='yellow')

        self.runtimer = None

        self.frame = 0
        frametimer = Timer(self.canvas, speed, self.changeFrame)
        frametimer.start()

    def gotoPos(self, x, y):
        dx = x - self.manPos[0] - self.centerX
        dy = y - self.manPos[1] - self.centerY
        self.canvas.move(self.obj, dx, dy)
        self.manPos = [x, y]

    def movePos(self, dx, dy):
        self.canvas.move(self.obj, dx, dy)
        self.manPos[0] = self.manPos[0] + dx
        self.manPos[1] = self.manPos[1] + dy

    def changeFrame(self):
        self.frame = self.frame+1
        if self.frame == 4:
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

    def calcdist(self, point1, point2):
        return math.sqrt(
            math.pow((point1[0]-point2[0]), 2)+math.pow((point1[1]-point2[1]), 2))

    def goto(self, target):
        self.direct = self.getDir(self.manPos, target)
        duration = self.calcdist(self.manPos, target)

        if self.runtimer is not None:
            self.runtimer.stop()

        self.runtimer = Timer(self.canvas, 10, self.running)
        self.target = target
        dx = (target[0]-self.manPos[0]) / duration
        dy = (target[1]-self.manPos[1]) / duration
        self.action = 1
        self.runtimer.start((dx,dy))

    def running(self,pos):
        duration = math.sqrt(
            math.pow((self.manPos[0]-self.target[0]), 2)+math.pow((self.manPos[1]-self.target[1]), 2))
        if duration <= 1:
            self.action = 0
            self.runtimer.stop()
            self.runtimer = None

        self.movePos(pos[0],pos[1])