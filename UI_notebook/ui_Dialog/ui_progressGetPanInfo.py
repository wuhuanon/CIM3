import wx


class ProgressPanInfo(wx.Dialog):
    def __init__(self, parent, range1=100, range2=100):
        super(ProgressPanInfo, self).__init__(parent)
        mainBox = wx.BoxSizer(wx.VERTICAL)
        guageSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.title1 = wx.StaticText(self, -1, "")
        self.title2 = wx.StaticText(self, -1, "")
        self.gauge = wx.Gauge(self, range=range1)
        self.gauge2 = wx.Gauge(self, range=range2)
        guageSizer.Add(self.title1, 1, wx.CENTER | wx.ALL, 5)
        guageSizer.Add(self.gauge, 1, wx.EXPAND | wx.ALL, 5)
        guageSizer.Add(self.title2, 1, wx.ALL | wx.CENTER, 5)
        guageSizer.Add(self.gauge2, 1, wx.EXPAND | wx.ALL, 5)

        mainBox.Add(guageSizer, 1, wx.EXPAND, 10)

        mainBox.Add((0, 0), 1, wx.EXPAND, 10)
        self.SetSizer(mainBox)
        self.Show()
        # print(12)

    def setTitle1(self, title):
        self.title1.SetLabel(title)

    def setTitle2(self, title):
        self.title2.SetLabel(title)

    def setGauge1Value(self, value):
        self.gauge.SetValue(value)

    def setGauge2Value(self, value):
        self.gauge2.SetValue(value)

    def setGauge1Range(self, Range):
        self.gauge.SetRange(Range)

    def setGauge2Range(self, Range):
        self.gauge2.SetRange(Range)

    def getGauge1Value(self):
        return self.gauge.GetValue()

    def getGauge2Value(self):
        return self.gauge2.GetValue()

    def addGauge1(self, value=1):
        self.setGauge1Value(self.getGauge1Value() + value)

    def addGauge2(self, value=1):
        self.setGauge2Value(self.getGauge2Value() + value)