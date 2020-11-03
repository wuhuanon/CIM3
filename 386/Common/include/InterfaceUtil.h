
#ifndef __INTERFACE_UTIL_H_34968382_INCLUDED__
#define __INTERFACE_UTIL_H_34968382_INCLUDED__

#define INTF_V_METHOD_TABLE_STRUCT_NAME(IntfName)           __v_method_table_st_for_##IntfName##__
#define INTF_V_METHOD_TABLE_FIELD_NAME(IntfName)            __v_method_table_for_##IntfName##__
#define INTF_V_METHOD_TABLE_PTR                             __v_method_table_pointer__
#define INST_SUPER_FIELD_NAME                               __super_class_field__
#define INST_V_METHOD_TABLE_NAME(IntfName)                  __gc_v_method_table_for_##IntfName##__

#define DECLARE_INTF_METHOD_NO_PARA(retType, intfMethdName) typedef retType (*intfMethdName)(void*);
#define DECLARE_INTF_METHOD_BEGIN(retType, intfMethdName)   typedef retType (*intfMethdName)(void*,
#define DECLARE_INTF_METHOD_END()                           );

#define DECLARE_INTF_BEGIN()                                \
    typedef struct                                          \
    {

#define DECLARE_INTF_END(IntfName)                          \
    }INTF_V_METHOD_TABLE_STRUCT_NAME(IntfName);             \
    typedef struct                                          \
    {                                                       \
        const INTF_V_METHOD_TABLE_STRUCT_NAME(IntfName) *INTF_V_METHOD_TABLE_PTR;  \
    }IntfName;

#define DECLARE_SUPER_INTF(SuperIntfName)                   INTF_V_METHOD_TABLE_STRUCT_NAME(SuperIntfName)    INTF_V_METHOD_TABLE_FIELD_NAME(SuperIntfName);

#define DECLARE_INTF_EXTEND_BEGIN(SuperIntfName)            \
    DECLARE_INTF_BEGIN()                                    \
        DECLARE_SUPER_INTF(SuperIntfName)

#define DEFINE_INTF_IMPL_BEGIN()                            \
    typedef struct                                          \
    {                                                       \
        const void *INTF_V_METHOD_TABLE_PTR;

#define DEFINE_INTF_IMPL_EXTEND_BEGIN(SuperClsName)         \
    typedef struct                                          \
    {                                                       \
        union                                               \
        {                                                   \
            SuperClsName INST_SUPER_FIELD_NAME;             \
            const void *INTF_V_METHOD_TABLE_PTR;            \
        };

#define DEFINE_INTF_IMPL_END(ImplClsName)                   \
    }ImplClsName;

#define DEFINE_INTF_IMPL_EXTEND(ImplClsName, SuperClsName)  \
    DEFINE_INTF_IMPL_EXTEND_BEGIN(SuperClsName)             \
    DEFINE_INTF_IMPL_END(ImplClsName)

#define DEFINE_INTF_METHOD_IMPL_BEGIN(clsName, IntfName)    \
    static const INTF_V_METHOD_TABLE_STRUCT_NAME(IntfName)  INST_V_METHOD_TABLE_NAME(clsName) = {

#define DEFINE_INTF_METHOD_IMPL_END()                       };

#define INTF_V_PTR(pIntf)                                   ((pIntf)->INTF_V_METHOD_TABLE_PTR)
#define INTF_SUPER(pVPtr, superIntfName)                    (&(pVPtr)->INTF_V_METHOD_TABLE_FIELD_NAME(superIntfName))

#define INST_INIT_INTF(pInst, ClsName)                      INTF_V_PTR(pInst) = &INST_V_METHOD_TABLE_NAME(ClsName)

#endif//__INTERFACE_UTIL_H_34968382_INCLUDED__
