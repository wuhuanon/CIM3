import struct
import time
from SocketTCp.SocketTCp import ClientSocket
from instruct_parse.ClientServerInterface import BaseServer
from instruct_parse.ParseHeaderRes import *

ipadddress=(("10.100.102.66", 63994))
class CIIssu(BaseServer):
    def __init__(self, address=ipadddress):
        self.__conn = ClientSocket()
        self.address = address
        super().__init__(address, self.__conn)

    def SetStatusByIdx(self, panIdx, err=0):
        buff = struct.pack("IH", panIdx, err)
        buff = SetProtocolHeader(FCPS_MODULE_CI, CI_INS_SET_STATUS_BY_INDEX, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        return status
def f(ipaddress):
    for i in range(100):
        CI = CIIssu(ipaddress)
        print(CI.connect(False))
        print(CI.SetStatusByIdx(i))
        print(123)
        time.sleep(3)
        CI.close()
if __name__ == "__main__":
    import time
    from multiprocessing import Process



    ipa = [("10.100.102.66", 63994), ("10.100.102.66", 64006)]
    for i in range(2):
        print()
        p = Process(target=f, args=(ipa[i],))
        p.start()
        # p.join()
    # print(time.strptime("2020-10-26 16:32:25", "%Y-%m-%d %H:%M:%S"))

