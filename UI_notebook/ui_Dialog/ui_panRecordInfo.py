import time

import wx


from UI_notebook.ui_Dialog.ui_PanView import *


class PanRecordList(MyListCtrl):
    def __init__(self, parent, id, pan_id, pan, order_id, size=(-1, -1)):
        super(PanRecordList, self).__init__(parent, id, Messages.PAN_RECORD, size, style =
        wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|ULC.ULC_SINGLE_SEL |  ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)
        self.pan_id = pan_id
        self.pan = pan
        self.order_id = order_id

    def InitData(self):
        job_info_active = self.server.CIM_QueryRecordInActiveJob(self.order_id, self.pan_id)
        job_info_finish = self.server.CIM_QueryLoggedRecordInFinishedJob(self.order_id, self.pan_id)
        job_info_active.extend(job_info_finish)

        for job_info in job_info_active:
            data = self.JobInfoToData(job_info)
            pos = self.addItem(data)
            self.InitStatus(pos)

    def addItem(self, data):
        if data:
            pos = self.GetItemCount()
            self.InsertStringItem(pos, data[0])
            for i in range(1, len(data)):
                index = self.SetStringItem(pos, i, str(data[i]))
            self.Refresh()
            return pos

    def JobInfoToData(self, job_info):
        data = []
        pan_infos = self.server.CIM_QueryLogByPan(self.order_id, job_info[0], self.pan)
        if pan_infos:
            data.append(str(job_info[0]))
            pan_info = pan_infos[0]
            status = PanViewList.GetPanStatus(pan_info[3])
            data.extend([status, time.strftime("%Y-%m-%d %H:%M:%S", pan_info[4])])
        return data

    def InitStatus(self, index, col=Messages.PAN_RECORD.get(Messages.PAN_STATUS)[0]):

        if col == Messages.PAN_RECORD.get(Messages.PAN_STATUS)[0]:
            fontMask = ULC.ULC_MASK_FONTCOLOUR | ULC.ULC_MASK_FONT
            item = self.GetItem(index, col)
            item.SetMask(fontMask)
            status = item.GetText()
            if status == STATUS_SUCCESS or status == Messages.STATUS_PUBLIC:
                item.SetTextColour(wx.GREEN)
            elif status == STATUS_FAIL:
                item.SetTextColour(wx.RED)
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.FONTWEIGHT_BOLD)
            item.SetFont(font)
            self.SetItem(item)

class PanRecordInfo(wx.Dialog):
    def __init__(self, parent, pan_id, pan, order_id):
        super(PanRecordInfo, self).__init__(parent, title='', size=(700, 250))
        panel = wx.Panel(self)
        # First create the controls
        self.listCtrl = PanRecordList(panel,-1, pan_id, pan, order_id, size=(600, -1))
        self.listCtrl.InitData()
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.listCtrl, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(mainSizer)
        self.Centre()
        # mainSizer.SetSizeHints(self)
        # self.InitData()
        self.ShowModal()