#ifndef __ICRYPT_SERVICE_H_50354674_INCLUDED__
#define __ICRYPT_SERVICE_H_50354674_INCLUDED__

#include <KeyStruct.h>
#include <InterfaceUtil.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef int (*CS_InjectSymmKeyFuncPtr)(void *pThis, dword_t keyType, const byte_t* pKeyVal, dword_t keyValLen, symm_key_value_t* key);
typedef int (*CS_InjectRSAKeyFuncPtr)(void* pThis, const rsa_key_plain_value_t *pKeyVal, rsa_key_value_t* pOut);
typedef int (*CS_GenerateSymmKeyFuncPtr)(void *pThis, dword_t keyType, symm_key_value_t* pKey);
typedef int (*CS_GenerateRSAKeyFuncPtr)(void *pThis, dword_t keySize, const byte_t* pPubExp, dword_t pubExpLen, rsa_key_value_t* pKey);
typedef int (*CS_CalcKCVFuncPtr)(void *pThis, dword_t keyType, const byte_t* keyVal, dword_t keyValLen, kcv_t* pKCV);
typedef int (*CS_DigestFuncPtr)(void *pThis, dword_t digestType, const void* pIn, dword_t inSize, void *pOut, dword_t* pOutSize);
typedef int (*CS_SymmCryptFuncPtr)(void *pThis, dword_t keyType, const symm_key_value_t *pKeyVal, dword_t mech, const void *pIn, dword_t inSize, void *pOut, bool_t bEnc);
typedef int (*CS_RSAPrivateEncryptFuncPtr)(void *pThis, const rsa_key_value_t *pKeyVal, const void *pIn, dword_t inSize, void* pOut, dword_t* pOutSize);
typedef int (*CS_RSAPublicDecryptFuncPtr)(void *pThis, const rsa_pub_key_value_t *pKeyVal, const void *pIn, dword_t inSize, void* pOut, dword_t* pOutSize);
typedef int (*CS_RSASignFuncPtr)(void *pThis, const rsa_key_value_t *pKeyVal, const void *pIn, dword_t inSize, void* pOut, dword_t* pOutSize);
typedef int (*CS_RSAVerifyFuncPtr)(void *pThis, const rsa_pub_key_value_t *pKeyVal, const void *pIn, dword_t inSize, const void* pSignData);

DECLARE_INTF_BEGIN()
    CS_InjectSymmKeyFuncPtr     InjectSymmKey;
    CS_InjectRSAKeyFuncPtr      InjectRSAKey;
    CS_GenerateSymmKeyFuncPtr   GenerateSymmKey;
    CS_GenerateRSAKeyFuncPtr    GenerateRSAKey;
    CS_CalcKCVFuncPtr           CalcKCV;
    CS_DigestFuncPtr            Digest;
    CS_SymmCryptFuncPtr         SymmCrypt;
    CS_RSAPrivateEncryptFuncPtr RSAPrivateEncrypt;
    CS_RSAPublicDecryptFuncPtr  RSAPublicDecrypt;
    CS_RSASignFuncPtr           RSASign;
    CS_RSAVerifyFuncPtr         RSAVerify;
DECLARE_INTF_END(ICryptService)

#define ICS_InjectSymmKey(pThis, keyType, pKeyVal, keyValLen, key)                  INTF_V_PTR(pThis)->InjectSymmKey(pThis, keyType, pKeyVal, keyValLen, key)
#define ICS_InjectRSAKey(pThis, pKeyVal, pOut)                                      INTF_V_PTR(pThis)->InjectRSAKey(pThis, pKeyVal, pOut)
#define ICS_GenerateSymmKey(pThis, keyType, pKey)                                   INTF_V_PTR(pThis)->GenerateSymmKey(pThis, keyType, pKey)
#define ICS_GenerateRSAKey(pThis, keySize, pPubExp, pubExpLen, pKey)                INTF_V_PTR(pThis)->GenerateRSAKey(pThis, keySize, pPubExp, pubExpLen, pKey)
#define ICS_CalcKCV(pThis, keyType, pKeyVal, keyValLen, pKCV)                       INTF_V_PTR(pThis)->CalcKCV(pThis, keyType, pKeyVal, keyValLen, pKCV)
#define ICS_Digest(pThis, digestType, pIn, inSize, pOut, pOutSize)                  INTF_V_PTR(pThis)->Digest(pThis, digestType, pIn, inSize, pOut, pOutSize)
#define ICS_SymmCrypt(pThis, keyType, pKeyVal, mech, pIn, inSize, pOut, bEnc)       INTF_V_PTR(pThis)->SymmCrypt(pThis, keyType, pKeyVal, mech, pIn, inSize, pOut, bEnc)
#define ICS_RSAPrivateEncrypt(pThis, pKeyVal, pIn, inSize, pOut, pOutSize)          INTF_V_PTR(pThis)->RSAPrivateEncrypt(pThis, pKeyVal, pIn, inSize, pOut, pOutSize)
#define ICS_RSAPublicDecrypt(pThis, pKeyVal, pIn, inSize, pOut, pOutSize)           INTF_V_PTR(pThis)->RSAPublicDecrypt(pThis, pKeyVal, pIn, inSize, pOut, pOutSize)
#define ICS_RSASign(pThis, pKeyVal, pIn, inSize, pOut, pOutSize)                    INTF_V_PTR(pThis)->RSASign(pThis, pKeyVal, pIn, inSize, pOut, pOutSize)
#define ICS_RSAVerify(pThis, pKeyVal, pIn, inSize, pSignData)                       INTF_V_PTR(pThis)->RSAVerify(pThis, pKeyVal, pIn, inSize, pSignData)

#ifdef __cplusplus
}
#endif

#endif//defined __ICRYPT_SERVICE_H_50354674_INCLUDED__
