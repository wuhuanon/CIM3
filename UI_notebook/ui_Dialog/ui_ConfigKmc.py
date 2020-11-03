import wx
from Control_id.config_premession import Messages
from UI_notebook.ui_Dialog.ui_messageBox import showStatusMessage
from instruct_parse.ClientServerInterface import KMClientServerInterface


class ConfigKmc(wx.Dialog):
    def __init__(self, parent, kmc = "", bank_name = ""):
        super(ConfigKmc, self).__init__(None, title='', size=(275, 200))
        self.parent = parent
        self.kmc = kmc
        self.bank_name = bank_name
        self.server = parent.server

        self.InitUI()

    def InitUI(self):
        # self.SetSize((600, 600))
        panel = wx.Panel(self)
        keylab = wx.StaticText(panel, -1, "KCV:")
        verlab = wx.StaticText(panel, -1, "Ver:")
        KM = KMClientServerInterface()
        flag = KM.connect()
        if not flag:
            dlg = wx.MessageDialog(None, "Failed to connect to server", "Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            self.Destroy()
            return
        pdklist = KM.KM_EnumPDK(self.bank_name, 5)
        KM.close()
        self.kmcs = [(i[-1][-1], i[-1][0]) for i in pdklist]
        # self.kmcs.append(self.kmc)
        self.key_c = wx.ComboBox(panel, -1, self.kmc, choices=[i[0] for i in self.kmcs], size=(200, 25), style=wx.TE_READONLY)
        self.key_v = wx.TextCtrl(panel, -1, str(self.kmcs[self.key_c.FindString(self.kmc)][1]), style=wx.TE_READONLY)
        # self.key_c = wx.TextCtrl(panel, -1, self.kmc[-1], size=(175, 25))
        self.key_c.Bind(wx.EVT_TEXT, self.OnSelect)
        saveBtn = wx.Button(panel, -1, "OK")
        cancelBtn = wx.Button(panel, -1, "Cancel")
        cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        saveBtn.Bind(wx.EVT_BUTTON, self.OnSave)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        addrSizer = wx.GridBagSizer(hgap=5, vgap=5)



        addrSizer.Add(keylab, pos=(1, 0),
                      flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.key_c, pos=(1, 1), flag=wx.EXPAND)

        addrSizer.Add(verlab, pos=(2, 0),
                      flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.key_v, pos=(2, 1), flag=wx.EXPAND)

        mainSizer.Add(addrSizer, 1, wx.EXPAND | wx.ALL, 10)

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

        self.Centre()
        # mainSizer.SetSizeHints(self)
        self.ShowModal()
        # self.Fit()

    def OnSelect(self, event):
        self.key_v.SetValue(str(self.kmcs[self.key_c.GetSelection()][1]))


    def OnCancel(self, event):
        self.Destroy()

    def OnSave(self, event):
        if not self.key_c.GetValue():
            self.key_c.SetFocus()
            return
        self.kmc = self.kmcs[self.key_c.GetSelection()]
        self.Destroy()