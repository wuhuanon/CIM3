#ifndef __EXEC_UTIL_H_INCLUDED_39472642__
#define __EXEC_UTIL_H_INCLUDED_39472642__

#include <typedef.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

#define ExecUtil_DeclarePtrAndCountImpl(type, ptrName, countName, gCacheBuf, gCacheSize)    \
type* ptrName = (type*)gCacheBuf;                                                           \
dword_t countName = gCacheSize / sizeof(type)

#define ExecUtil_ExecImpl(ret, func, noEnoughRet, pBuf, type, count, gCacheBuf, gCacheSize) \
    do{                                                             \
            ret = func;                                             \
            if(noEnoughRet == ret)                                  \
            {                                                       \
                dword_t newSize4ExceUtil = sizeof(type)*count;      \
                free(gCacheBuf);                                    \
                gCacheBuf = malloc(newSize4ExceUtil);               \
                if(NULL == gCacheBuf)                               \
                {                                                   \
                    gCacheSize = 0;                                 \
                    ret = noEnoughRet;                              \
                }                                                   \
                else                                                \
                {                                                   \
                    gCacheSize = newSize4ExceUtil;                  \
                    pBuf = (type*)gCacheBuf;                        \
                    ret = func;                                     \
                }                                                   \
            }                                                       \
    }while(0)


#define MemUtil_DeclarePtrAndCountImpl(type, ptrName, countName)    \
    type* ptrName;                                                  \
    dword_t countName

#define MemUtil_AllocImpl(type, name, count, errCode, gCacheBuf, gCacheSize) \
    do{                                                     \
        dword_t size4MemUtil = sizeof(type)*(count);        \
        if(gCacheSize < size4MemUtil)                       \
        {                                                   \
            free(gCacheBuf);                                \
            gCacheBuf = malloc(size4MemUtil);               \
            if(NULL == gCacheBuf)                           \
            {                                               \
                gCacheSize = 0;                             \
                return errCode;                             \
            }                                               \
            else                                            \
            {                                               \
                gCacheSize = size4MemUtil;                  \
                name = (type*)gCacheBuf;                    \
            }                                               \
        }                                                   \
        else                                                \
        {                                                   \
            name = (type*)gCacheBuf;                        \
        }                                                   \
    }while(0)

extern void   *g_exec_util_cache;
extern dword_t  g_exec_util_cache_size;

#define ExecUtil_DeclarePtrAndCount(type, ptrName, countName)       ExecUtil_DeclarePtrAndCountImpl(type, ptrName, countName, g_exec_util_cache, g_exec_util_cache_size)
#define ExecUtil_Exec(ret, func, noEnoughRet, pBuf, type, count)    ExecUtil_ExecImpl(ret, func, noEnoughRet, pBuf, type, count, g_exec_util_cache, g_exec_util_cache_size)

#define MemUtil_DeclarePtrAndCount(type, ptrName, countName)        MemUtil_DeclarePtrAndCountImpl(type, ptrName, countName)
#define MemUtil_Alloc(type, name, count, errCode)                   MemUtil_AllocImpl(type, name, count, errCode, g_exec_util_cache, g_exec_util_cache_size)

#ifdef __cplusplus
}
#endif

#endif
