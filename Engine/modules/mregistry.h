#ifndef CUTE_MODULE_REGISTRY_H
#define CUTE_MODULE_REGISTRY_H

#include <stdint.h>

#include "modules/mdef.h"

#include "modules/console.h"


static CtModuleFunc* ct_module_dispatch_map[] = {
	CT_MODULE_REFER(console)
};


#define _CT_COUNT_FUNC(MOD) sizeof(CT_MODULE_REFER(MOD))/sizeof(CT_MODULE_REFER(MOD)[0])

static uint32_t ct_module_func_count[] = {
	_CT_COUNT_FUNC(console)
};

#endif // CUTE_MODULE_REGISTRY_H