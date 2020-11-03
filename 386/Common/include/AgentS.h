#ifndef __AGENT_S_H_92387445_INCLUDED__
#define __AGENT_S_H_92387445_INCLUDED__

#include <typedef.h>
#include <IProtocol.h>

#ifdef __cplusplus
extern "C" {
#endif

enum
{
    AGENT_ERROR_SUCCEEDED = 0,
    AGENT_ERROR_WRITE_FAILED = -1,
    AGENT_ERROR_READ_FAILED = -2,
    AGENT_ERROR_TIMEOUT = -3,
};

typedef struct
{
    IProtocol4S* protocol;
    uint privilege_high;
    uint privilege_low;
    uint status;
}agents_t;

#define AGENTS_SEND_DATA(pAgent, buf, size, errCode)        do{if(IPROTOCOL4S_SEND((pAgent)->protocol, buf, size) != 0) return errCode;}while(0)
#define AGENTS_FINISH_SEND_DATA(pAgent, errCode)            do{if(IPROTOCOL4S_FINISH_SEND((pAgent)->protocol) != 0) return errCode;}while(0)
#define AGENTS_RECV_DATA(pAgent, buf, size, to, errCode)    do{if(IPROTOCOL4S_RECV((pAgent)->protocol, buf, size, to) != 0) return errCode;}while(0)
#define AGENTS_FINISH_RECV_DATA(pAgent, to, errCode)        do{if(IPROTOCOL4S_FINISH_RECV((pAgent)->protocol,to) != 0) return errCode;}while(0)

#ifdef __cplusplus
}
#endif

#endif
