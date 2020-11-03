import wx
from Control_id.config_premession import  Messages, UserInfo
from UI_notebook.MyCheckBox import MyCheckBox
from UI_notebook.MyListCtrl import MyListCtrl
from UI_notebook.ui_Dialog.ui_messageBox import showStatusMessage
from UI_notebook.ui_Dialog.ui_PanView import PanView
from tool.DateTime import getEffectDate
from wx.lib.agw import ultimatelistctrl as ULC

ID_VIEW_PAN = 10000

class ListCtrl(MyListCtrl):

    def __init__(self, parent, id=-1,data=None, size=(-1, -1)):
        super().__init__(parent, id, Messages.FAIL_FIELDS, size, style =
        wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|ULC.ULC_SINGLE_SEL)
        if data:
            self.data = data
            self.InitData()
        else:
            self.data = [["File1", "10000", "10000", "10000"],
                         ["File2", "10000", "10000", "10000"],
                         ["File3", "10000", "10000", "10000"],
                         ["File4", "10000", "10000", "10000"]]
            for data in self.data:
                item = self.Append(data)


    def InitData(self):
        self.data = [["File1", "10000", "10000", "10000"],
                     ["File2", "10000", "10000", "10000"],
                     ["File3", "10000", "10000", "10000"],
                     ["File4", "10000", "10000", "10000"]]
        for data in self.data:

            item = self.Append(data)
            self.SetPyData(item, data[1])
        # for k, v in self.data.items():
        #     fileName = k
        #     success = "0"
        #     fail = "0"
        #     if v:
        #         rincom = str(len(v))
        #     else:
        #         rincom = "10000"




class FileView(wx.Dialog):
    def __init__(self, parent, server):
        super(FileView, self).__init__(None, title='Add', size=(700, 500))
        self.parent = parent
        self.jobList = self.parent.jobList
        self.server = server

        self.InitUI()

    def InitUI(self):
        # self.SetSize((600, 600))
        panel = wx.Panel(self)
        # First create the controls
        self.listCtrl = ListCtrl(panel, data=self.jobList.GetPyData(self.jobList.currentItem), size=(600, -1))
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.listCtrl, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(mainSizer)
        self.listCtrl.Bind(wx.EVT_RIGHT_UP, self.OnShowPopup)


        self.Centre()
        self.createRightMenu()
        # mainSizer.SetSizeHints(self)
        # self.InitData()
        self.ShowModal()
        # self.Fit()

    def InitData(self):
        self.old_type = self.parent.dvc.GetValue(self.index, Messages.TABLE_FIELDS.get(Messages.USER_TYPE)[0])
        self.old_limit = self.parent.dvc.GetItemData(self.parent.dvc.RowToItem(self.index))
        self.type.SetValue(self.old_type)
        if self.old_type == Messages.WINDOWS_USER:
            self.date.Enable(False)
            self.date.SetSelection(self.date.GetCount()-1)
            self.changeADSA(False)
        for i in range(len(self.checkCtrl)):
            checkBox = self.checkCtrl[i]
            flag = self.old_limit >> (checkBox.bit - 1) & 1
            self.checkCtrl[i].SetValue(flag)

    def createRightMenu(self):
        '''
        右键菜单
        :return:
        '''
        self.popupmenu = wx.Menu()  # 创建一个菜单
        # bmp = setIcon(CID.imagePath+r"\nexterror.png")
        item = wx.MenuItem(self.popupmenu, ID_VIEW_PAN, 'PAN')
        # item.SetBitmap(bmp)
        self.Bind(wx.EVT_MENU, self.onViewPan, id=ID_VIEW_PAN)
        self.popupmenu.Append(item)


    def onViewPan(self, event):
        PanView(self, self.server)

    def OnShowPopup(self, event):  # 弹出显示
        # item = event.GetItem()
        # self.listCtrl.SetFocus()
        # self.listCtrl.currentItem = event.GetIndex()
        # self.listCtrl.Select(event.Index)
        # if item:
        self.PopupMenu(self.popupmenu)


    def OnCancel(self, event):
        self.Destroy()
