
class Timer:
    def __init__(self, canvas, Interval, callback):
        self.canvas = canvas
        self.callback = callback
        self.Interval = Interval
        self.isRun = False

    def start(self):
        self.isRun = True
        self.Doloop()

    def stop(self):
        self.isRun = False

    def setInterval(self, Interval):
        self.Interval = Interval

    def Doloop(self):
        self.callback()
        if self.isRun:
            self.canvas.after(self.Interval, self.Doloop)
