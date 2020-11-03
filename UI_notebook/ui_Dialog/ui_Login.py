from win32gui import SendMessage
from ctypes import windll

import wx
from win32con import WM_CLOSE

from Control_id.config_premession import Messages, UserInfo

from Control_id import ctrl_id as ID
# from UI_notebook.ui_Dialog.ui_messageBox import showStatusMessage
from UI_notebook.ui_Dialog.ui_messageBox import showStatusMessage
from instruct_parse.InstructionsModel import KMSErrorList
from tool.encrypt_algorithm.PinEncrypt import pinEncrypt

about_txt = """\
Login"""

FAILE = 0
SUCCESS = 1
RESET = 2

ADMIN = "Admin"
SUPERADMIN = "SuperAdmin"

class LoginDialog(wx.Dialog):
    def __init__(self,parent,inter, size=(350, 250)):
        wx.Dialog.__init__(self, parent, ID.ID_LOGIN_DIALOG, "Login", size=size)
        self.inter = inter
        self.result = FAILE
        self.InitUi()

    def InitUi(self):
        about   = wx.StaticText(self, -1, "Login")
        about.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        type_l  = wx.StaticText(self, -1, "Type:")
        name_l = wx.StaticText(self, -1, "Name:")
        pin_l = wx.StaticText(self, -1, "Pin:", )

        self.type_t  = wx.ComboBox(self, -1, ADMIN, choices=[ADMIN, SUPERADMIN], style=wx.TE_READONLY)
        self.type_t.Bind(wx.EVT_TEXT, self.OnTypeChange)
        self.name_t = wx.TextCtrl(self,-1, "", style= wx.TE_LEFT | wx.TE_PROCESS_ENTER)
        self.pin_t = wx.TextCtrl(self,-1, "", style=wx.TE_PASSWORD | wx.TE_LEFT | wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.onOkay, self.name_t)
        self.Bind(wx.EVT_TEXT_ENTER, self.onOkay, self.pin_t)
        self.Bind(wx.EVT_CLOSE, self.Exit)
        # Use standard button IDs

        okay = wx.Button(self, -1, "OK")
        # okay.SetDefault()
        okay.Bind(wx.EVT_BUTTON, self.onOkay)
        cancel = wx.Button(self, -1, "cancel")
        cancel.Bind(wx.EVT_BUTTON, self.exit)
        # Layout with sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(about, 0, wx.CENTER, 5)
        sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)

        fgs = wx.FlexGridSizer(3, 2, 10, 10)
        fgs.Add(type_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.type_t, 0, wx.EXPAND)
        fgs.Add(name_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.name_t, 0, wx.EXPAND)
        fgs.Add(pin_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.pin_t, 0, wx.EXPAND)
        fgs.AddGrowableCol(1)
        sizer.Add(fgs, 1, wx.EXPAND|wx.ALL, 5)

        # btns = wx.StdDialogButtonSizer()
        # btns.AddButton(okay)
        # okay.Bind(wx.EVT_BUTTON, self.onOkay)
        # btns.AddButton(cancel)
        # btns.Realize()
        # sizer.Add(btns, 1, wx.CENTER|wx.ALL, 5)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(okay)
        btnSizer.Add((20, 20), 1)
        btnSizer.Add(cancel)
        btnSizer.Add((20, 20), 1)
        sizer.Add(btnSizer, 0, wx.EXPAND | wx.BOTTOM, 20)

        self.SetSizer(sizer)
        self.Center()
        # self.ShowModal()
        # sizer.Fit(self)

    def OnTypeChange(self, event):
        type = self.type_t.GetValue()
        if type == ADMIN:
            self.name_t.SetValue("")
            self.name_t.Enable(True)
        else:
            self.name_t.SetValue("SuperAdmin")
            self.name_t.Enable(False)

    def Exit(self, event):
        self.Destroy()
        # wx.Exit()
        # self.exit(event)
        mainFrame = wx.Window.FindWindowById(ID.ID_MAIN_FRAME)
        if mainFrame:
            wx.CallLater(200, lambda: SendMessage(mainFrame.GetHandle(), WM_CLOSE, 0, 0))
        event.Skip()

    def onOkay(self, event):
        user_name = self.name_t.GetValue()
        pin = self.pin_t.GetValue()
        user_type = self.type_t.GetValue()
        if not user_name:
            self.name_t.SetFocus()
            return
        if not pin:
            self.pin_t.SetFocus()
            return

        if user_type == ADMIN:
            data = self.inter.loginAdmin(name=user_name, pin=pinEncrypt(pin))
            result = showStatusMessage(data['status'], self.inter)
            if result:
                self.result = SUCCESS
                if data['status'] == Messages.STATUS_RESET:
                    self.result = RESET
                UserInfo.id = data['data']['id']
                UserInfo.pin = pin
                UserInfo.isSuperAdmin = False
                self.Destroy()
        else:
            response = self.inter.loginSuperAdmin(pin=pinEncrypt(pin))
            flag = showStatusMessage(response['status'], self.inter)
            if flag:
                self.result = SUCCESS
                if response['status'] == Messages.STATUS_RESET:
                    self.result = RESET
                UserInfo.id = ""
                UserInfo.isSuperAdmin = True
                UserInfo.pin = pin
                # self.Close()
                self.Destroy()


    def exit(self, event):

        # self.EndModal(self.result)

        # self.Destroy()
        mainFrame = wx.Window.FindWindowById(ID.ID_MAIN_FRAME)
        if mainFrame:
            mHwnd = mainFrame.GetHandle()
            hwnd = windll.user32.GetLastActivePopup(mHwnd)
            if hwnd != mHwnd:
                SendMessage(hwnd, WM_CLOSE, 0, 0)
                # wx.CallAfter(mainFrame.Destroy)
                # wx.Exit()
                wx.CallLater(200, lambda: SendMessage(mHwnd, WM_CLOSE, 0, 0))  # 再次 发送关闭消息，
            # else:
            #     win32gui.SendMessage(mHwnd, WM_CLOSE, 0, 0)
            # mainFrame.Close()
            # mainFrame.Destroy()


            # mainFrame._mgr.UnInit()
        # self.Close()
        wx.Exit()
        
        event.Skip()


# app = wx.PySimpleApp()
#
# dlg = LoginDialog()
# dlg.ShowModal()
# dlg.Destroy()
#
# app.MainLoop()
