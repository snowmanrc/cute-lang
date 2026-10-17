from Compiler.defs.symbols import Container

UNK_CONTAINER    = Container("unknown", True)
NONE_CONTAINER   = Container("none", True)
INT_CONTAINER    = Container("int", True)
UINT_CONTAINER   = Container("uint", True)
FLOAT_CONTAINER  = Container("float", True)
BOOL_CONTAINER   = Container("bool", True)
CHAR_CONTAINER   = Container("char", True)

PRIMTIVES = [UNK_CONTAINER, NONE_CONTAINER, INT_CONTAINER, UINT_CONTAINER, FLOAT_CONTAINER, BOOL_CONTAINER, CHAR_CONTAINER]
