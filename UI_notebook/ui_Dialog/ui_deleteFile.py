import wx
import wx.lib.agw.customtreectrl as CT
from pubsub import pub

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

class DeleteFile(wx.Dialog):
    def __init__(self, parent):
        super(DeleteFile, self).__init__(parent, title='Add', size=(635, 500))
        self.parent = parent
        self.checkCtrl = []
        self.server = parent.server
        self.InitUI()
        self.ShowModal()

    def InitUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        toolSizer = wx.BoxSizer(wx.HORIZONTAL)

        button = wx.Button(self, -1, "Delete")
        toolSizer.Add(button, 0, wx.ALL | wx.CENTER, 5)
        button.Bind(wx.EVT_BUTTON, self.OnDelete)
        self.tree = CT.CustomTreeCtrl(self, -1, agwStyle=wx.TR_HAS_BUTTONS | wx.TR_HAS_VARIABLE_ROW_HEIGHT |
                                                         CT.TR_HIDE_ROOT | CT.TR_FULL_ROW_HIGHLIGHT |
                                                         CT.TR_AUTO_CHECK_CHILD | CT.TR_AUTO_TOGGLE_CHILD |
                                                        CT.TR_AUTO_CHECK_PARENT
                                      )
        il = wx.ImageList(16, 16)

        for items in ArtIDs[1:-1]:
            bmp = wx.ArtProvider.GetBitmap(eval(items), wx.ART_TOOLBAR, (16, 16))
            il.Add(bmp)
        self.tree.AssignImageList(il)
        self.root = self.tree.AddRoot("")
        order_lst = self.server.CIM_EnumOrderName()
        # order_lst = ["templ1", "templ2"]
        for order in order_lst:
            child = self.tree.AppendItem(self.root, order)
            self.tree.SetItemImage(child, 24, which=wx.TreeItemIcon_Normal)
            self.tree.SetItemImage(child, 13, which=wx.TreeItemIcon_Expanded)
            file_lst = self.server.CIM_QueryOrderDataFile(order)
            child.SetData(order)
            # file_lst = ["file1", "file2", "file3"]
            for file in file_lst:
                child2 = self.tree.AppendItem(child, file, 1)
                pan_count = 0
                file_info = self.server.CIM_QueryDataFileInfo(file)
                if file_info:
                    pan_count = file_info[1][1]
                # self.tree.SetItemText(child2, str(pan_count), 1)
                # self.SetItemImage(file, 0, which=wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(child2, 24, which=wx.TreeItemIcon_Normal)
                self.tree.SetItemImage(child2, 13, which=wx.TreeItemIcon_Expanded)

                # child2.SetData([i for i in range(pan_count)])
        sizer.Add(toolSizer, 0, wx.EXPAND, 1)
        sizer.Add(self.tree, 1, wx.EXPAND, 1)
        self.SetSizer(sizer)

    def GetAllSelectFile(self, item_obj, files=[]):
        (item, cookie) = self.tree.GetFirstChild(item_obj)
        while item:
            if self.tree.IsItemChecked(item):
                files.append(item)
            if self.tree.ItemHasChildren(item):
                self.GetAllSelectFile(item, files)

            # if self.custom_tree.HasChildren(item):
            #     self.GetAllChildren(item, childrenlist)
            (item, cookie) = self.tree.GetNextChild(item_obj, cookie)

        return files

    def GetAllChildren(self, item_obj):

        item_list = []
        (item, cookie) = self.tree.GetFirstChild(item_obj)
        while item:
            item_list.append(item)
            # if self.custom_tree.HasChildren(item):
            #     self.GetAllChildren(item, childrenlist)
            (item, cookie) = self.tree.GetNextChild(item_obj, cookie)

        return item_list

    def OnDelete(self, event):
        files_item = self.GetAllSelectFile(self.root, [])
        for file_item in files_item:
            status = self.server.CIM_DelDataFile(self.tree.GetItemText(file_item))
            if status:
                pub.sendMessage("status", message=status)
            else:
                self.tree.Delete(file_item)
        lst = self.GetAllChildren(self.root)
        for i in lst:
            if not self.tree.HasChildren(i):
                self.tree.Delete(i)
                self.tree.RefreshLine(i)

