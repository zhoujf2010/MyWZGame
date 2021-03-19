
class Timer:
    def __init__(self, canvas, Interval, callback):
        self.canvas = canvas
        self.callback = callback
        self.Interval = Interval
        self.isRun = False

    def start(self,param =None):
        self.isRun = True
        self.param = param
        self.Doloop(param)

    def stop(self):
        self.isRun = False

    def setInterval(self, Interval):
        self.Interval = Interval

    def Doloop(self,param):
        if param is None:
            self.callback()
        else:
            self.callback(param)
        if self.isRun:
            self.canvas.after(self.Interval, self.Doloop,param)
