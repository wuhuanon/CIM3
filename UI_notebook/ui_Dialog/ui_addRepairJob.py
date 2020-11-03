import wx
from wx.lib.scrolledpanel import ScrolledPanel
from Control_id.config_premession import Messages, UserInfo
from UI_notebook.MyCheckBox import MyCheckBox
from UI_notebook.MyListCtrl import MyListCtrl
from UI_notebook.MyValidate import DigitsValidator
from UI_notebook.ui_Dialog.ui_messageBox import showStatusMessage
from Control_id import ctrl_id as ID
from wx.lib.agw import ultimatelistctrl as ULC

SELECT_BUT = 1001
DESELECT_BUT = 1002

class PanRepairList(MyListCtrl):
    def __init__(self, parent, id, size=(-1, -1)):
        super(PanRepairList, self).__init__(parent,id, Messages.PAN_PEPAIR_FIELDS, size)
        # self.SetSecondGradientColour('red')
        self.parent = parent
        self.realData = []
        for i in range(20000):
            self.realData.append([str(i), 'machine%d'% i, "success", "2020-01-01", 'User1', False])
        self.data = self.realData
        self.SetItemCount(len(self.data))
        # self.Append(data)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.attr1 = ULC.UltimateListItemAttr(font=font)
        # self.attr1.SetTextColour(wx.RED)
        self.attr2 = ULC.UltimateListItemAttr(font=font)
        # self.attr1.SetTextColour(wx.GREEN)
        # self.attr1.SetBackgroundColour(wx.Colour(180,180,180))
        # self.attr1.Enable(False)
        info = self.GetColumn(0)
        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT | ULC.ULC_MASK_CHECK
        info._kind = 1
        info.Check(False)
        self.titflag = False
        self.SetColumn(0, info)
        self.Bind(ULC.EVT_LIST_ITEM_CHECKED, self.onCheck)
        self.Bind(ULC.EVT_LIST_COL_CHECKING, self.onCheckTitle)

    def onCheck(self, event):
        item = event.GetItem()
        if item.IsChecked():
            self.data[self.currentItem][-1] = True
        else:
            self.data[self.currentItem][-1] = False

        self.changeColCheck()

    def GetFlag(self):
        for i in self.data:
            if not i[-1]:
                return False
        return True


    def onCheckTitle(self, event):
        self.titflag = not self.titflag
        def changeSelect(data):
            data[-1] = self.titflag
            return data
        if self.titflag:
            self.data = list(map(changeSelect, self.data))
        else:
            self.data = list(map(changeSelect, self.data))

    def changeColCheck(self):
        flag = self.GetFlag()
        self.titflag = flag
        info = self.GetColumn(0)
        info.Check(flag)
        self.SetColumn(0, info)

    def searchItem(self, pan):
        search = []
        for i in self.realData:
            if pan in i[0]:
                search.append(i)
        if len(search) == 0 and pan:
            dlg = wx.MessageDialog(self.parent, "Noting Find",
                                   "Search",
                                   wx.OK | wx.ICON_INFORMATION
                                   # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                   )
            dlg.ShowModal()
            dlg.Destroy()
            self.data = self.realData
        else:
            self.data = search
        self.SetItemCount(len(self.data))
        self.Refresh()

    def OnGetItemText(self, item, col):
        return self.data[item][col]

    def OnGetItemTextColour(self, item, col):
        text = self.data[item][col]
        if col == Messages.PAN_PEPAIR_FIELDS.get(Messages.PAN_STATUS)[0]:
            if text == "success":
                return wx.Colour(wx.GREEN)
            elif text == 'fail':
                return wx.Colour(wx.RED)
        else:
            return None

    def OnGetItemToolTip(self, item, col):
        return None



    # def OnGetItemColumnImage(self, item, column):
    #
    #     return self.randomLists[item%5]


    # def OnGetItemImage(self, item):
    #
    #     return self.randomLists[item%5]


    def OnGetItemAttr(self, item):

        return self.attr1
        # if item % 3 == 1:
        #     return self.attr1
        # elif item % 3 == 2:
        #     return self.attr2
        # else:
        #     return None


    # def OnGetItemColumnCheck(self, item, column):
    #
    #     if item%3 == 0:
    #         return True
    #
    #     return False


    def OnGetItemCheck(self, item):

        return self.data[item][-1]



    # def OnGetItemColumnKind(self, item, column):
    #
    #     if item%3 == 0:
    #         return 2
    #     elif item%3 == 1:
    #         return 1
    #
    #     return 0
    def OnGetItemKind(self, item):
        # self.GetItem(item)
        return 1


class AddRepairJob(wx.Dialog):
    def __init__(self, parent, server):
        super(AddRepairJob, self).__init__(None, title='Add', size=(750, 600), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.parent = parent
        self.server = server
        self.InitUI()

    def InitUI(self):
        # self.SetSize((600, 600))
        panel = wx.Panel(self)
        # First create the controls
        line = wx.StaticText(panel, -1, "——")
        # topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))


        # nameLbl = wx.StaticText(panel, -1, "PAN")
        self.listCtrl = PanRepairList(panel, -1, size=(700, 550))
        dataLen = len(self.listCtrl.data)
        startList = [str(x*1000) for x in range(dataLen//1000)]
        self.startSelect = wx.ComboBox(panel, -1, "1",size=(65, 25), choices=startList, validator=DigitsValidator())
        self.endSelect = wx.ComboBox(panel, -1, "",size=(65, 25), choices=[], validator=DigitsValidator())
        selectBut = wx.Button(panel, SELECT_BUT, 'Select')
        selectBut.Bind(wx.EVT_BUTTON, self.onSelect)
        deselectBut = wx.Button(panel, DESELECT_BUT, 'DeSelect')
        deselectBut.Bind(wx.EVT_BUTTON, self.onSelect)
        pan_l = wx.StaticText(panel, -1, "PAN:")
        self.search = wx.SearchCtrl(panel, -1)
        searchBtu = wx.Button(panel, -1, 'Search')
        searchBtu.Bind(wx.EVT_BUTTON, self.onSearch)
        saveBtn = wx.Button(panel, -1, "OK")
        cancelBtn = wx.Button(panel, -1, "Cancel")
        saveBtn.Bind(wx.EVT_BUTTON, self.OnSave)
        cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        toolSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(toolSizer, 0, wx.ALL | wx.EXPAND, 5)
        toolSizer.Add(self.startSelect, 0, wx.ALL, 5)
        toolSizer.Add(line, 0, wx.TOP | wx.BOTTOM, 5)
        toolSizer.Add(self.endSelect, 0, wx.ALL, 5)
        toolSizer.Add(selectBut, 0, wx.ALL, 5)
        toolSizer.Add(deselectBut, 0, wx.ALL, 5)
        toolSizer.Add((20, 20), 1)
        toolSizer.Add(pan_l, 0, wx.ALL, 5)
        toolSizer.Add(self.search, 0, wx.ALL, 5)
        toolSizer.Add(searchBtu, 0, wx.ALL, 5)

        mainSizer.Add(self.listCtrl, 1, wx.EXPAND | wx.ALL, 10)
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

        self.Centre()
        # mainSizer.SetSizeHints(self)
        self.ShowModal()


    def onSearch(self, event):
        text = self.search.GetValue()
        self.listCtrl.searchItem(text)
            
    def OnCancel(self, event):
        self.Destroy()

    def onSelect(self, event):

        start = self.startSelect.GetValue()
        if not start:
            self.startSelect.SetFocus()
            return
        start = int(start)
        end = self.endSelect.GetValue()
        if not end:
            self.endSelect.SetFocus()
            return
        end = int(end)

        for i in range(start-1, end+1):
            if event.GetId() == SELECT_BUT:
                self.listCtrl.data[i][-1] = True
            else:
                self.listCtrl.data[i][-1] = False
        self.listCtrl.changeColCheck()
        self.listCtrl.Refresh()

    def OnSave(self, event):
        data = []
        def getSelect(data):
            return data[-1] == True
        # result = self.server.addLocalUser(name=name, real_name=real, email=email, phone=phone,lock_status=status,
        #                                   effect_day=effect, limit = limit)
        # flag = showStatusMessage(result['status'], self.server)
        # if flag == 1:
        #     dlg = wx.TextEntryDialog(self, "Your pin is", value=result['data']['pin'],
        #                              style=wx.OK)
        #     dlg.ShowModal()
        #     dlg.Destroy()
        #
        #
        #     self.Destroy()
        # elif flag < 0:
        #     self.Destroy()
        # else:
        #     pass
