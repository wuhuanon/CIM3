
#ifndef __CA_H_INLUDED_35036685__
#define __CA_H_INLUDED_35036685__

#define CA_NAME_VISA            "VISA"
#define CA_DESC_VISA            ""

#define CA_NAME_MASTER_CARD     "MasterCard"
#define CA_DESC_MASTER_CARD     ""

#define CA_NAME_UNION_PAY       "UnionPay"
#define CA_DESC_UNION_PAY       ""

#define CA_RID_VISA             {0xA0, 0x00, 0x00, 0x00, 0x03}
#define CA_RID_MASTER_CARD      {0xA0, 0x00, 0x00, 0x00, 0x04}
#define CA_RID_UNIONPAY         {0xA0, 0x00, 0x00, 0x03, 0x33}

#define KEY_TEMPLATE_NAME_DDA   "DDA"
#define KEY_TEMPLATE_DESC_DDA   ""
#define KEY_TEMPLATE_NAME_SDA   "SDA"
#define KEY_TEMPLATE_DESC_SDA   ""

#define KEY_NAME_VISA_AC        "AC"
#define KEY_NAME_VISA_MAK       "MAC"
#define KEY_NAME_VISA_ENC       "ENC"
#define KEY_NAME_VISA_RSA       "IssuerPK"

#define KEY_DESC_VISA_AC        ""
#define KEY_DESC_VISA_MAK       ""
#define KEY_DESC_VISA_ENC       ""
#define KEY_DESC_VISA_RSA       ""

#define KEY_NAME_MCA_MAS4C      "MAS4C"
#define KEY_NAME_MCA_CT_AC      "AC_CT"
#define KEY_NAME_MCA_CT_ENC     "ENC_CT"
#define KEY_NAME_MCA_CT_MAC     "MAC_CT"
#define KEY_NAME_MCA_CT_KDCVD3  "KDCVC3_CT"
#define KEY_NAME_MCA_CT_DNMK    "DNMK_CT"
#define KEY_NAME_MCA_CL_AC      "AC_CL"
#define KEY_NAME_MCA_CL_ENC     "ENC_CL"
#define KEY_NAME_MCA_CL_MAC     "MAC_CL"
#define KEY_NAME_MCA_CL_KDCVD3  "KDCVC3_CL"
#define KEY_NAME_MCA_CL_DNMK    "DNMK_CL"

#define KEY_DESC_MCA_MAS4C      ""
#define KEY_DESC_MCA_CT_AC      ""
#define KEY_DESC_MCA_CT_ENC     ""
#define KEY_DESC_MCA_CT_MAC     ""
#define KEY_DESC_MCA_CT_KDCVD3  ""
#define KEY_DESC_MCA_CT_DNMK    ""
#define KEY_DESC_MCA_CL_AC      ""
#define KEY_DESC_MCA_CL_ENC     ""
#define KEY_DESC_MCA_CL_MAC     ""
#define KEY_DESC_MCA_CT_KDCVD3  ""
#define KEY_DESC_MCA_CL_DNMK    ""

#define EMV_PUB_KEY_3           {3}
#define EMV_PUB_KEY_75537       {1,0,1}

enum
{
    VISA_SI_DC = 0,
    VISA_SI_ELECTRON = 1,
    VISA_SI_VPAY = 2,
    VISA_SI_INTER_LINK = 3,
    VISA_SI_PLUS = 4,
};

#define VISA_SI_VALUE           \
    {0x10, 0x10, 0x00, 0x00},   \
    {0x20, 0x10, 0x00, 0x00},   \
    {0x20, 0x20, 0x00, 0x00},   \
    {0x30, 0x10, 0x00, 0x00},   \
    {0x80, 0x10, 0x00, 0x00},

enum
{
    UNIONPAY_SI_DC = 0,
    UNIONPAY_SI_DEBIT = 1,
    UNIONPAY_SI_CREDIT = 2,
    UNIONPAY_SI_QUASI = 3,
    UNIONPAY_SI_ECASH = 4,
};

#define UNIONPAY_SI_VALUE       \
    {0x01, 0x01, 0x00, 0x00},   \
    {0x01, 0x01, 0x01, 0x00},   \
    {0x01, 0x01, 0x02, 0x00},   \
    {0x01, 0x01, 0x03, 0x00},   \
    {0x01, 0x01, 0x06, 0x00},

#endif
