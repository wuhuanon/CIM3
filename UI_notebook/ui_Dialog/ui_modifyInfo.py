import wx

from Control_id.config_premession import Messages
from UI_notebook.ui_Dialog.ui_messageBox import showStatusMessage


class ModifyInfo(wx.Dialog):
    def __init__(self, parent, index, server):
        super(ModifyInfo, self).__init__(None, title='Modify', size=(400, 250))
        self.parent = parent
        self.index = index
        self.server = server
        self.old_phone = ""
        self.old_real = ""
        self.old_email = ""
        self.checkCtrl = []
        self.InitUI()

    def InitUI(self):
        # self.SetSize((600, 600))
        panel = wx.Panel(self)
        # First create the controls
        topLbl = wx.StaticText(panel, -1, "Modify Info")  # 1 创建窗口部件
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        nameLbl = wx.StaticText(panel, -1, "Real Name:")


        self.old_real = self.parent.dvc.GetValue(self.index, Messages.TABLE_FIELDS.get(Messages.REAL_NAME, [""])[0])
        self.real_name = wx.TextCtrl(panel, -1, self.old_real, size=(300, 25))


        phoneLbl = wx.StaticText(panel, -1, "Phone:")
        self.old_phone = self.parent.dvc.GetValue(self.index, Messages.TABLE_FIELDS.get(Messages.PHONE, [''])[0])
        self.phone = wx.TextCtrl(panel, -1, self.old_phone)
        emailLbl = wx.StaticText(panel, -1, "Email:")
        self.old_email = self.parent.dvc.GetValue(self.index, Messages.TABLE_FIELDS.get(Messages.EMAIL, [''])[0])
        self.email = wx.TextCtrl(panel, -1, self.old_email)
        
        saveBtn = wx.Button(panel, -1, "OK")
        cancelBtn = wx.Button(panel, -1, "Cancel")
        cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        saveBtn.Bind(wx.EVT_BUTTON, self.OnSave)
        # Now do the layout.
        # mainSizer is the top-level one that manages everything
        # 2 垂直的sizer
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topLbl, 0, wx.ALL, 5)
        mainSizer.Add(wx.StaticLine(panel), 0,
                      wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        # addrSizer is a grid that holds all of the address info
        # 3 地址列
        addrSizer = wx.GridBagSizer( hgap=5, vgap=5)
        # addrSizer.AddGrowableCol(1)
        addrSizer.Add(nameLbl, pos=(0, 0),
                      flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.real_name, pos=(0, 1), flag=wx.EXPAND|wx.ALL)
       
        # 4 带有空白空间的行
        # addrSizer.Add((10, 10))  # some empty space
        # addrSizer.Add(addr2, 0, wx.EXPAND)
        # addrSizer.Add(cstLbl, 0,
        #               wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        # the city, state, zip fields are in a sub-sizer
        # 5 水平嵌套
        # cstSizer = wx.BoxSizer(wx.HORIZONTAL)
        # cstSizer.Add(city, 1)
        # cstSizer.Add(state, 0, wx.LEFT | wx.RIGHT, 5)
        # cstSizer.Add(zip)
        # addrSizer.Add(cstSizer, 0, wx.EXPAND)
        # 6 电话和电子邮箱
        addrSizer.Add(phoneLbl, pos=(1, 0),
                      flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.phone, pos=(1, 1), flag=wx.EXPAND)
        addrSizer.Add(emailLbl, pos=(2, 0),
                      flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.email, pos=(2, 1), flag=wx.EXPAND)

      
        # now add the addrSizer to the mainSizer

       
        mainSizer.Add(addrSizer, 1, wx.EXPAND | wx.ALL, 10)
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
        name = self.real_name.GetValue()
        phone = self.phone.GetValue()
        email = self.email.GetValue()
        if name == self.old_real and phone == self.old_phone and self.old_email == email:
            self.Destroy()
        else:
            response = self.server.updateNormalUserInfo(real_name=name, phone=phone, email=email,
                                                        id=self.parent.dvc.datas[self.index]['id'])

            flag = showStatusMessage(response['status'], self.server)
            if flag == 1:
                self.parent.dvc.SetValue(name, self.index, Messages.TABLE_FIELDS.get(Messages.REAL_NAME, "")[0])
                self.parent.dvc.SetValue(phone, self.index, Messages.TABLE_FIELDS.get(Messages.PHONE, "")[0])
                self.parent.dvc.SetValue(email, self.index, Messages.TABLE_FIELDS.get(Messages.EMAIL, "")[0])
                self.Destroy()
            elif flag < 0:
                self.Destroy()
            


