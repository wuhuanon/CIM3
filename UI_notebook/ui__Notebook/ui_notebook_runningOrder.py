
import wx
import wx.dataview as dv
import wx.lib.newevent
from pubsub import pub
from wx.lib.splitter import MultiSplitterWindow
import wx.lib.scrolledpanel as scrolled
from Control_id import ctrl_id as ID
from Control_id.config_premession import *
from UI_notebook.Base_Tree import BaseTreeList
from UI_notebook.MyListCtrl import MyListCtrl
from UI_notebook.ui_Dialog.ui_FileView import FileView
from UI_notebook.ui_Dialog.ui_addRepairJob import AddRepairJob
from UI_notebook.ui_Dialog.ui_configJob import ConfigJobDialog
from UI_notebook.ui_Dialog.ui_messageBox import showStatusMessage
from UI_notebook.ui_Dialog.ui_PanView import PanView

from UI_notebook.ui_Dialog.ui_modifyInfo import ModifyInfo
from UI_notebook.ui_Dialog.ui_ConfigKmc import ConfigKmc
# from UI_notebook.ui_Dialog.ui_testplot import plotDialog
from UI_notebook.ui_Dialog.ui_progressGetPanInfo import ProgressPanInfo
from UI_notebook.ui_Dialog.ui_querylog import QueryLog
from UI_notebook.ui_Dialog.ui_wizardAddJob import AddJob, ConfirmPanList
from UI_notebook.ui_Dialog.ui_wizardRepairJob import RepairJob
from UI_notebook.ui__Notebook.ui_notebook_base import BasePanel
from UI_notebook.ui_permission import premessionPanel
from wx.lib.agw import ultimatelistctrl as ULC
import wx.lib.resizewidget as rw
import wx.lib.agw.hypertreelist as HTL

from instruct_parse.ClientServerInterface import ClientServerInterface

ID_ITEM_START = 10000
ID_ITEM_INFO = 10001
ID_ITEM_REPAIR = 10002
ID_ITEM_DELETE = 10003
ID_ITEM_LOG = 10004
ID_ITEM_ORDERLOG = 10005

ID_ITEM_CREATE_JOB = 10010
ID_ITEM_DELETE_JOB = 10011

ID_ITEM_DELETE_FILE = 10012





class JobList(MyListCtrl):
    def __init__(self, parent, id, order_id, key_info, IsRunning, size=(1000, 200)):
        super(JobList, self).__init__(parent, id, Messages.RUN_JOB_FIELDS, size, style =
        wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES|ULC.ULC_SINGLE_SEL | ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)
        # self.SetSecondGradientColour('red')
        self.parent = parent
        self.order_id = order_id
        self.key_info = key_info
        # self.Append(data)

        self.createRightMenu()
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)

        # self.SetSize(1000, 200)
        if IsRunning:
            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.getJobruntime, self.timer)
            self.timer.Start(10000)
        # self.idList = []

        pub.subscribe(self.setTimmer, "connect")

    def setTimmer(self, flag):
        if hasattr(self, "timer"):
            if flag:
                self.timer.Start()
            else:
                self.timer.Stop()

    def AcceptsFocusFromKeyboard(self):
        return False

    def getJobruntime(self, event):
        count = self.GetItemCount()
        for i in range(count):
            job_status = self.getColumnText(i, Messages.RUN_JOB_FIELDS.get(Messages.JOB_STATUS, "")[0])
            if job_status == Messages.STATUS_PUBLIC or job_status == Messages.STATUS_PRIVATE:
                job_id = int(self.getColumnText(i, Messages.RUN_JOB_FIELDS.get(Messages.JOB_ID, "")[0]))
                blank_count, success_count, fail_count = self.server.CIM_QueryIssueInfo(self.order_id, job_id)
                self.updateRunTime(i, blank_count, success_count, fail_count)
                if blank_count == 0:
                    status = self.server.CIM_StopTask(self.order_id, job_id)
                    if not status:
                        col = Messages.RUN_JOB_FIELDS.get(Messages.JOB_STATUS, "")[0]
                        self.setColumnText(i, col, Messages.STATUS_STOPPING)
                        self.InitStatus(i)
                    # self.server.CIM_FinishTask(self.order_id, job_id)
                    # if not status:
                    #     data = [job_id, blank_count, success_count, fail_count, Messages.STATUS_FINISH]
                    #     pos = self.addItem(data)
                    #     self.SetItemBackgroundColour(pos, wx.GREEN)
                    #     self.DeleteItem(i)

    def updateRunTime(self,row, blank, success, fail):
        blank_col = Messages.RUN_JOB_FIELDS.get(Messages.ALL_COUNT, "")[0]
        success_col = Messages.RUN_JOB_FIELDS.get(Messages.SUCCESS_COUNT, "")[0]
        fail_col = Messages.RUN_JOB_FIELDS.get(Messages.FAIL_COUNT, "")[0]

        self.setColumnText(row, blank_col, str(blank))
        self.setColumnText(row, success_col, str(success))
        self.setColumnText(row, fail_col, str(fail))

    def getDatafromServer(self):
        jobList = self.server.CIM_EnumJob(self.order_id)

        active_job = []
        terminated_job = []
        for job_id in jobList:
            jobInfo = self.server.CIM_QueryJobInfo(self.order_id, job_id)
            if jobInfo[1] == 1:
                active_job.append((job_id, jobInfo))
            else:
                terminated_job.append((job_id, jobInfo))
        for job in active_job:
            jobInfo = job[1]
            job_id = job[0]
            if jobInfo:
                jobdesc = jobInfo[-1]
                runtimeInfo = self.server.CIM_QueryTaskInfo(self.order_id, job_id)
                if runtimeInfo:
                    job_status = getStatus(runtimeInfo[0])
                    dev_name = self.server.CIM_QueryMachine(runtimeInfo[1])[0]
                    kmc = runtimeInfo[3]
                    blank_count, success_count, fail_count = self.server.CIM_QueryIssueInfo(self.order_id, job_id)
                    data = [job_id, blank_count, success_count, fail_count, job_status, dev_name, kmc, jobdesc]
                    pos = self.addItem(data)

                    self.SetPyData(pos, {KEY_INFO: self.key_info, KMC_INFO: kmc, DEV_ID: runtimeInfo[1]})
        for job1 in terminated_job:
            jobInfo = job1[1]
            job_id = job1[0]
            if jobInfo:
                jobdesc = jobInfo[-1]
                blank_count, success_count, fail_count = self.server.CIM_QueryIssueInfo(self.order_id, job_id)
                data = [job_id, blank_count, success_count, fail_count, "Finished", "", "", jobdesc]
                pos = self.addItem(data)
                # self.EnableItem(pos, enable=False)
                self.SetItemBackgroundColour(pos, wx.GREEN)

        self.Refresh()

    def createRightMenu(self):
        '''
        右键菜单
        :return:
        '''
        self.popupmenu = wx.Menu()  # 创建一个菜单
        # bmp = setIcon(CID.imagePath+r"\nexterror.png")
        item = wx.MenuItem(self.popupmenu, ID_ITEM_START, 'Start')
        # item.SetBitmap(bmp)
        self.Bind(wx.EVT_MENU, self.startJob, id=ID_ITEM_START)
        self.popupmenu.Append(item)
        item = wx.MenuItem(self.popupmenu, ID_ITEM_DELETE, 'Finish')
        # item.SetBitmap(bmp)
        self.Bind(wx.EVT_MENU, self.finish, id=ID_ITEM_DELETE)
        self.popupmenu.Append(item)
        item = wx.MenuItem(self.popupmenu, ID_ITEM_LOG, "Log")
        self.Bind(wx.EVT_MENU, self.OnLog, id=ID_ITEM_LOG)
        self.popupmenu.Append(item)

    def OnLog(self, event):
        # PanView(self, self.server)
        job_id = self.GetJobID()
        QueryLog(self.parent, self.order_id, job_id)
    def OnShowPopup(self, event):
        # item = event.GetItem()
        self.SetFocus()
        self.currentItem = self.GetFirstSelected()

        if self.currentItem >= 0:
            status_text = self.getColumnText(self.currentItem, Messages.RUN_JOB_FIELDS.get(Messages.JOB_STATUS, [1])[0])
            # type_text = self.jobList.GetItem(event.GetIndex(), Messages.JOB_FIELDS.get(Messages.USER_TYPE)[0])
            if status_text == Messages.STATUS_PRIVATE or status_text == Messages.STATUS_PUBLIC:
                self.popupmenu.Enable(ID_ITEM_DELETE, False)
                self.popupmenu.Enable(ID_ITEM_START, True)
                self.popupmenu.SetLabel(ID_ITEM_START, "Stop")
            elif status_text == Messages.STATUS_STOPPING:
                return
            elif status_text == Messages.STATUS_FINISH:
                self.popupmenu.Enable(ID_ITEM_DELETE, False)
                self.popupmenu.Enable(ID_ITEM_START, False)
            else:
                self.popupmenu.Enable(ID_ITEM_DELETE, True)
                self.popupmenu.Enable(ID_ITEM_START, True)
                self.popupmenu.SetLabel(ID_ITEM_START, "Start")
            self.PopupMenu(self.popupmenu)

    def InitData(self):
        self.getDatafromServer()

    def startJob(self, event):
        try:
            row = self.currentItem
            col = Messages.RUN_JOB_FIELDS.get(Messages.JOB_STATUS, "")[0]
            text = self.getColumnText(row, col)
            # item = self.jobList.setColumnText()
            if text == Messages.STATUS_PUBLIC or text == Messages.STATUS_PRIVATE:
                status = self.server.CIM_StopTask(self.order_id, int(self.getColumnText(
                    row, Messages.RUN_JOB_FIELDS.get(Messages.JOB_ID, "")[0])))

                if status:
                    pub.sendMessage("status", message=status)
                else:
                    self.setColumnText(row, col, Messages.STATUS_STOPPING)

            else:

                ConfigJobDialog(self)

            self.InitStatus(row, col)
            self.Refresh()
        except Exception as e:
            print(e)

    def finish(self, event):
        dlg = wx.MessageDialog(self, 'Are you finish?',
                               'Hint',
                               wx.YES_NO | wx.ICON_WARNING
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        if dlg.ShowModal() == wx.ID_YES:
            # response = self.server.deleteUser(id=self.dvc.datas[self.row]['id'])
            # flag = showStatusMessage(response['status'], self.server)
            # if flag:
            status = self.server.CIM_FinishTask(self.order_id, int(self.getColumnText(self.currentItem,
                                                                           Messages.RUN_JOB_FIELDS.get(Messages.JOB_ID)[
                                                                               0])))
            if status:
                pub.sendMessage("status", message=status)
            else:
                job_id = self.getColumnText(self.currentItem, Messages.RUN_JOB_FIELDS.get(Messages.JOB_ID)[0])
                blank, success, fail = self.server.CIM_QueryIssueInfo(self.order_id, int(job_id))
                data = [job_id, blank, success, fail, Messages.STATUS_FINISH]
                pos = self.addItem(data)
                self.SetItemBackgroundColour(pos, wx.GREEN)
                self.DeleteItem(self.currentItem)
        dlg.Destroy()

    def addItem(self, data, activeItem = False):

        count = self.GetItemCount()
        pos = count
        if activeItem:
            for i in range(count):
                if self.getColumnText(i, Messages.RUN_JOB_FIELDS.get(Messages.JOB_STATUS)[0]) == Messages.STATUS_FINISH:
                    pos = i
                    break
        self.InsertStringItem(pos, str(data[0]))
        for i in range(1, len(data)):
            index = self.SetStringItem(pos, i, str(data[i]))
            self.InitStatus(index, i)
        self.OnSize(None)
        return pos

    def InitStatus(self, index, col=Messages.RUN_JOB_FIELDS.get(Messages.JOB_STATUS)[0]):

        if col == Messages.RUN_JOB_FIELDS.get(Messages.JOB_STATUS)[0]:
            fontMask = ULC.ULC_MASK_FONTCOLOUR | ULC.ULC_MASK_FONT
            item = self.GetItem(index, col)
            item.SetMask(fontMask)
            status = item.GetText()
            if status == Messages.STATUS_PRIVATE or status == Messages.STATUS_PUBLIC:
                item.SetTextColour(wx.GREEN)
            elif status == Messages.STATUS_STOPPED:
                item.SetTextColour(wx.RED)
            elif status == Messages.STATUS_STOPPING:
                item.SetTextColour(wx.YELLOW)
            elif status == Messages.STATUS_FINISH:
                self.SetItemBackgroundColour(index, wx.GREEN)
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.FONTWEIGHT_BOLD)
            item.SetFont(font)
            self.SetItem(item)

    def GetJobID(self):
        job_id = int(self.getColumnText(self.currentItem, Messages.RUN_JOB_FIELDS.get(Messages.JOB_ID, (0, 0))[0]))
        return job_id
ArtIDs = [ "None",
           "wx.ART_ADD_BOOKMARK",
           "wx.ART_DEL_BOOKMARK",
           "wx.ART_HELP_SIDE_PANEL",
           "wx.ART_HELP_SETTINGS",
           "wx.ART_HELP_BOOK",
           "wx.ART_HELP_FOLDER",
           "wx.ART_HELP_PAGE",
           "wx.ART_GO_BACK",
           "wx.ART_GO_FORWARD",
           "wx.ART_GO_UP",
           "wx.ART_GO_DOWN",
           "wx.ART_GO_TO_PARENT",
           "wx.ART_GO_HOME",
           "wx.ART_FILE_OPEN",
           "wx.ART_PRINT",
           "wx.ART_HELP",
           "wx.ART_TIP",
           "wx.ART_REPORT_VIEW",
           "wx.ART_LIST_VIEW",
           "wx.ART_NEW_DIR",
           "wx.ART_HARDDISK",
           "wx.ART_FLOPPY",
           "wx.ART_CDROM",
           "wx.ART_REMOVABLE",
           "wx.ART_FOLDER",
           "wx.ART_FOLDER_OPEN",
           "wx.ART_GO_DIR_UP",
           "wx.ART_EXECUTABLE_FILE",
           "wx.ART_NORMAL_FILE",
           "wx.ART_TICK_MARK",
           "wx.ART_CROSS_MARK",
           "wx.ART_ERROR",
           "wx.ART_QUESTION",
           "wx.ART_WARNING",
           "wx.ART_INFORMATION",
           "wx.ART_MISSING_IMAGE",
           "SmileBitmap"
           ]

ORDER_DEPTH = 2
FILE_DEPTH = 4
JOB_DEPTH = 3

ACTIVE_FLAG = 1
FINISH_FLAG = 2

FILE_ITEM_TEXT = "File"
class OrderTree(BaseTreeList):
    def __init__(self, parent, id):
        super(OrderTree, self).__init__(parent, id)
        self.GetMainWindow().Bind(wx.EVT_RIGHT_UP, self.OnContextMenu)

    def InitData(self):
        orderList = self.server.CIM_EnumOrder()
        self.AddColumn("Order", width=400)
        self.AddColumn("Id", width=200)
        self.root = self.AddRoot("root")
        for order_id in orderList:
            self.AddOrederItem(order_id)
        # self.ExpandAll()
        self.Refresh()

    def OnContextMenu(self, event):
        currentItem = self.GetSelection()
        ndepth = self.getItemDepth(currentItem)
        if ndepth == ORDER_DEPTH:
            self.createOrderMenu()
        elif ndepth == FILE_DEPTH:
            self.createFileMenu()
        elif ndepth == JOB_DEPTH:
            pass

    def AddOrederItem(self, order_id, auto = True, active=True):
        flag = FINISH_FLAG
        if active:
            flag = ACTIVE_FLAG
        orderInfo = self.server.CIM_QueryOrderInfo(order_id)
        if orderInfo and orderInfo[0][1] == flag:
            orderItem = self.AppendItem(self.root, orderInfo[0][0])
            self.SetItemText(orderItem, str(order_id), 1)
            itemData = {"order_id": order_id, "job_ctrl": None}
            fileList = self.server.CIM_EnumOrderDataFile(order_id)
            fileItem = self.AppendItem(orderItem, FILE_ITEM_TEXT)
            if auto:
                for file_id in fileList:
                    fileInfo = self.server.CIM_QueryOrderDataFileInfo(order_id, file_id)
                    if fileInfo and fileInfo[-2] >= 0:
                        file_item = self.AppendItem(fileItem, fileInfo[0])
                        self.SetItemText(file_item, str(file_id), 1)
                        file_item.SetData({"file_id": file_id})

            jobItem = self.AppendItem(orderItem, "Job")
            job_item = self.AppendItem(jobItem, "")
            ctrl = JobList(self, -1, order_id, [orderInfo[1], orderInfo[2],
                                                orderInfo[3], orderInfo[4]], active)
            if auto:
                ctrl.InitData()
            # ctrl = ConfirmPanList(self, data=[(1, "as")]*10)
            self.SetItemWindow(job_item, ctrl, False)
            itemData["job_ctrl"] = ctrl
            self.SetPyData(orderItem, itemData)

    def AddFileItem(self, order_id, file_id):
        orderItems = self.GetAllChildren(self.root)
        for orderItem in orderItems:
            if self.getOrderId(orderItem) == order_id:
                childs = self.GetAllChildren(orderItem)
                for i in childs:
                    if self.GetItemText(i) == FILE_ITEM_TEXT:
                        file_info = self.server.CIM_QueryOrderDataFileInfo(order_id, file_id)
                        if file_info and file_info[2] >= 0:
                            item = self.AppendItem(i, file_info[0])
                            self.SetItemText(item, str(file_id), 1)
                            self.SetPyData(item, {"file_id": file_id})

    def createOrderMenu(self):
        popupmenu = wx.Menu()  # 创建一个菜单
        # bmp = setIcon(CID.imagePath+r"\nexterror.png")
        item = wx.MenuItem(popupmenu, ID_ITEM_CREATE_JOB, 'Create job')
        # item.SetBitmap(bmp)
        self.Bind(wx.EVT_MENU, self.createJob, id=ID_ITEM_CREATE_JOB)
        popupmenu.Append(item)
        item = wx.MenuItem(popupmenu, ID_ITEM_DELETE_JOB, 'Finish')
        self.Bind(wx.EVT_MENU, self.finishOrder, id=ID_ITEM_DELETE_JOB)
        popupmenu.Append(item)
        item = wx.MenuItem(popupmenu, ID_ITEM_ORDERLOG, 'Log')
        self.Bind(wx.EVT_MENU, self.OnLogOrder, id=ID_ITEM_ORDERLOG)
        popupmenu.Append(item)
        self.PopupMenu(popupmenu)

    def createFileMenu(self):
        popupmenu = wx.Menu()  # 创建一个菜单
        # bmp = setIcon(CID.imagePath+r"\nexterror.png")
        item = wx.MenuItem(popupmenu, ID_ITEM_DELETE_FILE, 'Delete')
        # item.SetBitmap(bmp)
        self.Bind(wx.EVT_MENU, self.deleteFile, id=ID_ITEM_DELETE_FILE)
        popupmenu.Append(item)
        self.PopupMenu(popupmenu)

    def GetOrderJobWindow(self, order_id):
        orderItems = self.GetAllChildren(self.root)
        for item in orderItems:
            itemData = self.GetPyData(item)
            if itemData and itemData.get("order_id", 0) == order_id:
                return itemData.get("job_ctrl", None)

    def getOrderId(self, item=None):
        if not item:
            item = self.getOrderItem()
        if item and self.getItemDepth(item)==ORDER_DEPTH:
            itemData = self.GetPyData(item)
            if itemData:
                return itemData.get("order_id", 0)
        return 0

    def getOrderItem(self, item=None):
        if not item:
            item = self.GetSelection()
        while self.getItemDepth(item) !=2:
            if item is None:
                return None
            item = self.GetItemParent(item)
        return item

    def createJob(self, event):
        AddJob(self, self.server)

    def deleteFile(self, event):
        currentItem = self.GetSelection()
        file_id = currentItem.GetData().get("file_id")
        if file_id:
            dlg = wx.MessageDialog(self, 'Are you Delete?',
                                   'Hint',
                                   wx.YES_NO | wx.ICON_WARNING
                                   # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                   )
            if dlg.ShowModal() == wx.ID_YES:
                status = self.server.CIM_DelOrderDataFile(self.getOrderId(), file_id)
                if status:
                    pub.sendMessage("status", message=status)
                else:
                    self.Delete(currentItem)
    def finishOrder(self, event):

        orderItem = self.getOrderItem()
        order_id = self.getOrderId()
        dlg = wx.MessageDialog(self, 'Please confirm that all tasks under this order have stopped or ended?',
                               'Hint',
                               wx.YES_NO | wx.ICON_WARNING
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        if dlg.ShowModal() == wx.ID_YES:
            status = self.server.CIM_FinishOrder(order_id)
            if status > 0:
                pub.sendMessage("status", message=status)
            else:
                self.Delete(orderItem)
                finishOrder = wx.Window.FindWindowById(ID.ID_NOTEBOOK_DELETEJOB)
                if finishOrder:
                    finishOrder.OrderTree.AddOrederItem(order_id, True, False)
        self.SetFocus()

    def OnLogOrder(self, event):
        QueryLog(self.parent, self.getOrderId(), 0)

    def Delete(self, item):
        if self.getItemDepth(item) == ORDER_DEPTH:
            ctrl = self.GetPyData(item).get("job_ctrl", None)
            if hasattr(ctrl, "timer"):
                ctrl.timer.Stop()
        super().Delete(item)




class RunJobView(wx.Panel):
    def __init__(self, parent,server, id=-1, model=None, size=(-1, -1)):
        wx.Panel.__init__(self, parent, id=id, size=size)
        self.parent = parent
        self.server = server
        self.row = 0
        self.tree = OrderTree(self, -1)
        # self.jobList = JobList(self, -1, size=(1000, -1))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.tree, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        self.createRightMenu()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.getEvent, self.timer)
        self.timer.Start(3000)
        pub.subscribe(self.setTimmer, "connect")


    def setTimmer(self, flag):
        if flag:
            self.timer.Start()
        else:
            self.timer.Stop()

    def getEvent(self, event):
        lst = self.server.CIM_FetchEvent()
        for i in lst:
            event_type, order_id, jobFileid, datetime = i
            if event_type > 0x200:
                jobList = self.tree.GetOrderJobWindow(order_id)
                if jobList:
                    item = jobList.SerachItem(Messages.RUN_JOB_FIELDS.get(Messages.JOB_ID)[0], jobFileid)
                    if item:
                        if event_type == Event.CI_EVENT_TASK_STOPPED:
                            col = Messages.RUN_JOB_FIELDS.get(Messages.JOB_STATUS)[0]
                            jobList.setColumnText(item.GetId(), col, Messages.STATUS_STOPPED)
                            jobList.InitStatus(item.GetId(), col)
                            pub.sendMessage("Log", message="Order id :%d Job(id:%d) Stopped" % (order_id, jobFileid))
                            col_blank = Messages.RUN_JOB_FIELDS.get(Messages.ALL_COUNT)[0]
                            col_success = Messages.RUN_JOB_FIELDS.get(Messages.SUCCESS_COUNT)[0]
                            col_fail = Messages.RUN_JOB_FIELDS.get(Messages.FAIL_COUNT)[0]
                            blank_count = jobList.getColumnText(item, col_blank)
                            success_count = jobList.getColumnText(item, col_success)
                            fail_count = jobList.getColumnText(item, col_fail)

                            if jobList.getColumnText(item, col_blank) == "0":
                                status = self.server.CIM_FinishTask(order_id, jobFileid)
                                if not status:
                                    data = [jobFileid, blank_count, success_count, fail_count, Messages.STATUS_FINISH]

                                    pos = jobList.addItem(data)
                                    jobList.InitStatus(pos)
                                    jobList.Select(jobList.currentItem)
                                    jobList.DeleteItem(item.GetId())
                        elif event_type == Event.CI_EVENT_TASK_LOCKED:
                            pass
                        elif event_type == Event.CI_EVENT_TASK_UNLOCKED:
                            pass
            elif event_type == Event.CI_EVENT_ORDER_NEW:
                self.tree.AddOrederItem(order_id, False)
                pub.sendMessage("Log", message="Order id :%d  Add" % (order_id))

            elif event_type == Event.CI_EVENT_FILE_NEW:
                self.tree.AddFileItem(order_id, jobFileid)
                pub.sendMessage("Log", message="Order id :%d File(id:%d) Add" % (order_id, jobFileid))

    def OnInit(self):

        # self.jobList.DeleteAllItems()
        self.tree.InitData()


    def createRightMenu(self):
        '''
        右键菜单
        :return:
        '''
        self.popupmenu = wx.Menu()  # 创建一个菜单
        # bmp = setIcon(CID.imagePath+r"\nexterror.png")
        item = wx.MenuItem(self.popupmenu, ID_ITEM_START, 'Start')
        # item.SetBitmap(bmp)
        self.parent.Bind(wx.EVT_MENU, self.startJob, id=ID_ITEM_START)
        self.popupmenu.Append(item)

        # item = wx.MenuItem(self.popupmenu, ID_ITEM_INFO, 'Information')
        # # item.SetBitmap(bmp)
        # self.parent.Bind(wx.EVT_MENU, self.onInfo, id=ID_ITEM_INFO)
        # self.popupmenu.Append(item)
        #
        # item = wx.MenuItem(self.popupmenu, ID_ITEM_REPAIR, 'Repair card JOB')
        # # item.SetBitmap(bmp)
        # self.parent.Bind(wx.EVT_MENU, self.repairCard, id=ID_ITEM_REPAIR)
        # self.popupmenu.Append(item)

        item = wx.MenuItem(self.popupmenu, ID_ITEM_DELETE, 'Delete')
        # item.SetBitmap(bmp)
        self.parent.Bind(wx.EVT_MENU, self.delete, id=ID_ITEM_DELETE)
        self.popupmenu.Append(item)
        item = wx.MenuItem(self.popupmenu, 11111, "statistics")
        self.parent.Bind(wx.EVT_MENU, self.plot, id=11111)
        self.popupmenu.Append(item)

    def plot(self, event):
        # ProgressPanInfo(self.parent)
        PanView(self, self.server, )
        pass
        # plotDialog(self)

    def OnShowPopup(self, event):
        # item = event.GetItem()
        self.jobList.SetFocus()
        self.jobList.currentItem = self.jobList.GetFirstSelected()

        if self.jobList.currentItem >= 0:
            status_text = self.jobList.getColumnText(self.jobList.currentItem, Messages.RUN_JOB_FIELDS.get(Messages.JOB_STATUS, [1])[0])
            # type_text = self.jobList.GetItem(event.GetIndex(), Messages.JOB_FIELDS.get(Messages.USER_TYPE)[0])
            if status_text == Messages.STATUS_PRIVATE or status_text == Messages.STATUS_PUBLIC:
                self.popupmenu.Enable(ID_ITEM_DELETE, False)
                self.popupmenu.SetLabel(ID_ITEM_START, "Stop")
            elif status_text == Messages.STATUS_STOPPING:
                return
            else:
                self.popupmenu.Enable(ID_ITEM_DELETE, True)
                self.popupmenu.SetLabel(ID_ITEM_START, "Start")
            # self.popupmenu.SetLabel(ID.ID_LOCK, "Lock")

            # if status_text == Messages.STATUS_LOCK:
            #     self.popupmenu.SetLabel(ID.ID_LOCK, "Unlock")
            self.parent.PopupMenu(self.popupmenu)

    def resetPin(self, event):
        ConfigKmc(self, self.row, self.server)


    def startJob(self, event):
        try:
            row = self.jobList.currentItem
            col = Messages.RUN_JOB_FIELDS.get(Messages.JOB_STATUS, "")[0]
            text = self.jobList.getColumnText(row,col)
            # item = self.jobList.setColumnText()
            if text == Messages.STATUS_PUBLIC or text == Messages.STATUS_PRIVATE:
                # response = self.server.unLock(id=self.jobList.datas[self.row]['id'])
                # flag = showStatusMessage(response['status'], self.server)
                # if flag:
                self.server.CIM_StopTask(int(self.jobList.getColumnText(
                    row, Messages.RUN_JOB_FIELDS.get(Messages.JOB_ID, "")[0])))
                self.jobList.setColumnText(row, col, Messages.STATUS_STOPPING)

            else:

                ConfigJobDialog(self)

            self.jobList.InitStatus(row, col)
            self.jobList.Refresh()
        except Exception as e:
            print(e)

    def onInfo(self, event):
        if type(self.jobList.GetPyData(self.jobList.currentItem)) == list:
            PanView(self, self.server)
        else:
            FileView(self, self.server)

    def repairCard(self, event):
        RepairJob(self, self.server)

    def delete(self, event):
        dlg = wx.MessageDialog(self, 'Are you delete?',
                               'Hint',
                               wx.YES_NO | wx.ICON_WARNING
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
        if dlg.ShowModal() == wx.ID_YES:
            # response = self.server.deleteUser(id=self.dvc.datas[self.row]['id'])
            # flag = showStatusMessage(response['status'], self.server)
            # if flag:
            status = self.server.CIM_DelJob(int(self.jobList.getColumnText(self.jobList.currentItem,
                                                              Messages.RUN_JOB_FIELDS.get(Messages.JOB_ID)[0])))
            if status:
                pub.sendMessage("status", message=status)
            else:

                panel_delete = wx.Window.FindWindowById(ID.ID_NOTEBOOK_DELETEJOB)
                if panel_delete:
                    jobList = panel_delete.jobList
                    jobList.addItem(self.jobList.getColumnText(self.jobList.currentItem, Messages.RUN_JOB_FIELDS.get(Messages.JOB_ID)[0]),
                                     )
                self.jobList.DeleteItem(self.jobList.currentItem)
        dlg.Destroy()
