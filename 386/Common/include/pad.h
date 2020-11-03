#ifndef __PAD_H_4344573234287567435_DEFINED__
#define __PAD_H_4344573234287567435_DEFINED__

#include <typedef.h>
#include <Constants.h>

uint	PAD_ISO9797M2Padding(void *pBuf, uint inLen, word_t blockSize);
int PAD_ISO9797M2Unpadding(void *pBuf, word_t blockSize);

uint PAD_MakePadding(void *pBlock, uint inLen, word_t blockSize, int padType);
int PAD_MakeUnPadding(void *pBlock, word_t blockSize, int padType);

#endif
