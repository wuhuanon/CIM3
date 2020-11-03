#ifndef __COMM_FACTORY_H_34573890_INCLUDED__
#define __COMM_FACTORY_H_34573890_INCLUDED__

#include <QTcpSocket>
#include <IComm.h>

void CommFactory_Init(uint count);
void CommFactory_Final();
IComm* CommFactory_NewByQTcpSocket(QTcpSocket*);
QTcpSocket* CommFactory_DelFromQTcpSocket(IComm*);

#endif
