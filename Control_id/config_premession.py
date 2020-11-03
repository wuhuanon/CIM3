
CI_EVENT_ORDER_NEW      = 0x0001
CI_EVENT_FILE_NEW       = 0x0101
CI_EVENT_TASK_STOPPED   = 0x0201
CI_EVENT_TASK_LOCKED    = 0x0202
CI_EVENT_TASK_UNLOCKED  = 0x0203


IninPer = {"角色1":0x0002, "角色2":0x0010}
KEY_INFO = "key_info"
KMC_INFO = "kmc_info"
DEV_ID = "dev_id"
'''
{field:[index, size]}
'''

class Messages():
    JOB_ID = 'Job Id'
    ORDER_INFO = "Order"
    ALL_COUNT = "Blank Count"
    SUCCESS_COUNT = "Success Count"
    FAIL_COUNT = "Fail Count"
    SURPLUS_COUNT = "Surplus Count"
    MACHINE = 'Machine'
    DELETE_TIME = "Delete Time"
    KMC = "KMC"
    JOB_STATUS = "Status"
    JOB_TYPE = "Type"
    JOB_DES = "Des"
    RUN_JOB_FIELDS = {JOB_ID:[0, 10], ALL_COUNT: [1, 10], SUCCESS_COUNT: [2, 10], FAIL_COUNT: [3, 10],
                      JOB_STATUS: [4, 10], MACHINE: [5, 10], KMC: [6, 15],  JOB_DES:[7, 25]}
    DELETE_JOB_FIELDS = {JOB_ID: [0, 10], ORDER_INFO: [1, 30], ALL_COUNT: [2, 10],
                         SUCCESS_COUNT: [3, 10], FAIL_COUNT: [4, 10], JOB_DES: [5, 30]}
    PAN_INDEX = "Index"
    PAN = "Pan"
    PAN_MACHINE = "Machine"
    PAN_STATUS = "Status"
    PAN_DATE = "Date"
    PAN_USER = "User"
    PAN_PEPAIR_FIELDS = {PAN: [0, 40], PAN_MACHINE: [1, 20], PAN_STATUS: [2, 14], PAN_DATE: [3, 14], PAN_USER: [4, 12]}
    MACHINE_ID="ID"
    MACHINE_NAME = "Machine Name"
    MACHINE_IP = "Machine IP"
    MACHINE_STATUS = "Status"
    MACHINE_MANUFACTURER = "Manufacturer"
    MACHINE_ABOUT = "About"
    MACHINE_FIELDS = {MACHINE_ID:[0, 10], MACHINE_NAME: [1, 30], MACHINE_IP: [2, 20],
                      MACHINE_ABOUT: [3, 40]}



    FILE_DATA = "Total data"
    FILE_SUCCESS = "Successful account"
    FILE_FALI = "Fail account"
    FAIL_INCOMPLETE = "incomplete account"
    FILE_NAME = "File Name"
    FAIL_FIELDS = {FILE_DATA:[0, 25], FILE_SUCCESS: [1, 25], FILE_FALI: [2, 25], FAIL_INCOMPLETE: [3, 25]}

    PAN_VIEW_FIELDS = {PAN: [0, 20],FILE_NAME:[1, 35], PAN_MACHINE: [2, 20], PAN_STATUS: [3, 10], PAN_DATE: [4, 15]}

    TASK_ACTIVE = "Exist in active task "
    TASK_TERMINATE = "Exist terminated in task"

    PAN_ADD_FIELDS = {PAN_INDEX:[0, 20], PAN:[1, 30], TASK_ACTIVE: [2, 25], TASK_TERMINATE: [3, 25]}
    PAN_CONFIRM_FIELDS = {PAN_INDEX: [0, 20], PAN: [1, 80]}

    PAN_RECORD = {JOB_ID:[0, 30], PAN_STATUS: [1, 30],  PAN_DATE: [2, 40]}

    STATUS_START = "Starting"
    STATUS_STOP = "Stop"
    STATUS_PUBLIC = "Public"
    STATUS_PRIVATE = "Private"
    STATUS_STOPPING = "Stopping"
    STATUS_STOPPED = "Stopped"
    STATUS_FINISH = "Finished"

class UserInfo():
    id = ""
    pin = ""
    isSuperAdmin = False




CI_TASK_STATUS_RUNNING_PUBLIC = 1
CI_TASK_STATUS_RUNNING_PRIVATE = 2
CI_TASK_STATUS_STOPPING = 3
CI_TASK_STATUS_STOPPED = 4


job_status = {CI_TASK_STATUS_RUNNING_PUBLIC: Messages.STATUS_PUBLIC, CI_TASK_STATUS_RUNNING_PRIVATE: Messages.STATUS_PRIVATE,
              CI_TASK_STATUS_STOPPING: Messages.STATUS_STOPPING, CI_TASK_STATUS_STOPPED: Messages.STATUS_STOPPED}

TASK_COMMON = "Common Tasks"
TASK_ISSUING = "Issuing Tasks"
TASK_TYPE_COMMON = 1
TASK_TYPE_ISSUING = 2

def getStatus(status):
    return job_status.get(status, 0)

def getJobType(type):
    if type == TASK_TYPE_COMMON:
        return TASK_COMMON
    else:
        return TASK_ISSUING

def getTypeFlag(stringType):
    if stringType == Messages.LOCAL_USER:
        return 0
    else:
        return 1

class Event():
    CI_EVENT_ORDER_NEW = 0x0001
    CI_EVENT_FILE_NEW = 0x0101
    CI_EVENT_TASK_STOPPED = 0x0201
    CI_EVENT_TASK_LOCKED = 0x0202
    CI_EVENT_TASK_UNLOCKED = 0x0203

def getJobEvent(event):
    if event == Event.CI_TASK_EVENT_STOPPED:
        return

if __name__ == "__main__":
    print(Messages.VALID_DATE)
    Messages.User = 5
    print(Messages.User)
    Messages.User = 4
    print(Messages.User)
