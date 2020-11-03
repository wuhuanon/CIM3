import wx
from wx.lib.scrolledpanel import ScrolledPanel
from Control_id.config_premession import  IninPer, Messages
from UI_notebook.MyCheckBox import MyCheckBox
from UI_notebook.ui_Dialog.ui_messageBox import showStatusMessage
from tool.DateTime import getEffectDate, GetNowDate
from Control_id import ctrl_id as ID

class AddWindow(wx.Dialog):
    def __init__(self, parent, server):
        super(AddWindow, self).__init__(None, title='Add', size=(635, 500))
        self.parent = parent
        self.checkCtrl = []
        self.server = server
        self.InitUI()

    def InitUI(self):
        # self.SetSize((600, 600))
        panel = wx.Panel(self)
        # First create the controls
        topLbl = wx.StaticText(panel, -1, "Add Windows User")  # 1 创建窗口部件
        topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        nameLbl = wx.StaticText(panel, -1, Messages.ADD_USER_NAME)
        self.name = wx.TextCtrl(panel, -1, "", size=(400, 25))
        realLbl = wx.StaticText(panel, -1, Messages.ADD_REAL_NAME)
        self.real = wx.TextCtrl(panel, -1, "")

        phoneLbl = wx.StaticText(panel, -1, Messages.ADD_PHONE)
        self.phone = wx.TextCtrl(panel, -1, "")
        emailLbl = wx.StaticText(panel, -1, Messages.ADD_EMAIL)
        self.email = wx.TextCtrl(panel, -1, "")
        # noteLbl = wx.StaticText(panel, -1, "Comment:")
        # note = wx.TextCtrl(panel, -1, "")

        roleLbl = wx.StaticText(panel, -1, Messages.ADD_ROLE)
        self.role = wx.ComboBox(panel, -1, "", choices=list(IninPer.keys()), style = wx.TE_READONLY)
        self.role.Bind(wx.EVT_TEXT, self.OnChange)
        saveBtn = wx.Button(panel, -1, "OK")
        cancelBtn = wx.Button(panel, -1, "Cancel")
        saveBtn.Bind(wx.EVT_BUTTON, self.OnSave)
        cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)

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
        addrSizer.Add(self.name, pos=(0, 1), flag=wx.EXPAND|wx.ALL)

        addrSizer.Add(realLbl, pos=(1, 0),
                      flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.real, pos=(1, 1), flag=wx.EXPAND)

        addrSizer.Add(phoneLbl, pos=(2, 0),
                      flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.phone, pos=(2, 1), flag=wx.EXPAND)
        addrSizer.Add(emailLbl, pos=(3, 0),
                      flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.email, pos=(3, 1), flag=wx.EXPAND)


        addrSizer.Add(roleLbl, pos=(4, 0),
                      flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        addrSizer.Add(self.role, pos=(4, 1), flag=wx.EXPAND)
        # now add the addrSizer to the mainSizer
        scroll_panel = ScrolledPanel(panel, -1, size=(600, 200))
        scroll_panel.SetupScrolling()
        staticBox = wx.StaticBox(scroll_panel, -1, "Permission")
        checkSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        box = wx.FlexGridSizer(0, 3, 3, 3)
        checkSizer.Add(box, 0, wx.EXPAND | wx.ALL, 10)
        for i in PerList.PERLIST:
            label = list(i.keys())[0]
            bit = i.get(label)
            if bit == Messages.KEY_LIMIT_BIT or bit == Messages.ADMIN_LIMIT_BIT:
                continue
            check = MyCheckBox(scroll_panel, label, i.get(label))
            box.Add(check, 1, wx.EXPAND | wx.ALL, 5)
            self.checkCtrl.append(check)
        # 7 添加Flex sizer
        scroll_panel.SetSizer(checkSizer)
        addrSizer.Add(scroll_panel, pos=(5, 0), span=(1, 2), flag=wx.EXPAND)
        mainSizer.Add(addrSizer, 1, wx.EXPAND | wx.ALL, 10)
       
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(saveBtn)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(cancelBtn)
        btnSizer.Add((20, 20), 1)
        mainSizer.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        panel.SetSizer(mainSizer)
      
        self.Centre()
        # mainSizer.SetSizeHints(self)
        self.ShowModal()
        self.Fit()

    def OnChange(self, event):
        premession = IninPer.get(self.role.GetValue(), 0)
        for i in range(len(self.checkCtrl)):
            checkBox = self.checkCtrl[i]
            flag = premession >> (checkBox.bit - 1) & 1
            self.checkCtrl[i].SetValue(flag)


    def OnCancel(self, event):
        self.Destroy()

    def OnSave(self, event):
        data = []
        name = self.name.GetValue()
        if not name:
            self.name.SetFocus()
            return 
        real = self.real.GetValue()
        phone = self.phone.GetValue()
        email = self.email.GetValue()

        limit = self.GetLimit()
        result = self.server.addWindowsUser(name=name, real_name=real, email=email, phone=phone, limit=limit)
        flag = showStatusMessage(result['status'], self.server)
        panel = wx.Window.FindWindowById(ID.ID_NOTEBOOK_RUNJOB)
        if flag == 1 and panel:
            data.insert(Messages.TABLE_FIELDS.get(Messages.ID)[0], str(panel.dvc.GetItemCount()+1))
            data.insert(Messages.TABLE_FIELDS.get(Messages.USER_NAME)[0], self.name.GetValue())
            data.insert(Messages.TABLE_FIELDS.get(Messages.REAL_NAME)[0], self.real.GetValue())
            data.insert(Messages.TABLE_FIELDS.get(Messages.USER_TYPE)[0], Messages.WINDOWS_USER)
            data.insert(Messages.TABLE_FIELDS.get(Messages.STATUS)[0], Messages.STATUS_NORMAL)
            data.insert(Messages.TABLE_FIELDS.get(Messages.PHONE)[0], self.phone.GetValue())
            data.insert(Messages.TABLE_FIELDS.get(Messages.EMAIL)[0], self.email.GetValue())

            data.insert(Messages.TABLE_FIELDS.get(Messages.VALID_DATE)[0], getEffectDate(years=100))
            data.insert(Messages.TABLE_FIELDS.get(Messages.CREATE_DATE)[0], GetNowDate())
            limit = self.GetLimit()

            role = "Other"
            data.insert(Messages.TABLE_FIELDS.get(Messages.ROLE)[0], role)
            panel.dvc.AppendItem(data, limit)
            self.Destroy()
        elif flag < 0:
            self.Destroy()
        else:
            pass

    def GetLimit(self):
        limit = 0
        for i in self.checkCtrl:
            if i.IsChecked():
                bit = i.bit
                limit = limit | 1 << (bit - 1)
        return limit

if __name__ == "__main__":
    import random
    # help(random.randrange)
    import binascii
    import donna25519 as curve25519

    bobs_private = curve25519.PrivateKey()
    bobs_public = bobs_private.get_public()
    print("BOb's Private Key:", binascii.hexlify(bobs_private.private))
    print("BOb's Public Key:", binascii.hexlify(bobs_public.public))

    Alis_private = curve25519.PrivateKey()
    Alis_public = Alis_private.get_public()
    print("Alis's Private Key:", binascii.hexlify(Alis_private.private))
    print("Alis's Public Key:", binascii.hexlify(Alis_public.public))

    # Alis pub --> bob
    bobs_sharekey = bobs_private.do_exchange(Alis_public)
    # Bobs pub -->Alis
    alis_sharekey = Alis_private.do_exchange(bobs_public)

    print("Bob's Share Key:", binascii.hexlify(bobs_sharekey))
    print("Alis's Share Key:", binascii.hexlify(alis_sharekey))