#ifndef __IPROTOCOL_93031584_INCLUDED__
#define __IPROTOCOL_93031584_INCLUDED__

#include <typedef.h>
#include <InterfaceUtil.h>

#ifdef __cplusplus
extern "C" {
#endif

enum
{
    PROTOCOL_ERR_SUCCEEDED = 0,
    PROTOCOL_ERR_WRITE_FAILED = 1,
    PROTOCOL_ERR_READ_FAILED = 2,
    PROTOCOL_ERR_TIMEOUT = 3,
    PROTOCOL_ERR_REJECTED = 4,
};

typedef int (*IProtocol_Send)(void* pThis, const void* pBuf, uint size);
typedef int (*IProtocol_Recv)(void* pThis, void* pBuf, uint size, uint waittime);

typedef int (*IProtocol_FinishSend)(void* pThis);
typedef int (*IProtocol_FinishRecv)(void* pThis, uint waittime);

typedef int (*IProtocol_Crypt)(void* pThis, const void* pInBuf, uint inSize, void* pOutBuf, uint* pOutSize, bool_t bEnc);

typedef int (*IProtocol4S_Accept)(void* pThis);
typedef int (*IProtocol4S_Reject)(void* pThis);

typedef int (*IProtocol4C_HandShake)(void* pThis);

DECLARE_INTF_BEGIN()
    const IProtocol_Send            send;
    const IProtocol_Recv            recv;
    const IProtocol_FinishSend      finish_send;
    const IProtocol_FinishRecv      finish_recv;
    const IProtocol_Crypt           crypt;
DECLARE_INTF_END(IProtocol)

DECLARE_INTF_EXTEND_BEGIN(IProtocol)
    const IProtocol4S_Accept        accept;
    const IProtocol4S_Reject        reject;
DECLARE_INTF_END(IProtocol4S)

DECLARE_INTF_EXTEND_BEGIN(IProtocol)
    const IProtocol4C_HandShake     hand_shake;
DECLARE_INTF_END(IProtocol4C)

#define IPROTOCOL_SEND(pThis, pBuf, size)             INTF_V_PTR(pThis)->send(pThis, pBuf, size)
#define IPROTOCOL_RECV(pThis, pBuf, size, timeout)    INTF_V_PTR(pThis)->recv(pThis, pBuf, size, timeout)
#define IPROTOCOL_FINISH_SEND(pThis)                  INTF_V_PTR(pThis)->finish_send(pThis)
#define IPROTOCOL_FINISH_RECV(pThis, timeout)         INTF_V_PTR(pThis)->finish_recv(pThis, timeout)

#define IPROTOCOL4S_SEND(pThis, pBuf, size)           INTF_SUPER(INTF_V_PTR(pThis), IProtocol)->send(pThis, pBuf, size)
#define IPROTOCOL4S_RECV(pThis, pBuf, size, timeout)  INTF_SUPER(INTF_V_PTR(pThis), IProtocol)->recv(pThis, pBuf, size, timeout)
#define IPROTOCOL4S_FINISH_SEND(pThis)                INTF_SUPER(INTF_V_PTR(pThis), IProtocol)->finish_send(pThis)
#define IPROTOCOL4S_FINISH_RECV(pThis, timeout)       INTF_SUPER(INTF_V_PTR(pThis), IProtocol)->finish_recv(pThis, timeout)

#define IPROTOCOL4C_SEND(pThis, pBuf, size)           INTF_SUPER(INTF_V_PTR(pThis), IProtocol)->send(pThis, pBuf, size)
#define IPROTOCOL4C_RECV(pThis, pBuf, size, timeout)  INTF_SUPER(INTF_V_PTR(pThis), IProtocol)->recv(pThis, pBuf, size, timeout)
#define IPROTOCOL4C_FINISH_SEND(pThis)                INTF_SUPER(INTF_V_PTR(pThis), IProtocol)->finish_send(pThis)
#define IPROTOCOL4C_FINISH_RECV(pThis, timeout)       INTF_SUPER(INTF_V_PTR(pThis), IProtocol)->finish_recv(pThis, timeout)

#define IPROTOCOL4S_ACCEPT(pThis)                     INTF_V_PTR(pThis)->accept(pThis)
#define IPROTOCOL4S_REJECT(pThis)                     INTF_V_PTR(pThis)->reject(pThis)
#define IPROTOCOL4C_HANDSHAKE(pThis)                  INTF_V_PTR(pThis)->hand_shake(pThis)

#define IPROTOCOL_CRYPT(pThis, pBuf, pInBuf, inSize, pOutBuf, pOutSize, bEnc) INTF_V_PTR(pThis)->crypt(pThis, pInBuf, inSize, pOutBuf, pOutSize, bEnc)

#define IPROTOCOL_ENCRYPT(pThis, pBuf, pInBuf, inSize, pOutBuf, pOutSize)     IPROTOCOL_CRYPT(pThis, pBuf, pInBuf, inSize, pOutBuf, pOutSize, TRUE)
#define IPROTOCOL_DECRYPT(pThis, pBuf, pInBuf, inSize, pOutBuf, pOutSize)     IPROTOCOL_CRYPT(pThis, pBuf, pInBuf, inSize, pOutBuf, pOutSize, FALSE)

#ifdef __cplusplus
}
#endif

#endif
