import locale
import time

import wx
import wx.adv

from UI_notebook.ui_Dialog.ui_PanView import PanView
from instruct_parse.ClientServerInterface import ClientServerInterface

RADIO_ALLCOUNT = "All count"
RADIO_TIME = "Time   "
RADIO_PAN = "Pan    "
RADIO_PANANDTIME = "PanAndTime"


class QueryLog(wx.Dialog):
    def __init__(self, parent, order_id, job_id=0):
        super(QueryLog, self).__init__(parent, title='Pan', size=(380, 300))
        self.parent = parent
        self.server = ClientServerInterface()
        self.order_id = order_id
        self.job_id = job_id
        self.main_box = wx.BoxSizer(wx.VERTICAL)
        # ways_box = wx.BoxSizer(wx.HORIZONTAL)
        self.body_box = wx.GridBagSizer(hgap=5, vgap=20)
        self.button_box = wx.BoxSizer(wx.HORIZONTAL)
        # self.main_box.Add(ways_box, 0, wx.ALL | wx.EXPAND, 10)
        self.main_box.Add(self.body_box, 0, wx.ALL | wx.EXPAND, 10)
        self.main_box.Add(self.button_box, 0, wx.ALL | wx.EXPAND, 10)
        # self.body_box.SetDimension(-1, -1, 100, 100)
        self.radio_ctrls = []
        all_count_ways = wx.RadioButton(self, -1, RADIO_ALLCOUNT)

        time_ways      = wx.RadioButton(self, -1, RADIO_TIME)
        pan_ways      = wx.RadioButton(self, -1, RADIO_PAN)
        pan_and_time_ways      = wx.RadioButton(self, -1, RADIO_PANANDTIME)
        self.radio_ctrls.extend([all_count_ways, time_ways, pan_ways, pan_and_time_ways])
        if job_id == 0:
            all_count_ways.Enable(False)


        self.body_box.Add(all_count_ways, pos=(0, 0),
                      flag=wx.ALIGN_CENTER)
        self.body_box.Add(time_ways, pos=(0, 1),
                      flag=wx.ALIGN_CENTER)
        self.body_box.Add(pan_ways, pos=(0, 2),
                      flag=wx.ALIGN_CENTER)
        self.body_box.Add(pan_and_time_ways, pos=(0, 3),
                      flag=wx.ALIGN_CENTER)

        self.dateCtrls = []
        self.start_time_static = wx.StaticText(self, -1, 'StartTime:')
        self.start_time_dateCtrl = wx.adv.DatePickerCtrl(self, -1, size=(130, -1), style=wx.adv.DP_DROPDOWN )
        self.start_time_timeCtrl = wx.adv.TimePickerCtrl(self, -1, size=(130, -1))
        self.end_time_static = wx.StaticText(self, -1, 'EndTime:')
        self.end_time_dateCtrl = wx.adv.DatePickerCtrl(self, -1, style=wx.adv.DP_DROPDOWN)
        self.end_time_timeCtrl = wx.adv.TimePickerCtrl(self, -1, )
        self.dateCtrls.extend([self.start_time_static, self.start_time_dateCtrl, self.start_time_timeCtrl,
                               self.end_time_static, self.end_time_dateCtrl, self.end_time_timeCtrl])
        self.updateDateCtrl(True)

        self.panCtrls = []
        self.static_Pan = wx.StaticText(self, -1, 'Pan')
        self.pan_text = wx.TextCtrl(self, -1, "")
        self.pan_text.SetMaxLength(20)
        self.panCtrls.extend([self.static_Pan, self.pan_text])
        self.body_box.Add(self.start_time_static, pos=(1, 0),
                      flag=wx.EXPAND)
        self.body_box.Add(self.start_time_dateCtrl, pos=(1, 1), span=(1, 2),
                     flag=wx.EXPAND)
        self.body_box.Add(self.start_time_timeCtrl, pos=(1, 3),
                     flag=wx.EXPAND)

        self.body_box.Add(self.end_time_static, pos=(2, 0),
                     flag=wx.EXPAND)
        self.body_box.Add(self.end_time_dateCtrl, pos=(2, 1), span=(1, 2),
                     flag=wx.EXPAND)
        self.body_box.Add(self.end_time_timeCtrl, pos=(2, 3),
                     flag=wx.EXPAND)

        self.body_box.Add(self.static_Pan, pos=(3, 0),
                     flag=wx.EXPAND)
        self.body_box.Add(self.pan_text, pos=(3, 1),span=(1, 3),
                     flag=wx.EXPAND)


        self.button = wx.Button(self, -1, "Search", size=(-1, 25))
        self.button.Bind(wx.EVT_BUTTON, self.OnSearch)

        # self.button2 = wx.Button(self, -1, "Cancel")
        self.body_box.Add(wx.StaticText(self, -1, ""), pos=(4, 1),
                          flag=wx.EXPAND )
        # self.body_box.Add(self.button2, pos=(4, 2),
        #                   flag=wx.EXPAND)

        self.button_box.Add(self.button, 1, wx.LEFT , 250)
        # self.button_box.Add(self.button2, 1, wx.ALL, 10)



        # self.Fit()
        # self.updateDateCtrl(False)
        # self.upDatePanCtrl(False)

        self.main_box.Layout()
        self.SetSizer(self.main_box, True)
        for radio in self.radio_ctrls:
            self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioSelect, radio)
        # time_ways.SetValue(True)
        # self.start_time_timeCtrl.Show(True)
        self.Center()
        self.ShowModal()



    def updateDateCtrl(self, flag):
        for i in self.dateCtrls:
            self.body_box.Show(i, flag)

    def upDatePanCtrl(self, flag):
        for i in self.panCtrls:
            self.body_box.Show(i, flag)



    def OnRadioSelect(self, event):
        radio_selected = event.GetEventObject()
        text = radio_selected.GetLabel()
        if text == RADIO_ALLCOUNT:
            self.updateDateCtrl(False)
            self.upDatePanCtrl(False)
        elif text == RADIO_TIME:
            self.updateDateCtrl(True)
            self.upDatePanCtrl(False)
        elif text == RADIO_PAN:
            self.upDatePanCtrl(True)
            self.updateDateCtrl(False)
        elif text == RADIO_PANANDTIME:
            self.updateDateCtrl(True)
            self.upDatePanCtrl(True)
        # self.main_box.Layout()

    def OnSearch(self, event):
        # pass
        locale.setlocale(locale.LC_ALL, "")
        startDate = self.start_time_dateCtrl.GetValue().FormatISODate()  # 2020-10-28
        startTime = self.start_time_timeCtrl.GetValue().FormatISOTime()  # HH:MM:SS
        endDate = self.end_time_dateCtrl.GetValue().FormatISODate()  # 2020-10-28
        endTime = self.end_time_timeCtrl.GetValue().FormatISOTime()  # HH:MM:SS
        time1 = time.strptime("%s %s" % (startDate, startTime), "%Y-%m-%d %H:%M:%S")
        time2 = time.strptime("%s %s" % (endDate, endTime), "%Y-%m-%d %H:%M:%S")
        Pan = self.pan_text.GetValue()
        pan_logs = []
        for i in range(len(self.radio_ctrls)):
            radio = self.radio_ctrls[i]
            if radio.GetValue():
                if self.pan_text.IsShown() and not Pan:
                    dlg = wx.MessageDialog(self, "Please Inter Pan",
                                           "Error",
                                           wx.OK | wx.ICON_ERROR
                                           # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                           )
                    dlg.ShowModal()
                    dlg.Destroy()
                    return

                Pan = "%" + Pan + "%"

                if i == 0:
                    job_info = self.server.CIM_QueryJobInfo(self.order_id, self.job_id)
                    pan_logs = self.server.CIM_QueryLogByIndex(self.order_id, self.job_id, 0, job_info[0])
                elif i == 1:

                    pan_logs = self.server.CIM_QueryLogByTime(self.order_id, self.job_id, time1, time2)
                    # print(self.start_time_dateCtrl.GetValue().FormatISODate())
                elif i == 2:

                    pan_logs = self.server.CIM_QueryLogByPan(self.order_id, self.job_id, Pan)

                elif i == 3:
                    pan_logs = self.server.CIM_QueryLogByTimeAndPAN(self.order_id, self.job_id, Pan, time1, time2)


        if not pan_logs:
            dlg = wx.MessageDialog(self, "Noting Find",
                                 "Search",
                                 wx.OK | wx.ICON_INFORMATION
                                 # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                 )
            dlg.ShowModal()
            dlg.Destroy()
            return
        self.ViewPan(pan_logs)

    def ViewPan(self, datas):
        PanView(self, self.server, {"order_id": self.order_id, "job_id": self.job_id, "data": datas})