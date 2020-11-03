#ifndef DATATEMPLATE_DBC_H
#define DATATEMPLATE_DBC_H
#include <profileStruct.h>
#include <typedef.h>
#include <AgentC.h>

#ifdef __cplusplus
extern "C" {
#endif

int DT_EnumPaymentInf(agentc_t *pAgent, c_payment_define** pPaymentInf, dword_t *numOf);
int DT_QueryPaymentTags(agentc_t *pAgent,const c_payment_define* pPaymentInf, c_tag_define** pPayment, dword_t *numOf);
int DT_NewPayment(agentc_t *pAgent, const c_tag_define* pPayment, dword_t count);
int DT_DelPayment(agentc_t *pAgent,const c_payment_define* paymentNameVersion);
int DT_UpdatePayment(agentc_t *pAgent, const c_tag_define* pTags, dword_t count);

int DT_EnumProfileInf(agentc_t *pAgent, c_profile_define** pProfile, dword_t *pCount);
int DT_QueryProfileInf(agentc_t *pAgent, const char* profile_dgi_group, c_profile_define* pProfile);
int DT_QueryProfileDGIs(agentc_t *pAgent, const c_profile_define* pProfile, char** pDGIs);
int DT_NewProfile(agentc_t *pAgent,const c_profile_DGIs* pProDGIs);
int DT_DelProfile(agentc_t *pAgent, const c_profile_define* pProfile);
int DT_UpdateProfile(agentc_t *pAgent,const c_profile_DGIs* pProDGIs);

int DT_EnumDataTemplate(agentc_t *pAgent, c_template_define** pTempl, dword_t *numOf);
int DT_QueryDataTemplate(agentc_t *pAgent, const c_template_info* pTemplInf, c_template_define *pTempl);
int DT_NewDataTemplate(agentc_t *pAgent, const c_template_define* pTempl);
int DT_DelDataTemplate(agentc_t *pAgent, const c_template_info* pTemplInf);
int DT_UpdateDataTemplate(agentc_t *pAgent, const c_template_define* pTempl);

#ifdef __cplusplus
}
#endif
#endif // DATATEMPLATE_DBC_H
