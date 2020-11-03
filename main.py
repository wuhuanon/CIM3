import wx
import sys
from Control_id.config_premession import UserInfo
from UI_notebook.MainFrame import MyFrame
from UI_notebook.ui_Dialog.ui_Login import LoginDialog
from UI_notebook.ui_Dialog.ui_configJob import ConfigJobDialog
from instruct_parse.ClientServerInterface import ClientServerInterface
from Control_id import ctrl_id as ID
# fp = open("output.txt", "w+")
# stdout = sys.stdout
# sys.stdout = fp
class App(wx.App):

    def OnInit(self):
        # 创建窗口对象
        # panel_main = wx.Window.FindWindowById(ID.ID_MAIN_FRAME)
        # panel_change = wx.Window.FindWindowById(ID.ID_CHANGE_DIALOG)
        # panel_login = wx.Window.FindWindowById(ID.ID_LOGIN_DIALOG)
        # if panel_main:
        #     panel_main.EndModal(0)
        #     del panel_main
        # if panel_change:
        #     panel_change.Destroy()
        #     del panel_change
        # server = None
        server = ClientServerInterface()
        status = server.connect()
        if not status:
            dlg = wx.MessageDialog(None, "Failed to connect to server", "Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return False

        # dlg = LoginDialog(None, server)
        # dlg.ShowModal()
        # if dlg.result:
        #     if dlg.result == 2:
        #         dlg_change = ChangePinDialog(None, server, UserInfo.pin)
        #         if dlg_change.flag > 0:
        #             frame = MyFrame(None, server)
        #             frame.CenterOnScreen()
        #             frame.Show()
        #     else:
        frame = MyFrame(None, server)
        frame.CenterOnScreen()
        frame.Show()
        return True

if __name__ == "__main__":
    app = App()
    app.MainLoop()