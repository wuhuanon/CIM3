#ifndef __AGENT_C_H_85684567_INCLUDED__
#define __AGENT_C_H_85684567_INCLUDED__

#include <typedef.h>

#include <IProtocol.h>
#include <ICryptService.h>

#ifdef __cplusplus
extern "C" {
#endif

enum
{
    AGENTC_ERROR_SUCCEEDED = 0,
    AGENTC_ERROR_WRITE_FAILED = -1,
    AGENTC_ERROR_READ_FAILED = -2,
    AGENTC_ERROR_TIMEOUT = -3,
};

typedef struct
{
    IProtocol4C* protocol;
    ICryptService* crypt_service;
}agentc_t;

void AgentC_Init(agentc_t *pAgent, IProtocol4C* pProtocol);

#define AGENTC_SEND_DATA(pAgent, buf, size)	do{if(IPROTOCOL4C_SEND((pAgent)->protocol, buf, size) != 0) return FCPS_ERROR_COMM_FAILED;}while(0)
#define AGENTC_FINISH_SEND_DATA(pAgent)		do{if(IPROTOCOL4C_FINISH_SEND((pAgent)->protocol) != 0) return FCPS_ERROR_COMM_FAILED;}while(0)
#define AGENTC_RECV_DATA(pAgent, buf, size, to) do{if(IPROTOCOL4C_RECV((pAgent)->protocol, buf, size, to) != 0) return FCPS_ERROR_COMM_FAILED;}while(0)
#define AGENTC_FINISH_RECV_DATA(pAgent, to)     do{if(IPROTOCOL4C_FINISH_RECV((pAgent)->protocol,to) != 0) return FCPS_ERROR_COMM_FAILED;}while(0)


#ifdef __cplusplus
}
#endif

#endif
