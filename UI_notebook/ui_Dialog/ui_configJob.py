import wx
import re

from Control_id.config_premession import *
from UI_notebook.ui_Dialog.ui_Login import LoginDialog
from UI_notebook.ui_Dialog.ui_messageBox import showStatusMessage
from pubsub import pub
from Control_id import ctrl_id as ID
from UI_notebook.ui_Dialog.ui_ConfigKmc import ConfigKmc

about_txt = """\
Login"""


class ConfigJobDialog(wx.Dialog):
    def __init__(self,parent, Title="", size=(350, 200)):
        wx.Dialog.__init__(self, parent, ID.ID_CONFIG_JOB, Title, size=size)
        self.parent = parent
        self.server = parent.server
        self.flag = False
        self.jobList = parent
        # Create the text controls
        self.InitUi()

    def InitUi(self):

        machine_l  = wx.StaticText(self, -1, "Machine:")

        key_l = wx.StaticText(self, -1, "Key")
        # confirm_pin_l = wx.StaticText(self, -1, "*Confirm Pin:")

        self.itemData = self.jobList.GetPyData(self.jobList.currentItem)
        self.machineID = self.itemData.get(DEV_ID, 0)
        kmc_info = self.itemData[KMC_INFO]
        self.kmc = kmc_info
        self.bank_name = self.itemData[KEY_INFO][0]
        self.decList = [0]
        self.decList.extend(self.server.CIM_EnumMachine())
        machines = map(lambda devId: (self.server.CIM_QueryMachine(devId), devId), self.decList)

        machines = filter(lambda x: x[0][-2] >= 0, machines)
        self.machines = [(i[0][0], i[1]) for i in machines]
        self.machine_c  = wx.ComboBox(self, -1, "", choices=[i[0] for i in self.machines], style=wx.TE_READONLY)
        for i in range(len(self.machines)):
            dev = self.machines[i]
            if self.machineID == dev[-1]:
                self.machine_c.SetSelection(i)

        self.key_b = wx.Button(self, -1, "Replace Key")
        self.Bind(wx.EVT_BUTTON, self.onKey, self.key_b)
        okay = wx.Button(self, -1, "Ok", size=(80, 30))
        okay.SetDefault()
        okay.Bind(wx.EVT_BUTTON, self.onOkay)
        cancel = wx.Button(self, -1, "Cancel",  size=(80, 30))
        cancel.Bind(wx.EVT_BUTTON, self.OnCanel)

        # Layout with sizers
        sizer = wx.BoxSizer(wx.VERTICAL)

        fgs = wx.FlexGridSizer(0, 2, 10, 10)
        fgs.Add(machine_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.machine_c, 0, wx.EXPAND)
        fgs.Add(key_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.key_b, 0, wx.ALL)
        # fgs.Add(confirm_pin_l, 0, wx.ALIGN_RIGHT)
        # fgs.Add(self.con_pin_t, 0, wx.EXPAND)
        fgs.AddGrowableCol(1)
        sizer.Add(fgs, 0, wx.EXPAND | wx.ALL, 20)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(okay)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(cancel)
        btnSizer.Add((20, 20), 1)
        sizer.Add(btnSizer, 0, wx.EXPAND | wx.ALL, 10)
        #
        self.SetSizer(sizer)
        self.Center()
        self.ShowModal()
 
        # sizer.Fit(self)
    def onKey(self, event):

        dlg = ConfigKmc(self, self.kmc, self.bank_name)
        self.kmc = dlg.kmc


    def onOkay(self, event):
        index = self.machine_c.GetSelection()
        if index < 0:
            index = 0
        self.machineID = self.machines[index][-1]
        machine_name = self.machine_c.GetValue()

        status = self.server.CIM_StartTask(self.parent.order_id, int(
            self.jobList.getColumnText(self.jobList.currentItem, Messages.RUN_JOB_FIELDS.get(Messages.JOB_ID)[0])
        ), self.machineID, self.kmc, self.parent.key_info[-1])
        if not status:

            self.jobList.setColumnText(self.jobList.currentItem, Messages.RUN_JOB_FIELDS.get(Messages.MACHINE)[0], machine_name)
            self.jobList.setColumnText(self.jobList.currentItem, Messages.RUN_JOB_FIELDS.get(Messages.KMC)[0], self.kmc)
            self.jobList.setColumnText(self.jobList.currentItem, Messages.RUN_JOB_FIELDS.get(Messages.JOB_STATUS)[0],
                                       Messages.STATUS_PRIVATE if self.machineID else Messages.STATUS_PUBLIC)
            self.Destroy()
            self.jobList.SetFocus()
            # print(self.kmc)
            self.jobList.GetPyData(self.jobList.currentItem)[KMC_INFO] = self.kmc
            self.jobList.GetPyData(self.jobList.currentItem)[DEV_ID] = self.machineID
        else:
            pub.sendMessage("status", message=status)

    def OnCanel(self, event):
        self.Close()
        # self.EndModal(0)
        self.Destroy()
        event.Skip()


if __name__ == "__main__":

    app = wx.PySimpleApp()

    dlg = ConfigJobDialog()
    dlg.ShowModal()
    dlg.Destroy()

    app.MainLoop()



