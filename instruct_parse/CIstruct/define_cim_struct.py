import struct
import sys
import time

from tool.api_parsechar import BinaryToChar, CharToBinary


MAGNE_NAME_LEN_MAX = 100
PAYMENT_NAME_MAX = 31
DATE_BUFF_MAX = 12
BANK_BUFF_MAX = 64
BIN_VALUE_MAX = 9
PROFILE_DGI_GROUP_MAX = PAYMENT_NAME_MAX*3
DESCRIPTION_MAX = 150
KEY_DEF_GROUP_MAX = 3340
PAN_NAME_LEN_MAX = 20
BANK_NAME_LEN_MAX=63
ORDER_NAME_LEN_MAX=63
BIN_NAME_LEN_MAX = 9
KCV_LEN_MAX=8
KEY_BUFF_LENMAX = 32
CI_JOB_DESC_LEN=255
KEY_DESC_LEN_MAX=255
CI_DATA_FILE_DESC_LEN=255

def removepad(a):

    if type(a) == bytes:
        endIndex = a.index(b"\00")
        return a[:endIndex]
    elif type(a) == str:
        endIndex = a.index(b"\00".decode())
        a.strip(a[:endIndex])

    else:
        return a


class DefineName(object):
    def __init__(self, data, maxLength):
        self.dataLength = len(data)
        if self.dataLength > maxLength:
            data = data[:maxLength]
        self.data = data
        self.maxLength = maxLength

        self.fmt = "@h%ds0H" % (maxLength+1)


    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.dataLength, self.data.encode("utf-8"))
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, value, isBuff = True):
        if isBuff:
            self.dataLength, self.data = struct.unpack(self.fmt, value)
        else:
            self.dataLength, self.data = struct.unpack(self.fmt, CharToBinary(value))

        self.data = self.data[:self.dataLength]
        # self.data = removepad(self.data)
        return self.data.decode('utf-8')


    def sizeof(self):
        return struct.calcsize(self.fmt)

class DefineBuffer(object):
    def __init__(self, data, maxLength):
        self.dataLength = len(CharToBinary(data))
        if self.dataLength > maxLength:
            data = data[:maxLength]
        self.data = data
        self.maxLength = maxLength

        self.fmt = "@i%ds0l" % maxLength


    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.dataLength, CharToBinary(self.data))
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, value, isBuff = True):
        if isBuff:
            self.dataLength, self.data = struct.unpack(self.fmt, value)
        else:
            self.dataLength, self.data = struct.unpack(self.fmt, CharToBinary(value))

        self.data = self.data[:self.dataLength]
        # self.data = removepad(self.data)
        return BinaryToChar(self.data)


    def sizeof(self):
        return struct.calcsize(self.fmt)

class magnetic_file_name(DefineName):
    def __init__(self, data=""):
        super(magnetic_file_name, self).__init__(data, MAGNE_NAME_LEN_MAX)

class CI_data_file_desc_t(DefineName):
    def __init__(self, data=""):
        super(CI_data_file_desc_t, self).__init__(data, CI_DATA_FILE_DESC_LEN)

class PAN_name(DefineName):
    def __init__(self, data=""):
        super(PAN_name, self).__init__(data, PAN_NAME_LEN_MAX)

class CI_device_name(DefineName):
    def __init__(self, data=""):
        super(CI_device_name, self).__init__(data, 63)

class CI_Desc(DefineName):
    def __init__(self, data=""):
        super(CI_Desc, self).__init__(data, 255)

class bank_name_t(DefineName):
    def __init__(self, data=''):
        super(bank_name_t, self).__init__(data, BANK_NAME_LEN_MAX)

class order_name_t(DefineName):
    def __init__(self, data=''):
        super(order_name_t, self).__init__(data, ORDER_NAME_LEN_MAX)

class bin_name_t(DefineName):
    def __init__(self, data=''):
        super(bin_name_t, self).__init__(data, BIN_NAME_LEN_MAX)

class key_desc_t(DefineName):
    def __init__(self, data=''):
        super(key_desc_t, self).__init__(data, KEY_DESC_LEN_MAX)

class kcv_t(DefineBuffer):
    def __init__(self, data=''):
        super(kcv_t, self).__init__(data, KCV_LEN_MAX)

class wrapped_symm_key_buf_t(DefineBuffer):
    def __init__(self, data=""):
        super(wrapped_symm_key_buf_t, self).__init__(data, KEY_BUFF_LENMAX)

class symm_key_enum_value_t(kcv_t):
    def __init__(self, kcv=''):
        super(symm_key_enum_value_t, self).__init__(kcv)

class bank_addr_t(bank_name_t):
    def __init__(self, addr=''):
        super(bank_addr_t, self).__init__(addr)

class ip_addr_t(DefineName):
    def __init__(self, ip_addr=""):
        super(ip_addr_t, self).__init__(ip_addr, 39)

class CI_device_desc_t(DefineName):
    def __init__(self, desc=""):
        super(CI_device_desc_t, self).__init__(desc, 255)

class CI_job_desc_t(DefineName):
    def __init__(self, desc=""):
        super(CI_job_desc_t, self).__init__(desc, CI_JOB_DESC_LEN)

class PAN_record_CI_info_t(object):
    def __init__(self, pan_name="", file_id=0, dev_id=0, status=0, datetime=0):
        self.pan_name = PAN_name(pan_name)
        self.file_id = file_id
        self.dev_id = dev_id
        self.status = status
        self.datetime = datetime
        self.fmt = "@%dsIIII0L" % (self.pan_name.sizeof())

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.pan_name.pack(True), self.file_id, self.dev_id, self.status, self.datetime)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff):
        if not isBuff:
            data = CharToBinary(data)
        self.pan_name, self.file_id, self.dev_id, self.status, self.datetime = struct.unpack(self.fmt, data)
        return PAN_name().unpack(self.pan_name), self.file_id, self.dev_id, self.status, self.datetime


class symm_key_ref_t:
    def __init__(self, key_type=0, kcv=''):
        self.key_type = key_type
        self.kcv = kcv_t(kcv)
        self.fmt = 'I%ds0l' % (kcv_t().sizeof())

    def pack(self, toBuff=True):
        buff = struct.pack(self.fmt, self.key_type, self.kcv.pack(True))
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)
        # return api_util.CharToBinary(self.packChar())
    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.key_type, self.kcv = struct.unpack(self.fmt, data)
        kcv = kcv_t().unpack(self.kcv)
        return self.key_type, kcv

    def sizeof(self):
        return struct.calcsize(self.fmt)

class c_template_define(object):
    def __init__(self, **kwargs):
        self.templ_name = kwargs.get("templ_name", "").encode('utf-8')
        self.user_status = int(kwargs.get("use_status", 0))
        self.templ_version = int(kwargs.get("templ_version", 0))
        self.creator_name = kwargs.get("creator_name", "").encode('utf-8')
        self.created_date = kwargs.get("created_date", "").encode('utf-8')
        self.payment_name = kwargs.get("payment_name", "").encode('utf-8')
        self.payment_version = kwargs.get("payment_version", "").encode('utf-8')
        self.bank_name = kwargs.get("bank_name", "").encode('utf-8')
        self.bin_value = kwargs.get("bin_value", "").encode('utf-8')
        self.card_name = kwargs.get("card_name", "").encode('utf-8')
        self.sup_pse_ppse = int(kwargs.get("sup_pse_ppse", 0))
        self.ppse_dgi_group = kwargs.get("ppse_dgi_group", "").encode('utf-8')
        self.pse_dgi_group = kwargs.get("pse_dgi_group", "").encode('utf-8')
        self.desc_value = kwargs.get("desc_value", "").encode('utf-8')
        self.profile_dgi_group = kwargs.get("profile_dgi_group", "").encode('utf-8')
        self.key_def_nums = int(kwargs.get("key_def_nums", 0))
        self.key_def_group = kwargs.get("key_def_group", "").encode('utf-8')
        self.fmt = "@{0}sii{1}s{2}s{3}s{4}s{5}s{6}s{7}si{8}s{9}s{10}s{11}si{12}s0l".format(PAYMENT_NAME_MAX, PAYMENT_NAME_MAX,
                                                                                           DATE_BUFF_MAX, PAYMENT_NAME_MAX,
                                                                                           PAYMENT_NAME_MAX, BANK_BUFF_MAX,
                                                                                           BIN_VALUE_MAX, BANK_BUFF_MAX,
                                                                                           PROFILE_DGI_GROUP_MAX,
                                                                                           PROFILE_DGI_GROUP_MAX,
                                                                                           DESCRIPTION_MAX,
                                                                                           PROFILE_DGI_GROUP_MAX,
                                                                                           KEY_DEF_GROUP_MAX)

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.templ_name, self.user_status, self.templ_version, self.creator_name,
                           self.created_date, self.payment_name, self.payment_version, self.bank_name, self.bin_value,
                           self.card_name, self.sup_pse_ppse, self.ppse_dgi_group, self.pse_dgi_group, self.desc_value,
                           self.profile_dgi_group, self.key_def_nums, self.key_def_group)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def uppack(self, data, isbuff=True):
        if not isbuff:
            data = CharToBinary(data)

        self.templ_name, self.user_status, self.templ_version, self.creator_name, self.created_date, self.payment_name, \
        self.payment_version, self.bank_name, self.bin_value, self.card_name, self.sup_pse_ppse, self.ppse_dgi_group,\
        self.pse_dgi_group, self.desc_value, self.profile_dgi_group, self.key_def_nums, self.key_def_group = \
            map(removepad, struct.unpack(self.fmt, data))
        # if tochar:
        return {"templ_name": self.templ_name.decode('utf-8'), "user_status": self.user_status,
                "creator_name": self.creator_name.decode("utf-8"), "templ_version": self.templ_version,
                "created_date": self.created_date.decode("utf-8"), "payment_name": self.payment_name.decode('utf-8'),
                "payment_version": self.payment_version.decode('utf-8'), "bank_name": self.bank_name.decode('utf-8'),
                "bin_value": self.bin_value.decode('utf-8'), "card_name": self.card_name.decode("utf-8"),
                "sup_pse_ppse":self.sup_pse_ppse, "ppse_dgi_group":self.ppse_dgi_group.decode('utf-8'),
                "pse_dgi_group": self.pse_dgi_group.decode('utf-8'), "desc_value": self.desc_value.decode('utf-8'),
                "profile_dgi_group": self.profile_dgi_group.decode('utf-8'), "key_def_nums": self.key_def_nums,
                "key_def_group": self.key_def_group.decode('utf-8')}
        # else:
        #     return {"templ_name": BinaryToChar(self.templ_name), "user_status": BinaryToChar(self.user_status),
        #             "creator_name": BinaryToChar(self.creator_name), "templ_version": BinaryToChar(self.templ_version),
        #             "created_date": BinaryToChar(self.created_date),
        #             "payment_name": BinaryToChar(self.payment_name),
        #             "payment_version": BinaryToChar(self.payment_version),
        #             "bank_name": BinaryToChar(self.bank_name),
        #             "bin_value": BinaryToChar(self.bin_value), "card_name": BinaryToChar(self.card_name),
        #             "sup_pse_ppse": BinaryToChar(self.sup_pse_ppse), "ppse_dgi_group": BinaryToChar(self.ppse_dgi_group),
        #             "pse_dgi_group": BinaryToChar(self.pse_dgi_group), "desc_value": BinaryToChar(self.desc_value),
        #             "profile_dgi_group": BinaryToChar(self.profile_dgi_group), "key_def_nums": BinaryToChar(self.key_def_nums),
        #             "key_def_group": BinaryToChar(self.key_def_group)}

    def sizeof(self):
        return struct.calcsize(self.fmt)




class PAN_CI_info(object):
    def __init__(self, panName= "", taskId = None):
        self.panName = panName
        self.taskId = taskId

    def pack(self, toBuff=True):
        buff = PAN_name(self.panName).pack(toBuff=True) + struct.pack('l', self.taskId)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        panLength = PAN_name().sizeof()
        if not isBuff:
            data = CharToBinary(data)
        panNameStruct, task = map(removepad, struct.unpack("%dsl0l"% panLength, data))
        panName = PAN_name().unpack(panNameStruct)
        return panName, task


class CI_PAN_info_t():
    def __init__(self, pan_id= "", pan_name = ""):
        self.panID = pan_id
        self.panName = PAN_name(pan_name)
        self.fmt = "I%ds" % self.panName.sizeof()

    def pack(self, toBuff=True):
        buff = struct.pack(self.fmt, self.panID, self.panName.pack(True))
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):

        if not isBuff:
            data = CharToBinary(data)
        self.panID, self.panName = struct.unpack(self.fmt, data)
        return self.panID, PAN_name().unpack(self.panName)

    def sizeof(self):
        return struct.calcsize(self.fmt)

class CI_device_info(object):
    def __init__(self, dev_name="", ip_addr="", status=0, desc=""):
        self.dev_name = CI_device_name(dev_name)
        self.ip_addr = ip_addr_t(ip_addr)
        self.status = status
        self.desc = CI_device_desc_t(desc)
        self.fmt = "@%ds%dsi%ds0l" %(self.dev_name.sizeof(), self.ip_addr.sizeof(), self.desc.sizeof())

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt,self.dev_name.pack(True), self.ip_addr.pack(True),self.status, self.desc.pack(True))
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, value, isBuff=True):
        if not isBuff:
            value = CharToBinary(value)
        self.dev_name, self.ip_addr,self.status, self.desc = struct.unpack(self.fmt, value)
        return CI_device_name().unpack(self.dev_name), ip_addr_t().unpack(self.ip_addr),self.status, CI_device_desc_t().unpack(self.desc)

class c_template_info(object):
    def __init__(self, name="", version=0):
        self.name = name
        self.version = version
        self.fmt = "@%dsi0l" % PAYMENT_NAME_MAX

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.name.encode('utf-8'), self.version)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, value, isBuff=True):
        if not isBuff:
            value = CharToBinary(value)
        self.name, self.version = map(removepad, struct.unpack(self.fmt, value))
        return self.name.decode('utf-8'), self.version

    def sizeof(self):
        return struct.calcsize(self.fmt)

class CI_magnetic_file_info_t(object):
    def __init__(self, file_name="", pan_count = 0, status=0, file_desc = ""):
        self.file_name = magnetic_file_name(file_name)
        self.pan_count = pan_count
        self.status = status
        self.file_desc = CI_data_file_desc_t(file_desc)
        self.fmt = "%dsii%ds0l" % (self.file_name.sizeof(), self.file_desc.sizeof())

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.file_name.pack(True), self.pan_count, self.status,
                           self.file_desc.pack(True))
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, value, isBuff=True):
        if not isBuff:
            value = CharToBinary(value)
        self.file_name, self.pan_count, self.status, self.file_desc = struct.unpack(self.fmt, value)
        return magnetic_file_name().unpack(self.file_name), self.pan_count,self.status, CI_data_file_desc_t().unpack(self.file_desc)

    def sizeof(self):
        return struct.calcsize(self.fmt)


class CI_job_info(object):
    def __init__(self, PanCount=0, status=0, desc=""):
        self.count = PanCount
        self.status = status
        self.desc = CI_job_desc_t(desc)
        self.fmt = "II%ds0L"%(self.desc.sizeof())

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.count, self.status, self.desc.pack(True))
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.count, self.status, self.desc = struct.unpack(self.fmt, data)

        return self.count, self.status, CI_job_desc_t().unpack(self.desc)

    def sizeof(self):
        return struct.calcsize(self.fmt)

class CI_active_job_info():
    def __init__(self, CI_job_info=None, kmc_vesion=0, CI_dev_ID=0):
        self.CI_job_info = CI_job_info
        if not self.CI_job_info:
            self.CI_job_info = CI_job_info()
        self.kmc_version = kmc_vesion
        self.CI_dev_ID = CI_dev_ID
        self.fmt = "@%dsii0l"% self.CI_job_info.sizeof()

    def pack(self, toBuff=False):
        buff = self.CI_job_info.pack(True) + struct.pack("ii", self.kmc_version, self.CI_dev_ID)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self,data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        CI_job, self.kmc_version, self.CI_dev_ID = struct.unpack(self.fmt, data)
        return self.CI_job_info.unpack(CI_job, True), self.kmc_version, self.CI_dev_ID

class data_file_CI_info():
    def __init__(self, numPan=0, okCount=0, failCount=0):
        self.numPan = numPan
        self.okCount = okCount
        self.failCount = failCount
        self.fmt = "@III"

    def pack(self, toBuff):
        buff = struct.pack(self.fmt, self.numPan, self.okCount, self.failCount)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.numPan, self.okCount, self.failCount = struct.unpack(self.fmt, data)
        return self.numPan, self.okCount, self.failCount

class CI_data_query_info():
    def __init__(self, panName="", status=0, datetime=0):
        self.panName = panName
        self.status = status
        self.datetime = datetime
        self.fmt = "@%dsii" % PAN_name().sizeof()

    def pack(self, toBuff=False):
        buff = PAN_name(self.panName).pack(True) + struct.pack("@ii", self.status, self.datetime)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        pan, self.status, self.datetime = struct.unpack(self.fmt, data)
        self.panName = PAN_name().unpack(pan)
        return self.panName, self.status, self.datetime

class CI_key_base_info_t(object):

    def __init__(self, bank_name='', bin_name='', pTK=symm_key_ref_t(), pPEK=symm_key_ref_t(),
                 pKMC=symm_key_ref_t(), pKMU=symm_key_ref_t(), diversify_kmc=0, diversify_kmu=0):
        self.bank_name = bank_name_t(bank_name)
        self.bin_name = bin_name_t(bin_name)
        self.TK = pTK
        self.PEK = pPEK
        self.KMC = pKMC
        self.KMU = pKMU
        self.divkmc = diversify_kmc
        self.divkmu = diversify_kmu
        self.fmt = '@%ds%dsxx%ds%ds%ds%dsII0l' % (
            self.bank_name.sizeof(),
            self.bin_name.sizeof(),
            self.TK.sizeof(),
            self.PEK.sizeof(),
            self.KMC.sizeof(),
            self.KMU.sizeof()
        )
    def pack(self, toBuff):
        buff = struct.pack(self.fmt, self.bank_name.pack(True), self.bin_name.pack(True), self.TK.pack(True),
                           self.PEK.pack(True), self.KMC.pack(True), self.KMU.pack(True), self.divkmc, self.divkmu)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.bank_name, \
        self.bin_name, \
        self.TK, \
        self.PEK, \
        self.KMC, \
        self.KMU, self.divkmc, self.divkmu = struct.unpack(self.fmt, data)
        return bank_name_t().unpack(self.bank_name), bin_name_t().unpack(self.bin_name), \
               symm_key_ref_t().unpack(self.TK), symm_key_ref_t().unpack(self.PEK),\
               symm_key_ref_t().unpack(self.KMC), symm_key_ref_t().unpack(self.KMU), self.divkmc, self.divkmu

    def sizeof(self):
        return struct.calcsize(self.fmt)


class symm_key_value_t(object):
    def __init__(self, mech_enc=0, keybuff="", kcv=""):
        self.mech_enc = mech_enc
        self.keybuff = wrapped_symm_key_buf_t(keybuff)
        self.kcv = kcv_t(kcv)
        self.fmt = "I%ds%ds0L" % (self.keybuff.sizeof(), self.kcv.sizeof())


    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.mech_enc, self.keybuff.pack(True), self.kcv.pack(True))
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.mech_enc, self.keybuff, self.kcv = struct.unpack(self.fmt, data)
        return self.mech_enc, wrapped_symm_key_buf_t().unpack(self.keybuff), kcv_t().unpack(self.kcv)

    def sizeof(self):
        return struct.calcsize(self.fmt)

class order_key_info_t(object):
    def __init__(self, bank_name='', bin_name='',TK_type=0, KMC_type=0,KMU_type=0,PEK_type=0, TK_kcv="",
                 pKMC=symm_key_value_t(), pKMU=symm_key_value_t(), pPEK=symm_key_value_t(), diversify_kmc=0, diversify_kmu=0):
        self.bank_name = bank_name_t(bank_name)
        self.bin_name = bin_name_t(bin_name)
        self.TK_type = TK_type
        self.KMC_type = KMC_type
        self.KMU_type = KMU_type
        self.PEK_type = PEK_type
        self.TK_kcv = kcv_t(TK_kcv)
        self.KMC = pKMC
        self.KMU = pKMU
        self.PEK = pPEK
        self.divkmc = diversify_kmc
        self.divkmu = diversify_kmu
        self.fmt = '@%ds%dsIIII%ds%ds%ds%dsII0l' % (
            self.bank_name.sizeof(),
            self.bin_name.sizeof(),
            self.TK_kcv.sizeof(),
            self.KMC.sizeof(),
            self.KMU.sizeof(),
            self.PEK.sizeof()
        )
    def pack(self, toBuff):
        buff = struct.pack(self.fmt, self.bank_name.pack(True), self.bin_name.pack(True), self.TK_type, self.KMC_type,
                           self.KMU_type, self.PEK_type, self.TK_kcv.pack(True), self.KMC.pack(True),
                           self.KMU.pack(True), self.PEK.pack(True), self.divkmc, self.divkmu)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.bank_name, \
        self.bin_name, \
        self.TK_type, \
        self.KMC_type, \
        self.KMU_type, \
        self.PEK_type, \
        self.TK_kcv, \
        self.KMC, \
        self.KMU, self.PEK, self.divkmc, self.divkmu = struct.unpack(self.fmt, data)
        return bank_name_t().unpack(self.bank_name), bin_name_t().unpack(self.bin_name), \
               self.TK_type, self.KMC_type, self.KMU_type, self.PEK_type, kcv_t().unpack(self.TK_kcv), \
               symm_key_value_t().unpack(self.KMC), symm_key_value_t().unpack(self.KMU),symm_key_value_t().unpack(self.PEK),\
               self.divkmc, self.divkmu

    def sizeof(self):
        return struct.calcsize(self.fmt)

class CI_job_base_info_t(object):
    def __init__(self, order_name="", job_desc="", job_type=1, numPAN=0, status=0):
        self.order_info = order_name_t(order_name)
        self.job_desc = CI_job_desc_t(job_desc)
        self.job_type = job_type
        self.numPan = numPAN
        self.status = status
        self.fmt = "@%ds%dsIII0L" % (self.order_info.sizeof(), self.job_desc.sizeof())

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.order_info.pack(True), self.job_desc.pack(True), self.job_type
                           , self.numPan, self.status)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.order_info, self.job_desc, self.job_type, self.numPan, self.status = \
            struct.unpack(self.fmt, data)

        return order_name_t().unpack(self.order_info), CI_job_desc_t().unpack(self.job_desc), self.job_type, \
               self.numPan, self.status

    def sizeof(self):
        return struct.calcsize(self.fmt)

class CI_task_static_info_t(object):
    def __init__(self, task_id=0, job_base_info = CI_job_base_info_t(), key_base_info=order_key_info_t()):
        self.task_id = task_id
        self.job_info = job_base_info
        self.key_info = key_base_info
        self.fmt = "@I%ds%ds" % (self.job_info.sizeof(), self.key_info.sizeof())

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.task_id, self.job_info.pack(True), self.key_info.pack(True))
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self,data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.task_id, self.job_info, self.key_info = struct.unpack(self.fmt, data)
        # print(BinaryToChar(self.key_info))
        return self.task_id, CI_job_base_info_t().unpack(self.job_info), order_key_info_t().unpack(self.key_info)

    def sizeof(self):
        return struct.calcsize(self.fmt)


class CI_task_runtime_info_t(object):
    def __init__(self, status=0, dev_id=1, port=0, kmc_kcv="", diversify_method_KM=0):
        self.status = status
        self.dev_id = dev_id
        self.port = port
        self.kcv = kcv_t(kmc_kcv)
        self.diversify = diversify_method_KM
        self.fmt = "IIHxx%dsI0L" % (self.kcv.sizeof())

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.status, self.dev_id, self.port, self.kcv.pack(True), self.diversify)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.status, self.dev_id, self.port, self.kcv, self.diversify = struct.unpack(self.fmt, data)
        return self.status, self.dev_id, self.port, kcv_t().unpack(self.kcv), self.diversify

    def sizeof(self):
        return struct.calcsize(self.fmt)

class CI_active_task_info_t(object):
    def __init__(self, task_static = CI_task_static_info_t(), task_runtime = CI_task_runtime_info_t()):
        self.task_static = task_static
        self.task_runtime = task_runtime
        self.fmt = "%ds%ds0L" % (self.task_static.sizeof(), self.task_runtime.sizeof())


    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.task_static.pack(True), self.task_runtime.pack(True))
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.task_static, self.task_runtime = struct.unpack(self.fmt, data)
        return CI_task_static_info_t().unpack(self.task_static), CI_task_runtime_info_t().unpack(self.task_runtime)

    def sizeof(self):
        return struct.calcsize(self.fmt)

class CI_task_issue_info_t(object):
    def __init__(self, blank_count=0, succeeded_count=0, failed_count=0):
        self.blank_count = blank_count
        self.succeeded_count = succeeded_count
        self.failed_count = failed_count
        self.fmt = "III"

    def pack(self, toBuff = False):
        buff = struct.pack(self.fmt, self.blank_count, self.succeeded_count, self.failed_count)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.blank_count, self.succeeded_count, self.failed_count = struct.unpack(self.fmt, data)
        return self.blank_count, self.succeeded_count, self.failed_count

    def sizeof(self):
        return struct.calcsize(self.fmt)

class key_property_t():
    def __init__(self, usage=0, expiry_date=0, desc=""):
        self.usage = usage
        self.expiry_date = expiry_date
        self.desc = desc
        self.fmt = "@II%ds0l" % key_desc_t().sizeof()

    def pack(self, toBuff=False):
        buff = struct.pack("ii", self.usage, self.expiry_date) + key_desc_t(self.desc).pack(True)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self,data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        usage, expiry_date, desc = struct.unpack(self.fmt, data)
        key_desc = key_desc_t().unpack(desc)
        return usage, expiry_date, key_desc

    def sizeof(self):
        return struct.calcsize(self.fmt)

class CI_terminated_task_info_t(object):
    def __init__(self, task_static = CI_task_static_info_t(), blank_count=0, success_count=0, failed_count=0):
        self.task_static = task_static
        self.blank_count = blank_count
        self.success_count = success_count
        self.failed_count = failed_count
        self.fmt = "@%dsIII0L" % (self.task_static.sizeof())

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.task_static.pack(True), self.blank_count,
                           self.success_count, self.failed_count)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self,data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.task_static, self.blank_count, self.success_count, self.failed_count = struct.unpack(self.fmt, data)

        return CI_task_static_info_t().unpack(self.task_static), self.success_count, self.blank_count, self.failed_count

    def sizeof(self):
        return struct.calcsize(self.fmt)

class CI_task_event_t(object):
    ""
    def __init__(self, task_ID=0, event_type=0):
        self.task_id = task_ID
        self.event_type = event_type
        self.fmt = "II"

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.task_id, self.event_type)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self,data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.task_id, self.event_type = struct.unpack(self.fmt, data)

        return self.task_id, self.event_type

    def sizeof(self):
        return struct.calcsize(self.fmt)

class symm_key_enum_info_t():
    def __init__(self, key_ver=0, key_property_t=key_property_t(), kcv=""):
        self.key_ver = key_ver
        self.key_property_t= key_property_t
        self.kcv= kcv
        self.fmt = "@i%ds%ds"%(key_property_t.sizeof(), symm_key_enum_value_t().sizeof())

    def pack(self, toBuff=False):
        buff = struct.pack("I", self.key_ver) + self.key_property_t.pack(True) + symm_key_enum_value_t(self.kcv).pack(True)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        key_ver, key_property, kcv = struct.unpack(self.fmt, data)
        return key_ver, key_property_t().unpack(key_property), symm_key_enum_value_t().unpack(kcv)

    def sizeof(self):
        return struct.calcsize(self.fmt)

class pdk_enum_info_t():
    def __init__(self, key_type=0, symm_key_enum_info_t= symm_key_enum_info_t()):
        self.key_type = key_type
        self.key_enum = symm_key_enum_info_t
        self.fmt = "@i%ds0l" % self.key_enum.sizeof()

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.key_enum)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        key_type, key_enum = struct.unpack(self.fmt, data)
        return key_type, symm_key_enum_info_t().unpack(key_enum)

    def sizeof(self):
        return struct.calcsize(self.fmt)

class pdk_key_addr_t():
    def __init__(self, bank_addr='', key_class=0):

        self.bank_addr = bank_addr_t(bank_addr)
        self.key_class = key_class
        self.fmt = '%dsI0l' % (bank_addr_t().sizeof())

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.bank_addr.pack(True), self.key_class)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def packChar(self):
        return struct.pack(self.fmt, self.bank_addr, self.key_class)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.bank_addr, self.key_class = struct.unpack(self.fmt, data)
        return bank_addr_t().unpack(self.bank_addr), self.key_class


    def sizeof(self):
        return struct.calcsize(self.fmt)


################################################################

class CI_order_info_t():
    def __init__(self, order_name="", status=1):
        self.order_name = order_name_t(order_name)
        self.status = status
        self.fmt = "%dsI0L" % (self.order_name.sizeof())

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.order_name.pack(True), self.key_info.pack(True), self.status)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.order_name, self.status = struct.unpack(self.fmt, data)
        return order_name_t().unpack(self.order_name), self.status

    def sizeof(self):
        return struct.calcsize(self.fmt)

class job_ref_t():
    def __init__(self, order_id, job_id):
        self.order_id = order_id
        self.job_id = job_id
        self.fmt = "II"

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.order_id, self.job_id)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.order_id, self.job_id = struct.unpack(self.fmt, data)
        return self.order_id, self.job_id

    def sizeof(self):
        return struct.calcsize(self.fmt)

class tm():
    def __init__(self, struct_time = time.localtime()):
        self.struct_time = struct_time
        self.sec = self.struct_time.tm_sec
        self.min = self.struct_time.tm_min
        self.hour = self.struct_time.tm_hour
        self.mday = self.struct_time.tm_mday
        self.mon = self.struct_time.tm_mon-1
        self.year = self.struct_time.tm_year-1900
        self.wday = self.struct_time.tm_wday+1
        self.yday = self.struct_time.tm_yday-1
        self.isdst = self.struct_time.tm_isdst
        self.fmt = "IIIIIIIIi"
    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.sec, self.min, self.hour, self.mday, self.mon,
                           self.year, self.wday, self.yday, 0)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.sec,self.min, self.hour, self.mday, self.mon, self.year, \
        self.wday, self.yday, self.isdst = struct.unpack(self.fmt, data)

        return time.struct_time((self.year+1900, self.mon+1, self.mday,  self.hour, self.min, self.sec,
                                  self.wday-1, self.yday+1, self.isdst))

    def sizeof(self):
        return struct.calcsize(self.fmt)

class PAN_CI_log_t():
    def __init__(self, pan_name="", file_id=0, dev_id=0, status=0, datetime=tm()):
        self.pan_name  = PAN_name(pan_name)
        self.file_id = file_id
        self.dev_id = dev_id
        self.status = status
        self.datetime = datetime
        self.fmt = "%dsIII%ds0L" % (self.pan_name.sizeof(), self.datetime.sizeof())

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.pan_name.pack(True), self.file_id, self.dev_id, self.status,
                           self.datetime.pack(True))
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.pan_name, self.file_id, self.dev_id, self.status, self.datetime = struct.unpack(self.fmt, data)
        return PAN_name().unpack(self.pan_name), self.file_id, self.dev_id, self.status, tm().unpack(self.datetime)

    def sizeof(self):
        return struct.calcsize(self.fmt)


class CI_job_issue_info_t():
    def __init__(self, blank_count=0, succeeded_count=0, failed_count=0):
        self.blank_count = blank_count
        self.succeeded_count = succeeded_count
        self.fail_count = failed_count
        self.fmt = "III"

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.blank_count, self.succeeded_count, self.fail_count)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.blank_count, self.succeeded_count, self.fail_count = struct.unpack(self.fmt, data)
        return self.blank_count, self.succeeded_count, self.fail_count

    def sizeof(self):
        return struct.calcsize(self.fmt)

class CI_job_record_t():
    def __init__(self, job_id=0, record_idx=0):
        self.job_id = job_id
        self.record_idx = record_idx
        self.fmt = "II"

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.job_id, self.record_idx)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.job_id, self.record_idx = struct.unpack(self.fmt, data)
        return self.job_id, self.record_idx

    def sizeof(self):
        return struct.calcsize(self.fmt)

class CI_event_t():
    def __init__(self,event_type=0, order_id=0,taskOrFileId=0, date_time=0):
        self.order_id = order_id
        self.event_type = event_type
        self.taskFileId = taskOrFileId
        self.date_time = date_time
        self.fmt = "IIII"

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.event_type, self.order_id, self.taskFileId, self.date_time)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.event_type, self.order_id, self.taskFileId, self.date_time = struct.unpack(self.fmt, data)

        return self.event_type, self.order_id, self.taskFileId, self.date_time

    def sizeof(self):
        return struct.calcsize(self.fmt)

class CI_file_event_t():
    def __init__(self, file_ID=0, event_type=0):
        self.file_id = file_ID
        self.event_type = event_type
        self.fmt = "II"

    def pack(self, toBuff=False):
        buff = struct.pack(self.fmt, self.file_id, self.event_type)
        if toBuff:
            return buff
        else:
            return BinaryToChar(buff)

    def unpack(self, data, isBuff=True):
        if not isBuff:
            data = CharToBinary(data)
        self.file_id, self.event_type = struct.unpack(self.fmt, data)

        return self.file_id, self.event_type

    def sizeof(self):
        return struct.calcsize(self.fmt)

if __name__ == "__main__":
    # d = c_template_define(templ_name="temple1", use_status=0, templ_version=1, creator_name='creator1',
    #                       created_date='2020-6-7', payment_name="pament1", payment_version='2', bank_name="bank1",
    #                       bin_value='1234435', card_name="card1", sup_pse_ppse=1, ppse_dgi_group='ppse_group',
    #                       pse_dgi_group="pse_group", desc_value='desc1', profile_dgi_group='file1', key_def_nums=33,
    #                       key_def_group="ket_group")

    # print(d.sizeof())
    # print(d.pack())
    # dict = d.uppack(d.pack(False), False)
    # for k, v in dict.items():
    #     print(k, v)
    #
    # p = PAN_CI_info("panname1", 1)
    # print(p.pack(False))
    # print(p.unpack(p.pack(), ))
    # t = c_template_info("sdfgg", 0)
    # print(t.pack(True))
    # print(t.unpack(t.pack(False), False))
    #
    # ci = CI_job_info()
    #
    # act = CI_active_job_info(ci, 1, 23)
    # print(act.pack())
    # ci2, kmc, ds = act.unpack(act.pack(True), True)
    #
    # print(kmc, ds)
    # for k, v in ci2.items():
    #     print(k, v)

    # print(ci.pack())
    # dict = ci.unpack(ci.pack(True), True)
    # for k, v in dict.items():
    #     print(k, v)

    # a = data_file_CI_info(1, 2, 3)
    # print(a.unpack(a.pack(True)))

    # a = CI_data_query_info("5465453355", 0, 186563)
    # print(a.pack())
    # print(a.unpack(a.pack(True)))

    # b = bank_name_t("12354")
    # print(b.sizeof())
    # print(b.pack())
    # a = key_property_t(0, 1, "sdsf")
    # b = symm_key_enum_info_t(1, a, "6565")
    # c = pdk_enum_info_t(2, b)
    # print(c.pack())
    # print(c.unpack(c.pack(False), False))
    # print(a.unpack("030000003030300000000000", False))
    #**********************************************************************************
    import sys
    base_info = CI_key_base_info_t("bank1", "bin11", symm_key_ref_t(0, "AAA"),
                                      symm_key_ref_t(0, "BBB"), symm_key_ref_t(0, "CCC"),
                                      symm_key_ref_t(0, "DDD"), 0, 0)
    print(base_info.sizeof())
    # print(base_info.unpack(base_info.pack(True)))
    # pan = CI_device_info("12.75", "dwsfsg")
    # print(pan.pack(False))
    # print(CI_device_name().sizeof())
    # pan.fmt = "@H%dsxxxxxxxx"% PAN_NAME_LEN_MAX
    # print(pan.pack())
    print(CharToBinary("8BAF47"))
    k = symm_key_ref_t(0, CharToBinary("8BAF47"))
    print(k.pack(False))
