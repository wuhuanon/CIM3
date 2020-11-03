#ifndef __CONSTANTS_UD_H_INCLUDED_57568777__
#define __CONSTANTS_UD_H_INCLUDED_57568777__

enum
{
    KEY_CLASS_LMK = 0,
    KEY_CLASS_ZMK = 1,
    KEY_CLASS_KEK = 2,
    KEY_CLASS_TK = 3,
    KEY_CLASS_PEK = 4,
    KEY_CLASS_KMC = 5,
    KEY_CLASS_KMU = 6,
    KEY_CLASS_UDK = 7,
    KEY_CLASS_BIN = 0x100,
    KEY_CLASS_UNKNOWN = -1,
};

enum
{
    KEY_TYPE_SDES = 1,
    KEY_TYPE_DDES = 2,
    KEY_TYPE_TDES = 3,
    KEY_TYPE_AES = 4,
    KEY_TYPE_RSA = 0x101,
    KEY_TYPE_UNKNOWN = -1,
};

enum
{
    KEY_TYPE_MASK_SDES = 1 << 0,
    KEY_TYPE_MASK_DDES = 1 << 1,
    KEY_TYPE_MASK_TDES = 1 << 2,
    KEY_TYPE_MASK_AES = 1 << 3,
    KEY_TYPE_MASK_RSA = 1 << 4,
};

enum
{
    CA_TYPE_VISA = 1,
    CA_TYPE_UNIONPAY = 2,
    CA_TYPE_MASTERCARD = 3,
    CA_TYPE_UNKNOWN = -1,
};

enum
{
    CERT_TYPE_VISA = 1,
    CERT_TYPE_UNIONPAY = 2,
    CERT_TYPE_MASTERCARD = 3,
    CERT_TYPE_UNKNOWN = -1,
};

enum
{
    MECH_MODE_ECB = 0x00000000,
    MECH_MODE_CBC = 0x00010000,
    MECH_MODE_UNKNOWN = 0xFFFF0000,
};

#if 0
    MECH_SDES_ECB = 1,
    MECH_SDES_CBC = 2,
    MECH_SDES_CBC_PAD = 3,
    MECH_TDES_ECB = 4,
    MECH_TDES_CBC = 5,
    MECH_TDES_CBC_PAD = 6,
#endif

enum
{
    MECH_MODE_X509 = 0x01010000,
};

#if 0
enum
{
    MECH_NO_MAC = 0,
    MECH_SDES_MAC = 1,
    MECH_TDES_MAC = 2,

    MECH_RSA_MAC_X509 = 0x01010000,
};
#endif

enum
{
        DIGEST_ID_NONE = 0,
        DIGEST_ID_SHA1 = 1,
        DIGEST_ID_SHA224 = 2,
        DIGEST_ID_SHA256 = 3,
        DIGEST_ID_SHA384 = 4,
        DIGEST_ID_SHA512 = 5,
        DIGEST_ID_MD5 = 6,
};

enum
{
    PAD_TYPE_NO_PAD = 0,
    PAD_TYPE_ISO9797_M1 = 1,
    PAD_TYPE_ISO9797_M2 = 2,
    PAD_TYPE_PKCS5 = 3,
};

enum
{
    DP_TASK_OP_TO_FIRST = 1,
    DP_TASK_OP_TO_LAST = 2,
    DP_TASK_OP_FORWARD = 3,
    DP_TASK_OP_AFTERWARD = 4,
};

#define MECH_WRAP_GET_PAD_TYPE(mech)        ((mech) & 0xFFFF)
#define MECH_WRAP_GET_MECH_ENC(mech)        ((mech) & 0xFFFF0000)

#endif
