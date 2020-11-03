#ifndef C_DATA_STRUCT_H
#define C_DATA_STRUCT_H

#include "Constants_ud.h"

#define PROFILE_TYPE_MAX            (7+1)//payment, pse, ppse
#define PAYMENT_NAME_MAX            (30+1)
#define TAG_MAX                     (4+1)
#define TAG_VALUE_MAX               (256*2)
#define DESCRIPTION_MAX             150
#define RSA_CSSN_LENGTH             (6+1)

#define DGI_GROUP                   3//00~99


#define TAG_ENCODE_HEX                  0
#define TAG_ENCODE_DECIML               1
#define TAG_ENCODE_ASCII                2//Character
#define TAG_ENCODE_MAX                  10
typedef struct
{
    char payment_name[PAYMENT_NAME_MAX];
    char payment_version[PAYMENT_NAME_MAX];
}c_payment_define;

//Format in DGI: Tag + length
#define TAG_SDAD                        "9f4b"
#define TAG_AC                          "9f26"
#define TAG_CID                         "9F27"
#define TAG_ATC                         "9F36"

typedef struct
{
    char payment_name[PAYMENT_NAME_MAX];
    char payment_version[PAYMENT_NAME_MAX];
    char tag[TAG_MAX];
    char tag_exten[DGI_GROUP];
    char tag_encode[TAG_ENCODE_MAX];
    int tag_value_max;
    int tag_value_min;
    int tag_value_len;
    char tag_value[TAG_VALUE_MAX];
    char desc_value[DESCRIPTION_MAX];
}c_tag_define;

#define SPACER_DGI_ELE              '#'
#define SPACER_DGI_ITEM             '$'
//name+version+profile
#define PROFILE_DGI_GROUP_MAX       (PAYMENT_NAME_MAX*3)
#define FLAG_YES_NO_MAX             4//'yes' or 'no'
#define FLAG_DATA_TYPE_MAX          6//'tlv' or 'value'
#define DGI_TYPE_TLV                1
#define DGI_TYPE_V                  2

#define SUPPORT_YES         1
#define SUPPORT_NO          0

#define DGI_ENC_NO          "No"
#define DGI_ENC_YES         "Yes"

typedef struct
{
    int  dgi_temp_70;
    char dgi[TAG_MAX];    
    char dgi_format[FLAG_DATA_TYPE_MAX];    
    char dgi_enc[FLAG_YES_NO_MAX];
    char dgi_value[TAG_VALUE_MAX];
    char dgi_group_id[DGI_GROUP];    
    //char profile_dgi_group[PROFILE_DGI_GROUP_MAX];

}c_dgi_define;

#define INSTANCE_AID_MAX            33//(16*2+1)
#define AIP_AFL_SIZE_MAX            201
#define SPACER_AFL_ITEM             '$'

#define AIP_SDA_MASK                0x40
#define AIP_DDA_MASK                0x20
#define isSupportSDA(api_byte1)     (AIP_SDA_MASK==(api_byte1&AIP_SDA_MASK))
#define isSupportDDA(api_byte1)     (AIP_DDA_MASK==(api_byte1&AIP_DDA_MASK))
#define MAX_TIME_BUF                20//'yyyy-MM-dd hh:mm:ss'+1
typedef struct
{
    char payment_name[PAYMENT_NAME_MAX];
    char payment_version[PAYMENT_NAME_MAX];
    char profile_name[PAYMENT_NAME_MAX];
    char instance_aid[INSTANCE_AID_MAX];
    char profile_type[PROFILE_TYPE_MAX];
    char rsa_e[RSA_CSSN_LENGTH];
    char rsa_cssn[RSA_CSSN_LENGTH];
    int rsa_pk_size;
    char profile_dgi_group[PROFILE_DGI_GROUP_MAX];//primary:payment name+version+profile
    char aip_afl_buffer[AIP_AFL_SIZE_MAX];//num+item(aip+afl)+$+item(aip+afl)+$+item(aip+afl)
    int dgi_nums;
    char edit_time[MAX_TIME_BUF];
}c_profile_define;

#define DGIs_NUM                60
#define DGI_DEF_GROUP_MAX       (sizeof(c_dgi_define)*DGIs_NUM+1)
typedef struct
{
    c_profile_define profile_Inf;
    char DGI_Buf[DGI_DEF_GROUP_MAX];
}c_profile_DGIs;

//dd.MM.yyyy
#define DATE_BUFF_MAX               12
#define BANK_BUFF_MAX               64
#define RID_VALUE_MAX               17
#define BIN_VALUE_MAX               9

#define SUPPORT_NULL                0
#define SUPPORT_PSE                 1
#define SUPPORT_PPSE                2
#define SUPPORT_PSE_PPSE            3

typedef struct
{
    char bank[BANK_BUFF_MAX];
    char rid[RID_VALUE_MAX];
    char bin[BIN_VALUE_MAX];
}c_keyDef_head;

#define SPACER_KEY_ELE          '%'
#define SPACER_KEY_INDEX        '#'
#define SPACER_KEY_PRIMARY      ','

#define KEY_NAME_MAX            64
#define KEY_DIGEST_MAX          (32*2+4)

#define IS_SELECTED             1
#define NOT_SELECTED            0
typedef struct
{
    char key_name[KEY_NAME_MAX];
    int key_ver;
    int key_type;
    int cert_index;
    int key_rsa_cert_id;
    int key_size;//when cert:is "public key version"
    int  kcv_len;
    int isSelected;
    char key_kcv_digest[KEY_DIGEST_MAX];    
}c_key_define;

#define KEY_DEF_NUMS                20
//not include:isSelected+key_rsa_cert_id
#define KEY_DEF_GROUP_MAX           (KEY_DEF_NUMS*(sizeof(c_key_define)+7))//3340


typedef struct
{
    char templ_name[PAYMENT_NAME_MAX];//primary_1
    int templ_version;//primary_2
}c_template_info;

#define DATA_TEMPLATE_USED_YES      1
#define DATA_TEMPLATE_USED_NO       0
typedef struct
{
    char templ_name[PAYMENT_NAME_MAX];//primary_1
    int use_status;
    int templ_version;//primary_2
    char creator_name[PAYMENT_NAME_MAX];
    char created_date[DATE_BUFF_MAX];
    char payment_name[PAYMENT_NAME_MAX];
    char payment_version[PAYMENT_NAME_MAX];
    char bank_name[BANK_BUFF_MAX];
    char bin_value[BIN_VALUE_MAX];
    char card_name[BANK_BUFF_MAX];
    int  sup_pse_ppse;//
    char ppse_dgi_group[PROFILE_DGI_GROUP_MAX];
    char pse_dgi_group[PROFILE_DGI_GROUP_MAX];
    char desc_value[DESCRIPTION_MAX];
    char profile_dgi_group[PROFILE_DGI_GROUP_MAX];
    int key_def_nums;
    char key_def_group[KEY_DEF_GROUP_MAX];
}c_template_define;

enum
{
    DP_KEY_TK = 1,
    DP_KEY_BIN_SYMM,
    DP_KEY_BIN_RSA,
    DP_KEY_CERT,
    DP_KEY_PEK,
    DP_KEY_KMC,
    DP_KEY_KMU,
};


#endif // C_DATA_STRUCT_H
