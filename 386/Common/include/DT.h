#ifndef __DT_H_58638462_INCLUDED__
#define __DT_H_58638462_INCLUDED__

#include <typedef.h>
#include <AgentC.h>
#include <FCPS.h>

#ifdef __cplusplus
extern "C" {
#endif

int DT_EnumBank(agentc_t *pAgent, bank_info_t** ppInfo, dword_t *pCount);
int DT_EnumBIN(agentc_t *pAgent, const bank_addr_t* addr, bin_info_t** ppInfo, dword_t *pCount);
int DT_EnumKeyDefOfBIN(agentc_t *pAgent, const bin_addr_t* addr, key_def_t** ppInfo, dword_t *pCount);
int DT_EnumPDK(agentc_t *pAgent, const pdk_key_addr_t *addr, pdk_enum_info_t **ppInfo, dword_t *pCount);
int DT_EnumBINKey(agentc_t *pAgent, const bin_key_addr_t *addr, dword_t *pKeyType, void **ppInfo, dword_t *pCount);
int DT_QueryPDK(agentc_t *pAgent, const pdk_key_addr_t *addr, dword_t keyVer, pdk_t *pKey);
int DT_QueryBINKey(agentc_t *pAgent, const bin_key_addr_t *addr, dword_t keyVer, dword_t *pKeyType, void **ppKey);
int DT_EnumCAIPKC(agentc_t *pAgent, const cert_addr_t* pAddr, ca_ipkc_enum_info_t **ppIPKC, dword_t* pCount);
int DT_QueryCAIPKC(agentc_t *pAgent, const cert_addr_t *pAddr, dword_t ver, ca_ipkc_t *pIPKC);

#ifdef __cplusplus
}
#endif

#endif
