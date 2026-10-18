#ifndef CUTE_MODULE_SPEC_H
#define CUTE_MODULE_SPEC_H

#include <stdint.h>

#include "core/core.h"
#include "core/context.h"
#include "modules/mdef.h"
#include "modules/mregistry.h"


struct CtModuleFuncArg {
	uint8_t    arg_start_slot;
	uint8_t    return_slot;
	CtEngine*  engine;
	CtContext* active_context;
};


CtModuleFunc
ct_module_get_func(uint32_t module, uint32_t func) {

	if (module >= sizeof(ct_module_dispatch_map)/sizeof(ct_module_dispatch_map[0])) {
		return NULL;
	}

	CtModuleFunc* module_map = ct_module_dispatch_map[module];

	if (func >= ct_module_func_count[module]) {
		return NULL;
	}

	return module_map[func];
}


#endif // CUTE_MODULE_SPEC_H