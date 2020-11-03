import wx, numpy as np
import pylab as plt
import matplotlib
from matplotlib.patches import Rectangle
# matplotlib使用WxAgg為後台, 將matplotlib嵌入wxPython中
matplotlib.use("WxAgg")
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

class plotDialog(wx.Dialog):
    def __init__(self, parent):
        super(plotDialog, self).__init__(None, title='Pan', size=(750, 600))
        self.parent = parent
        self.figure = plt.Figure()
        self.figureCanvas = FigureCanvas(self, -1, self.figure)
        box = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(box)
        box.Add(self.figureCanvas, 1, wx.EXPAND | wx.ALL, 1)
        self.axes = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])  # 新增子區域, 參數為left, bottom, width, height
        self.x = np.linspace(0, 100, 100)
        self.y = np.sin(2 * np.pi * self.x)
        self.axes.OnLog(self.x, self.y)

        self.figureCanvas.draw()
        self.Init()
        self.ShowModal()
    def Init(self):
        self.axes.clear()
        # self.parent.jobList.get
        labels = ["success(11501)", "fail(499)"]
        word_size = [11501, 499]
        colors = ['green', 'red']
        explode = [0, 0.05]  # 0 表示不凸出, 值越大凸越大
        self.axes.pie(word_size, explode=explode, labels=labels, autopct="%3.1f%%", colors=colors, textprops={'fontsize':20, 'color':'yellow'})
        self.figureCanvas.draw()




