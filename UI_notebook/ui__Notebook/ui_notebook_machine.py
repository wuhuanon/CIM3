import wx
import wx.dataview as dv
import wx.lib.newevent
from pubsub import pub
from wx.lib.splitter import MultiSplitterWindow
import wx.lib.scrolledpanel as scrolled
from Control_id import ctrl_id as ID
from Control_id.config_premession import *
from UI_notebook.MyListCtrl import MyListCtrl
from UI_notebook.ui_Dialog.ui_FileView import FileView
from UI_notebook.ui_Dialog.ui_addMachine import AddMachine
from wx.lib.agw import ultimatelistctrl as ULC

ID_ITEM_MODIFY = 20000
ID_ITEM_DELETE = 20001

class MachineList(MyListCtrl):
    def __init__(self, parent, id, size=(-1, -1)):
        super(MachineList, self).__init__(parent, id, Messages.MACHINE_FIELDS, size, style =
        wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|ULC.ULC_SINGLE_SEL |  ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)

    def InitData(self):
        machine_list = self.server.CIM_EnumMachine()
        for machine_id in machine_list:
            machine_info = self.server.CIM_QueryMachine(machine_id)
            if machine_info:
                pos = self.GetItemCount()
                if machine_info[-2] > 0:
                    self.InsertStringItem(pos, str(machine_id))
                    self.SetStringItem(pos, Messages.MACHINE_FIELDS.get(Messages.MACHINE_NAME)[0], str(machine_info[0]))
                    self.SetStringItem(pos, Messages.MACHINE_FIELDS.get(Messages.MACHINE_IP)[0], str(machine_info[1]))
                    self.SetStringItem(pos, Messages.MACHINE_FIELDS.get(Messages.MACHINE_ABOUT)[0], str(machine_info[3]))
    def addItem(self, data):
        pos = self.GetItemCount()
        self.InsertStringItem(pos, data[0])
        for i in range(1, len(data)):
            index = self.SetStringItem(pos, i, str(data[i]))
        self.Refresh()
        return pos



class MachineView(wx.Panel):
    def __init__(self, parent, server, id=-1, model=None, size=(-1, -1)):
        wx.Panel.__init__(self, parent, id=id, size=size)
        self.parent = parent
        self.server = server
        self.row = 0
        self.machineList = MachineList(self, -1, size=(1000, -1))
        selectBut = wx.Button(self, -1, 'Add')
        selectBut.Bind(wx.EVT_BUTTON, self.OnAdd)
        sizer = wx.BoxSizer(wx.VERTICAL)
        toolSizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(toolSizer, 0, wx.ALL | wx.EXPAND, 5)
        toolSizer.Add(selectBut, 0, wx.ALL, 5)
        toolSizer.Add((20, 20), 1)

        # toolSizer.Add(self.search, 0, wx.ALL, 5)
        # toolSizer.Add(searchBtu, 0, wx.ALL, 5)

        sizer.Add(self.machineList, 1, wx.EXPAND)
        # sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)


        self.machineList.Bind(wx.EVT_RIGHT_UP, self.OnShowPopup)
        self.SetAutoLayout(1)
        # self.SetupScrolling()
        self.createRightMenu()

    def OnInit(self):

        self.machineList.DeleteAllItems()
        self.machineList.InitData()

    def OnAdd(self, event):
        AddMachine(self, self.server)

    def OnSearch(self, event):
        text = self.search.GetValue()
        self.machineList.searchItem(text)


    def createRightMenu(self):
        '''
        右键菜单
        :return:
        '''
        self.popupmenu = wx.Menu()  # 创建一个菜单
        # bmp = setIcon(CID.imagePath+r"\nexterror.png")
        item = wx.MenuItem(self.popupmenu, ID_ITEM_MODIFY, 'Modify')
        # item.SetBitmap(bmp)
        self.parent.Bind(wx.EVT_MENU, self.OnModify, id=ID_ITEM_MODIFY)
        self.popupmenu.Append(item)


        item = wx.MenuItem(self.popupmenu, ID_ITEM_DELETE, 'Delete')
        # # item.SetBitmap(bmp)
        self.parent.Bind(wx.EVT_MENU, self.delete, id=ID_ITEM_DELETE)
        self.popupmenu.Append(item)

    def OnShowPopup(self, event):
        # item = event.GetItem()
        self.machineList.SetFocus()
        self.machineList.currentItem = self.machineList.GetFirstSelected()
        self.parent.PopupMenu(self.popupmenu)

    def OnModify(self, event):
        # ModifyMachine(self, self.server)
        dlg = wx.TextEntryDialog(self, "Please enter device  description", "Modify",
                                 self.machineList.getColumnText(self.machineList.currentItem,
                                                                Messages.MACHINE_FIELDS.get(Messages.MACHINE_ABOUT)[0]))
        dlg.SetMaxLength(254)
        if dlg.ShowModal() == wx.ID_OK:
            status = self.server.CIM_UpdateMachine(int(self.machineList.getColumnText(self.machineList.currentItem,
                                                                                      Messages.MACHINE_FIELDS.get(Messages.MACHINE_ID)[0])),
                                                   self.machineList.getColumnText(self.machineList.currentItem,
                                                                                  Messages.MACHINE_FIELDS.get(Messages.MACHINE_ABOUT)[0]))
            if not status:
                self.machineList.setColumnText(self.machineList.currentItem,
                                               Messages.MACHINE_FIELDS.get(Messages.MACHINE_ABOUT)[0], dlg.GetValue())
                self.machineList.Refresh()
            else:
                pub.sendMessage("status", message=status)
    def onInfo(self, event):
        FileView(self, self.server)



    def delete(self, event):
        dlg = wx.MessageDialog(self, 'Are you delete?',
                               'Hint',
                               wx.YES_NO | wx.ICON_WARNING
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        if dlg.ShowModal() == wx.ID_YES:
            status = self.server.CIM_DelMachine(int(self.machineList.getColumnText(self.machineList.currentItem,
                                                                                   Messages.MACHINE_FIELDS.get(Messages.MACHINE_ID)[0])))
            if not status:
                self.machineList.DeleteItem(self.machineList.currentItem)
            else:
                pub.sendMessage("status", message=status)
        dlg.Destroy()
