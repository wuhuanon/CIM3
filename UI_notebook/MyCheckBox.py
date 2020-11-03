import wx
class MyCheckBox(wx.CheckBox):
    def __init__(self, parent, lable, bit, id=-1, style=0):
        super(MyCheckBox, self).__init__(parent, id, lable, style=style)
        self.bit = bit