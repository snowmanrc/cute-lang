#ifndef CUTE_MODULE_DEF_H
#define CUTE_MODULE_DEF_H

struct CtModuleFuncArg;
typedef struct CtModuleFuncArg CtModuleFuncArg;

typedef void (*CtModuleFunc)(CtModuleFuncArg*);

#define CT_MODULE_DEFINE(NAME) CtModuleFunc _ct_module_ ## NAME ## _func_map[]
#define CT_MODULE_REFER(NAME) _ct_module_ ## NAME ## _func_map

#endif // CUTE_MODULE_DEF_H