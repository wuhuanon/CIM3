import time

import wx

from Control_id.config_premession import Messages, UserInfo
from UI_notebook.MyListCtrl import MyListCtrl
from UI_notebook.ui_Dialog.ui_messageBox import showStatusMessage
from wx.lib.agw import ultimatelistctrl as ULC


STATUS_SUCCESS = "Success"
STATUS_FAIL = "Fail"

class PanViewList(MyListCtrl):
    def __init__(self, parent, id, dataDict, size=(-1, -1)):
        super(PanViewList, self).__init__(parent,id, Messages.PAN_VIEW_FIELDS, size)
        # self.SetSecondGradientColour('red')
        self.parent = parent
        self.order_id = dataDict.get("order_id", 0)
        self.job_id = dataDict.get("job_id", 0)

        def initData(x):
            listData = list(x)
            listData.append(" ")
            listData[3] = self.GetPanStatus(listData[3])
            if listData[4].tm_year == 1970:
                listData[4] = " "
            else:
                listData[4] = time.strftime("%Y-%m-%d %H:%M:%S", listData[4])
            return listData
        if not dataDict :
            self.realData = []
            for i in range(200000):
                self.realData.append([str(i+1), 'machine%d'% i,"success", "2020-01-01", 'User1'])
        else:
            data = dataDict.get("data", [])
            datas = map(initData, data)
            self.realData = list(datas)
        self.data = self.realData
        self.SetItemCount(len(self.data))
        # self.Append(data)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.attr1 = ULC.UltimateListItemAttr(font=font)
        # self.attr1.SetTextColour(wx.RED)
        self.Bind(ULC.EVT_LIST_COL_CLICK, self.OnTest)

    def OnTest(self, event):
        print(event.GetColumn())

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
        # print(self.data)
        if type(self.data[item][col]) != str:
            if col == 1:

                self.data[item][col] = self.server.CIM_QueryOrderDataFileInfo(self.order_id, self.data[item][col])[0]
            elif col == 2:

                self.data[item][col] = self.server.CIM_QueryMachine(self.data[item][col])[0]
            elif col == 3:

                self.data[item][col] = self.GetPanStatus(self.data[item][col])
            elif col == 4:
                self.data[item][col] = time.strftime("%Y-%m-%d %H:%M:%S", self.data[item][col])
        return self.data[item][col]

    @staticmethod
    def GetPanStatus(status):
        if status == 0:
            return " "
        elif status & 0x40000000:
            if status == 0x40000000:
                return STATUS_SUCCESS
            else:
                return STATUS_FAIL
        return " "

    def OnGetItemTextColour(self, item, col):
        # self.SetItemBackgroundColour
        text = self.data[item][col]
        if col == Messages.PAN_VIEW_FIELDS.get(Messages.PAN_STATUS)[0]:
            if text == STATUS_SUCCESS:
                return wx.Colour(wx.GREEN)
            elif text == STATUS_FAIL:
                return wx.Colour(wx.RED)
        else:
            return None

    def OnGetItemToolTip(self, item, col):
        return None



    def OnGetItemAttr(self, item):

        return self.attr1





    def OnGetItemKind(self, item):
        # self.GetItem(item)
        return 0

class PanView(wx.Dialog):
    def __init__(self, parent, server, data, ):
        super(PanView, self).__init__(None, title='Pan', size=(1200, 600))
        self.parent = parent
        self.checkCtrl = []
        self.soAdmin = []
        self.server = server
        self.data = data
        self.InitUI()

    def InitUI(self):
        # self.SetSize((600, 600))
        panel = wx.Panel(self)
        # First create the controls


        # saveBtn = wx.Button(panel, -1, "OK")
        # cancelBtn = wx.Button(panel, -1, "Cancel")
        # cancelBtn.Bind(wx.EVT_BUTTON, self.OnCancel)
        # saveBtn.Bind(wx.EVT_BUTTON, self.OnSave)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.listCtrl = PanViewList(panel, -1,self.data, size=(1150, 550))


        mainSizer.Add(self.listCtrl, 1, wx.EXPAND | wx.ALL, 10)
        # The buttons sizer will put them in a row with resizeable
        # gaps between and on either side of the buttons
        # 8 按钮行
        # btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        # btnSizer.Add((20, 20), 1)
        # # btnSizer.Add(saveBtn)
        # btnSizer.Add((20, 20), 1)
        # btnSizer.Add(cancelBtn)
        # btnSizer.Add((20, 20), 1)
        # mainSizer.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        panel.SetSizer(mainSizer)

        self.Centre()
        # mainSizer.SetSizeHints(self)
        # self.InitData()
        self.ShowModal()
        # self.Fit()

    def InitData(self):
        self.old_limit = self.parent.dvc.GetItemData(self.parent.dvc.RowToItem(self.index))
        for i in range(len(self.checkCtrl)):
            checkBox = self.checkCtrl[i]
            flag = self.old_limit >> (checkBox.bit - 1) & 1
            self.checkCtrl[i].SetValue(flag)

    def OnCheck(self, event):
        for i in self.soAdmin:
            if event.GetEventObject() != i:
                if event.IsChecked():
                    i.SetValue(0)
                #     i.Enable(False)
                # else:
                #     i.Enable(True)



    def OnCancel(self, event):
        self.Destroy()

    def OnSave(self, event):
        pass

    def GetLimit(self):
        limit = 0
        for i in self.checkCtrl:
            if i.IsChecked():
                bit = i.bit
                limit = limit | 1 << (bit - 1)
        return limit