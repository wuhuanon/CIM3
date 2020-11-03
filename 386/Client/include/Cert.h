#ifndef __CERT_H_13956323_INCLUDED__
#define __CERT_H_13956323_INCLUDED__

#include <typedef.h>
#include <KeyStruct.h>
#include <FCPS.h>
#include <AgentC.h>
#include <QFile>

enum
{
    CERT_ERR_SUCCEEDED = 0,
    CERT_ERR_SERVER = 1,
    CERT_ERR_KEY_LEN = 2,
    CERT_ERR_FORMAT = 3,
    CERT_ERR_KEY_MISMATCH = 4,
    CERT_ERR_FILE_OP = 5,
};

int CertVisa_GenIPKC(ICryptService *cryptService, const rsa_key_value_t* pKey, const bin_name_t* pBIN, word_t expiryDate, const tracking_number_t *tn, const service_identifier_t *si, void* pSignData);
int CertVisa_ParseCAPKC(ICryptService* pCS, rsa_pub_key_value_t* pKey, const void *pSignData, byte_t* pPKidx, service_identifier_t* si, void* pRID, word_t *pExpiryDate, void* pDigest);
int CertVisa_ParseCAIPKC(ICryptService* pCS, const rsa_pub_key_value_t* pKeyIsser, const rsa_pub_key_value_t* pKeyCA, const void *pSignData, byte_t *pBIN, ca_ipkc_data_t* pCertData);

int CertFileVisa_GenIPKC(int certType, const rsa_pub_key_value_t* pKey, const tracking_number_t *tn, const void* pSignData,  QFile* file);
int CertFileVisa_VerifyCAPKC(ICryptService *pCS, QFile *pFile, byte_t* pRID, rsa_pub_key_value_t* pKey, byte_t *pPubKeyIdx, service_identifier_t *si, word_t *pExpiryDate, void* pSignBuf);
int CertFileVisa_VerifyCAIPKC(agentc_t *pAgent, QFile *pFile, const RID_t *rid, const rsa_pub_key_value_t* pKeyIssuer, byte_t *pBIN, ca_ipkc_data_t* pCert, void* pSignData, void* pDetachedData, dword_t *pCAModLen);
int CertFileVisa_GenCAIPKC(const rsa_pub_key_value_t* pIsserPK, const byte_t *pBIN, const ca_ipkc_data_t* pCert, const void* pSignData, const void* pDetachedData, dword_t caModLen, QFile *pFile);

#endif
