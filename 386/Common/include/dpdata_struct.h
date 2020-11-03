#ifndef DPDATA_STRUCT_H
#define DPDATA_STRUCT_H

#include <typedef.h>
#include <KeyStruct.h>
#include <profileStruct.h>

#ifdef __cplusplus
extern "C" {
#endif

#define DGI_SINGLE_LEN_MAX      (255*2)
#define DGI_FILE_LEN_MAX        (260*2*60)

#define PAN_NAME_LEN_MAX        20
#define AID_NAME_LEN_MAX        16
#define DGI_BUF_LEN_MAX         (255*2)
#define MAGNE_REC_LEN_MAX       1024
#define DECODE_REC_LEN_MAX      256
#define DATE_TIME_LEN_MAX       19

DEFINE_NAME(date_time_t ,    DATE_TIME_LEN_MAX);
DEFINE_NAME(PAN_name_t ,    PAN_NAME_LEN_MAX);
DEFINE_NAME(magnetic_record_t ,     MAGNE_REC_LEN_MAX);
DEFINE_NAME(decode_record_t ,     DECODE_REC_LEN_MAX);
DEFINE_NAME(APP_AID_t ,     AID_NAME_LEN_MAX);
DEFINE_NAME(DGI_buf_t ,     DGI_BUF_LEN_MAX);


#define MAGNE_NAME_LEN_MAX      100
#define DECODE_PLUGIN_NAME      63
#define FILE_CREATOR_NAME       63
#define DECODE_FOMAT_BUF        2000
#define MAG_FILE_DESC_LEN_MAX   255
#define ORDER_NAME_LEN_MAX      63

DEFINE_NAME(magnetic_file_name_t ,      MAGNE_NAME_LEN_MAX);
DEFINE_NAME(plugin_name_t ,             DECODE_PLUGIN_NAME);
DEFINE_NAME(field_Table_name_t ,        DECODE_PLUGIN_NAME);
DEFINE_NAME(file_creator_name_t ,       FILE_CREATOR_NAME);
DEFINE_NAME(dp_operator_name_t ,        FILE_CREATOR_NAME);
DEFINE_NAME(decode_format_t ,           DECODE_FOMAT_BUF);
DEFINE_NAME(magnetic_file_desc_t,       MAG_FILE_DESC_LEN_MAX);
DEFINE_NAME(order_name_t,               ORDER_NAME_LEN_MAX);


bool_t DPS_CheckMagneticFileName(magnetic_file_name_t *pName);

#define TAG_CA_PKI                      0x8F
#define TAG_SDA                         0x93
#define TAG_issuerCert                  0x90
#define TAG_issuerE                     0x9F32
#define TAG_issuerPKRemainder           0x92
#define TAG_issuerDAC                   0x9f45//Data Authentication code
#define TAG_iccCert                     0x9f46
#define TAG_iccE                        0x9f47
#define TAG_iccPKRemainder              0x9f48
#define TAG_SDA_TagList                 0x9f4a//Static Data Authentication Tag List

#define TAG_Track2EquivalentData        0x57
#define TAG_Track1DiscretionaryData     0x9f1f
#define TAG_PAN                         0x5A
#define TAG_CardHolderName              0x5F20
#define TAG_CardHolderName2             0x9F0B
#define TAG_ExpirationDate              0x5F24
#define TAG_EffectiveDate               0x5F25
#define TAG_ServiceCode                 0x5f30

#define TAG_MAX_57                          19
#define TAG_MAX_PAN                         10
#define TAG_MAX_CardHolderName              26
#define TAG_MIN_CardHolderName              2
#define TAG_LEN_ExpirationDate              3
#define TAG_LEN_EffectiveDate               3
#define TAG_LEN_ServiceCode                 2

//others:emboss and track
#define TAG_Track1        "DF01"
#define TAG_Track2        "DF02"
#define TAG_Expiration    "DF03"
#define TAG_PAN_4         "DF04"
#define TAG_CVV2          "DF05"
#define TAG_System_RFU    "DF06"

#define LOACTION_TYPE_AFL               0
#define LOACTION_TYPE_MAGNETIC          1

#define EMV_DES2_KEY_MAX                16

#define PAYMENT_VISA                    "VISA"
#define PAYMENT_VISA_DC                 "VSDC"
#define PAYMENT_VISA_Q                  "QVSDC"

#define PAYMENT_MASTERCARD              "MASTERCARD"
#define PAYMENT_MASTERCARD_1            "mchip"
#define PAYMENT_MASTERCARD_2            "m/chip"
#define PAYMENT_MASTERCARD_3            "mca"

#define PAYMENT_UICS                    "unionpay"
#define PAYMENT_UICS_1                  "UICS"
#define PAYMENT_UICS_2                  "PBOC"
#define PAYMENT_UICS_3                  "qPBOC"

enum
{
    DPTASK_FINISH_SINGLE = 0,
    DPTASK_FINISH_ALL = -1,
    DPTASK_ERROR = 1
};

enum
{
    PVT_SUCCEEDED = 0,
    PVT_ERROR_QUERY_MAGNETIC_FILE,
    PVT_ERROR_LINK_MYSQL,
    PVT_ERROR_QUERY_TEMPLATE,
    PVT_ERROR_QUERY_PROFILE,
    PVT_ERROR_QUERY_PROFILE_DGI,
    PVT_NOT_EXIST_PAN_RECORD,
    PVT_ERROR_NEW_DPTASK,
    PVT_NOT_EXIST_PAN_DATA,
    PVT_NOT_EXIST_AIP_AFL,
    PVT_NOT_EXIST_CA_INDEX,
    PVT_NOT_EXIST_ISSUER_CERT,
    PVT_NOT_EXIST_ISSUER_E,
    PVT_KEY_NO_TRANS_KEY,
    PVT_KEY_NO_ISSUER_RSA,
    PVT_KEY_NO_ISSUER_CERT,
    PVT_NOT_EXIST_SDA,
    PVT_DDA_LACK_ICC_CERT,
    PVT_DDA_LACK_ICC_E,
    PVT_ERR_SDA_Integrity_check,
    PVT_NOT_EXIST_TRACK2,
    PVT_NOT_EXIST_TRACK1,
    PVT_NOT_EXIST_PAN,
    PVT_NOT_EXIST_PAN_IN_MAGNETIC,
    PVT_NOT_EXIST_CardholderName,
    PVT_NOT_EXIST_ExpirationDate,
    PVT_NOT_EXIST_EffectiveDate,
    PVT_NOT_EXIST_ServiceCode,
    PVT_ICC_RSA_unpaired,
    PVT_ICC_CRT_unpaired,
    PVT_PIN_RSA_unpaired,
    PVT_ERROR_GEN_ICC_RSA,
    PVT_ERROR_GEN_ICC_CRT,
    PVT_ERROR_GEN_ICC_STD,
    PVT_ERROR_GEN_DES2,
    PVT_PROFILE_TLV_TAG_ERROR,
    PVT_PROFILE_TLV_LENGTH_ERROR,
    PVT_PROFILE_DGI_VALUE_ERROR,
    PVT_EXCEED_DGI_MAX_255,
    PVT_DTS_CONNECT_FAILED,
    PVT_FILE_HAS_DELETED,
    PVT_UNWRAP_KEY_FAILED,
    PVT_ERROR_NEW_DPRECORD,
    PVT_ERROR_WRITE_DGI,
    PVT_ERROR_DESTROY_HANDLE,
    PVT_ERROR_PROCESS_ISSUER_CERT,
    PVT_ERROR_SET_STATUS,
    PVT_TASK_TEMPLATE_BACKUP_ERROR
};

enum
{
    APP_TYPE_PSE = 1,
    APP_TYPE_PPSE,
    APP_TYPE_Payment
};
enum
{
    DP_DGI_ENC_NO = 0,
    DP_DGI_ENC_YES
};
enum
{
    PAN_STATUS_DP = 0,
    PAN_STATUS_CI//其他值表示执行CI的次数
};
#define FORMAT_BUF_MAX          200
#define NAME_FIELD_OFF_ELE          0
#define TYPE_FIELD_OFF_ELE          1

#define START_POS_OFF_INTER             0
#define START_CHAR_OFF_INTER            1
#define END_LENGTH_OFF_INTER            2
#define END_CHAR_OFF_INTER              3
#define MASK_OFF_INTER                  4

#define FIELD_TYPE_USER_DEF         1//field(type#name#value)
#define FIELD_TYPE_INTER            2//field(type#name#start pos#start char#end len#end char#mask#)
#define FIELD_TYPE_CONCAT           3//field(type#name#subfield1&subfield2&...)

#define SPACER_NAME_CONCAT          '&'
#define SPACER_FIELD_ELE            '#'
#define SPACER_FIELD_ITEM           '$'

#define COUNT_FIELD_OFF_ITEM         0
typedef struct
{
    field_Table_name_t      table_name;
    decode_format_t         decord_format_buf;//field1 $ field2 $ field3 $ ...
}field_Table;

//export file:magnetic_record + '%' + IC_record
#define OFFSET_MAGNETIC_RECORD  0

#define SPACER_ELEMENT          '%'
typedef struct
{
    word_t app_type;
    APP_AID_t app_aid;
    word_t dgi_sum;
    word_t dgi_index;
    word_t dgi_enc;
    DGI_buf_t dgi_buf;//(type+Len+AID +总计+第x个+是否加密+DGI+Length(FF00FF)+DATA) % () % ()
}app_dgi_s;

typedef struct
{
    dword_t             pan_idx;
    PAN_name_t          pan_name;
    decode_record_t     ic_decode_data;
}pan_record_t;

#define DP_RECORD_STATUS_SUCCESS      0
typedef struct
{
    dword_t         PAN_inf_id;
    dword_t         dp_task_id;
    int             status;
    date_time_t     DP_dateTime;
}pan_dp_record_inf;

typedef struct
{
    dword_t         self_id;
    c_template_info template_inf;
}dp_DT_used;

enum
{
    FILE_STATUS_DP_IDLE,
    FILE_STATUS_DP_INI,
    FILE_STATUS_DP_OK,
    FILE_STATUS_DP_FROZEN,
    FILE_STATUS_DP_DELETED
};

typedef struct
{
    dword_t                 self_id;
    magnetic_file_name_t    mag_file_name;
    bin_name_t              bin_val;
    field_Table_name_t      field_table;
    plugin_name_t           decode_plugin;
    dword_t                 file_status;
    dword_t                 pan_count;
    dword_t                 finished_count;
    file_creator_name_t     creat_user;
    date_time_t             creat_datetime;
}magnetic_file_inf;


typedef struct
{
    bin_name_t              bin_val;
    dword_t                 file_status;
    dword_t                 pan_count;
}magnetic_file_query_info;

typedef struct
{
    magnetic_file_query_info    file_query_info;
    dword_t                     finished_count;
}magnetic_file_Task_info;

#define EMV_SFI_MAX                 0x0A
#define DGI_LENGTH_FF               0xFF

#define DGI_CT_DESkeys               0x8000
#define DGI_CT_DESkeysKCV               0x9000
#define DGI_CL_DESkeys               0x8001
#define DGI_CL_DESkeysKCV               0x9001
#define DGI_OfflinePIN               0x8010
#define DGI_PINRelatedData               0x9010
#define DGI_ICCPriKey               0x8101
#define DGI_ICCPubKey               0x8103
#define DGI_DDA_CRT_P               0x8205
#define DGI_DDA_CRT_Q               0x8204
#define DGI_DDA_CRT_DP               0x8203
#define DGI_DDA_CRT_DQ               0x8202
#define DGI_DDA_CRT_U               0x8201
#define DGI_PIN_CRT_P               0x8305
#define DGI_PIN_CRT_Q               0x8304
#define DGI_PIN_CRT_DP               0x8303
#define DGI_PIN_CRT_DQ               0x8302
#define DGI_PIN_CRT_U               0x8301

#define isIncluding_YES             1
#define isIncluding_NO              0


#define DGI_MCA_CT_KDCVC3               0x8400
#define DGI_MCA_CL_KDCVC3               0x8401
#define DGI_MCA_AC_MASTER               0x8004
#define DGI_MCA_CT_DNMK                 0xA006
#define DGI_MCA_CL_DNMK                 0xA016

#define FCPS_IP_ADDR_LEN_MAX            39

DEFINE_NAME(ip_addr_t, FCPS_IP_ADDR_LEN_MAX);

typedef struct
{
    dword_t key_type;
    kcv_t kcv;
}symm_key_ref_t;

#define SYMM_KEY_VAL_EQUAL(pKey1, pKey2)    ((pKey1)->len == (pKey1)->len && memcmp((pKey1)->val, (pKey2)->val, (pKey1)->len) == 0)
#define SYMM_KEY_EQUAL(pKey1, pKey2)        (SYMM_KEY_VAL_EQUAL(&(pKey1)->key_buf, &(pKey2)->key_buf) && KCV_EQUAL(&(pKey1)->kcv, &(pKey2)->kcv))

enum
{
    MAG_FILE_EVENT_NEW = 1,
    MAG_FILE_EVENT_DEL = 2,
    MAG_FILE_EVENT_FREEZE = 3,
    MAG_FILE_EVENT_UNFREEZE = 4,
    MAG_FILE_EVENT_DP_START = 5,
    MAG_FILE_EVENT_DP_EXIT = 6,
};

typedef struct
{
    magnetic_file_name_t file_name;
    dword_t             event;
}mag_file_event_t;

typedef struct
{
    magnetic_file_name_t data_file_name;
    dword_t finished_count;
}task_info_t;

#define EMV_DER_OP_A            0
#define EMV_DER_OP_B            1
#define DER_MASK_KMC            100
#define DER_MASK_KMU            10
#define DER_MASK_EMV            1
typedef struct
{
    //dword_t             emv_derivation;//1st:gp-kmc,2st:gp-kmu,3st:emv; 1st*100+2st*10+3st
    c_template_info     template_inf;
    ip_addr_t           client_addr;
    dp_operator_name_t  operator_name;
    byte_t              CSN_start[3];
}dp_task;


typedef struct
{
    magnetic_file_query_info    file_inf;
    dp_task                     task_pan;
}DP_Task_inf;


#define ORDER_STATUS_ACTIVE         0
#define ORDER_STATUS_TERMINAL       1
typedef struct
{
    c_template_info     template_info;
    profileVer_Inf_t    profile_info;
    word_t              status;
}order_info_t;

typedef struct
{
    magnetic_file_name_t magnetic_file_name;
    bin_name_t BIN;
    plugin_name_t DecodePlugin;
    field_Table_name_t Table_name;
    word_t count;
    dword_t fmtVer;
}DP_file_upload_info_t;


typedef struct
{
    bank_name_t bank_name;
    bin_name_t bin_name;
    dword_t key_type_TK;
    dword_t key_type_KMC;
    dword_t key_type_KMU;
    dword_t key_type_PEK;
    kcv_t TK_kcv;
    symm_key_value_t KMC;
    symm_key_value_t KMU;
    symm_key_value_t PEK;
    dword_t diversify_method_KMC;
    dword_t diversify_method_KMU;
}order_key_info_t;

bool_t DS_CheckOrderKeyInfo(order_key_info_t *pKeyInfo);
bool_t DS_OrderKeyInfoEqual(const order_key_info_t *pInfo1, const order_key_info_t *pInfo2);

#ifdef __cplusplus
}
#endif

#endif // DPDATA_STRUCT_H
