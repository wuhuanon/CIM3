import wx

from Control_id.config_premession import Messages
from UI_notebook.MyValidate import DigitsValidator
from UI_notebook.ui_Dialog.ui_messageBox import showStatusMessage


class ModifyMachine(wx.Dialog):
    def __init__(self, parent, server):
        super(ModifyMachine, self).__init__(None, title='', size=(500, 250))
        self.parent = parent
        self.server = server
        self.ip_index = Messages.MACHINE_FIELDS.get(Messages.MACHINE_IP)[0]
        self.manufacturer_index = Messages.MACHINE_FIELDS.get(Messages.MACHINE_MANUFACTURER)[0]
        self.about_index = Messages.MACHINE_FIELDS.get(Messages.MACHINE_ABOUT)[0]
        self.InitUI()

    def InitUI(self):
        # self.SetSize((600, 600))
        panel = wx.Panel(self)

        # ip_l = wx.StaticText(panel, -1, "IP:")
        # self.ip_t = wx.TextCtrl(panel, -1, self.parent.jobList.getColumnText(self.parent.jobList.currentItem,
        #                         self.ip_index), size=(320, 25))
        #
        # manufacturer_l = wx.StaticText(panel, -1, Messages.MACHINE_MANUFACTURER + ":")
        # self.manufacturer_t = wx.TextCtrl(panel, -1, self.parent.jobList.getColumnText(self.parent.jobList.currentItem,
        #                         self.manufacturer_index) )
        about_l = wx.StaticText(panel, -1, Messages.MACHINE_ABOUT + ":")
        self.about_t = wx.TextCtrl(panel, -1, self.parent.jobList.getColumnText(self.parent.jobList.currentItem,
                                self.about_index))

        saveBtn = wx.Button(panel, -1, "OK")
        cancelBtn = wx.Button(panel, -1, "Cancel")
        cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        saveBtn.Bind(wx.EVT_BUTTON, self.OnSave)
        # Now do the layout.
        # mainSizer is the top-level one that manages everything
        # 2 垂直的sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        # 3 地址列
        addrSizer = wx.GridBagSizer(hgap=5, vgap=5)
        # addrSizer.AddGrowableCol(1)

        addrSizer.Add(ip_l, pos=(0, 0),
                      flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.ip_t, pos=(0, 1), flag=wx.EXPAND | wx.ALL)

        # 4 带有空白空间的行
        # addrSizer.Add((10, 10))  # some empty space

        addrSizer.Add(manufacturer_l, pos=(1, 0),
                      flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.manufacturer_t, pos=(1, 1), flag=wx.EXPAND)
        addrSizer.Add(about_l, pos=(2, 0),
                      flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.about_t, pos=(2, 1), flag=wx.EXPAND)

        # now add the addrSizer to the mainSizer

        mainSizer.Add(addrSizer, 1, wx.EXPAND | wx.ALL, 40)
        # The buttons sizer will put them in a row with resizeable
        # gaps between and on either side of the buttons
        # 8 按钮行
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(saveBtn)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(cancelBtn)
        btnSizer.Add((20, 20), 1)
        mainSizer.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        panel.SetSizer(mainSizer)
        # Fit the frame to the needs of the sizer.  The frame will
        # automatically resize the panel as needed.  Also prevent the
        # frame from getting smaller than this size.
        # mainSizer.Fit(self)
        # self.changeCheck(self.parent.dvc.GetItemData(self.parent.dvc.RowToItem(self.index)))
        self.Centre()
        # mainSizer.SetSizeHints(self)
        self.ShowModal()
        self.Fit()

    def OnCancel(self, event):
        self.Destroy()

    def OnSave(self, event):

        ip = self.ip_t.GetValue()

        manu = self.manufacturer_t.GetValue()
        about = self.about_t.GetValue()
        self.parent.jobList.modifyItem(self.parent.jobList.currentItem, self.ip_index, ip)
        self.parent.jobList.modifyItem(self.parent.jobList.currentItem, self.manufacturer_index, manu)
        self.parent.jobList.modifyItem(self.parent.jobList.currentItem, self.about_index, about)
        # self.parent.jobList.Refresh()
        self.Destroy()





