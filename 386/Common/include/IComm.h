#ifndef __ICOMM_H_94726442_INCLUDED__
#define __ICOMM_H_94726442_INCLUDED__

#include <typedef.h>
#include <InterfaceUtil.h>

#ifdef __cplusplus
extern "C" {
#endif

enum
{
    COMM_ERROR_SUCCEEDED = 0,
    COMM_ERROR_WRITE_FAILED = 1,
    COMM_ERROR_READ_FAILED = 2,
    COMM_ERROR_TIMEOUT = 3,
};

DECLARE_INTF_METHOD_BEGIN(int, IComm_Send)
    const void* pBuf, uint size
DECLARE_INTF_METHOD_END()

DECLARE_INTF_METHOD_BEGIN(int, IComm_Recv)
    void* pBuf, uint size, uint waittime
DECLARE_INTF_METHOD_END()

DECLARE_INTF_BEGIN()
    const IComm_Send           send;
    const IComm_Recv           recv;
DECLARE_INTF_END(IComm)

#define ICOMM_SEND(pThis, pBuf, size)         INTF_V_PTR(pThis)->send(pThis, pBuf, size)
#define ICOMM_RECV(pThis, pBuf, size, wt)     INTF_V_PTR(pThis)->recv(pThis, pBuf, size, wt)

#ifdef __cplusplus
}
#endif

#endif
