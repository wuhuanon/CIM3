import wx.lib.agw.hypertreelist as HTL
import wx
import wx.lib.agw.customtreectrl as CT
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

class BaseTreeList(HTL.HyperTreeList):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=(600, 500),
                 style=wx.SUNKEN_BORDER,
                 agwStyle=wx.TR_HAS_BUTTONS | HTL.TR_HIDE_ROOT | HTL.TR_HAS_VARIABLE_ROW_HEIGHT | HTL.TR_FULL_ROW_HIGHLIGHT):

        HTL.HyperTreeList.__init__(self, parent, id, pos, size, style, agwStyle)
        self.parent = parent
        self.server = ClientServerInterface()
        il = wx.ImageList(16, 16)

        for items in ArtIDs[1:-1]:
            bmp = wx.ArtProvider.GetBitmap(eval(items), wx.ART_TOOLBAR, (16, 16))
            il.Add(bmp)
        self.item = None


    def getItemDepth(self, item):
        nDepth = 0

        while (item):
            item = self.GetItemParent(item)
            nDepth += 1
        return nDepth



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
            (item, cookie) = self.GetNextChild(item_obj, cookie)

        return item_list


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
        return self.item and self.getItemSelect(self.item)