import random
import string
import time
import copy

import wx
from pubsub import pub

from Control_id.config_premession import *
from UI_notebook.MyCheckBox import MyCheckBox
from UI_notebook.MyListCtrl import MyListCtrl
from UI_notebook.MyValidate import DigitsValidator
from UI_notebook.ui_Dialog.ui_messageBox import showStatusMessage
from Control_id import ctrl_id as ID
from wx.lib.agw import ultimatelistctrl as ULC
# import threading
from UI_notebook.ui_Dialog.ui_panRecordInfo import PanRecordInfo
from instruct_parse.ClientServerInterface import ClientServerInterface

SELECT_BUT = 1001
DESELECT_BUT = 1002

NOT_CHECK_ALL = 0
CHECK_ALL = 1
SOME_CHECK = 2

TITLE_COL_UNSELECT = 0
TITLE_COL_SELECT = 1


MENU_ITEM_JOB = 12000
MENU_ITEM_COPY = 12001
class AddPanList(MyListCtrl):
    def __init__(self, parent, id, check , order_id, file_id, data, job_type, size=(-1, -1)):
        super(AddPanList, self).__init__(parent, id, Messages.PAN_ADD_FIELDS, size)
        # self.SetSecondGradientColour('red')
        self.parent = parent
        self.job_type = job_type
        self.order_id = order_id
        self.realData = copy.deepcopy(data)
        if not self.realData:
            self.realData = []
            self.dic = {}
            file_info = self.server.CIM_QueryOrderDataFileInfo(order_id, file_id)
            if file_info:
                file_pans = self.server.CIM_QueryOrderDataFilePAN(order_id, file_id, 0, file_info[1])
                file_id_list = list(map(lambda x: x[0], file_pans))
                len_pans = len(file_pans)
                for i in range(len_pans):

                    l = [file_id_list[i], str(i), str(file_pans[i][1]), None, None, check]
                    self.realData.append(l)
                self.dic = dict(zip(file_id_list, self.realData))
            # if check:
            #     for i in self.realData:
            #         i[3] = True
        else:
            self.dic = dict(zip([i[0] for i in self.realData], self.realData))
            if check == CHECK_ALL or check == NOT_CHECK_ALL:
                for i in self.realData:
                    i[-1] = check
        self.data = self.realData
        self.SetItemCount(len(self.data))
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
        if check != CHECK_ALL:
            info.Check(0)
        else:
            info.Check(1)
        self.titflag = True
        if check == NOT_CHECK_ALL or check == SOME_CHECK:
            self.titflag = False
        self.SetColumn(0, info)
        self.Bind(ULC.EVT_LIST_ITEM_CHECKED, self.onCheck)
        self.Bind(ULC.EVT_LIST_COL_CHECKING, self.onCheckTitle)
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)
        self.createRightMenu()

    def OnShowPopup(self, event):
        self.PopupMenu(self.popupmenu)

    def createRightMenu(self):
        self.popupmenu = wx.Menu()  # 创建一个菜单
        item = wx.MenuItem(self.popupmenu,MENU_ITEM_JOB, 'Job Record')
        self.Bind(wx.EVT_MENU, self.JobRecord, id=MENU_ITEM_JOB)
        self.popupmenu.Append(item)

        item = wx.MenuItem(self.popupmenu, MENU_ITEM_COPY, 'Copy Pan')
        self.Bind(wx.EVT_MENU, self.CopyPan, id=MENU_ITEM_COPY)
        self.popupmenu.Append(item)

    def JobRecord(self, event):

        PanRecordInfo(self, self.realData[self.currentItem][0], self.realData[self.currentItem][2], self.order_id)

    def CopyPan(self, event):
        self.do = wx.TextDataObject()
        self.do.SetText(self.realData[self.currentItem][2])
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(self.do)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Unable to open the clipboard", "Error")

    def onCheck(self, event):
        item = event.GetItem()
        if item.IsChecked() and item.IsEnabled():
            self.data[self.currentItem][-1] = True
        else:
            self.data[self.currentItem][-1] = False

        self.changeColCheck()

    def InitData(self):
        # lst1 = filter(lambda x: x[3] is None, self.realData)
        # lst2 = [i[0] for i in lst1]
        # active_records = self.server.QueryRecordCountInActiveJob(lst2)
        # terminat_records = self.server.QueryLogCountInTerminatedJob(lst2)
        # for i in range(len(lst2)):
        #     self.dic[lst2[i]][3] = str(active_records[i])
        #     self.dic[lst2[i]][4] = str(terminat_records[i])
        # result = []
        # for i in range(len(self.realData)):
        #     if self.GetItemEnable(i) and self.realData[i][-1]:
        #         result.append(self.realData[i])
        return self.realData

    def GetFlag(self):
        for i in range(len(self.data)):
            if not self.GetItemEnable(i, False):
                continue
            if not self.data[i][-1]:
                return False
        return True

    def onChecked(self, item, check):

        if self.GetItemEnable(item, False):
            self.data[item][-1] = check
        else:
            self.data[item][-1] = False




    def onCheckTitle(self, event):
        self.titflag = not self.titflag

        def changeSelect(data):
            # if data[-1]:
            data[-1] = self.titflag
            # else:
            #     data[-1] = False
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
            if pan in i[2]:
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
        if self.data[item][3] is None:
            pan_id = self.data[item][0]
            active_records = self.server.QueryRecordExistInActiveJob(self.order_id, [pan_id])
            self.data[item][3] = str(active_records[0])
            terminat_records = self.server.QueryLogExistInFinishedJob(self.order_id, [pan_id])
            self.data[item][4] = str(terminat_records[0])

        return str(self.data[item][col+1])

    def OnGetItemTextColour(self, item, col):
        # text = self.data[item][col]
        if self.GetItemEnable(item, False):

            return wx.Colour(wx.GREEN)

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

    def GetItemEnable(self, item, data_flag=True):
        if self.data[item][3] is None and data_flag:
            pan_id = self.data[item][0]
            active_records = self.server.QueryRecordCountInActiveJob([pan_id])
            self.data[item][3] = str(active_records[0] if active_records else "")
            terminat_records = self.server.QueryLogCountInTerminatedJob([pan_id])
            self.data[item][4] = str(terminat_records[0] if terminat_records else "")
        if self.job_type == TASK_TYPE_COMMON:
            return (self.data[item][3] == "0" and self.data[item][4] == "0") or self.data[item][3] is None
        else:
            return (self.data[item][3] == "0" and self.data[item][4]) or self.data[item][3] is None

    def OnGetItemAttr(self, item):
        # if self.job_type == TASK_COMMON
        # if not self.data[item][-1]:
        #     self.attr1.Enable(False)
        # else:
        #     self.attr1.Enable(True)
        # return self.attr1
        self.attr1.Enable(self.GetItemEnable(item))

        # if self.job_type == TASK_TYPE_COMMON:
        #     self.attr1.Enable(self.data[item][1] == "0" and self.data[item][2] == "0")
        # else:
        #     self.attr1.Enable(self.data[item][1] != "0")
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

        if self.GetItemEnable(item):
            return self.data[item][-1]
        return False

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


class AddPan(wx.Dialog):
    def __init__(self, parent, check_flag, file_id, data):
        super(AddPan, self).__init__(None, title='Add', size=(750, 600),
                                     style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        # self.server = ClientServerInterface(1)
        self.listData = data
        self.data = []
        self.parent = parent
        self.file_id = file_id
        self.check_flag = check_flag
        self.InitUI()

    def InitUI(self):
        # self.SetSize((600, 600))
        panel = wx.Panel(self)
        # First create the controls
        line = wx.StaticText(panel, -1, "——")
        # topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

        # nameLbl = wx.StaticText(panel, -1, "PAN")
        self.listCtrl = AddPanList(panel, -1, self.check_flag,self.parent.order_id, self.file_id, self.listData, self.parent.parent.GetJobType(), size=(700, 550))
        dataLen = len(self.listCtrl.data)
        startList = [str(x * 1000) for x in range(dataLen // 1000)]
        self.startSelect = wx.ComboBox(panel, -1, "1", size=(65, 25), choices=startList, validator=DigitsValidator())
        self.endSelect = wx.ComboBox(panel, -1, "", size=(65, 25), choices=[], validator=DigitsValidator())
        self.startSelect.Bind(wx.EVT_TEXT, self.OnModify)
        self.endSelect.Bind(wx.EVT_TEXT, self.OnModify)
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
        data = self.listData
        self.data = data
        if data:
            flag = self.listCtrl.titflag
            try:
                filter(lambda x: x[-1], self.data).__next__()
                flag2 = True
            except StopIteration:
                flag2 = False
            if not flag and flag2:
                self.check_flag = 2
            elif flag:
                self.check_flag = 1
            else:
                self.check_flag = 0
        self.Destroy()

    def OnModify(self, event):

        start = self.startSelect.GetValue()
        end = self.endSelect.GetValue()
        if not end:
            self.endSelect.SetBackgroundColour("white")
            return

        if end < start:
            self.endSelect.SetBackgroundColour((255, 124, 128))
        else:
            self.endSelect.SetBackgroundColour("white")
        self.startSelect.Refresh()
        self.endSelect.Refresh()

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
        if end < start:
            self.endSelect.SetFocus()
            return
        for i in range(start - 1, end + 1):
            if event.GetId() == SELECT_BUT:
                self.listCtrl.onChecked(i, True)
            else:
                self.listCtrl.onChecked(i, False)
        self.listCtrl.changeColCheck()
        self.listCtrl.Refresh()

    def OnSave(self, event):
        data = self.listCtrl.InitData()

        self.data = data
        flag = self.listCtrl.titflag
        try:
            filter(lambda x:x[-1], self.data).__next__()
            flag2 = True
        except StopIteration:
            flag2 = False
        if not flag and flag2:
            self.check_flag = 2
        elif flag:
            self.check_flag = 1
        else:
            self.check_flag = 0
        self.Destroy()
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
