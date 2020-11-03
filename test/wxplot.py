import wx, numpy as np
import pylab as plt
import matplotlib
from matplotlib.patches import Rectangle
# matplotlib使用WxAgg為後台, 將matplotlib嵌入wxPython中
matplotlib.use("WxAgg")
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, size = wx.Size( 800,640))
        self.figure=plt.Figure()
        self.figureCanvas=FigureCanvas(self,-1, self.figure)
        box=wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(box)
        box.Add(self.figureCanvas,1,wx.EXPAND|wx.ALL,1)
        self.axes=self.figure.add_axes([0.1, 0.1, 0.8, 0.8])#新增子區域, 參數為left, bottom, width, height
        self.x=np.linspace(0,100,100)
        self.y=np.sin(2*np.pi*self.x)
        self.axes.OnLog(self.x, self.y)

        self.figureCanvas.draw()
        box_btn=wx.BoxSizer(wx.HORIZONTAL)
        box_btn.SetMinSize(wx.Size(-1, 50))
        self.btnBar=wx.Button(self, wx.ID_ANY,"長條圖")
        self.btnPie = wx.Button(self, wx.ID_ANY, "圓餅圖")
        box_btn.Add(self.btnBar, 1, wx.EXPAND|wx.ALL, 1)
        box_btn.Add(self.btnPie, 1, wx.EXPAND|wx.ALL, 1)
        box.Add(box_btn, 0, wx.EXPAND|wx.ALL,1)
        self.Layout()
        self.btnBar.Bind(wx.EVT_BUTTON, self.OnBarClick)
        self.btnPie.Bind(wx.EVT_BUTTON, self.OnPieClick)
        self.axes.grid()
    def OnBarClick(self, event):
        self.axes.clear()#清除原圖
        self.axes.grid(linestyle='-.')#增加格
        self.axes.set(xlim=[0,20], ylim=[0,1], title="Bar")
        self.axes.set_aspect("auto")#回復自動比例
        self.axes.set_ylim(0,1, emit=True,auto=True)
        x=np.linspace(0,20,20)
        uniform_samples = np.random.uniform(size=20)#產生20組介於0與1之間均勻分配隨機變數
        self.axes.bar(x,uniform_samples)
        self.figureCanvas.draw()
    def OnPieClick(self, event):
        self.axes.clear()
        labels = ["day1", "day2", "day3", "day4", "day5", "day6"]
        word_size = [2000, 3250, 4600, 2300, 3600, 5600]
        colors = ['#9999ff', '#ff9999', '#7777aa', '#2442aa', '#dd5555', "green"]
        explode = [0, 0, .05, 0, 0, 0]#0 表示不凸出, 值越大凸越大
        self.axes.pie(word_size, explode=explode, labels=labels, autopct="%3.1f%%", colors=colors)
        self.figureCanvas.draw()
app=wx.App()
frame=MainFrame(None)
frame.Show()
app.MainLoop()