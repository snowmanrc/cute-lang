
# Architecture

### Overview

`Cute` is a 64-bit register-based virtual machine toolchain consisting of two components:

1. `compiler`: Compiles `.ct` text files into `.cute` executable images.
2. `engine`: The runtime that loads and executes `.cute` images.


### Toolchain Pipeline
```
Source Code (.ct)
		|
	    v
┌────────────────────┐
│    Cute Compiler   │  (Compiling code file/s to a single image file)
└────────────────────┘
		|
		v
Executable Image (.cute)
		|
		v
┌────────────────────┐
│    Cute Engine     │  (Executing image file)
└────────────────────┘
```

### Project Structure
``` bash
.
├── Compiler # Main Cute Compiler
│   ├── defs # common definitions required by the compiler
│   ├── lexing  # converts source code into tokens
│   ├── parsing # parses tokens to construct an ast
│   ├── loading # manages lexer and parser calls to make an ast for multiple files
│   ├── resolution # name resolution and operation resolution
│   ├── checking # type checking
│   ├── codegen # converting AST to bytecode
│   └── orchestrating # sets up and calls everything
│
├── Engine # Main Engine Source Code
│   ├── common # common headers needed throughout the engine
│   ├── core # heart of the runtime
│   ├── image # image loading and management
│   ├── objects # objects subsystem, gc, object defintions and manager
│   ├── utils # small utils needed in the engine
│   └── main # entry point of the engine
│
├── dev # Place for testing
│
├── editor # tooling for editors
│
└── docs # Documentation
	├── development # todos and stuff
	├── modules # docs on individual modules
    └── records # list of recorded design choices
```