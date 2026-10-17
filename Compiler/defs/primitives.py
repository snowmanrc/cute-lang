from Compiler.defs.symbols import Container

UNK_CONTAINER   = Container("unknown", True)
VOID_CONTAINER  = Container("void", True)
INT_CONTAINER   = Container("int", True)
FLOAT_CONTAINER = Container("float", True)
BOOL_CONTAINER  = Container("bool", True)
CHAR_CONTAINER  = Container("char", True)

PRIMTIVES = [UNK_CONTAINER, VOID_CONTAINER, INT_CONTAINER, FLOAT_CONTAINER, BOOL_CONTAINER, CHAR_CONTAINER]
