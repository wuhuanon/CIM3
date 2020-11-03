import os
import random
import socket
import json
import struct
import time

from win32gui import SendMessage
from ctypes import windll
from Control_id import ctrl_id as ID
import wx
from win32con import WM_CLOSE
from pubsub import pub

from SocketTCp.SocketTCp import ClientSocket
from instruct_parse import InstructionsModel as IM
from instruct_parse.ParseHeaderRes import SetProtocolHeader, CheckResp
from instruct_parse.CIstruct import define_cim_struct as CI
from instruct_parse.InstructionsModel import *
from tool.Single import singleton
from tool.api_parsechar import BinaryToChar, CharToBinary

from config.config_server.ApiConfig import ConfigFile

config = ConfigFile()
if __name__ == '__main__':
    KM = (("10.100.101.28", 9888))
    CIM = (("10.100.101.82", 20202))
else:
    CIM = (config.get("CIMServer", "address"), int(config.get("CIMServer", 'port')))

    KM = (config.get("KMServer", "address"), int(config.get("KMServer", 'port')))
CIF = (("10.100.102.66", 20201))
# KM = (("10.100.101.28", 9888))
# CIM = (("10.100.102.66", 20202))

DTS=(("10.100.101.28", 9666))


class BaseServer():
    def __init__(self, address, conn=None):
        self.address = address
        self.__conn = conn

    def close(self):
        self.__conn.close()

    def connect(self, receive_flag=True):
        self.__conn.connect(address=self.address)
        if receive_flag:
            data = self.__conn.recive(8)
            data = BinaryToChar(data)
            if data == CIM_SERVER_SUCCESS:
                return True
            else:
                return False
        return True

    def restart(self):
        self.__conn = ClientSocket()
        flag = self.connect()
        return flag

    def checkResponse(self, status):
        pass

    def sendRequestData(self, data):
        try:
            self.__conn.send(data)
            # return res
        except ConnectionAbortedError as e:
            import traceback
            traceback.print_exc()
            pass
            # return {'status':-7}
    def receiveData(self, MutilBlock=True):
        if not self.__conn.isConnect:
            pub.sendMessage("serverError")
        data = self.__conn.recive(12)
        result, status, length = CheckResp(data)

        # pub.sendMessage("status", message=status)
        if result:

            self.checkResponse(status)

            if length > 0:
                if MutilBlock:
                    data = self.__conn.recive(4)
                    count = struct.unpack('I', data)[0]
                    length -= 4
                    offset = 0
                    data = b''
                    if count > 0:
                        lgth = length//count
                    else:
                        lgth = 1

                    if lgth == 0:
                        lgth = length

                    if lgth > 1024:
                        lgth = 1024

                    while offset < length:
                        data1 = self.__conn.recive(lgth)
                        data += data1
                        offset += len(data1)
                        # time.sleep(0.001)
                    if len(data) != length:
                        return 0xFFFFFFFF, 0, b""
                    return status, count, data
                else:
                    lgth = length
                    if lgth > 1024:
                        lgth = 1024
                    offset = 0
                    data = b''
                    while offset < length:
                        rece_data = self.__conn.recive(lgth)
                        data += rece_data
                        offset += len(rece_data)
                        # time.sleep(0.001)
                    if len(data) != length:
                        return 0xFFFFFFFF, 0, b""
                    return status, 0, data
            else:
                return status, 0, b''

        else:
            return 0xFFFFFFFF, 0, b''
# from pubsub import pub
@singleton
class ClientServerInterface(BaseServer):

    def __init__(self, address=CIM):
        self.__conn = ClientSocket()
        self.address = address
        super().__init__(address, self.__conn)



    # def close(self):
    #     self.__conn.close()
    #
    # def connect(self):
    #     self.__conn.connect(connect=self.index)
    #
    #     data = self.__conn.recive(8)
    #     data = BinaryToChar(data)
    #     if data == CIM_SERVER_SUCCESS:
    #         return True
    #     else:
    #         return False

    def CIF_UploadDataFileBegin(self, file_name="", order_name="", pan_count = 0, status=0, file_desc = "",
                         key_base = b""):
        buff = CI.order_name_t(order_name).pack(True) + \
               CI.CI_magnetic_file_info_t(file_name, pan_count, status, file_desc).pack(True) + key_base

        buff = SetProtocolHeader(FCPS_MODULE_CIF, CIF_INS_NEW_DATA_FILE_BEGIN, len(buff)) + buff
        print(BinaryToChar(CI.order_name_t(order_name).pack(True)))
        print(BinaryToChar(CI.CI_magnetic_file_info_t(file_name, pan_count, status, file_desc).pack(True)))
        print(BinaryToChar(key_base))
        print(BinaryToChar(buff))
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        print(status)
        return status

    def CIF_UploadDataFile(self, PAN_name = "", EmbossData="", pICata=""):
        buff_emboss = struct.pack("%ds"% (len(EmbossData)), EmbossData.encode())
        buff_ci = struct.pack("%ds" % (len(pICata)), pICata.encode())
        pan = CI.PAN_name(PAN_name)
        length = struct.pack("HH", len(EmbossData), len(pICata))
        buff = pan.pack(True)  + length+\
             buff_emboss + buff_ci
        buff = SetProtocolHeader(FCPS_MODULE_CIF, CIF_INS_NEW_DATA_FILE_WRITE, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        return status

    def CIF_UploadDataFileCommit(self):
        buff = SetProtocolHeader(FCPS_MODULE_CIF, CIF_INS_NEW_DATA_FILE_COMMIT, 0)
        print(BinaryToChar(buff))
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        return status

    def CIF_UploadDataFileAbort(self):
        buff = SetProtocolHeader(FCPS_MODULE_CIF, CIF_INS_NEW_DATA_FILE_ABORT, 0)
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        return status

    def CIM_DelDataFile(self, file_name = ""):
        buff = CI.magnetic_file_name(file_name).pack(True)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, DP_INS_FILE_DEL, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        return status

    def CIM_EnumOrder(self):
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_ENUM_ORDER, 0)
        self.sendRequestData(buff)
        status, count, data = self.receiveData()
        length = struct.calcsize("I")
        offset = 0
        lst = []
        for i in range(count):
            order_id = struct.unpack("I", data[offset:offset+length])[0]
            offset += length
            lst.append(order_id)
        return lst

    def CIM_QueryOrderInfo(self, order_id):
        buff = struct.pack("I", order_id)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_ORDER_INFO, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        if status:
            return ""
        order_info, bank_name, kcv, key_type, diversify = \
            struct.unpack("=%ds%ds%dsII"%(CI.CI_order_info_t().sizeof(),
                                        CI.bank_name_t().sizeof(), CI.kcv_t().sizeof()), data)

        return CI.CI_order_info_t().unpack(order_info), CI.bank_name_t().unpack(bank_name), \
               CI.kcv_t().unpack(kcv), key_type, diversify

    def CIM_DelOrder(self, order_id):
        buff = struct.pack("I", order_id)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_DEL_ORDER, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        return status

    def CIM_EnumOrderDataFile(self, order_id):
        buff = struct.pack("I", order_id)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_ENUM_ORDER_DATA_FILE, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData()
        length = struct.calcsize("I")
        offset = 0
        lst = []
        for i in range(count):
            file_id = struct.unpack("I", data[offset:offset + length])[0]
            offset += length
            lst.append(file_id)
        return lst

    def CIM_QueryOrderDataFileInfo(self, order_id, file_id):
        buff = struct.pack("II", order_id, file_id)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_ORDER_DATA_FILE, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        if status:
            return CI.CI_magnetic_file_info_t().unpack(CI.CI_magnetic_file_info_t().pack(True))
        return CI.CI_magnetic_file_info_t().unpack(data)

    def CIM_QueryTemplateKeyInfo(self, order_name=""):
        buff = CI.order_name_t(order_name).pack(True)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_DT_KEY_INFO, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        if status:
            return ""
        return CI.order_key_info_t().unpack(data)



    def CIM_QueryOrderDataFilePAN(self,order_id, file_id=1, startIdx=0, count=0):

        search_count = count
        datas = b""
        status = 0
        while search_count > 0:
            search_count = min(50000, search_count)
            buff = struct.pack("IIIH",order_id, file_id, startIdx, search_count)
            buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_ORDER_DATA_FILE_PAN, len(buff)) + buff
            self.sendRequestData(buff)
            status, count1, data = self.receiveData(False)

            datas += data
            startIdx += search_count
            search_count = count-startIdx

        length = CI.CI_PAN_info_t().sizeof()
        offset = 0
        lst = []
        if status:
            return lst

        for i in range(count):
            pan_info = CI.CI_PAN_info_t().unpack(datas[offset:offset + length])
            offset += length
            lst.append(pan_info)
        return lst

    def CIM_DelOrderDataFile(self,order_id, file_id):
        buff = struct.pack("II",order_id, file_id)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_DEL_ORDER_DATA_FILE, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        return status

    def CIM_EnumMachine(self):
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_ENUM_MACHINE, 0)
        self.sendRequestData(buff)
        status, count, data = self.receiveData()
        length = struct.calcsize("I")
        offset = 0
        lst = []
        for i in range(count):
            dev_id = struct.unpack("I", data[offset:offset + length])[0]
            offset += length
            lst.append(dev_id)

        return lst

    def CIM_NewMachine(self, device_name="", ip="",status=1, desc =""):
        buff = CI.CI_device_info(device_name, ip, status,  desc).pack(True)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_NEW_MACHINE, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        if status:
            return status, ""
        return status, struct.unpack("I", data)[0]

    def CIM_UpdateMachine(self, dev_id=1, desc=""):
        buff = struct.pack("I", dev_id) + CI.CI_device_desc_t(desc).pack(True)

        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_UPDATE_MACHINE, len(buff)) + buff

        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        return status

    def CIM_QueryMachine(self, dev_id=0):
        buff = struct.pack("I", dev_id)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_MACHINE, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        if status:
            return "", "", 0, ""
        return CI.CI_device_info().unpack(data)

    def CIM_DelMachine(self, dev_id=""):
        buff = struct.pack("I", dev_id)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_DEL_MACHINE, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData()
        return status

    def CIM_NewJobBegin(self, order_id=0, job_desc=""):
        buff = struct.pack("I", order_id)  + \
               CI.CI_job_desc_t(job_desc).pack(True)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_NEW_JOB_BEGIN, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        return status

    def CIM_NewJobDataFile(self, file_id=1):
        buff = struct.pack("I", file_id)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_NEW_JOB_DATA_FILE, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        return status

    def CIM_NewJobUpload(self, pIdx = []):
        pan_count = len(pIdx)
        start_index = 0
        status = 0
        while pan_count > 0:
            pan_count = min(50000, pan_count)

            buff = struct.pack("H", pan_count) + b"".join(
                map(lambda x:struct.pack("I", x), pIdx[start_index: start_index + pan_count]))
            buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_NEW_JOB_PAN, len(buff)) + buff
            self.sendRequestData(buff)
            status, count, data = self.receiveData(False)
            if status:
                return status
            start_index += pan_count
            pan_count = len(pIdx)-start_index
        # print(data)
        return status


    def CIM_NewJobCommit(self):
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_NEW_JOB_COMMIT, 0)
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        if status or not data:
            return "", status
        return struct.unpack("I", data)[0], status

    def CIM_NewJobAbort(self):
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_NEW_JOB_ABORT, 0)
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        return status

    def CIM_EnumJob(self, order_id):
        buff = struct.pack("I", order_id)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_ENUM_JOB, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(True)

        length = struct.calcsize("I")
        offset = 0
        lst = []
        for i in range(count):
            job_id = struct.unpack("I", data[offset:offset + length])[0]
            offset += length
            lst.append(job_id)
        return lst

    def CIM_QueryJobInfo(self, order_id, job_id):
        buff = CI.job_ref_t(order_id, job_id).pack(True)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_JOB_INFO, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        if status:
            return CI.CI_job_info().unpack(CI.CI_job_info().pack(True))
        return CI.CI_job_info().unpack(data)

    def CIM_QueryTaskInfo(self, order_id, job_id):
        buff = CI.job_ref_t(order_id, job_id).pack(True)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_TASK_INFO, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        if status:
            return ""
        return CI.CI_task_runtime_info_t().unpack(data)

    def CIM_QueryIssueInfo(self, order_id, job_id):
        buff = CI.job_ref_t(order_id, job_id).pack(True)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_ISSUE_INFO, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        if status:
            return 0, 0, 0
        return CI.CI_job_issue_info_t().unpack(data)

    def CIM_QueryIssueInfo2(self, order_id, job_id):
        buff = CI.job_ref_t(order_id, job_id).pack(True)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_ISSUE_INFO, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        offset = 16
        length = CI.CI_active_task_info_t().sizeof()

        lst = []
        def gettaskInfo(count, data):
            offset = 0
            list_task = []
            for i in range(count):
                task_info = CI.CI_active_task_info_t().unpack(data[offset:offset + length])
                offset += length
                list_task.append(task_info)
            return list_task
        if data:
            count_public = struct.unpack("I", data[:4])[0]
            data_public = data[offset: offset+length*count_public]
            lst.append(gettaskInfo(count_public, data_public))
            offset += length*count_public

            count_private = struct.unpack("I", data[4:8])[0]
            data_private = data[offset: offset + length * count_private]
            lst.append(gettaskInfo(count_private, data_private))
            offset += length * count_private

            count_stopping = struct.unpack("I", data[8:12])[0]
            data_stopping = data[offset: offset + length * count_stopping]
            lst.append(gettaskInfo(count_stopping, data_stopping))
            offset += length * count_stopping

            count_stopped = struct.unpack("I", data[12:16])[0]
            data_stopped = data[offset: offset + length * count_stopped]
            lst.append(gettaskInfo(count_stopped, data_stopped))

        return lst


    def CIM_EnumTerminatedJobInfo(self):
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_ENUM_TERMINATED_JOB, 0)
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        length = struct.calcsize("I")
        offset = 0
        lst = []
        while offset<len(data):
            jobid = struct.unpack("I", data[offset:offset + length])[0]
            offset += length
            lst.append(jobid)
        #
        # for i in range(count):
        #     jobid = struct.unpack("I", data[offset:offset + length])[0]
        #     offset += length
        #     lst.append(jobid)

        return lst

    def CIM_QueryLogByIndex(self, order_id, job_id, startIdx, count):
        search_count = count
        datas = b""
        status = 0
        while search_count > 0:
            search_count = min(50000, search_count)
            buff =  CI.job_ref_t(order_id, job_id).pack(True) + struct.pack("IH",  startIdx, search_count)
            buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_LOG_BY_INDEX, len(buff)) + buff
            self.sendRequestData(buff)
            status, count1, data = self.receiveData(False)
            datas += data
            startIdx += search_count
            search_count = count - startIdx

        length = CI.PAN_CI_log_t().sizeof()
        offset = 0
        lst = []
        if status:
            return lst
        for i in range(count):
            pan_log = CI.PAN_CI_log_t().unpack(datas[offset:offset + length])
            offset += length
            lst.append(pan_log)
        return lst

    def CIM_QueryLogByTime(self,order_id, job_id, time1, time2):
        buff = CI.job_ref_t(order_id, job_id).pack(True) + CI.tm(time1).pack(True) + CI.tm(time2).pack(True)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_LOG_BY_TIME, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(True)
        length = CI.PAN_CI_log_t().sizeof()
        offset = 0
        lst=[]
        for i in range(count):
            pan_log = CI.PAN_CI_log_t().unpack(data[offset:offset + length])
            offset += length
            lst.append(pan_log)
        return lst

    def CIM_QueryLogByPan(self, order_id, job_id, pan):
        buff = CI.job_ref_t(order_id, job_id).pack(True) + CI.PAN_name(pan).pack(True)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_LOG_BY_PAN, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(True)
        length = CI.PAN_CI_log_t().sizeof()
        offset = 0
        lst = []
        for i in range(count):
            pan_log = CI.PAN_CI_log_t().unpack(data[offset:offset + length])
            offset += length
            lst.append(pan_log)
        return lst

    def CIM_QueryLogByTimeAndPAN(self, order_id, job_id, pan, time1, time2):
        buff = CI.job_ref_t(order_id, job_id).pack(True) + CI.tm(time1).pack(True) + CI.tm(time2).pack(True)+ CI.PAN_name(pan).pack(True)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_LOG_BY_TIME_AND_PAN, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(True)
        length = CI.PAN_CI_log_t().sizeof()
        offset = 0
        lst = []
        for i in range(count):
            pan_log = CI.PAN_CI_log_t().unpack(data[offset:offset + length])
            offset += length
            lst.append(pan_log)
        return lst

    def CIM_GetTaskEvent(self):
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_FETCH_TASK_EVENT, 0)
        self.sendRequestData(buff)
        status, count, data = self.receiveData(True)
        length = CI.CI_task_event_t().sizeof()
        offset = 0
        lst = []
        for i in range(count):
            task_event = CI.CI_task_event_t().unpack(data[offset:offset + length])
            offset += length
            lst.append(task_event)

        return lst

    def CIM_GetRunningTaskIssueInfo(self):
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_RUNNING_TASK_ISSUE_INFO, 0)
        self.sendRequestData(buff)
        status, count, data = self.receiveData(True)
        length = CI.CI_task_issue_info_t().sizeof()
        offset = 0
        lst = []
        for i in range(count):
            task_issue = CI.CI_task_issue_info_t().unpack(data[offset:offset + length])
            offset += length
            lst.append(task_issue)

        return lst

    def CIM_GetStoppedTaskIssueInfo(self, taskId):
        buff = struct.pack("I", taskId)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_STOPPED_TASK_ISSUE_INFO, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        if status:
            return (0, 0, 0)
        return CI.CI_task_issue_info_t().unpack(data)

    def GetTask_port(self, task_id):
        buff = struct.pack("I", task_id)
        buff = SetProtocolHeader(10, 8, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        if status:
            return ""
        return struct.unpack("H", data)

    def CIM_GetTaskLockEvent(self):
        pass

    def CIM_GetTaskTerminateEvent(self):
        pass

    def QueryRecordExistInActiveJob(self,order_id, panId_list):

        search_count = len(panId_list)
        start_index = 0
        datas = b""
        while search_count > 0:
            search_count = min(10000, search_count)
            buff = struct.pack("IH",order_id, search_count) + b"".join(
                map(lambda x:struct.pack("I", x), panId_list[start_index: start_index+search_count]))
            buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_RECORD_EXIST_IN_ACTIVE_JOB, len(buff)) + buff
            self.sendRequestData(buff)
            status, count, data = self.receiveData(False)
            datas += data
            start_index += search_count
            search_count = len(panId_list) - start_index
        length = struct.calcsize("I")
        offset = 0
        lst = []
        if datas:
            for i in range(len(panId_list)):
                record_count = struct.unpack("I", datas[offset:offset + length])[0]
                offset += length
                lst.append(record_count)
        return lst

    def QueryLogExistInFinishedJob(self,order_id, panId_list):

        search_count = len(panId_list)
        start_index = 0
        datas = b""
        while search_count > 0:
            search_count = min(10000, search_count)
            buff = struct.pack("IH", order_id, search_count) + b"".join(
                map(lambda x: struct.pack("I", x), panId_list[start_index: start_index+search_count]))
            buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_LOG_EXIST_IN_FINISHED_JOB, len(buff)) + buff
            self.sendRequestData(buff)
            status, count, data = self.receiveData(False)
            datas += data
            start_index += search_count
            search_count = len(panId_list) - start_index
        length = struct.calcsize("I")
        offset = 0
        lst = []
        if datas:
            for i in range(len(panId_list)):
                record_count = struct.unpack("I", datas[offset:offset + length])[0]
                offset += length
                lst.append(record_count)
        return lst



    def CIM_QueryRecordInActiveJob(self, order_id, pan_id):
        buff = struct.pack("II", order_id, pan_id)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_RECORD_IN_ACTIVE_JOB, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData()

        length = CI.CI_job_record_t().sizeof()
        offset = 0
        lst = []
        for i in range(count):
            job_record = CI.CI_job_record_t().unpack(data[offset:offset + length])
            offset += length
            lst.append(job_record)
        return lst

    def CIM_QueryLoggedRecordInFinishedJob(self, order_id, pan_id):
        buff = struct.pack("II", order_id, pan_id)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_QUERY_LOGGE_RECORD_IN_FINISHED_JOB, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData()

        length = CI.CI_job_record_t().sizeof()
        offset = 0
        lst = []
        for i in range(count):
            job_record = CI.CI_job_record_t().unpack(data[offset:offset + length])
            offset += length
            lst.append(job_record)
        return lst

    def CIM_StartTask(self, order_id, jobId=1, device_id=1, kmc="", diversifyKMC=0):
        buff = CI.job_ref_t(order_id, jobId).pack(True) + struct.pack("I", device_id) + CI.kcv_t(kmc).pack(True) \
               + struct.pack("I", diversifyKMC)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_START_TASK, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        # print(BinaryToChar(data), data)
        if data:
            print(struct.unpack("H", data))
        return status

    def CIM_StopTask(self, order_id, jobId):
        buff = CI.job_ref_t(order_id, jobId).pack(True)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_STOP_TASK, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)

        return status

    def CIM_FinishTask(self, order_id, jobId, desc=""):
        buff = CI.job_ref_t(order_id, jobId).pack(True) + CI.CI_job_desc_t(desc).pack(True)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_FINISH_TASK, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)

        return status

    def CIM_FinishOrder(self, order_id):
        buff = struct.pack("I", order_id)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_FINISH_ORDER, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)

        return status

    def CIM_GetTaskDevicePort(self, order_id, job_id):
        buff = CI.job_ref_t(order_id, job_id).pack(True)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_GET_TASK_DEVICE_PORT, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        if status:
            return status
        return struct.unpack("IH", data)

    def CIM_FetchEvent(self):
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_FETCH_ORDER_EVENT, 0)
        self.sendRequestData(buff)
        status, count, data = self.receiveData()
        length = CI.CI_event_t().sizeof()
        offset = 0
        lst = []
        for i in range(count):
            job_record = CI.CI_event_t().unpack(data[offset:offset + length])
            offset += length
            lst.append(job_record)
        return lst

    def CIM_FetchTaskEvent(self, order_id):
        buff = struct.pack("I", order_id)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_FETCH_TASK_EVENT, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData()
        print(status)
        length = CI.CI_order_event_t().sizeof()
        offset = 0
        lst = []
        for i in range(count):
            job_record = CI.CI_order_event_t().unpack(data[offset:offset + length])
            offset += length
            lst.append(job_record)
        return lst

    def CIM_FetchFileEvent(self, order_id):
        buff = struct.pack("I", order_id)
        buff = SetProtocolHeader(FCPS_MODULE_CIM, CIM_INS_FETCH_FILE_EVENT, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData()
        print(status)
        length = CI.CI_order_event_t().sizeof()
        offset = 0
        lst = []
        for i in range(count):
            job_record = CI.CI_order_event_t().unpack(data[offset:offset + length])
            offset += length
            lst.append(job_record)
        return lst


class KMClientServerInterface(BaseServer):

    def __init__(self, address=KM):
        self.__conn = ClientSocket()
        self.address = address
        super().__init__(address, self.__conn)
        self.__conn.settimeout(5)

    def KM_EnumPDK(self, addr, cls):
        buff = CI.pdk_key_addr_t(addr, cls).pack(True)
        buff = SetProtocolHeader(FCPS_MODULE_KEY_MGMT, KM_INS_ENUM_PDK, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData()
        length = CI.pdk_enum_info_t().sizeof()
        offset = 0
        lst = []
        for i in range(count):
            key_type, keyinfo = CI.pdk_enum_info_t().unpack(data[offset:offset + length])

            offset += length
            lst.append((key_type, keyinfo))
        return lst




class DPClientServerInterface(BaseServer):

    def __init__(self, address=DTS):
        self.__conn = ClientSocket()
        self.address = address
        super().__init__(address, self.__conn)

    def DPS_ExportDataFileBegin(self, file_name=""):
        buff = CI.magnetic_file_name(file_name).pack(True)
        buff = SetProtocolHeader(FCPS_MODULE_DP, DP_INS_EXPORT_DATA_FILE_BEGIN, len(buff)) + buff
        self.sendRequestData(buff)
        status, count, data = self.receiveData(False)
        # print(status, count, data)
        length_template = CI.c_template_info().sizeof()
        print(len(data[length_template+20:]))
        # if data:
        #     length_template = CI.c_template_info().sizeof()
        #     print(length_template)
        #     template_info = CI.c_template_info().unpack(data[0:length_template])
        #
        #     print(template_info)
        #     key_info = CI.order_key_info_t().unpack(data[length_template:])
        #     print(key_info)
        return data[length_template+20:]

if __name__ == "__main__":
    CIM1 = ClientServerInterface(CIF)
    print(CIM1.connect())
    DTS = DPClientServerInterface()
    print(DTS.connect(False))
    data = DTS.DPS_ExportDataFileBegin("MasterCard Template_00__5371640300036783.txt")
    # print(len(data))
    print(BinaryToChar(data))
    # data = CharToBinary(
    #     "16004D61737465724361726420466C657870617930303031000000000000000000000000000000000000000000000000000000000000000000000000000000000000060035333731363400000000000002000000020000000200000002000000050000008F4E4E825770646B0000000010000000B8A80D6CB9ABE053B0539B46E348AC22FCD06200D3ABF90028D162000000000005000000948CF0DA874F400000000000100000001879B094360F3FF564145DB71A62F809FCD06200D7ABF90028D16200000000000500000092006F342C4F400000000000100000000E88DFC596A593751FA81F788D484B6EFCD06200CFABF90028D1620000000000050000001DB2AC3EA54F40000000000000000000")
    # print(CI.order_key_info_t().unpack(data))
    # # print("343ADB440800020000000000")
    # # print(123)
    # print(CIM1.CIF_UploadDataFileBegin("MasterCard Template_00__5371640300036782.txt", "order_name3", pan_count=100, status=1,
    #                                  key_base=data), "ppp")
    print(CIM1.CIF_UploadDataFileBegin("file1", "order1", pan_count=100, status=1,
                                     key_base=data), "ppp")
    #"343ADB4406000100C60200000B006F726465725F6E616D653400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002800446174615F54656D706C6174655F30305F30305F343231333239303030313130303030302E7478740000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000640000000100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000D005649534120534F415030303031000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060034323133323900000000000002000000020000000200000002000000050000001DB2AC3EA570646B0000000010000000B58A340E9A0CEF42E20DB0BAA6F75B70FCD0620045FBC90028D16200000000000500000092006F342C4F400000000000100000002E78878E4AADA60F19896CBDCE3555FAFCD0620049FBC90028D162000000000005000000116A98C6CB4F400000000000100000005F4018EA4FDE7EA01CFECC287895CAADFCD0620041FBC90028D162000000000005000000948CF0DA874F40000000000000000000"
    # gauge = 0
    # start_time = time.perf_counter()
    # for i in range(100):
    #     pan = [str(random.randint(0, 9)) for _ in range(16)]
    #     print(CIM1.CIF_UploadDataFile("421" + "".join(pan), "", ""))
    # # print(CIM1.CIF_UploadDataFile("4212198536231189738"))
    # #     # if i%1000 == 0 and i > 0:
    # #     #     gauge += 1
    # #     #     end_time = time.perf_counter()
    # #     #     print(gauge, "%", "    ", end_time-start_time)
    # #     #     start_time = time.perf_counter()
    # # # print(CIM1.CIF_UploadDataFileAbort(), "asd")
    # print(CIM1.CIF_UploadDataFileCommit(), "sfh")

    # pan = []
    # for i in range(100):
    #     pan.append("".join([str(random.randint(0, 9)) for _ in range(18)]))

    # CIM1.CIM_NewJobUpload(pan)
    # print(BinaryToChar(struct.pack("30s", "Data Template_02".encode())))
#     print("***************************************************************************************")
# # ************************************************************************************************
    CIM2 = ClientServerInterface()
    print(CIM2.connect())
    # print(CIM2.CIM_QueryLogByPan(2, 3, "421%"))
    # time1 = time.strptime("2020-10-26 8-00-00", "%Y-%m-%d %H-%M-%S")
    # time2 = time.strptime("2020-10-27 23-00-00", "%Y-%m-%d %H-%M-%S")
    # print(CIM2.CIM_QueryLogByTime(2, 3, time1, time2))
    # print(""time.localtime())
    # print(time.localtime(0))
    # temps = time.strptime("1900-1-1 8-00-00", "%Y-%m-%d %H-%M-%S")
    # print(temps, type(temps))
    # print(time.struct_time((1900, 1, 1, 0, 0, 0, 0, 1, -1)))
#     # print(CIM2.CIM_DelDataFile("Data_Template_01_00_4213291000000000.txt"))
#     id = CIM2.CIM_EnumOrder()
    # print(id)
    # print(CIM2.CIM_QueryOrderInfo(2))
#     file_id = CIM2.CIM_EnumOrderDataFile(id)
#     print(file_id)
    # print(CIM2.CIM_QueryOrderDataFileInfo(id, file_id))
    # print(CIM2.CIM_QueryOrderDataFilePAN(id, file_id, 0, 100))
    # print(CIM2.CIM_NewMachine("me", "10.100.101.173", desc="jitai1"))
    # print(CIM2.CIM_EnumMachine())
    # print(CIM2.CIM_QueryMachine(1))
    # print(CIM2.CIM_UpdateMachine(1, "jitai2"))
    # print(CIM2.CIM_QueryMachine(1))


    # for i in range(200):
    # print(CIM2.CIM_NewJobBegin(2, "job_desc1234"))
    # print(CIM2.CIM_NewJobDataFile(2))
    # print(CIM2.CIM_NewJobUpload([i for i in range(100)]))
    # print(CIM2.CIM_NewJobUpload([13, 14, 15]))
    #     # print(CIM2.CIM_NewJobDataFile("SOAP_PPSE_02"))
    # print(CIM2.CIM_NewJobUpload([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
    # print(CIM2.CIM_NewJobCommit())
    #     if id[0]:
    #         print(CIM2.CIM_DelJob(id[0]))
    # print(CIM2.CIM_EnumJob(1))
    # print(CIM2.CIM_QueryJobInfo(1, 1))
    # print(CIM2.CIM_QueryTaskInfo(1, 1))
    # print(CIM2.CIM_QueryIssueInfo(2, 3))
    # print(CIM2.CIM_StartTask(2, 3, 1, "948CF0DA87", 0))
    # print(CIM2.CIM_GetTaskDevicePort(2, 3))
    # print(CIM2.CIM_StopTask(2, 3))
    # print(CIM2.CIM_EnumTerminatedJobInfo())
    # print(CIM2.CIM_QueryTerminatedJobInfo(14))
    # print(CIM2.CIM_GetTaskEvent())
    # print(CIM2.CIM_EnumActiveJobInfo())
    # print(CIM2.CIM_GetStoppedTaskIssueInfo(11))
    # print(CIM2.CIM_GetRunningTaskIssueInfo())

    #
    # print(CIM2.CIM_NewJobAbort())
    # print("-----------------------------------------------------------------------------------------")

    #
    # CIM3  = ClientServerInterface(2)
    # print(CIM3.connect())
    # print(CIM3.GetTask_port(1))
    # file_pans = CIM2.CIM_QueryDataFilePAN(5, 0, 100000)
    # file_id_list = list(map(lambda x:x[0], file_pans))
    # statrt_time = time.perf_counter()
    # active_records = CIM2.QueryRecordExistInActiveJob(2, [150, 151])
    # print(active_records)
    # terminat_records = CIM2.QueryLogExistInFinishedJob(2, [3, 4])
    # print(terminat_records)
    # activeRecord = CIM2.CIM_QueryRecordInActiveJob(2, 118)
    # print(activeRecord)
    # finishRecord = CIM2.QueryLoggedRecordInFinishedJob(2, 101)
    # print(CIM2.CIM_FetchEvent())
    # print(activeRecord)
    # print(active_records)
    # # print(active_records)
    # end_time = time.perf_counter()
    # print(end_time-statrt_time)
    # real = []
    # j = 0
    # len_pan = len(file_pans)
    # for i in range(len_pan):
    #     j += 1
    #     if j == 10000:
    #         j = 0
    #     # a = list(np.random.randint(10,size=19))
    #     # t1 = time.clock()
    #     l = [str(file_pans[i][1]), str(active_records[i]), str(terminat_records[i]), True]

        # l.append(l[1] == "0" and l[2] == "0")
        # real.append(l)

        # print(t2-t1, t3-t2, t4-t3, t5-t4)

    # print(end_time2-end_time)

    # KM = KMClientServerInterface(3)
    # KM.connect()




    # km = KMClientServerInterface()
    # print(km.connect())
    # print(km.KM_EnumPDK("VISA SOAP0001", 5))

