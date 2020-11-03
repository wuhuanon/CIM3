import wx
import abc
class BasePanel(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def OnInit(self):
        pass
if __name__ == "__main__":
    BasePanel()