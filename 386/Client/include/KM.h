#ifndef __KM_H_45879346_INCLUDED__
#define __KM_H_45879346_INCLUDED__

#include <typedef.h>
#include <IProtocol.h>
#include <KeyStruct.h>
#include <FCPS.h>
#include <ICryptService.h>
#include <AgentC.h>

#ifdef __cplusplus
extern "C" {
#endif

int KM_NewCA(agentc_t *pAgent, const CA_info_t* info);
int KM_DelCA(agentc_t *pAgent, const CA_name_t* name);
int KM_EnumCA(agentc_t *pAgent, CA_info_t** ppInfo, dword_t *pCount);

int KM_NewKeyTemplate(agentc_t *pAgent, const CA_addr_t* pAddr, const key_template_info_t* pInfo, const key_def_t* pKeyDef, dword_t count);
int KM_DelKeyTemplate(agentc_t *pAgent, const CA_addr_t* addr, const key_template_name_t* name);
int KM_EnumKeyTemplate(agentc_t *pAgent, const CA_addr_t* addr, key_template_info_t** ppInfo, dword_t *pCount);

int KM_NewKeyDef2Template(agentc_t *pAgent, const key_template_addr_t* addr, const key_def_t* info);
int KM_DelKeyDef4Template(agentc_t *pAgent, const key_template_addr_t* addr, const key_name_t* name);
int KM_EnumKeyDefOfTemplate(agentc_t *pAgent, const key_template_addr_t* addr, key_def_t** ppInfo, dword_t *pCount);

int KM_NewBank(agentc_t *pAgent, const bank_info_t* info);
int KM_DelBank(agentc_t *pAgent, const bank_name_t* name);
int KM_EnumBank(agentc_t *pAgent, bank_info_t** ppInfo, dword_t *pCount);

int KM_NewBIN(agentc_t *pAgent, const bank_addr_t* addr, const bin_info_t* info, const key_def_t* pKeyDef, dword_t count);
int KM_DelBIN(agentc_t *pAgent, const bank_addr_t* addr, const bin_name_t* name);
int KM_EnumBIN(agentc_t *pAgent, const bank_addr_t* addr, bin_info_t** ppInfo, dword_t *pCount);

int KM_NewKeyDef2UDK(agentc_t *pAgent, const bank_addr_t* addr, const key_def_t* info);
int KM_DelKeyDef4UDK(agentc_t *pAgent, const bank_addr_t* addr, const key_name_t* name);
int KM_EnumKeyDefOfUDK(agentc_t *pAgent, const bank_addr_t* addr, key_def_t** ppInfo, dword_t *pCount);

int KM_NewKeyDef2BIN(agentc_t *pAgent, const bin_addr_t* addr, const key_def_t* info);
int KM_DelKeyDef4BIN(agentc_t *pAgent, const bin_addr_t* addr, const key_name_t* name);
int KM_EnumKeyDefOfBIN(agentc_t *pAgent, const bin_addr_t* addr, key_def_t** ppInfo, dword_t *pCount);

int KM_NewPDK(agentc_t *pAgent, const pdk_key_addr_t *addr, const wrap_key_info_t* wrap_key, pdk_t *info, dword_t *pKeyVer);
int KM_EnumPDK(agentc_t *pAgent, const pdk_key_addr_t *addr, pdk_enum_info_t **ppInfo, dword_t *pCount);
int KM_QueryPDK(agentc_t *pAgent, const pdk_key_addr_t *addr, dword_t keyVer, const wrap_key_info_t* wrap_key, dword_t mechEnc, pdk_t *info);
int KM_DelPDK(agentc_t *pAgent, const pdk_key_addr_t *addr, dword_t keyVer);

int KM_NewUDK(agentc_t *pAgent, const udk_key_addr_t *addr, const wrap_key_info_t* wrap_key, dword_t keyType, void *info, dword_t *pKeyVer);
int KM_EnumUDK(agentc_t *pAgent, const udk_key_addr_t *addr, dword_t *pKeyType, void **ppInfo, dword_t *pCount);
int KM_QueryUDK(agentc_t *pAgent, const udk_key_addr_t *addr, dword_t keyVer, const wrap_key_info_t* wrap_key, dword_t mechEnc, dword_t* pKeyType, void* *ppBuf);
int KM_DelUDK(agentc_t *pAgent, const udk_key_addr_t *addr, dword_t keyVer);

int KM_NewBINKey(agentc_t *pAgent, const bin_key_addr_t *addr, const wrap_key_info_t* wrap_key, dword_t keyType, void *info, dword_t *pKeyVer);
int KM_EnumBINKey(agentc_t *pAgent, const bin_key_addr_t *addr, dword_t *pKeyType, void **ppInfo, dword_t *pCount);
int KM_QueryBINKey(agentc_t *pAgent, const bin_key_addr_t *addr, dword_t keyVer, const wrap_key_info_t* wrap_key, dword_t mechEnc, dword_t* pKeyType, void* *ppBuf);
int KM_DelBINKey(agentc_t *pAgent, const bin_key_addr_t *addr, dword_t keyVer);

int KM_InjectLMK2HSM(agentc_t* pAgent, const LMK_inject_info_t* LMK_inject_info);
int KM_InjectLMK2KMS(agentc_t* pAgent, const LMK_inject_info_t* LMK_inject_info, dword_t *pKeyVer);
int KM_GetLMKInfo(agentc_t* pAgent, LMK_query_info_t* LMK_Query_info);

int KM_ReWrapKeyFromLMK(agentc_t *pAgent, const bank_addr_t *addr, const wrap_key_info_t* wrap_key, dword_t mechEnc, dword_t keyType, void* pKey);
int KM_ReWrapKeyToLMK(agentc_t *pAgent, const bank_addr_t *addr, const wrap_key_info_t* wrap_key, dword_t keyType, void* pKey);

int KM_NewCAPKC(agentc_t *pAgent, const RID_t *rid, byte_t pkIdex, const rsa_pub_key_value_t *pKey, const void *pSignData);
int KM_DelCAPKC(agentc_t *pAgent, const RID_t *rid, byte_t pkIdx);
int KM_EnumCAPKC(agentc_t *pAgent, const RID_t *rid, byte_t **ppPKidx, dword_t* pCount);
int KM_QueryCAPKC(agentc_t *pAgent, const RID_t *rid, byte_t pkIdex, rsa_pub_key_value_t *pKey);

int KM_NewCAIPKC(agentc_t *pAgent, const cert_addr_t* pAddr, const ca_ipkc_t* pIPKC, dword_t *pVersion);
int KM_DelCAIPKC(agentc_t *pAgent, const cert_addr_t* pAddr, dword_t version);
int KM_EnumCAIPKC(agentc_t *pAgent, const cert_addr_t* pAddr, ca_ipkc_enum_info_t **ppIPKC, dword_t* pCount);
int KM_QueryCAIPKC(agentc_t *pAgent, const cert_addr_t* pAddr, dword_t version, ca_ipkc_t* pIPKC);

int CryptServiceClientFactory_Init();
ICryptService* CryptServiceClientFactory_New(IProtocol4C* pProtocol);

#ifdef __cplusplus
}
#endif

#endif
