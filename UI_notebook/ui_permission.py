import wx
from wx.lib.scrolledpanel import ScrolledPanel
from Control_id import ctrl_id as ID
from UI_notebook.MyCheckBox import MyCheckBox


class premessionPanel(ScrolledPanel):
    def __init__(self, parent, id,server, size=(200,-1)):
        ScrolledPanel.__init__(self, parent, id=id,size=size)
        # panel = wx.Panel(parent, -1)
        self.server = server
        # self.scrollPael = ScrolledPanel(self, -1)
        self.SetupScrolling()
        panel = wx.Panel(self, -1)
        # box = wx.BoxSizer(wx.VERTICAL)
        staticBox = wx.StaticBox(panel, -1, "Permession")
        font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        staticBox.SetFont(font)
        checkSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        self.checkCtrl = []
        panel.Enable(False)
        # resopnse = self.server.getAllLimitInfo()
        
        # if resopnse['status'] == 0 and resopnse['data']:
        #     PerList.PERLIST = resopnse['data']
        
        for i in PerList.PERLIST:
            label = list(i.keys())[0]
            button = MyCheckBox(panel, label, i.get(label))
            # button.SetRefData()
            self.checkCtrl.append(button)
            button.Bind(wx.EVT_CHECKBOX, self.onClick)

            checkSizer.Add(button, 1, wx.EXPAND | wx.ALL, 3)
        panel.SetSizer(checkSizer)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        # button = wx.Button(self, -1, "OK")
        # sizer.Add(button, 0, wx.EXPAND)
        self.SetSizer(sizer)
        # panel.Hide()

        


    def changeStatue(self, premession):
        
        for i in range(len(self.checkCtrl)):
            checkBox = self.checkCtrl[i]
            flag = premession >> (checkBox.bit-1) & 1
            self.checkCtrl[i].SetValue(flag)
        self.Refresh()

    def onClick(self, event):
        pass
