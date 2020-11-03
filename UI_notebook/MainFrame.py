#!/usr/bin/env python

import wx
import os
import time
import win32process

from wx.lib.agw.pybusyinfo import PyBusyInfo

from Control_id import ctrl_id as ID
from SocketTCp.SocketTCp import ClientSocket
from UI_notebook.ui_Dialog.ui_addRepairJob import AddRepairJob
from UI_notebook.ui_Dialog.ui_addWindows import AddWindow
from UI_notebook.ui_Dialog.ui_configJob import ConfigJobDialog
from UI_notebook.ui_Dialog.ui_deleteFile import DeleteFile
from UI_notebook.ui_Dialog.ui_wizardAddJob import AddJob
from UI_notebook.ui__Notebook.ui_notebook_finishOrder import FinishedOrderView
from UI_notebook.ui__Notebook.ui_notebook_machine import MachineView
from UI_notebook.ui__Notebook.ui_notebook_runningOrder import RunJobView

# bitmapDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Icon")

from pubsub import pub
import wx.lib.agw.flatmenu as FM
from wx.lib.agw.artmanager import ArtManager, RendererBase, DCSaver
from wx.lib.agw.fmresources import ControlFocus, ControlPressed
from wx.lib.agw.fmresources import FM_OPT_IS_LCD

import wx.lib.agw.aui as AUI


AuiPaneInfo = AUI.AuiPaneInfo
AuiManager = AUI.AuiManager
_hasAUI = True


#----------------------------------------------------------------------

#-------------------------------
# Menu items IDs
#-------------------------------

MENU_STYLE_DEFAULT = wx.NewIdRef()
MENU_STYLE_XP = wx.NewIdRef()
MENU_STYLE_2007 = wx.NewIdRef()
MENU_STYLE_VISTA = wx.NewIdRef()
MENU_STYLE_MY = wx.NewIdRef()
MENU_USE_CUSTOM = wx.NewIdRef()
MENU_LCD_MONITOR = wx.NewIdRef()
MENU_HELP = wx.NewIdRef()

MENU_DISABLE_MENU_ITEM = wx.NewIdRef()
MENU_REMOVE_MENU = wx.NewIdRef()
MENU_TRANSPARENCY = wx.NewIdRef()

MENU_NEW_FILE = 10005
MENU_SAVE = 10006
MENU_OPEN_FILE = 10007
MENU_NEW_FOLDER = 10008
MENU_COPY = 10009
MENU_CUT = 10010
MENU_PASTE = 10011


def switchRGBtoBGR(colour):

    return wx.Colour(colour.Blue(), colour.Green(), colour.Red())


def CreateBackgroundBitmap():

    mem_dc = wx.MemoryDC()
    bmp = wx.Bitmap(200, 300)
    mem_dc.SelectObject(bmp)

    mem_dc.Clear()

    # colour the menu face with background colour
    top = wx.Colour("blue")
    bottom = wx.Colour("light blue")
    filRect = wx.Rect(0, 0, 200, 300)
    mem_dc.GradientFillConcentric(filRect, top, bottom, wx.Point(100, 150))

    mem_dc.SelectObject(wx.NullBitmap)
    return bmp

#------------------------------------------------------------
# A custom renderer class for FlatMenu
#------------------------------------------------------------

class FM_MyRenderer(FM.FMRenderer):
    """ My custom style. """

    def __init__(self):

        FM.FMRenderer.__init__(self)


    def DrawMenuButton(self, dc, rect, state):
        """Draws the highlight on a FlatMenu"""

        self.DrawButton(dc, rect, state)


    def DrawMenuBarButton(self, dc, rect, state):
        """Draws the highlight on a FlatMenuBar"""

        self.DrawButton(dc, rect, state)


    def DrawButton(self, dc, rect, state, colour=None):

        if state == ControlFocus:
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().BackgroundColour())
        elif state == ControlPressed:
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().HighlightBackgroundColour())
        else:   # ControlNormal, ControlDisabled, default
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().BackgroundColour())

        # Draw the button borders
        dc.SetPen(wx.Pen(penColour))
        dc.SetBrush(wx.Brush(brushColour))
        dc.DrawRoundedRectangle(rect.x, rect.y, rect.width, rect.height,4)


    def DrawMenuBarBackground(self, dc, rect):

        # For office style, we simple draw a rectangle with a gradient colouring
        vertical = ArtManager.Get().GetMBVerticalGradient()

        dcsaver = DCSaver(dc)

        # fill with gradient
        startColour = self.menuBarFaceColour
        endColour   = ArtManager.Get().LightColour(startColour, 90)

        dc.SetPen(wx.Pen(endColour))
        dc.SetBrush(wx.Brush(endColour))
        dc.DrawRectangle(rect)


    def DrawToolBarBg(self, dc, rect):

        if not ArtManager.Get().GetRaiseToolbar():
            return

        # fill with gradient
        startColour = self.menuBarFaceColour()
        dc.SetPen(wx.Pen(startColour))
        dc.SetBrush(wx.Brush(startColour))
        dc.DrawRectangle(0, 0, rect.GetWidth(), rect.GetHeight())


#------------------------------------------------------------
# Declare our main frame
#------------------------------------------------------------

class MyFrame(wx.Frame):

    def __init__(self, parent, server):

            wx.Frame.__init__(self, parent,id=ID.ID_MAIN_FRAME, size=(1300, 700), style=wx.DEFAULT_FRAME_STYLE |
                              wx.NO_FULL_REPAINT_ON_RESIZE)
            self.server = server
            # self.SetIcon(images.Mondrian.GetIcon())
            wx.SystemOptions.SetOption("msw.remap", "0")
            self.SetTitle("CIMSys")
            if _hasAUI:
                self._mgr = AuiManager()
                self._mgr.SetManagedWindow(self)

            self._popUpMenu = None
            pub.subscribe(self.showErr, "status")
            pub.subscribe(self.writeLog, "Log")
            pub.subscribe(self.restart, "serverError")
            mainSizer = wx.BoxSizer(wx.VERTICAL)

            # Create a main panel and place some controls on it
            mainPanel = wx.Panel(self, -1)

            panelSizer = wx.BoxSizer(wx.VERTICAL)
            mainPanel.SetSizer(panelSizer)

            logPanel = wx.Panel(self, -1)
            boxsizer = wx.BoxSizer(wx.VERTICAL)

            self.logContrl = wx.TextCtrl(logPanel, -1, size=(0, 150), style=wx.TE_MULTILINE | wx.TE_READONLY)
            self.logContrl.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
            boxsizer.Add(self.logContrl, 1, wx.EXPAND)
            logPanel.SetSizer(boxsizer)

            hs = wx.BoxSizer()

            self.nb = AUI.AuiNotebook(self, agwStyle=AUI.AUI_NB_TOP  | \
                       AUI.AUI_NB_SCROLL_BUTTONS | AUI.AUI_NB_CLOSE_ON_ALL_TABS
                        )
            # self.nb.Bind(AUI.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnClose)
            # self.nb.Bind(AUI.EVT_AUINOTEBOOK_PAGE_CHANGING, self.OnSelect)



            panel = RunJobView(self.nb, server, ID.ID_NOTEBOOK_RUNJOB)
            panel.OnInit()
            # panel2 = DeleteJobView(self.nb, server, ID.ID_NOTEBOOK_DELETEJOB)
            # l = panel.OnInit()
            # if not l:
            #     panel.Destroy()
            # else:
            self.nb.AddPage(panel, "Running Order", True)
            # self.nb.AddPage(panel2, "Delete Job", False)
            hs.Add(self.nb, 0, wx.ALL, 1)
            self.Bind(wx.EVT_CLOSE, self.Exit)
            self.nb.SetCloseButton(0, False)
            # self.nb.SetCloseButton(1, False)

            panelSizer.Add(hs, 0, wx.EXPAND, 5)



            statusbar = self.CreateStatusBar(2)
            statusbar.SetStatusWidths([-2, -1])
            # statusbar fields
            statusbar_fields = [(""),
                                ("Welcome !")]

            for i in range(len(statusbar_fields)):
                statusbar.SetStatusText(statusbar_fields[i], i)

            self.CreateMenu()
            self.ConnectEvents()
            # self.creatPremession()
            mainSizer.Add(self._mb, 0, wx.EXPAND)
            # mainSizer.Add(mainPanel, 1, wx.EXPAND)
            # self.SetSizer(mainSizer)
            # mainSizer.Layout()

            if _hasAUI:
                # AUI support
                self._mgr.AddPane(self.nb, AuiPaneInfo().Name("main_panel").
                CenterPane())

                self._mgr.AddPane(logPanel, AuiPaneInfo().Name("Log_panel").Caption("Event Log").Bottom().
                                  CloseButton(False).MinimizeButton())
                # self._mgr.AddPane(logPanel2, AuiPaneInfo().Name("Log_panel2").Bottom())
                self._mb.PositionAUI(self._mgr)
                self._mgr.Update()

            ArtManager.Get().SetMBVerticalGradient(True)
            ArtManager.Get().SetRaiseToolbar(False)

            self._mb.Refresh()
            # self._mtb.Refresh()

            self.CenterOnScreen()

    def writeLog(self, message):
        nowtime = time.strftime("%H:%M:%S" ,time.localtime())
        self.logContrl.write(nowtime + " : " + message + "\r\n")

    def restart(self):
        pub.sendMessage("connect", flag=False)
        dlg = wx.MessageDialog(None, 'Connection timeout whether to reconnect?',
                               'Error',
                               wx.YES_NO | wx.ICON_ERROR | wx.CENTER | wx.STAY_ON_TOP
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )

        while True:
            if dlg.ShowModal() == wx.ID_YES:
                busy = PyBusyInfo("Connecting", parent=self, title="Really Busy")

                wx.Yield()
                flag = self.server.restart()
                if flag:
                    dlg.Destroy()
                    pub.sendMessage("connect", flag=True)
                    break
                else:
                    dlg.SetMessage("Connect Fail, Whether to reconnect?")
            else:
                dlg.Destroy()
                mainFrame = wx.Window.FindWindowById(ID.ID_MAIN_FRAME)
                mHwnd = mainFrame.GetHandle()
                threadpid, procpid = win32process.GetWindowThreadProcessId(mHwnd)
                os.popen('taskkill.exe /F /pid:' + str(procpid))

                return
            del busy

    def Exit(self, event):
        self.Destroy()
        wx.Exit()
        # event.Skip()

    def OnSelect(self, event):
        index = event.GetSelection()
        if index >= 0:
            page = self.nb.GetPage(index)
            # page.OnInit()
        event.Skip()

    def showErr(self, message):
        # wx.MessageBox(str(message), "Error", wx.OK | wx.ICON_ERROR)
        dlg = wx.MessageDialog(self, str(message),
                               'Error',
                               wx.YES_NO | wx.ICON_ERROR
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()

    def OnClose(self, event):
        ctrl = self._mgr.GetPane("minibar_panel")
        panel = wx.Window.FindWindowById(ID.ID_PREMESSION_FRAME)

        # print(self.premession_dict.get(self.model.GetValue(items, 1)))
        if panel:
            panel.changeStatue(0)
        ctrl.Hide()
        self._mgr.Update()
        event.Skip()
    def CreateMenu(self):

        # Create the menubar
        self._mb = FM.FlatMenuBar(self, wx.ID_ANY, 32, 5, options = FM_OPT_IS_LCD )

        fileMenu  = FM.FlatMenu()

        helpMenu = FM.FlatMenu()

        self.newMyTheme = self._mb.GetRendererManager().AddRenderer(FM_MyRenderer())
        self._mb.GetRendererManager().SetTheme(self.newMyTheme)


        # user_bmp = wx.Bitmap(os.path.join(bitmapDir, "user.png"), wx.BITMAP_TYPE_PNG)
        # change_pin_bmp = wx.Bitmap(os.path.join(bitmapDir, "ChangePin.png"), wx.BITMAP_TYPE_PNG)
        # add_local_bmp = wx.Bitmap(os.path.join(bitmapDir, "AddLocalUser.png"), wx.BITMAP_TYPE_PNG)
        # add_windows_bmp = wx.Bitmap(os.path.join(bitmapDir, "AddWindowsUser.png"), wx.BITMAP_TYPE_PNG)
        #
        # user_bmp_32 = wx.Bitmap(os.path.join(bitmapDir, "user_32.png"), wx.BITMAP_TYPE_PNG)
        # change_pin_bmp_32 = wx.Bitmap(os.path.join(bitmapDir, "ChangePin_32.png"), wx.BITMAP_TYPE_PNG)
        # add_local_bmp_32 = wx.Bitmap(os.path.join(bitmapDir, "AddLocalUser_32.png"), wx.BITMAP_TYPE_PNG)
        # add_windows_bmp_32 = wx.Bitmap(os.path.join(bitmapDir, "AddWindowsUser_32.png"), wx.BITMAP_TYPE_PNG)
        #
        # exitImg = wx.Bitmap(os.path.join(bitmapDir, "exit-16.png"), wx.BITMAP_TYPE_PNG)
        # helpImg = wx.Bitmap(os.path.join(bitmapDir, "help-16.png"), wx.BITMAP_TYPE_PNG)

        # Create a context menu
        context_menu = FM.FlatMenu()



        item = FM.FlatMenuItem(fileMenu, ID.ID_MENU_MACHINE, "&Machine\tCtrl+N", "Machine", wx.ITEM_NORMAL, None)
        fileMenu.AppendItem(item)
        item.SetContextMenu(context_menu)

        # self._mb.AddTool(ID.ID_MENU_USER, "Machine", user_bmp_32)

        # item = FM.FlatMenuItem(fileMenu, ID.ID_MENU_CHANGE_PIN, "&Change Pin\tCtrl+S", "Change Pin", wx.ITEM_NORMAL,
        #                        None, change_pin_bmp)
        # fileMenu.AppendItem(item)
        # self._mb.AddTool(ID.ID_MENU_CHANGE_PIN, "Change Pin", change_pin_bmp_32)
        #
        # fileMenu.AppendSeparator()   # Separator
        #

        #

        item = FM.FlatMenuItem(fileMenu, ID.ID_MENU_DELETE_JOB, "&Finished Order", "Finished Order", wx.ITEM_NORMAL,
                               None)
        fileMenu.AppendItem(item)

        # item = FM.FlatMenuItem(fileMenu, ID.ID_MENU_DELETE_FILE, "&Delete File", "Delete File", wx.ITEM_NORMAL,
        #                        None)
        # fileMenu.AppendItem(item)


        fileMenu.AppendSeparator()
        item = FM.FlatMenuItem(fileMenu, wx.ID_EXIT, "E&xit\tAlt+Q", "Exit demo", wx.ITEM_NORMAL, None)
        fileMenu.AppendItem(item)



        # Demonstrate how to set custom font and text colour to a FlatMenuItem
        item.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, "Courier New"))
        item.SetTextColour("Red")





            # multipleMenu.AppendItem(item)

        # multipleMenu.SetNumberColumns(2)

        # historyMenu.Append(wx.ID_OPEN, "&Open...")
        # self.historyMenu = historyMenu
        # self.filehistory = FM.FileHistory()
        # self.filehistory.UseMenu(self.historyMenu)


        item = FM.FlatMenuItem(helpMenu, MENU_HELP, "&About\tCtrl+A", "About...", wx.ITEM_NORMAL, None)
        helpMenu.AppendItem(item)

        # fileMenu.SetBackgroundBitmap(CreateBackgroundBitmap())

        self._mb.Append(fileMenu, "&File")

        self._mb.Append(helpMenu, "&Help")


    def ConnectEvents(self):

        # Attach menu events to some handlers
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnMachine, id=ID.ID_MENU_MACHINE)
        # self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnAddJob, id=ID.ID_MENU_ADD_JOB)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnQuit, id=wx.ID_EXIT)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnAbout, id=MENU_HELP)
        self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnDeleteJob, id=ID.ID_MENU_DELETE_JOB)
        # self.Bind(FM.EVT_FLAT_MENU_SELECTED, self.OnDeleteFile, id=ID.ID_MENU_DELETE_FILE)




    def OnQuit(self, event):

        if _hasAUI:
            self._mgr.UnInit()
        self.Close()
        self.Destroy()
        # wx.GetApp().OnInit()
        event.Skip()

    def OnMachine(self, event):

        ctrlWindow = wx.Window.FindWindowById(ID.ID_NOTEBOOK_MACHINE)
        if ctrlWindow:
            self.nb.SetSelection(self.nb.GetPageIndex(ctrlWindow))
        else:
            panel = MachineView(self.nb, self.server, ID.ID_NOTEBOOK_MACHINE)
            panel.OnInit()
            self.nb.AddPage(panel, "Machine", True)

            self._mgr.Update()

    def OnDeleteJob(self, event):
        ctrlWindow = wx.Window.FindWindowById(ID.ID_NOTEBOOK_DELETEJOB)
        if ctrlWindow:
            self.nb.SetSelection(self.nb.GetPageIndex(ctrlWindow))
        else:
            panel2 = FinishedOrderView(self.nb, self.server, ID.ID_NOTEBOOK_DELETEJOB)
            panel2.OnInit()
            self.nb.AddPage(panel2, "Finished Order", True)

    def OnDeleteFile(self, event):
        DeleteFile(self)

    def OnChangePin(self, event):
        dlg = ConfigJobDialog(self, self.server)


    def OnAddJob(self, event):

        AddJob(self, self.server)

    def OnStyle(self, event):

        eventId = event.GetId()

        if eventId == MENU_STYLE_DEFAULT:
            self._mb.GetRendererManager().SetTheme(FM.StyleDefault)
        elif eventId == MENU_STYLE_2007:
            self._mb.GetRendererManager().SetTheme(FM.Style2007)
        elif eventId == MENU_STYLE_XP:
            self._mb.GetRendererManager().SetTheme(FM.StyleXP)
        elif eventId == MENU_STYLE_VISTA:
            self._mb.GetRendererManager().SetTheme(FM.StyleVista)
        elif eventId == MENU_STYLE_MY:
            self._mb.GetRendererManager().SetTheme(self.newMyTheme)

        self._mb.ClearBitmaps()

        self._mb.Refresh()
        self.Update()


    def OnAbout(self, event):

        msg = "This is System"

        dlg = wx.MessageDialog(self, msg, "User System",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()




