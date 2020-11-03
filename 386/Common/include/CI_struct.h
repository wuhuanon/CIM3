#ifndef CI_STRUCT_H
#define CI_STRUCT_H

#include <typedef.h>
#include <KeyStruct.h>
#include <profileStruct.h>
#include <dpdata_struct.h>


#define CI_ORDER_STATUS_NEW         0
#define CI_ORDER_STATUS_NORMAL      1
#define CI_ORDER_STATUS_FINISHED    2
#define CI_ORDER_STATUS_DELETED     3

#define CI_JOB_STATUS_NEW           0
#define CI_JOB_STATUS_VALID         1
#define CI_JOB_STATUS_FINISHED      2

#define CI_FILE_STATUS_NEW          0
#define CI_FILE_STATUS_NORMAL       1
#define CI_FILE_STATUS_DELETED      2

#define CI_JOB_TYPE_NORMAL          1
#define CI_JOB_TYPE_FIX             2

#define CI_DEV_STATUS_NORMAL        0
#define CI_DEV_STATUS_DELETED       1

enum
{
    CI_RECORD_STATUS_BLANK = 0,
};

#define CI_RECORD_MASK_FETCHED      0x80000000UL
#define CI_RECORD_MASK_ISSUED       0x40000000UL

#define CI_DEVICE_NAME_LEN      63

#define CI_JOB_DESC_LEN         255
#define CI_DATA_FILE_DESC_LEN   255
#define CI_DEVICE_DESC_LEN      255

DEFINE_NAME(CI_job_desc_t, CI_JOB_DESC_LEN);
DEFINE_NAME(CI_device_desc_t, CI_DEVICE_DESC_LEN);
DEFINE_NAME(CI_data_file_desc_t, CI_DATA_FILE_DESC_LEN);

enum
{
    CI_TASK_STATUS_RUNNING_PUBLIC = 1,
    CI_TASK_STATUS_RUNNING_PRIVATE = 2,
    CI_TASK_STATUS_STOPPING = 3,
    CI_TASK_STATUS_STOPPED = 4,
};

typedef struct
{
    PAN_name_t PAN;
    dword_t file_ID;
    dword_t dev_ID;
    dword_t status;
    dword_t ci_datetime;
}PAN_CI_log_t;

DEFINE_NAME(CI_device_name_t, CI_DEVICE_NAME_LEN);

typedef struct
{
    CI_device_name_t dev_name;
    ip_addr_t addr;
    dword_t status;
    CI_device_desc_t desc;
}CI_device_info_t;

typedef struct
{
    order_name_t order_name;
    order_key_info_t key_info;
    dword_t status;
}CI_order_info_t;

typedef struct
{
    magnetic_file_name_t file_name;
    dword_t PAN_count;
    dword_t status;
    CI_data_file_desc_t desc;
}CI_magnetic_file_info_t;

typedef struct
{
    dword_t PAN_count;
    dword_t status;
    CI_job_desc_t desc;
}CI_job_info_t;

typedef struct
{
    dword_t status;
    dword_t dev_ID;
    word_t port;
    kcv_t KCV_of_KMC;
    dword_t diversify_method_KMC;
}CI_task_runtime_info_t;

typedef struct
{
    dword_t task_ID;
    CI_job_info_t static_info;
    CI_task_runtime_info_t runtime_info;
}CI_active_task_info_t;

typedef struct
{
    dword_t blank_count;
    dword_t succeeded_count;
    dword_t failed_count;
}CI_job_issue_info_t;

typedef struct
{
    dword_t task_ID;
    CI_job_info_t static_info;
    CI_job_issue_info_t issue_info;
}CI_finished_task_info_t;

enum
{
    CI_ORDER_EVENT_NEW = 1,
};

typedef struct
{
    dword_t order_ID;
    dword_t event_type;
}CI_order_event_t;

enum
{
    CI_TASK_EVENT_STOPPED = 1,
    CI_TASK_EVENT_LOCK = 2,
    CI_TASK_EVENT_UNLOCK = 3,
};

typedef struct
{
    dword_t task_ID;
    dword_t event_type;
}CI_task_event_t;

enum
{
    CI_FILE_EVENT_NEW = 1,
};

typedef struct
{
    dword_t file_ID;
    dword_t event_type;
}CI_file_event_t;

typedef struct
{
    dword_t pan_ID;
    PAN_name_t pan;
}CI_PAN_info_t;

typedef struct
{
    dword_t job_ID;
    dword_t record_idx;
}CI_job_record_t;

typedef struct
{
    dword_t  order_ID;
    dword_t job_ID;
}job_ref_t;

#endif // DPDATA_STRUCT_H
