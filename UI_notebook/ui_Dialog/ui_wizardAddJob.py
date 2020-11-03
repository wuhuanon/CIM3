import time
import traceback

import wx
import wx.adv
from pubsub import pub
from wx.adv import Wizard as wiz
from wx.adv import WizardPage, WizardPageSimple
from Control_id.config_premession import *
from UI_notebook.MyListCtrl import MyListCtrl
from UI_notebook.MyTreeList import HyperTreeList
from UI_notebook.ui_Dialog.ui_ConfigKmc import ConfigKmc
from Control_id import ctrl_id as ID
import wx.lib.agw.customtreectrl as CT
from instruct_parse.ClientServerInterface import ClientServerInterface
import wx.lib.agw.pybusyinfo as PBI
from wx.lib.agw import ultimatelistctrl as ULC
def makePageTitle(wizPg, title):
    sizer = wx.BoxSizer(wx.VERTICAL)
    wizPg.SetSizer(sizer)
    title = wx.StaticText(wizPg, -1, title)
    title.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
    sizer.Add(title, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    sizer.Add(wx.StaticLine(wizPg, -1), 0, wx.EXPAND|wx.ALL, 5)
    return sizer

class ConfirmPanList(MyListCtrl):
    def __init__(self, parent, id=-1, data=[], size=(400, 200)):
        super(ConfirmPanList, self).__init__(parent, id, Messages.PAN_CONFIRM_FIELDS, size)
        # self.SetSecondGradientColour('red')
        self.parent = parent
        self.realData = data

        self.data = self.realData
        self.SetItemCount(len(self.data))
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.attr1 = ULC.UltimateListItemAttr(font=font)
        # self.attr1.SetTextColour(wx.RED)
        self.attr2 = ULC.UltimateListItemAttr(font=font)
        # self.attr1.SetTextColour(wx.GREEN)
        # self.attr1.SetBackgroundColour(wx.Colour(180,180,180))
        # self.attr1.Enable(False)


    def InitData(self):
        # lst1 = filter(lambda x: x[3] is None, self.realData)
        # lst2 = [i[0] for i in lst1]
        # active_records = self.server.QueryRecordCountInActiveJob(lst2)
        # terminat_records = self.server.QueryLogCountInTerminatedJob(lst2)
        # for i in range(len(lst2)):
        #     self.dic[lst2[i]][3] = str(active_records[i])
        #     self.dic[lst2[i]][4] = str(terminat_records[i])
        # result = []
        # for i in range(len(self.realData)):
        #     if self.GetItemEnable(i) and self.realData[i][-1]:
        #         result.append(self.realData[i])
        return self.realData

    def OnGetItemText(self, item, col):

        return str(self.data[item][col])

    def OnGetItemTextColour(self, item, col):

        return None

    def OnGetItemToolTip(self, item, col):
        return None





    def OnGetItemAttr(self, item):
        return None



    def OnGetItemCheck(self, item):


        return False


    def OnGetItemKind(self, item):
        # self.GetItem(item)
        return 0

class TitledPage(wx.adv.WizardPageSimple):
    def __init__(self, parent, title):
        WizardPageSimple.__init__(self, parent)
        self.sizer = makePageTitle(self, title)


class SupplementPage(wx.adv.WizardPage):
    def __init__(self, parent):
        WizardPage.__init__(self, parent)
        self.parent = parent
        self.next = self.prev = None
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        job_type_l = wx.StaticText(self, -1, "Job Type")
        self.job_type_c = wx.ComboBox(self, -1, TASK_COMMON, choices=[TASK_COMMON, TASK_ISSUING], style=wx.TE_READONLY)
        desc_l = wx.StaticText(self, -1, "Desc:")
        self.desc_t = wx.TextCtrl(self, -1, "")
        self.desc_t.SetMaxLength(254)
        # self.sizer.Add(job_type, 1, wx.EXPAND , 1)

        fgs = wx.FlexGridSizer(0, 2, 10, 10)
        fgs.Add(job_type_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.job_type_c, 1, wx.EXPAND)
        fgs.Add(desc_l, 0, wx.ALIGN_RIGHT)
        fgs.Add(self.desc_t, 1, wx.EXPAND)
        fgs.AddGrowableCol(1)
        self.sizer.Add(fgs, 1, wx.EXPAND | wx.ALL, 20)

    def GetJobType(self):
        return self.job_type_c.GetSelection()+1

    def GetDesc(self):
        return self.desc_t.GetValue()

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        """If the checkbox is set then return the next page's next page"""
        return self.next

    def GetPrev(self):
        return self.prev

class SkipNextPage(wx.adv.WizardPage):
    def __init__(self, parent, title):
        WizardPage.__init__(self, parent)
        self.server = parent.server
        self.next = self.prev = None
        # self.sizer = makePageTitle(self, title)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.machine = ""
        self.kmc = (0, "")

        # self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGING, self.onText)
        machine_l = wx.StaticText(self, -1, "Machine:")
        desc_l = wx.StaticText(self, -1, "Desc:")
        key_l = wx.StaticText(self, -1, "Key")
        # confirm_pin_l = wx.StaticText(self, -1, "*Confirm Pin:")

        self.machine_c = wx.ComboBox(self, -1, "", choices=[""] + parent.server.CIM_EnumMachine(), style=wx.TE_READONLY)
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

    def SetKMC(self, template_info):
        template_name, template_ver = template_info
        key_info = self.server.CIM_QueryTemplateKeyInfo(template_name, template_ver)
        self.kmc = key_info[-4] if key_info else (0, "")

    def onKey(self, event):

        dlg = ConfigKmc(self, self.kmc)
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

    # def onText(self, event):
    #     page = event.GetPage()
    #     # if event.GetDirection() and (not page.tree.item or not self.GetPan()):
    #     #     wx.MessageBox("Please Select File!!", "Error", wx.OK | wx.ICON_ERROR)
    #     event.Veto()


class FileSelect(WizardPage):
    def __init__(self, parent,order_id, title):
        WizardPage.__init__(self, parent)
        self.next = self.prev = None

        # self.sizer = makePageTitle(self, title)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.tree = HyperTreeList(self, order_id)
        self.sizer.Add(self.tree, 0, wx.EXPAND, 5)
        self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGING, self.onText)
    # def GetClassDefaultAttributes(self, variant): # real signature unknown; restored from __doc__
    #
    #     return wx.WINDOW_VARIANT_LARGE

    def SetNext(self, next):

        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next

    def GetPrev(self):

        return self.prev

    def GetPan(self, job_type):
        return self.tree.GetCheckedPan(job_type)

    def GetOrder(self):
        return self.tree.orderItem.GetData()

    def GetJobType(self):
        return self.prev.GetJobType()

    def onText(self, event):
        page = event.GetPage()
        if event.GetDirection():
            if not page.tree.isSelect():
                wx.MessageBox("Please Select File!!", "Error", wx.OK | wx.ICON_ERROR)

                event.Veto()
                return
            self.next.initData()
#----------------------------------------------------------------------

class ConfirmSelect(WizardPage):
    def __init__(self, parent, title):
        WizardPage.__init__(self, parent)
        self.next = self.prev = None
        self.datas = {}
        # self.sizer = makePageTitle(self, title)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.tree = CT.CustomTreeCtrl(self, agwStyle=CT.TR_HAS_BUTTONS|CT.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.sizer.Add(self.tree, 1, wx.EXPAND | wx.ALL, 5)
        # self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGING, self.onText)

    def SetNext(self, next):

        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):

        return self.next

    def GetPrev(self):

        return self.prev

    def initData(self):
        start = time.perf_counter()
        self.tree.DeleteAllItems()
        if self.prev:
            self.datas = self.prev.GetPan(self.prev.GetJobType())
            for (order_id, order_name), v in self.datas.items():
                root = self.tree.AddRoot(order_name)
                for (file_id, file_name), pans in v.items():
                    file_item = self.tree.AppendItem(root, file_name)
                    ctrl = self.createListCtrl(pans)
                    self.tree.AppendItem(file_item, "", wnd=ctrl)
                    # self.tree.SetItemWindow(pan_item, wnd=ctrl)
                    # for pan in pans:
                    #     self.tree.AppendItem(file_item, str(pan[1]))
                    self.tree.Expand(file_item)
            self.tree.Expand(root)
        end = time.perf_counter()
        print(end-start)


    def createListCtrl(self, data):
        ctrl = ConfirmPanList(self.tree, data=data)
        return ctrl

    def GetDatas(self):
        return self.datas

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

class AddJob(wiz):
    def __init__(self, parent, server):
        super(AddJob, self).__init__(parent, -1, "")
        self.server = server
        self.parent = parent
        self.addPage()
        self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGING, self.onText)

    def addPage(self):
        page0 = SupplementPage(self)
        page1 = FileSelect(self,self.parent.getOrderId(), "Page 1")
        page2 = ConfirmSelect(self, "Page 2")
        # self.FitToPage(page0)
        page0.SetNext(page1)
        page1.SetPrev(page0)
        page1.SetNext(page2)
        page2.SetPrev(page1)
        # page1.SetNext(page2)
        # page2.SetPrev(page1)


        self.GetPageAreaSizer().Add(page0)
        self.GetPageAreaSizer().Add(page1)
        self.GetPageAreaSizer().Add(page2)
        if self.RunWizard(page0):
            pass
            busy = PBI.PyBusyInfo("Please wait ,Uploading the task", parent=None, title="Really Busy")
            try:
                # # maginc = page2.GetMachine()
                # # kmc = page2.GetKmc()
                desc = page0.GetDesc()
                #
                job_type = page0.GetJobType()
                #
                # start = time.clock()
                Pan = page2.GetDatas()
                # Pan = [i[0] for i in datas]
                # end = time.clock()
                # print(end-start)
                #
                order_info = list(Pan.keys())[0]
                keyInfo = self.server.CIM_QueryOrderInfo(order_info[0])
                if not keyInfo:
                    del busy
                    return
                Allpan = Pan[order_info]
                count = 0
                self.server.CIM_NewJobBegin(order_info[0], desc)
                flag = False
                for (file_id, file_name), file_pan in Allpan.items():
                    if not file_pan:
                        continue
                    flag = True
                    self.server.CIM_NewJobDataFile(file_id)
                    self.server.CIM_NewJobUpload([int(i[0]) for i in file_pan])
                    count += len(file_pan)
                #
                job_id, status = self.server.CIM_NewJobCommit()
                #
                if not job_id and status:
                    pub.sendMessage("status", message=status)
                    return
                ctrl_pan = wx.Window.FindWindowById(ID.ID_NOTEBOOK_RUNJOB)
                joblist = ctrl_pan.tree.GetOrderJobWindow(order_info[0])
                if ctrl_pan:
                    success = 0
                    fail = 0
                    item = joblist.addItem([job_id, count, success, fail,
                                     Messages.STATUS_STOPPED, "", keyInfo[2], desc], True)
                    joblist.SetPyData(item, {KEY_INFO: keyInfo, KMC_INFO: keyInfo[2], DEV_ID: 0})
            except Exception as e:
                traceback.print_exc()
                del busy
            finally:
                del busy

    def onText(self, event):

        page = event.GetPage()
        if not page.tree.item:
            page.SetNext(None)