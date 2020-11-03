import wx

import os, sys

# try:
#     dirName = os.path.dirname(os.path.abspath(__file__))
# except:
#     dirName = os.path.dirname(os.path.abspath(sys.argv[0]))
#
# sys.path.append(os.path.split(dirName)[0])


from wx.lib.agw import ultimatelistctrl as ULC

from instruct_parse.ClientServerInterface import ClientServerInterface


class MyListCtrl(ULC.UltimateListCtrl):

    def __init__(self, parent, id=-1, fields={},size=(-1, -1), style = ULC.ULC_REPORT|ULC.ULC_VIRTUAL
                                                                      |ULC.ULC_HRULES|ULC.ULC_VRULES|ULC.ULC_SINGLE_SEL
                                                                    ):

        ULC.UltimateListCtrl.__init__(self, parent, id,size=size,
                                      agwStyle=style)
        self.server = ClientServerInterface(1)
        self.currentItem = None
        width = self.GetSize().width
        count = 0
        for key, value in sorted(fields.items(), key=lambda x: x[1][0]):

            self.InsertColumn(value[0], key, width=width // 100 * value[1])
            if count == len(fields)-1:
                self.SetColumnWidth(value[0], ULC.ULC_AUTOSIZE_FILL)
            count += 1

        self.Bind(ULC.EVT_LIST_ITEM_SELECTED, self.onSelect)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
        self._mainWin.Bind(wx.EVT_SCROLLWIN, self.OnScoll)

    def getColumnText(self, index, col):
        # print(index)

        item = self.GetItem(index, col)
        return item.GetText()
    
    def setColumnText(self, index, col, text):
        item = self.GetItem(index, col)
        item.SetText(text)
        self.SetItem(item)

    def setColumnText2(self, item, text):
        item.SetText(text)
        self.SetItem(item)

    def SerachItem(self, col, string):
        count = self.GetItemCount()
        for i in range(count):
            if str(string) in self.getColumnText(i, col):
                return self.GetItem(i, col)

    def OnMouse(self, event):
        if event.Dragging():
            return
        event.Skip()

        
    def onSelect(self, event):

        self.currentItem = event.GetIndex()
        self.Refresh()

    def OnScoll(self, event):
        event.Skip()
        self.Update()

