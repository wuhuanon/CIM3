#ifndef __PROTOCOL4S_FACTORY_51436234_INCLUDED__
#define __PROTOCOL4S_FACTORY_51436234_INCLUDED__

#include <typedef.h>

#include <IComm.h>
#include <IProtocol.h>

#ifdef __cplusplus
extern "C" {
#endif

void Protocol4SFactory_Init(uint count);
void Protocol4SFactory_Final();
IProtocol4S* Protocol4SFactory_New(IComm*);
IComm* Protocol4SFactory_Del(IProtocol4S*);

void Protocol4CFactory_Init(uint count);
void Protocol4CFactory_Final();
IProtocol4C* Protocol4CFactory_New(IComm*);
IComm* Protocol4CFactory_Del(IProtocol4C*);

#ifdef __cplusplus
}
#endif

#endif
