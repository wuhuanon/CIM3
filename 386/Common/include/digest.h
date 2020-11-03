#ifndef __DIGEST_H_467453_INCLUDED__
#define __DIGEST_H_467453_INCLUDED__

#include <typedef.h>
#include <Constants_ud.h>

#ifdef __cplusplus
extern "C" {
#endif

#define DIGEST_BLOCK_MAX_SIZE		64
#define DIGEST_RESULT_MAX_SIZE          64

typedef dword_t digest_id_t;

byte_t digest_get_result_size(digest_id_t algID);

#ifdef __cplusplus
}
#endif

#endif
