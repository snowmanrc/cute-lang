#ifndef CUTE_MODULE_CONSOLE_H
#define CUTE_MODULE_CONSOLE_H

#include "modules/mdef.h"

void
ct_module_console_write(CtModuleFuncArg* arg);


CT_MODULE_DEFINE(console) = {
	ct_module_console_write,
};

#endif // CUTE_MODULE_CONSOLE_H