#ifndef __CONSTANTS_CF_H_INCLUDED_55798547__
#define __CONSTANTS_CF_H_INCLUDED_55798547__

#include <Constants_ud.h>

#define USER_NAME_LENGTH_MAX			63
#define USER_GROUP_NAME_LENGTH_MAX		63

#define CA_NAME_LEN_MAX                 63
#define KEY_TEMPLATE_NAME_LEN_MAX       63
#define KEY_NAME_LEN_MAX                63
#define BANK_NAME_LEN_MAX               63

#define BIN_NAME_LEN_MIN                6
#define BIN_NAME_LEN_MAX                8

#define BIN_VALUE_LEN                   4

#define KEY_DESC_LEN_MAX                255
#define BIN_DESC_LEN_MAX                255
#define CA_DESC_LEN_MAX                 255
#define BANK_DESC_LEN_MAX               255
#define KEY_TEMPLATE_DESC_LEN_MAX       255
#define KEY_DESC_LEN_MAX                255
#define CERT_DESC_LEN_MAX               255

#define EMV_RID_LEN_MAX                 15

#define RSA_KEY_MOD_LEN_MIN             64
#define RSA_KEY_MOD_LEN_MAX             512

#define RSA_PUB_EXP_LEN_MAX             3
#define RSA_PRI_EXP_LEN_MAX             RSA_KEY_MOD_LEN_MAX

#define RSA_PRI_KEY_WRAPPED_LEN_MAX     4096

#define SYMM_KEY_LEN_MAX                TDES_KEY_LEN

#define SYMM_KEY_WRAPPED_LEN_MAX        ((TDES_KEY_LEN)+8)

#define SYMM_MAC_LEN_MAX                16

#define KCV_LEN_MAX                     8

#define KMS_MECHANISM_ENC_SYMM      MECH_MODE_ECB
#define KMS_MECHANISM_ENC_RSA       (MECH_MODE_ECB | PAD_TYPE_ISO9797_M2)
#define KMS_MECHANISM_DIGEST        DIGEST_ID_SHA256//fixed, in accordance with RSA key struct

#define CARD_DATA_NAME_LEN_MAX          255
#define KEY_VERSION_MAX                 255

#endif
