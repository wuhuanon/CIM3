import wx
import wx.adv
from wx.adv import Wizard as wiz
from wx.adv import WizardPage, WizardPageSimple

from Control_id.config_premession import Messages
from Control_id.config_premession import *
from UI_notebook.MyListCtrl import MyListCtrl
from UI_notebook.MyTreeList import HyperTreeList
from UI_notebook.MyValidate import DigitsValidator
from UI_notebook.ui_Dialog.ui_ConfigKmc import ConfigKmc
from Control_id import ctrl_id as ID
from wx.lib.agw import ultimatelistctrl as ULC

SELECT_BUT = 1001
DESELECT_BUT = 1002

class PanRepairList(MyListCtrl):
    def __init__(self, parent, id, size=(-1, -1)):
        super(PanRepairList, self).__init__(parent,id, Messages.PAN_PEPAIR_FIELDS, size)
        # self.SetSecondGradientColour('red')
        self.parent = parent
        self.realData = []
        for i in range(200001):
            self.realData.append([str(i+1), 'machine%d'% i, "success", "2020-01-01", 'User1', False])
        self.data = self.realData
        self.SetItemCount(len(self.data))
        # self.Append(data)
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.attr1 = ULC.UltimateListItemAttr(font=font)
        # self.attr1.SetTextColour(wx.RED)
        self.attr2 = ULC.UltimateListItemAttr(font=font)
        # self.attr1.SetTextColour(wx.GREEN)
        # self.attr1.SetBackgroundColour(wx.Colour(180,180,180))
        # self.attr1.Enable(False)
        info = self.GetColumn(0)
        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT | ULC.ULC_MASK_CHECK
        info._kind = 1
        info.Check(False)
        self.titflag = False
        self.SetColumn(0, info)
        self.Bind(ULC.EVT_LIST_ITEM_CHECKED, self.onCheck)
        self.Bind(ULC.EVT_LIST_COL_CHECKING, self.onCheckTitle)

    def onCheck(self, event):
        item = event.GetItem()
        if item.IsChecked():
            self.data[self.currentItem][-1] = True
        else:
            self.data[self.currentItem][-1] = False

        self.changeColCheck()

    def GetFlag(self):
        for i in self.data:
            if not i[-1]:
                return False
        return True


    def onCheckTitle(self, event):
        self.titflag = not self.titflag
        def changeSelect(data):
            data[-1] = self.titflag
            return data

        self.data = list(map(changeSelect, self.data))



    def changeColCheck(self):
        flag = self.GetFlag()
        self.titflag = flag
        info = self.GetColumn(0)
        info.Check(flag)
        self.SetColumn(0, info)

    def searchItem(self, pan):
        search = []
        for i in self.realData:
            if pan in i[0]:
                search.append(i)
        if len(search) == 0 and pan:
            dlg = wx.MessageDialog(self.parent, "Noting Find",
                                   "Search",
                                   wx.OK | wx.ICON_INFORMATION
                                   # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                   )
            dlg.ShowModal()
            dlg.Destroy()
            self.data = self.realData
        else:
            self.data = search
        self.SetItemCount(len(self.data))
        self.Refresh()

    def OnGetItemText(self, item, col):
        return self.data[item][col]

    def OnGetItemTextColour(self, item, col):
        text = self.data[item][col]
        if col == Messages.PAN_PEPAIR_FIELDS.get(Messages.PAN_STATUS)[0]:
            if text == "success":
                return wx.Colour(wx.GREEN)
            elif text == 'fail':
                return wx.Colour(wx.RED)
        else:
            return None

    def OnGetItemToolTip(self, item, col):
        return None



    # def OnGetItemColumnImage(self, item, column):
    #
    #     return self.randomLists[item%5]


    # def OnGetItemImage(self, item):
    #
    #     return self.randomLists[item%5]


    def OnGetItemAttr(self, item):

        return self.attr1
        # if item % 3 == 1:
        #     return self.attr1
        # elif item % 3 == 2:
        #     return self.attr2
        # else:
        #     return None


    # def OnGetItemColumnCheck(self, item, column):
    #
    #     if item%3 == 0:
    #         return True
    #
    #     return False


    def OnGetItemCheck(self, item):

        return self.data[item][-1]



    # def OnGetItemColumnKind(self, item, column):
    #
    #     if item%3 == 0:
    #         return 2
    #     elif item%3 == 1:
    #         return 1
    #
    #     return 0
    def OnGetItemKind(self, item):
        # self.GetItem(item)
        return 1

def makePageTitle(wizPg, title):
    sizer = wx.BoxSizer(wx.VERTICAL)
    wizPg.SetSizer(sizer)
    title = wx.StaticText(wizPg, -1, title)
    title.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
    sizer.Add(title, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    sizer.Add(wx.StaticLine(wizPg, -1), 0, wx.EXPAND|wx.ALL, 5)
    return sizer


class TitledPage(wx.adv.WizardPageSimple):
    def __init__(self, parent, title):
        WizardPageSimple.__init__(self, parent)
        self.sizer = makePageTitle(self, title)

class SupplementPage(wx.adv.WizardPage):
    def __init__(self, parent):
        WizardPage.__init__(self, parent)
        self.next = self.prev = None
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        job_type = wx.ComboBox(self, -1, "", choices=[TASK_COMMON, TASK_ISSUING])
        self.sizer.Add(job_type, 1, wx.EXPAND | wx.ALL, 1)

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        """If the checkbox is set then return the next page's next page"""

        return self.next

    def GetPrev(self):
        return self.prev

class ConfigPage(wx.adv.WizardPage):
    def __init__(self, parent, title):
        WizardPage.__init__(self, parent)
        self.next = self.prev = None
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.machine = ""
        self.kmc = ""
        machine_l = wx.StaticText(self, -1, "Machine:")
        desc_l = wx.StaticText(self, -1, "Desc:")
        key_l = wx.StaticText(self, -1, "Key")
        # confirm_pin_l = wx.StaticText(self, -1, "*Confirm Pin:")

        self.machine_c = wx.ComboBox(self, -1, "", choices=["", "Mechine1", "Mechine2"])
        self.desc_t = wx.TextCtrl(self, -1, "")
        self.key_b = wx.Button(self, -1, "Replace Key")

        fgs = wx.FlexGridSizer(0, 2, 10, 10)
        fgs.Add(machine_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.machine_c, 0, wx.EXPAND)
        fgs.Add(desc_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.desc_t, 0, wx.EXPAND)
        fgs.Add(key_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.key_b, 0, wx.ALL)
        # fgs.Add(confirm_pin_l, 0, wx.ALIGN_RIGHT)
        # fgs.Add(self.con_pin_t, 0, wx.EXPAND)
        fgs.AddGrowableCol(1)
        self.sizer.Add(fgs, 0, wx.EXPAND | wx.ALL, 20)

        self.Bind(wx.EVT_BUTTON, self.onKey, self.key_b)


    def onKey(self, event):
        dlg = ConfigKmc(self, "")
        self.kmc = dlg.kmc

    def GetKmc(self):
        return self.kmc

    def GetDesc(self):
        return self.desc_t.GetValue()

    def GetMachine(self):
        self.machine = self.machine_c.GetValue()
        return self.machine

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        """If the checkbox is set then return the next page's next page"""

        return None

    def GetPrev(self):
        return self.prev




class FileSelect(WizardPage):
    def __init__(self, parent, title):
        WizardPage.__init__(self, parent)
        self.next = self.prev = None
        self.data = []

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(mainSizer)
        line = wx.StaticText(self, -1, "——")
        # topLbl.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))

        # nameLbl = wx.StaticText(self, -1, "PAN")
        self.listCtrl = PanRepairList(self, -1, size=(700, 500))
        dataLen = len(self.listCtrl.data)
        startList = [str(x * 1000) for x in range(dataLen // 1000)]
        self.startSelect = wx.ComboBox(self, -1, "1", size=(65, 25), choices=startList, validator=DigitsValidator())
        self.startSelect.Bind(wx.EVT_TEXT, self.OnModify)
        self.endSelect = wx.ComboBox(self, -1, "", size=(65, 25), choices=[], validator=DigitsValidator())
        self.endSelect.Bind(wx.EVT_TEXT, self.OnModify)
        selectBut = wx.Button(self, SELECT_BUT, 'Select')
        selectBut.Bind(wx.EVT_BUTTON, self.onSelect)
        deselectBut = wx.Button(self, DESELECT_BUT, 'DeSelect')
        deselectBut.Bind(wx.EVT_BUTTON, self.onSelect)

        pan_l = wx.StaticText(self, -1, "PAN:")
        self.search = wx.SearchCtrl(self, -1)
        searchBtu = wx.Button(self, -1, 'Search')
        searchBtu.Bind(wx.EVT_BUTTON, self.onSearch)
        # mainSizer = wx.BoxSizer(wx.VERTICAL)
        toolSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(toolSizer, 0, wx.ALL | wx.EXPAND, 5)
        toolSizer.Add(self.startSelect, 0, wx.ALL, 5)
        toolSizer.Add(line, 0, wx.TOP | wx.BOTTOM, 5)
        toolSizer.Add(self.endSelect, 0, wx.ALL, 5)
        toolSizer.Add(selectBut, 0, wx.ALL, 5)
        toolSizer.Add(deselectBut, 0, wx.ALL, 5)
        toolSizer.Add((20, 20), 1)
        toolSizer.Add(pan_l, 0, wx.ALL, 5)
        toolSizer.Add(self.search, 0, wx.ALL, 5)
        toolSizer.Add(searchBtu, 0, wx.ALL, 5)

        mainSizer.Add(self.listCtrl, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(mainSizer)

        self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGING, self.onText)

    def onSearch(self, event):
        text = self.search.GetValue()
        self.listCtrl.searchItem(text)

    def OnModify(self, event):


        start = self.startSelect.GetValue()
        end = self.endSelect.GetValue()
        if not end:
            self.endSelect.SetBackgroundColour("white")
            return

        if end < start:
            self.endSelect.SetBackgroundColour((255, 124, 128))
        else:
            self.endSelect.SetBackgroundColour("white")
        self.startSelect.Refresh()
        self.endSelect.Refresh()

    def onSelect(self, event):

        start = self.startSelect.GetValue()
        if not start:
            self.startSelect.SetFocus()
            return
        start = int(start)
        end = self.endSelect.GetValue()
        if not end:
            self.endSelect.SetFocus()
            return
        end = int(end)
        if end < start:
            self.endSelect.SetFocus()
            return

        for i in range(start - 1, end):
            if event.GetId() == SELECT_BUT:
                self.listCtrl.data[i][-1] = True
            else:
                self.listCtrl.data[i][-1] = False
        self.listCtrl.changeColCheck()
        self.listCtrl.Refresh()

    def OnSave(self):

        def getSelect(data):
            return data[-1] == True

        self.data = list(filter(getSelect, self.listCtrl.realData))
        return self.data

    def SetNext(self, next):

        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):

        return self.next

    def GetPrev(self):

        return self.prev


    def onText(self, event):

        page = event.GetPage()

        if not self.OnSave():
            wx.MessageBox("Please Select File!!", "Error", wx.OK | wx.ICON_ERROR)
            event.Veto()

#----------------------------------------------------------------------

class UseAltBitmapPage(WizardPage):
    def __init__(self, parent, title):
        WizardPage.__init__(self, parent)
        self.next = self.prev = None
        self.sizer = makePageTitle(self, title)

        self.sizer.Add(wx.StaticText(self, -1, "This page uses a different bitmap"),
                       0, wx.ALL, 5)

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next

    def GetPrev(self):
        return self.prev

    # def GetBitmap(self):
    #     # You usually wouldn't need to override this method
    #     # since you can set a non-default bitmap in the
    #     # wxWizardPageSimple constructor, but if you need to
    #     # dynamically change the bitmap based on the
    #     # contents of the wizard, or need to also change the
    #     # next/prev order then it can be done by overriding
    #     # GetBitmap.
    #     return images.WizTest2.GetBitmap()


class RepairJob(wiz):
    def __init__(self, parent, server):
        super(RepairJob, self).__init__(parent, -1, "")
        self.addPage()
        self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGING, self.onText)

    def addPage(self):
        page0 = SupplementPage(self)
        page1 = FileSelect(self, "Page 1")
        page2 = ConfigPage(self, "Page 2")
        # self.FitToPage(page0)
        page0.SetNext(page1)
        page1.SetPrev(page0)
        page1.SetNext(page2)
        page2.SetPrev(page1)
        self.GetPageAreaSizer().Add(page0)
        if self.RunWizard(page0):
            Pan = page1.data
            maginc = page2.GetMachine()
            kmc = page2.GetKmc()
            desc = page2.GetDesc()
            ctrl_pan = wx.Window.FindWindowById(ID.ID_NOTEBOOK_RUNJOB)
            if ctrl_pan:
                joblist = ctrl_pan.jobList
                id = str(joblist.GetItemCount()+1)
                template = joblist.getColumnText(joblist.currentItem, Messages.RUN_JOB_FIELDS.get(Messages.ORDER_INFO)[0])
                count = 0
                if len(Pan):
                    count = len(Pan)
                else:
                    count = 10000
                success = count//2
                fail = count//3
                type = "Repair Job"
                item = joblist.addItem([id, template, count, success, fail, count-success-fail,
                                 Messages.STATUS_STOP, maginc, kmc, type, desc])
                joblist.SetPyData(item, Pan)

    def onText(self, event):

        page = event.GetPage()
        if not page.tree.item:
            page.SetNext(None)