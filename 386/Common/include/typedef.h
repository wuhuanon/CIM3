
#ifndef __TYPE_DEF_H_INCLUDED_64568953__
#define __TYPE_DEF_H_INCLUDED_64568953__

typedef unsigned char   byte_t;
typedef unsigned short  word_t;
typedef unsigned int    dword_t;

typedef unsigned int    bool_t;

typedef unsigned short  ushort;
typedef unsigned int    uint;

#ifndef TRUE
#define TRUE    1
#define FALSE   0
#endif

#define OUT
#define IN

#define DEFINE_NAME(type_name, MAX_LEN)     \
typedef struct                              \
{                                           \
    word_t len;                             \
    byte_t val[MAX_LEN+1];                  \
}type_name

#define DEFINE_BUFFER(buffer_name, MAX_LEN) \
typedef struct                              \
{                                           \
    dword_t len;                            \
    byte_t val[MAX_LEN];                    \
}buffer_name

#endif
