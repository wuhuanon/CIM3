
# from instruct_parse.InstructionsModel import Message



import wx

from Control_id import ctrl_id as ID
FAILE = 0
SUCCESS = 1
RESET = 2
def showStatusMessage(status, inter):
    if status != 0 and status != 3:
        wx.MessageBox(Message.get(status, 9),  "Error", wx.OK | wx.ICON_ERROR)
        if status < 0:
            inter.close()
           
            panel_login = wx.Window.FindWindowById(ID.ID_LOGIN_DIALOG)         
            if not panel_login:
                from UI_notebook.ui_Dialog.ui_Login import LoginDialog
                wx.MessageBox("Disconnected, please log in again", "Warning", wx.OK | wx.ICON_WARNING)
                # wx.GetApp().__del__()
                dlg = LoginDialog(None, inter)
                dlg.ShowModal()
                if dlg.result == FAILE:
                    return -1
                
            return 0
        return 0
    return 1


class MessageBox(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, title=title)
        text = wx.TextCtrl(self, style=wx.TE_READONLY|wx.BORDER_NONE)
        text.SetValue("Hi hi hi")
        text.SetBackgroundColour(wx.SystemSettings.GetColour(4))
        self.ShowModal()
        self.Destroy()
