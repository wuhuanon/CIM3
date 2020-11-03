
#ifndef __KEY_MGMT_H_INCLUDED_31704546__
#define __KEY_MGMT_H_INCLUDED_31704546__

#include <typedef.h>
#include <Constants.h>

#ifdef __cplusplus
extern "C" {
#endif

DEFINE_NAME(CA_name_t , CA_NAME_LEN_MAX);
DEFINE_NAME(bank_name_t , BANK_NAME_LEN_MAX);
DEFINE_NAME(bin_name_t , BIN_NAME_LEN_MAX);
DEFINE_NAME(key_name_t , KEY_NAME_LEN_MAX);
DEFINE_NAME(key_template_name_t , KEY_TEMPLATE_NAME_LEN_MAX);

DEFINE_NAME(CA_desc_t , CA_DESC_LEN_MAX);
DEFINE_NAME(bank_desc_t , BANK_DESC_LEN_MAX);
DEFINE_NAME(bin_desc_t , BIN_DESC_LEN_MAX);
DEFINE_NAME(key_desc_t , KEY_DESC_LEN_MAX);
DEFINE_NAME(cert_desc_t , CERT_DESC_LEN_MAX);
DEFINE_NAME(key_template_desc_t , KEY_TEMPLATE_DESC_LEN_MAX);

DEFINE_BUFFER(RID_t, EMV_RID_LEN_MAX);
DEFINE_BUFFER(kcv_t, KCV_LEN_MAX);
DEFINE_BUFFER(symm_key_buf_t, SYMM_KEY_LEN_MAX);
DEFINE_BUFFER(wrapped_symm_key_buf_t, SYMM_KEY_WRAPPED_LEN_MAX);
DEFINE_BUFFER(symm_mac_t, SYMM_MAC_LEN_MAX);
DEFINE_BUFFER(pub_exp_buf_t, RSA_PUB_EXP_LEN_MAX);
DEFINE_BUFFER(pri_exp_buf_t, RSA_PRI_EXP_LEN_MAX+8);
DEFINE_BUFFER(pri_exponent_buf_t, RSA_KEY_MOD_LEN_MAX/2+8);
DEFINE_BUFFER(wrapped_rsa_pri_key_buf_t, RSA_PRI_KEY_WRAPPED_LEN_MAX);

typedef byte_t tracking_number_t[TRACKING_NUMBER_SIZE];
typedef byte_t service_identifier_t[SERVICE_IDENTIFIER_SIZE];
typedef byte_t cert_serial_number_t[CERT_SERIAL_NUMBER_SIZE];

#define NAME_EQUAL(pName1, pName2)  ((pName1)->len == (pName2)->len && memcmp((pName1)->val, (pName2)->val, (pName1)->len) == 0)
#define BUFFER_EQUAL(pBuf1, pBuf2)  ((pBuf1)->len == (pBuf2)->len && memcmp((pBuf1)->val, (pBuf2)->val, (pBuf1)->len) == 0)
#define KCV_EQUAL(pKCV1, pKCV2)     BUFFER_EQUAL(pKCV1, pKCV2)
#define RID_EQUAL(pRID1, pRID2)     BUFFER_EQUAL(pRID1, pRID2)

typedef struct
{
    CA_name_t CA_name;
}CA_addr_t;

typedef struct
{
    CA_name_t name;
    CA_desc_t desc;
    RID_t RID;
}CA_info_t;

typedef struct
{
    bank_name_t bank_name;
}bank_addr_t;

typedef struct
{
    bank_name_t name;
    bank_desc_t desc;
}bank_info_t;

typedef struct
{
    CA_addr_t CA_addr;
    key_template_name_t key_template_name;
}key_template_addr_t;

typedef struct
{
    key_template_name_t name;
    key_template_desc_t desc;
}key_template_info_t;

typedef struct
{
    dword_t keyType;
    key_name_t  name;
    key_desc_t  desc;
}key_def_t;

typedef struct
{
    bank_addr_t bank_addr;
    bin_name_t bin_name;
}bin_addr_t;

typedef struct
{
    bin_name_t  name;
    bin_desc_t  desc;
    RID_t rid;
}bin_info_t;

typedef struct
{
    dword_t  usage;
    dword_t  expiry_date;
    key_desc_t desc;
}key_property_t;

typedef struct
{
    dword_t mech_enc;
    wrapped_symm_key_buf_t key_buf;
    symm_mac_t  mac;
    kcv_t   kcv;
}symm_key_value_t;

typedef struct
{
    key_property_t  property;//must be first
    symm_key_value_t	key_val;
} symm_key_t;

typedef struct
{
    symm_key_t key_info;
    dword_t key_type;
}pdk_t;

typedef struct
{
    kcv_t   kcv;
}symm_key_enum_value_t;

typedef struct
{
    dword_t key_ver;
    key_property_t  property;
    symm_key_enum_value_t	key_val;
} symm_key_enum_info_t;

typedef struct
{
    dword_t key_type;
    symm_key_enum_info_t key_info;
} pdk_enum_info_t;

typedef struct
{
    dword_t	key_size;
    pub_exp_buf_t exp;
    byte_t      mod[RSA_KEY_MOD_LEN_MAX];
}rsa_pub_key_value_t;

typedef struct
{
    dword_t mech_enc;
    rsa_pub_key_value_t pub_key;
    pri_exp_buf_t pri_exp;
    pri_exponent_buf_t pri_exponent[5];
    byte_t   digest[SHA256_DIGEST_SIZE];
}rsa_key_value_t;

typedef struct
{
    rsa_pub_key_value_t pub_key;
    byte_t pri_exp[RSA_KEY_MOD_LEN_MAX];
    byte_t P[RSA_KEY_MOD_LEN_MAX/2];
    byte_t Q[RSA_KEY_MOD_LEN_MAX/2];
    byte_t DP[RSA_KEY_MOD_LEN_MAX/2];
    byte_t DQ[RSA_KEY_MOD_LEN_MAX/2];
    byte_t InvQ[RSA_KEY_MOD_LEN_MAX/2];
}rsa_key_plain_value_t;

typedef struct
{    
    key_property_t  property;//must be first
    rsa_key_value_t  key_val;
}rsa_key_t;

typedef struct
{
    dword_t     key_size;
    byte_t      digest[SHA256_DIGEST_SIZE];
}rsa_key_enum_value_t;

typedef struct
{
    dword_t key_ver;
    key_property_t  property;
    rsa_key_enum_value_t  key_val;
}rsa_key_enum_info_t;

typedef struct
{
    dword_t key_class;
    dword_t key_ver;
}wrap_key_info_t;

typedef struct
{
    bank_addr_t bank_addr;
    dword_t key_class;
}pdk_key_addr_t;

typedef struct
{
    bank_addr_t bank_addr;
    key_name_t key_name;
}udk_key_addr_t;

typedef struct
{
    bin_addr_t  bin_addr;
    key_name_t key_name;
}bin_key_addr_t;

typedef struct
{
    bin_key_addr_t key_addr;
    dword_t key_ver;
}cert_addr_t;

typedef struct
{
    dword_t key_type;
    key_desc_t desc;
}LMK_basic_info_t;

typedef struct
{
    LMK_basic_info_t basic_info;
    symm_key_buf_t key_buf;
}LMK_inject_info_t;

typedef struct
{
    LMK_basic_info_t basic_info;
    dword_t key_ver;
    kcv_t   kcv;
    dword_t time;
}LMK_query_info_t;

typedef struct
{
    rsa_pub_key_value_t pub_key;
    byte_t sign_data[RSA_KEY_MOD_LEN_MAX];
}ca_pkc_t;

typedef struct
{
    byte_t pk_idx;
    dword_t sign_data_size;
    service_identifier_t si;
    byte_t sign_data[RSA_KEY_MOD_LEN_MAX];
    byte_t detached_data[RSA_KEY_MOD_LEN_MAX];
    cert_desc_t desc;
}ca_ipkc_t;

typedef struct
{
    byte_t pk_idx;
    service_identifier_t si;
    dword_t version;
    cert_desc_t desc;
}ca_ipkc_enum_info_t;

typedef struct
{
    cert_serial_number_t csn;
    byte_t pk_idx;
    word_t expiry_date;
    service_identifier_t si;
}ca_ipkc_data_t;

#define GET_KEY_STRUCT_SIZE(keyType)        (KEY_TYPE_RSA == (keyType) ? sizeof(rsa_key_t) : sizeof(symm_key_t))

bool_t KS_CheckKCV(const kcv_t *pKCV);
bool_t KS_CheckSymmKeyVal(const symm_key_value_t* pKeyValue);
bool_t KS_CheckRSAKeyVal(const rsa_key_value_t* pKeyValue);
bool_t KS_CheckRSAPubKeyVal(const rsa_pub_key_value_t* pKeyValue);
bool_t KS_CheckRSAPainKeyVal(const rsa_key_plain_value_t* pKeyValue);
bool_t KS_CheckRID(const RID_t* pRID);

bool_t KS_CheckKeyProperty(key_property_t* pKeyProperty);
bool_t KS_CheckSymmKey(symm_key_t* pKey);
bool_t KS_CheckRSAKey(rsa_key_t* pKey);
bool_t KS_CheckSymmKeyEnumInfo(symm_key_enum_info_t* pKeyInfo, dword_t count);
bool_t KS_CheckRSAKeyEnumInfo(rsa_key_enum_info_t* pKeyInfo, dword_t count);
bool_t KS_CheckPDK(pdk_t* pKey);
bool_t KS_CheckPDKEnumInfo(pdk_enum_info_t* pKeyInfo, dword_t count);

bool_t KS_CheckKeyVal(dword_t keyType, void* pKey);
bool_t KS_CheckKey(dword_t keyType, void* pKey);

bool_t KS_CheckCAInfo(CA_info_t* info, dword_t count);
bool_t KS_CheckCAName(CA_name_t* name);
bool_t KS_CheckCAAddr(CA_addr_t* addr);
bool_t KS_CheckKeyTemplateName(key_template_name_t* name);
bool_t KS_CheckKeyTemplateInfo(key_template_info_t* info, dword_t count);

bool_t KS_CheckKeyTemplateAddr(key_template_addr_t *addr);
bool_t KS_CheckKeyDef(key_def_t *pDef, dword_t count);
bool_t KS_CheckKeyName(key_name_t *name);

bool_t KS_CheckBankInfo(bank_info_t *info, dword_t count);
bool_t KS_CheckBankName(bank_name_t *name);

bool_t KS_CheckBankAddr(bank_addr_t *addr);
bool_t KS_CheckBinInfo(bin_info_t *pBINinfo, dword_t count);
bool_t KS_CheckBinName(bin_name_t *name);

bool_t KS_CheckBinAddr(bin_addr_t *pAddr);
bool_t KS_CheckPDKAddr(pdk_key_addr_t *pAddr);
bool_t KS_CheckUDKAddr(udk_key_addr_t* pAddr);
bool_t KS_CheckBinKeyAddr(bin_key_addr_t* pAddr);

bool_t KS_CheckLMKInjectInfo(LMK_inject_info_t* LMK_inject_info);
bool_t KS_CheckLMKQueryInfo(LMK_query_info_t* LMK_query_info);

bool_t KS_CheckCAIPKC(ca_ipkc_t *pIPKC);

bool_t KS_IsSupportedSymmKeyPadType(word_t padType);
bool_t KS_IsSupportedRSAKeyPadType(word_t padType);

#ifdef __cplusplus
}
#endif

#endif

