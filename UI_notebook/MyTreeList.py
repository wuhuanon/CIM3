import collections

import wx
import wx.lib.agw.hypertreelist as HTL
from Control_id.config_premession import *
from UI_notebook.ui_Dialog.ui_addPan import AddPan
from UI_notebook.ui_Dialog.ui_addRepairJob import AddRepairJob
from UI_notebook.ui_Dialog.ui_progressGetPanInfo import ProgressPanInfo
from instruct_parse.ClientServerInterface import ClientServerInterface

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

class HyperTreeList(HTL.HyperTreeList):

    def __init__(self, parent, order_id, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=(600, 500),
                 style=wx.SUNKEN_BORDER,
                 agwStyle=wx.TR_HAS_BUTTONS | wx.TR_HAS_VARIABLE_ROW_HEIGHT | HTL.TR_HIDE_ROOT | HTL.TR_FULL_ROW_HIGHLIGHT,
                 log=None):

        HTL.HyperTreeList.__init__(self, parent, id, pos, size, style, agwStyle)
        self.parent = parent
        self.server = ClientServerInterface()
        self.order_id = order_id
        il = wx.ImageList(16, 16)

        for items in ArtIDs[1:-1]:
            bmp = wx.ArtProvider.GetBitmap(eval(items), wx.ART_TOOLBAR, (16, 16))
            il.Add(bmp)
        self.AssignImageList(il)
        self.orderItem = None
        self.AddColumn("File")
        self.AddColumn("All count")
        # self.AddColumn("Column 2")
        # self.SetMainColumn(0)  # the one with the tree in it...
        self.SetColumnWidth(0, 400)

        self.root = self.AddRoot("root")
        self.SetItemImage(self.root, 24, which=wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root, 13, which=wx.TreeItemIcon_Expanded)
        order_info = self.server.CIM_QueryOrderInfo(self.order_id)

        # order_lst = ["templ1", "templ2"]
        if order_info:

            self.orderItem = self.AppendItem(self.root, order_info[0][0])
            self.SetItemImage(self.orderItem, 24, which=wx.TreeItemIcon_Normal)
            self.SetItemImage(self.orderItem, 13, which=wx.TreeItemIcon_Expanded)
            file_lst = self.server.CIM_EnumOrderDataFile(self.order_id)
            # self.orderItem.SetData(order)
            # file_lst = ["file1", "file2", "file3"]
            for file_id in file_lst:
                file_info = self.server.CIM_QueryOrderDataFileInfo(self.order_id, file_id)
                if file_info and file_info[-2] >= 0:

                    child2 = self.AppendItem(self.orderItem, file_info[0], 1)
                    child2.SetData({"file_id": file_id, "data":None})
                    pan_count = file_info[1]
                    self.SetItemText(child2, str(pan_count), 1)
                # self.SetItemImage(file, 0, which=wx.TreeItemIcon_Normal)
                    self.SetItemImage(child2, 24, which=wx.TreeItemIcon_Normal)
                    self.SetItemImage(child2, 13, which=wx.TreeItemIcon_Expanded)
                    self.SetItem3State(child2, True)
                # child2.SetData([i for i in range(pan_count)])
            self.Expand(self.orderItem)
        self.Bind(HTL.EVT_TREE_ITEM_CHECKING, self.OnSelChanging)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnMouse)

    def OnSelChanging(self, event):
        item = event.GetItem()
        if item.Is3State():
            if item.Get3StateValue() == 1:
                item.Set3StateValue(0)
                self.GetMainWindow().RefreshLine(item)
                return
            event.Skip()
            return

        if self.getItemDepth(item) == 2:

            self.checkItem(item, False)
            self.checkItem(self.orderItem, False)

            self.orderItem = item
        event.Skip()

    def OnMouse(self, event):
        item = event.GetItem()
        if self.getItemDepth(item) == 3:
            itemData = item.GetData()
            dlg = AddPan(self, item.Get3StateValue(), itemData.get("file_id", 0), itemData.get("data", None))
            itemData["data"] = dlg.data
            item.Set3StateValue(dlg.check_flag)
        event.Skip()

    def getItemDepth(self, item):
        nDepth = 0

        while (item):
            item = self.GetItemParent(item)
            nDepth += 1
        return nDepth

    def checkItem(self,item, bool):
        while item and self.getItemDepth(item) != 2:
            item = self.GetItemParent(item)

        if item :
            self.AutoCheckChild(item, bool)

    def AutoCheckChild(self, item, checked):

        (child, cookie) = self.GetFirstChild(item)

        torefresh = False
        if item.IsExpanded():
            torefresh = True

        while child:
            if child.GetType() == 1:
                self.CheckItem2(child, checked, torefresh=torefresh)
            self.AutoCheckChild(child, checked)
            (child, cookie) = self.GetNextChild(item, cookie)

    def GetAllChildren(self, item_obj):

        item_list = []
        (item, cookie) = self.GetFirstChild(item_obj)
        while item:
            item_list.append(item)
            # if self.custom_tree.HasChildren(item):
            #     self.GetAllChildren(item, childrenlist)
            (item, cookie) = self.GetNextChild(item_obj, cookie)

        return item_list

    def GetCheckedPan(self, job_type):
        AllPan = collections.OrderedDict()
        list_item = []
        (item, cookie) = self.GetFirstChild(self.orderItem)
        while item:
            if item.Get3StateValue()>0:


                list_item.append(item)

            (item, cookie) = self.GetNextChild(self.orderItem, cookie)
        file_count = len(list_item)
        dlg = wx.ProgressDialog("Progress", "", style=wx.PD_APP_MODAL, parent=self)
        for item in list_item:
            dlg.Update(0, item.GetText())
            dlg.Fit()
            itemData = item.GetData()
            AllPan[(itemData.get("file_id"), item.GetText())] = self.getSelectPans(item, job_type, dlg, item.Get3StateValue()==1)

        dlg.Destroy()
        return {(self.order_id, self.orderItem.GetText()): AllPan}

    def getSelectPans(self, item, job_type, dlg, check):
        itemData = item.GetData()
        file_id = itemData.get("file_id", 0)
        panData = itemData.get("data", None)

        def changeSelect(data):
            data[-1] = True

            return data
        if panData is None:
            panData = []
            file_info = self.server.CIM_QueryOrderDataFileInfo(self.order_id, file_id)
            if file_info:
                file_pans = self.server.CIM_QueryOrderDataFilePAN(self.order_id, file_id, 0, file_info[1])
                file_id_list = list(map(lambda x: x[0], file_pans))
                # active_records = self.server.QueryRecordCountInActiveJob(file_id_list)
                # terminat_records = self.server.QueryLogCountInTerminatedJob(file_id_list)
                len_pans = len(file_pans)
                for i in range(len_pans):
                    l = [file_id_list[i], str(i), str(file_pans[i][1]), None, None, True]
                    panData.append(l)
                itemData["data"] = panData

        if check:
            panData = list(map(changeSelect , panData))

        data = list(filter(lambda x: x[-1], panData))
        dic = dict(zip([i[0] for i in data], data))
        lst1 = filter(lambda x: x[3] is None, data)
        lst2 = [i[0] for i in lst1]
        lengths = len(lst2)
        # max = 80
        # if lengths%5000:
        #     max = lengths//5000+2
        # dlg = wx.ProgressDialog("Progress dialog example",
        #                         "An informative message",
        #                         maximum=max,
        #                         parent=self,
        #                         style=0
        #                               | wx.PD_APP_MODAL
        #                               | wx.PD_ESTIMATED_TIME
        #                               | wx.PD_REMAINING_TIME
        #                         # | wx.PD_AUTO_HIDE
        #                         )
        # keepGoing = True
        # count = 0
        # while keepGoing and count < max:
        #     count += 1
        #     wx.MilliSleep(250)
        #     # wx.Yield()
        #
        #     if count >= max / 2:
        #         (keepGoing, skip) = dlg.Update(count, "Half-time!")
        #     else:
        #         (keepGoing, skip) = dlg.Update(count)
        # dlg.Destroy()

        sept = 5000
        count = len(lst2)
        active_records = []
        terminat_records = []
        if count>=10000:

            offect = count//sept
            index = 0
            if offect % sept:
                dlg.SetRange(offect*2+3)
            else:
                dlg.SetRange(offect*2+1)
            chunk_lst = [lst2[i:i + sept] for i in range(0, len(lst2), sept)]
            for i in chunk_lst:
                active_record = self.server.QueryRecordExistInActiveJob(self.order_id, i)
                active_records.extend(active_record)
                dlg.Update(index + 1)
                index += 1
                terminat_record = self.server.QueryLogExistInFinishedJob(self.order_id, i)
                terminat_records.extend(terminat_record)
                dlg.Update(index+1)
                index += 1
        else:
            active_records = self.server.QueryRecordExistInActiveJob(self.order_id, lst2)
            terminat_records = self.server.QueryLogExistInFinishedJob(self.order_id, lst2)
        if len(active_records) != len(terminat_records):
            return []
        # while count > 0:
        #     count = min(10000, count)
        #     active_record = self.server.QueryRecordCountInActiveJob(lst2[start_index:start_index+count])
        #     active_records.extend(active_record)
        #     (keepGoing, skip) = dlg.Update(dlg.GetValue()+1)
        #     terminat_record = self.server.QueryLogCountInTerminatedJob(lst2[start_index:start_index+count])
        #     terminat_records.extend(terminat_record)
        #     (keepGoing, skip) = dlg.Update(dlg.GetValue()+1)
        #     start_index += count
        #     count = lengths-count
        for i in range(len(lst2)):
            dic[lst2[i]][3] = str(active_records[i])
            dic[lst2[i]][4] = str(terminat_records[i])
        result = []
        def GetItemEnable(item):
            if data[item][3] is None:
                pan_id = data[item][0]
                active_records = self.server.QueryRecordExistInActiveJob(self.order_id, [pan_id])
                data[item][3] = str(active_records[0])
                terminat_records = self.server.QueryLogExistInFinishedJob(self.order_id, [pan_id])
                data[item][4] = str(terminat_records[0])
            if job_type == TASK_TYPE_COMMON:
                return (data[item][3] == "0" and data[item][4] == "0") or data[item][3] is None
            else:
                return (data[item][3] == "0" and data[item][4]) or data[item][3] is None
        for i in range(len(data)):
            if GetItemEnable(i) and data[i][-1]:
                result.append((data[i][1], data[i][2]))
        return result

    def getItemSelect(self, item_obj):
        (item, cookie) = self.GetFirstChild(item_obj)
        while item:
            if self.IsItemChecked(item):
                return True

            # if self.custom_tree.HasChildren(item):
            #     self.GetAllChildren(item, childrenlist)
            (item, cookie) = self.GetNextChild(item_obj, cookie)
        return False

    def isSelect(self):
        return self.orderItem and self.getItemSelect(self.orderItem)