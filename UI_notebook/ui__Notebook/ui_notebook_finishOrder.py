import threading

import wx
import wx.dataview as dv
import wx.lib.newevent
from pubsub import pub
from wx.lib.splitter import MultiSplitterWindow
import wx.lib.scrolledpanel as scrolled
from Control_id import ctrl_id as ID
from Control_id.config_premession import *
from UI_notebook.Base_Tree import BaseTreeList
from UI_notebook.MyListCtrl import MyListCtrl
from UI_notebook.ui_Dialog.ui_FileView import FileView
from UI_notebook.ui_Dialog.ui_addRepairJob import AddRepairJob
from UI_notebook.ui_Dialog.ui_configJob import ConfigJobDialog
from UI_notebook.ui_Dialog.ui_messageBox import showStatusMessage
from UI_notebook.ui_Dialog.ui_PanView import PanView

from UI_notebook.ui_Dialog.ui_modifyInfo import ModifyInfo
from UI_notebook.ui_Dialog.ui_ConfigKmc import ConfigKmc
from UI_notebook.ui__Notebook.ui_notebook_runningOrder import OrderTree
from UI_notebook.ui_permission import premessionPanel
from wx.lib.agw import ultimatelistctrl as ULC

ID_ITEM_START = 11000
ID_ITEM_INFO = 11001
ID_ITEM_REPAIR = 11002
ID_ITEM_DELETE = 11003
ID_ITEM_LOG = 11004


class JobList(MyListCtrl):
    def __init__(self, parent, id, size=(-1, -1)):
        super(JobList, self).__init__(parent, id, Messages.DELETE_JOB_FIELDS, size)
        PRELOADED = 30
        self.data = []
        self.data = self.server.CIM_EnumTerminatedJobInfo()
        reload = min(len(self.data), PRELOADED)
        for i in range(reload):
            job_info = self.server.CIM_QueryTerminatedJobInfo(self.data[i])
            info = [str(self.data[i]), str(job_info[0][1][0]), str(job_info[1]),
                              str(job_info[2]), str(job_info[3]), job_info[0][1][1]]
            self.data[i] = info
            # self.SetStringItem(pos, Messages.DELETE_JOB_FIELDS.get(Messages.TEMPLATE_INFO)[0], str(job_info[0][1][0][0]))
            # self.SetStringItem(pos, Messages.DELETE_JOB_FIELDS.get(Messages.TEMPLATE_INFO)[0], str(job_info[0][1][0][0]))
            # self.SetStringItem(pos, Messages.DELETE_JOB_FIELDS.get(Messages.ALL_COUNT)[0], str(job_info[1]))
            # self.SetStringItem(pos, Messages.DELETE_JOB_FIELDS.get(Messages.SUCCESS_COUNT)[0], str(job_info[2]))
            # self.SetStringItem(pos, Messages.DELETE_JOB_FIELDS.get(Messages.FAIL_COUNT)[0], str(job_info[3]))
            # self.SetStringItem(pos, Messages.DELETE_JOB_FIELDS.get(Messages.JOB_DES)[0], job_info[0][1][1])
        self.SetItemCount(len(self.data))

    def OnGetItemText(self, item, col):
        if type(self.data[item]) == int:
            job_info = self.server.CIM_QueryTerminatedJobInfo(self.data[item])
            info = [str(self.data[item]), str(job_info[0][1][0]), str(job_info[1]),
                                  str(job_info[2]), str(job_info[3]), job_info[0][1][1]]
            self.data[item] = info
        else:
            info = self.data[item]
        return info[col]

    def OnGetItemToolTip(self, item, col):
        return None
    def OnGetItemKind(self, item):
        # self.GetItem(item)
        return 0

    def OnGetItemTextColour(self, item, col):
        return wx.Colour(wx.BLACK)

    def addItem(self, job_id):
        self.data.append(int(job_id))
        self.SetItemCount(len(self.data))
ORDER_DEPTH = 2
FILE_DEPTH = 4


class FinishOrder(OrderTree):
    def __init__(self, parent, id):
        super(FinishOrder, self).__init__(parent, id)
    def InitData(self):
        orderList = self.server.CIM_EnumOrder()
        self.AddColumn("Name", width=400)
        self.AddColumn("Id", width=200)
        self.root = self.AddRoot("root")
        for order_id in orderList:
            self.AddOrederItem(order_id, True, False)
        # self.ExpandAll()
        self.Refresh()

    # def OnContextMenu(self, event):
    #     currentItem = self.GetSelection()
    #     ndepth = self.getItemDepth(currentItem)
    #     if ndepth == ORDER_DEPTH:
    #         self.createOrderMenu()
    def createFileMenu(self):
        pass


    def createOrderMenu(self):
        popupmenu = wx.Menu()  # 创建一个菜单
        # bmp = setIcon(CID.imagePath+r"\nexterror.png")
        item = wx.MenuItem(popupmenu, ID_ITEM_DELETE, 'Delete')
        # item.SetBitmap(bmp)
        self.Bind(wx.EVT_MENU, self.OnDelete, id=ID_ITEM_DELETE)
        popupmenu.Append(item)
        item = wx.MenuItem(popupmenu, ID_ITEM_LOG, 'Log')
        # item.SetBitmap(bmp)
        self.Bind(wx.EVT_MENU, self.OnLogOrder, id=ID_ITEM_LOG)
        popupmenu.Append(item)
        self.PopupMenu(popupmenu)

    def OnDelete(self, event):
        dlg = wx.MessageDialog(self, 'Are you delete?',
                               'Hint',
                               wx.YES_NO | wx.ICON_WARNING
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        if dlg.ShowModal() == wx.ID_YES:
            status = self.server.CIM_DelOrder(self.getOrderId())
            if status:
                pub.sendMessage("status", message=status)
            else:
                self.Delete(self.GetSelection())
        dlg.Destroy()


class FinishedOrderView(wx.Panel):
    def __init__(self, parent, server, id=-1, size=(-1, -1)):
        wx.Panel.__init__(self, parent, id=id, size=size)
        self.parent = parent
        self.server = server
        self.row = 0
        self.OrderTree = FinishOrder(self, -1)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.OrderTree, 1, wx.EXPAND)
        # sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(1)

    def OnInit(self):
        self.OrderTree.InitData()


